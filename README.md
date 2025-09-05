Singapore COE Data Engineering Pipeline

Project Overview
This project demonstrates a complete data engineering pipeline to collect, process, and store data related to Singapore's Certificate of Entitlement (COE) system. The pipeline integrates data from two different sources—a public API and a PDF document—to build a structured data warehouse using a star schema in a PostgreSQL database.

This project showcases key skills in ETL (Extract, Transform, Load), dimensional modeling, and API/web scraping, all within a professional and reproducible repository structure.

Key Features
Multi-Source Data Ingestion: Extracts COE bidding results from the Data.gov.sg API and car model reference data by parsing an unstructured PDF from the National Climate Change Secretariat (NCCS).

Data Transformation: Cleans and reshapes the raw data into a star schema composed of a central fact table (fact_coe_monthly) and three dimension tables (date_dim, category_dim, and car_reference).

Database Loading: Loads the transformed data into a PostgreSQL database using SQLAlchemy, demonstrating end-to-end data flow into a robust, relational database.

Reproducibility: Uses a .env file for secure credential management and requirements.txt to ensure anyone can easily set up and run the pipeline.
