DROP TABLE IF EXISTS fact_coe_monthly CASCADE;
DROP TABLE IF EXISTS date_dim CASCADE;
DROP TABLE IF EXISTS category_dim CASCADE;
DROP TABLE IF EXISTS car_reference CASCADE;

CREATE TABLE date_dim(
    date_id INT PRIMARY KEY,
    year INT NOT NULL,
    month INT NOT NULL,
    quarter INT NOT NULL
);

CREATE TABLE category_dim(
    category_id INT PRIMARY KEY,
    category_code VARCHAR NOT NULL,
    description VARCHAR NOT NULL
);

CREATE TABLE car_reference(
    car_id SERIAL PRIMARY KEY,
    band VARCHAR,
    car_model VARCHAR NOT NULL,
    category_id INT REFERENCES category_dim(category_id)
);

CREATE TABLE fact_coe_monthly(
    fact_id INT PRIMARY KEY,
    date_id INT REFERENCES date_dim(date_id),
    category_id INT REFERENCES category_dim(category_id),
    monthly_quota INT NOT NULL,
    bids_success_monthly INT NOT NULL,
    bids_received_monthly INT NOT NULL,
    average_premium_monthly NUMERIC
);
