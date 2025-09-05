# 🚗 Singapore COE Data Engineering Pipeline

## 🧠 Overview

This project demonstrates a complete data engineering pipeline that extracts, processes, and stores data related to Singapore’s **Certificate of Entitlement (COE)** system. The pipeline integrates data from a public API and a PDF source to build a **dimensional model** in a **PostgreSQL** database using a **star schema**.

It showcases skills in:

- Data ingestion from multiple sources (API + PDF)
- Data cleaning and transformation
- Dimensional modeling and relational schema design
- Automated ETL using Python
- Reproducibility and environment setup

---

## 🔑 Key Features

- **📥 Multi-Source Ingestion**  
  Extracts COE bidding results from [Data.gov.sg API](https://data.gov.sg) and parses an unstructured PDF (e.g., from NCCS) for vehicle category reference data.

- **🧹 Data Transformation & Modeling**  
  Raw data is reshaped into a **star schema** with:
  - `fact_coe_monthly`
  - `date_dim`
  - `category_dim`
  - `car_reference`

- **💾 Database Loading**  
  Loads structured data into a **PostgreSQL** database using SQLAlchemy and pandas.

- **🔁 Reproducible Environment**  
  Uses `.env` for secret management and `requirements.txt` for environment setup.

---

## 🗂️ Project Structure

coe-analysis/
├── notebooks/
│ └── coe_eda.ipynb # Exploratory Data Analysis
├── sql/
│ └── schema.sql # Database schema (DDL)
├── src/
│ ├── etl_pipeline.py # ETL logic
│ └── main.py # Main entry script
├── .env.example # Environment variable template
├── requirements.txt # Python dependencies
└── README.md # Project documentation

---

## 🖥️ How to Run the Project

### ✅ Prerequisites

- Python 3.10+
- PostgreSQL installed (locally or via Docker)

### 📦 Setup Instructions

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-username/coe-analysis.git
   cd coe-analysis

2. **Create a virtual environment and install dependencies**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt

3. **Set up your environment variables**
Create a .env file in the root directory based on .env.example:
   ```env
   API_KEY=your_data_gov_sg_api_key
   PG_PASSWORD=your_postgresql_password

4. **Run the ETL pipeline**
   ```bash
   python src/main.py


This script will:
- Create the PostgreSQL database and tables
- Ingest data from the API and PDF
- Transform and load data into the star schema

## 📊 Example Insights
- 📉 COE prices trend higher in Q2 and Q3, suggesting seasonal spikes
- 🚘 Category B (larger vehicles) consistently has the highest average COE
- 📅 Most affordable periods for COE bidding are typically in early Q1
- 💡 Data supports smarter decision-making for vehicle purchases and forecasting

➡️ See notebooks/coe_eda.ipynb
 for data exploration and visualization.

## 📚 What I Learned
- How to build a modular, production-ready ETL pipeline in Python
- Parsing unstructured PDF documents into structured data
- Creating star schemas and dimensional models for analytics
- Managing secure credentials and environment reproducibility
- Writing clean, version-controlled code in a professional repo structure


