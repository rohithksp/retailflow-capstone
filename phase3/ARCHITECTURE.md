# Data Lake Architecture

## Bronze Zone (Raw)
- Location: s3://capstone-project-bucket-12345/raw/
- Purpose: Stores raw, unprocessed data exactly as ingested.
- Contents: Daily partitions of customers.csv, products.csv, orders_dayX.json, order_items_dayX.json.
- Retention: 90 days (lifecycle policy).
- Partitioning: dt=YYYY-MM-DD.

## Silver Zone (Clean)
- Location: s3://capstone-project-bucket-12345/silver/
- Purpose: Stores cleaned, schema-aligned data (null handling, type corrections).
- Contents: Transformed versions of raw datasets.
- Retention: NA.
- Partitioning: dt=YYYY-MM-DD.

## Gold Zone (Aggregated)
- Location: s3://capstone-project-bucket-12345/gold/
- Purpose: Stores business-ready aggregates and KPIs.
- Contents: Revenue by category, daily order volume, etc.
- Retention: Permanent.
- Partitioning: dt=YYYY-MM-DD.

## Naming Convention
- Prefixes: raw/, silver/, gold/.
- Partitioning: Hive-style `dt=YYYY-MM-DD`.
