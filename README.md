Singapore COE Data Engineering Pipeline
Project Overview
This project demonstrates a complete data engineering pipeline to collect, process, and store data related to Singapore's Certificate of Entitlement (COE) system. The pipeline integrates data from two different sources—a public API and a PDF document—to build a structured data warehouse using a star schema in a PostgreSQL database.

This project showcases key skills in ETL (Extract, Transform, Load), dimensional modeling, and API/web scraping, all within a professional and reproducible repository structure.

Key Features
Multi-Source Data Ingestion: Extracts COE bidding results from the Data.gov.sg API and car model reference data by parsing an unstructured PDF from the National Climate Change Secretariat (NCCS).

Data Transformation: Cleans and reshapes the raw data into a star schema composed of a central fact table (fact_coe_monthly) and three dimension tables (date_dim, category_dim, and car_reference).

Database Loading: Loads the transformed data into a PostgreSQL database using SQLAlchemy, demonstrating end-to-end data flow into a robust, relational database.

Reproducibility: Uses a .env file for secure credential management and requirements.txt to ensure anyone can easily set up and run the pipeline.

Repository Structure
coe-analysis/
├── data/
├── notebooks/
│   └── coe_eda.ipynb
├── src/
│   ├── etl_pipeline.py
│   └── main.py
├── sql/
│   └── schema.sql
├── .env.example
├── requirements.txt
└── README.md
How to Run the Project
1. Prerequisites
Make sure you have Python installed. The project was developed with Python 3.10+.

2. Set Up the Environment
First, clone this repository:

Bash

git clone https://github.com/your-username/coe-analysis.git
cd coe-analysis
Next, create a virtual environment and install the required packages:

Bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Configure Credentials
Create a .env file in the root directory based on the provided .env.example.

Ini, TOML

# .env.example
API_KEY=your_data_gov_sg_api_key
PG_PASSWORD=your_postgresql_password
Note: You'll need to sign up for a free Data.gov.sg API key.

4. Run the ETL Pipeline
Execute the main script from your terminal. This will perform all the ETL steps, from data extraction to loading the data into your PostgreSQL database.

Bash

python src/main.py
The script will handle creating the COE database and all necessary tables before loading the data.

Final Output
Once the pipeline is complete, you can connect to your PostgreSQL database and run SQL queries. The src/main.py script also includes a few sample queries to demonstrate how the data can be used to answer business questions, such as:

Average COE premium for each vehicle category.

A list of recommended car models based on affordable COE categories.

For a deeper dive into the initial data exploration and my thought process, please refer to the coe_eda.ipynb notebook in the notebooks/ folder.
