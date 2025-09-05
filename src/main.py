import pandas as pd
import sqlalchemy as db
import os
from dotenv import load_dotenv
from etl_pipeline import extract_coe_data_from_api, extract_car_data_from_pdf, transform_coe_data, transform_car_data, create_database_and_tables, load_data_into_db

# Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
PG_PASSWORD = os.getenv('PG_PASSWORD')
DB_NAME = 'COE'
DATABASE_URL = f'postgresql+psycopg2://postgres:{PG_PASSWORD}@localhost:5432/{DB_NAME}'

def run_etl_pipeline():
    """Runs the complete ETL pipeline."""
    print("--- 🏁 Starting COE Data ETL Pipeline ---")

    # 1. Extraction
    coe_df_raw = extract_coe_data_from_api(API_KEY)
    car_ref_df_raw = extract_car_data_from_pdf()

    if coe_df_raw is None or car_ref_df_raw is None:
        print("🚨 ETL pipeline aborted due to extraction errors.")
        return

    # 2. Transformation
    fact_coe_df, date_dim_df, category_dim_df = transform_coe_data(coe_df_raw)
    car_reference_df = transform_car_data(car_ref_df_raw)

    if car_reference_df is None:
        print("🚨 ETL pipeline aborted due to transformation errors.")
        return

    # 3. Loading
    engine = create_database_and_tables(DATABASE_URL)
    if engine:
        load_data_into_db(engine, fact_coe_df, date_dim_df, category_dim_df, car_reference_df)
        engine.dispose()
        print("✅ ETL pipeline completed successfully!")

def run_sample_queries():
    """Connects to the database and runs sample queries."""
    print("\n--- 📈 Running Sample Queries ---")
    engine = db.create_engine(DATABASE_URL)
    try:
        # Query 1: Average monthly premium per category
        query1 = "SELECT c.category_code, ROUND(AVG(f.average_premium_monthly), 2) AS average_monthly_premium FROM fact_coe_monthly f JOIN category_dim c ON f.category_id = c.category_id GROUP BY category_code ORDER BY AVG(f.average_premium_monthly);"
        df_avg_premium = pd.read_sql(query1, con=engine)
        print("\nAverage Monthly Premium by Category:")
        print(df_avg_premium)

        # Query 2: Recommended cars for the most affordable category
        query2 = "SELECT cr.band, cr.car_model, cd.category_code FROM car_reference cr JOIN category_dim cd ON cr.category_id = cd.category_id WHERE cd.category_code = 'Category A' AND cr.band IN ('A1', 'A2');"
        df_car_recommendation = pd.read_sql(query2, con=engine)
        print("\nRecommended Car Models (Category A, Bands A1 & A2):")
        print(df_car_recommendation)
    except Exception as e:
        print(f"❌ Error running sample queries: {e}")
    finally:
        if 'engine' in locals():
            engine.dispose()

if __name__ == "__main__":
    run_etl_pipeline()
    run_sample_queries()
