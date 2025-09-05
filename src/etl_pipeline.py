import requests
import pandas as pd
import os
import re
import pdfplumber
import sqlalchemy as db
from sqlalchemy import text
from sqlalchemy_utils import create_database
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
PG_PASSWORD = os.getenv('PG_PASSWORD')
DB_NAME = 'COE'
DATABASE_URL = f'postgresql+psycopg2://postgres:{PG_PASSWORD}@localhost:5432/{DB_NAME}'

# --- Extraction Functions ---
def extract_coe_data_from_api(api_key):
    """Extracts COE data from the Data.gov.sg API."""
    try:
        headers = {"x-api-key": api_key}
        params = {"resource_id": "d_69b3380ad7e51aff3a7dcc84eba52b8a", "limit": 5000}
        response = requests.get("https://data.gov.sg/api/action/datastore_search", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get('success') and 'records' in data['result']:
            df = pd.json_normalize(data['result']['records'])
            print("✅ API data extraction successful.")
            return df
        else:
            print("❌ API call failed or returned no records.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Network or API error occurred: {e}")
        return None

def extract_car_data_from_pdf():
    """Extracts car model data from a PDF document."""
    pdf_url = "https://www.nccs.gov.sg/files/docs/default-source/news-documents/cevs_revised_bands_eg_car_models_annex_a.pdf"
    pdf_filename = "cevs_revised_bands.pdf"
    records = []
    try:
        r = requests.get(pdf_url)
        r.raise_for_status()
        with open(pdf_filename, "wb") as f:
            f.write(r.content)
        text = ""
        with pdfplumber.open(pdf_filename) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        band_pattern = re.compile(r'\)\s*([A-Z]\d?)')
        matches = list(band_pattern.finditer(text))
        sections = []
        for i, m in enumerate(matches):
            start = m.start() + 1
            end = matches[i+1].start() + 1 if i+1 < len(matches) else len(text)
            band = m.group(1)
            content = text[start:end].strip()
            sections.append((band, content))
        car_id = 1
        for band, content in sections:
            parts = re.split(r',\s*(?![^\(]*\))', content)
            for part in parts:
                part = part.strip()
                if not part: continue
                cat_match = re.search(r'\(Cat\s*(A|B)', part)
                category = cat_match.group(1) if cat_match else None
                model_name = re.sub(r'\(.*?\)', '', part).strip()
                if model_name:
                    records.append({'car_id': car_id, 'band': band, 'car_model': model_name, 'category': category})
                    car_id += 1
        print("✅ PDF data extraction successful.")
        return pd.DataFrame(records)
    except (requests.exceptions.RequestException, pdfplumber.PDFPageCountError) as e:
        print(f"❌ Error extracting data from PDF: {e}")
        return None

# --- Transformation Functions ---
def transform_coe_data(df):
    """Transforms raw COE data into fact and dimension tables."""
    wanted_categories = ['Category A', 'Category B', 'Category E']
    df = df[df['vehicle_class'].isin(wanted_categories)].copy()
    numeric_cols = ['quota', 'bids_success', 'bids_received', 'premium']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=['premium'], inplace=True)
    category_dim = pd.DataFrame([
        {'category_id': 1, 'category_code': 'Category A', 'description': 'Cars <= 1600cc & <= 130bhp'},
        {'category_id': 2, 'category_code': 'Category B', 'description': 'Cars > 1600cc or > 130bhp'},
        {'category_id': 3, 'category_code': 'Category E', 'description': 'Open Category (any car)'}
    ])
    date_dim = pd.DataFrame({'month_str': sorted(df['month'].unique())})
    date_dim['date_id'] = date_dim['month_str'].str.replace('-', '').astype(int)
    date_dim['year'] = date_dim['month_str'].str[:4].astype(int)
    date_dim['month'] = date_dim['month_str'].str[5:7].astype(int)
    date_dim['quarter'] = ((date_dim['month'] - 1) // 3 + 1).astype(int)
    date_dim = date_dim[['date_id', 'year', 'month', 'quarter']]
    category_mapping = {row['category_code']: row['category_id'] for _, row in category_dim.iterrows()}
    df['category_id'] = df['vehicle_class'].map(category_mapping).astype(int)
    df['date_id'] = df['month'].str.replace('-', '').astype(int)
    fact_coe_monthly = df.groupby(['date_id', 'category_id']).agg(
        monthly_quota=('quota', 'sum'),
        bids_success_monthly=('bids_success', 'sum'),
        bids_received_monthly=('bids_received', 'sum'),
        average_premium_monthly=('premium', 'mean')
    ).reset_index()
    fact_coe_monthly['fact_id'] = range(1, len(fact_coe_monthly) + 1)
    fact_coe_monthly = fact_coe_monthly.astype({'monthly_quota': 'int', 'bids_success_monthly': 'int', 'bids_received_monthly': 'int'})
    print("✅ COE data transformation successful.")
    return fact_coe_monthly, date_dim, category_dim

def transform_car_data(df):
    """Transforms raw car data from PDF into a dimension table."""
    if df is None: return None
    proper_bands = ['A1', 'A2', 'A3', 'A4', 'B', 'C1', 'C2', 'C3', 'C4']
    df['band'] = pd.Categorical(df['band'], categories=proper_bands, ordered=True)
    category_map = {'A': 1, 'B': 2}
    df['category_id'] = df['category'].map(category_map).astype('Int64')
    df = df.drop(columns=['category'])
    car_reference_df = df.dropna(subset=['category_id']).copy()
    car_reference_df['category_id'] = car_reference_df['category_id'].astype(int)
    print("✅ Car data transformation successful.")
    return car_reference_df

# --- Loading Functions ---
def create_database_and_tables(db_url):
    """Creates the database and tables for the data warehouse."""
    try:
        engine = db.create_engine(db_url.rsplit('/', 1)[0] + '/postgres')
        if not db.database_exists(db_url):
            create_database(db_url)
            print(f"✅ Database '{DB_NAME}' created successfully.")
        else:
            print(f"ℹ️ Database '{DB_NAME}' already exists.")
        engine = db.create_engine(db_url)
        with engine.begin() as conn:
            with open('sql/schema.sql', 'r') as file:
                sql_commands = file.read()
                for command in sql_commands.split(';')[:-1]:
                    conn.execute(text(command))
            print("✅ Tables created successfully from schema.sql.")
        return engine
    except Exception as e:
        print(f"❌ Error creating database or tables: {e}")
        return None

def load_data_into_db(engine, fact_df, date_dim_df, category_dim_df, car_ref_df):
    """Loads DataFrames into the PostgreSQL database tables."""
    try:
        date_dim_df.to_sql('date_dim', con=engine, if_exists='append', index=False)
        category_dim_df.to_sql('category_dim', con=engine, if_exists='append', index=False)
        car_ref_df.to_sql('car_reference', con=engine, if_exists='append', index=False)
        fact_df.to_sql('fact_coe_monthly', con=engine, if_exists='append', index=False)
        print("✅ Data loaded into database tables successfully.")
    except Exception as e:
        print(f"❌ Error loading data into tables: {e}")
