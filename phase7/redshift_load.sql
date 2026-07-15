-- Load Customer Dimension
COPY dim_customer
FROM 's3://capstone-project-bucket-12345/curated/manifest/customers/customer_manifest.json'
IAM_ROLE 'arn:aws:iam::1232132:role/RedshiftIAMS3GlueFullAccess'
MANIFEST
FORMAT AS CSV
IGNOREHEADER 1;

-- Load Product Dimension
COPY dim_product
FROM 's3://capstone-project-bucket-12345/curated/manifest/products/product_manifest.json'
IAM_ROLE 'arn:aws:iam::1232132:role/RedshiftIAMS3GlueFullAccess'
MANIFEST
FORMAT AS CSV
IGNOREHEADER 1;

-- Load Fact Orders Items (Parquet)
COPY fact_orders_items
FROM 's3://capstone-project-bucket-12345/curated/fact_order_items/'
IAM_ROLE 'arn:aws:iam::1232132:role/RedshiftIAMS3GlueFullAccess'
FORMAT AS PARQUET;

-- Check load errors
SELECT starttime, filename, line_number, colname, type, raw_line, err_reason
FROM stl_load_errors
ORDER BY starttime DESC
LIMIT 20;
