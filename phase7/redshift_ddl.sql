-- Dimension: Customer
CREATE TABLE dim_customer (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    customer_segment VARCHAR(50)
)
DISTSTYLE ALL
SORTKEY(customer_id);

-- Dimension: Product
CREATE TABLE dim_product (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    brand VARCHAR(50)
)
DISTSTYLE ALL
SORTKEY(product_id);

-- Fact: Orders Items
CREATE TABLE fact_orders_items (
    order_id VARCHAR(50),
    order_date VARCHAR(50),       -- Parquet string
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    quantity BIGINT,              -- Parquet long
    amount DOUBLE PRECISION,      -- Parquet double
    dt VARCHAR(50)                -- partition column
)
DISTSTYLE KEY
DISTKEY(product_id)
SORTKEY(order_id, dt);

-- External schema
CREATE EXTERNAL SCHEMA spectrum_lake
FROM DATA CATALOG
DATABASE 'retail_lake_db'
IAM_ROLE 'arn:aws:iam::1232132:role/RedshiftIAMS3GlueFullAccess'
REGION 'us-east-1';

-- PII table
CREATE TABLE customer_pii (
    customer_id VARCHAR(10) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    phone_number VARCHAR(20),
    date_of_birth DATE
)
DISTSTYLE ALL;
