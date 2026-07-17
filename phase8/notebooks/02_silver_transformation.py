# Databricks notebook source
# =============================================================================
# CAPSTONE PROJECT
# Phase 8 - Databricks Lakehouse Track
#
# Notebook:
#     02_silver.py
#
# Purpose:
#     Transform Bronze clickstream data into a cleansed and conformed
#     Silver Delta table.
#
# Source:
#     retail.bronze.clickstream
#
# Target:
#     retail.silver.clickstream
#
# Features
# --------
# ✓ Cleansing
# ✓ Deduplication
# ✓ Standardization
# ✓ Timestamp Conversion
# ✓ Derived Columns
# ✓ Change Data Feed (CDF)
# ✓ Data Quality Validation
#
# Assignment Requirement:
#     Requirement 45
#
# =============================================================================

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window

import logging

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Runtime Parameters

# COMMAND ----------

dbutils.widgets.text("catalog", "retail")
dbutils.widgets.text("bronze_schema", "bronze")
dbutils.widgets.text("silver_schema", "silver")
dbutils.widgets.text("table", "clickstream")

CATALOG = dbutils.widgets.get("catalog")
BRONZE_SCHEMA = dbutils.widgets.get("bronze_schema")
SILVER_SCHEMA = dbutils.widgets.get("silver_schema")
TABLE = dbutils.widgets.get("table")

BRONZE_TABLE = f"{CATALOG}.{BRONZE_SCHEMA}.{TABLE}"
SILVER_TABLE = f"{CATALOG}.{SILVER_SCHEMA}.{TABLE}"

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Create Silver Schema

# COMMAND ----------

spark.sql(f"""
CREATE SCHEMA IF NOT EXISTS
{CATALOG}.{SILVER_SCHEMA}
""")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Create Silver Table (CDF Enabled)

# COMMAND ----------

spark.sql(f"""

CREATE TABLE IF NOT EXISTS {SILVER_TABLE}
(
session_id STRING,
customer_id STRING,
event_type STRING,
event_ts TIMESTAMP,
event_date DATE,
event_hour INT,
page STRING,
processing_timestamp TIMESTAMP,
source_file STRING
)
USING DELTA
TBLPROPERTIES
(
delta.enableChangeDataFeed=true
)
""")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. Read Bronze Table

# COMMAND ----------

bronze_df = spark.table(BRONZE_TABLE)

display(bronze_df.limit(10))

# COMMAND ----------
# MAGIC %md
# MAGIC ## 5. Bronze Record Count

# COMMAND ----------

bronze_count = bronze_df.count()

print(f"Bronze Records : {bronze_count}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 6. Data Cleansing
#
# MAGIC Operations
#
# MAGIC * Remove NULL Session IDs
# MAGIC * Remove NULL Customer IDs
# MAGIC * Remove NULL Event Timestamp
# MAGIC * Trim whitespace
# MAGIC * Convert text to lowercase
# MAGIC * Remove duplicate events

# COMMAND ----------

silver_df = (
bronze_df
.filter(col("session_id").isNotNull())
.filter(col("customer_id").isNotNull())
.filter(col("event_ts").isNotNull())
.withColumn(
"event_type",
lower(trim(col("event_type")))
)
.withColumn(
"page",
lower(trim(col("page")))
)
.withColumn(
"event_ts",
to_timestamp(col("event_ts"))
)
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 7. Remove Invalid Records

# COMMAND ----------

silver_df = silver_df.filter(
col("event_type").isin(
"search",
"click",
"cart",
"checkout"
)
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 8. Remove Duplicate Events
#
# MAGIC Duplicate Definition
#
# MAGIC Same
#
# MAGIC session_id
#
# MAGIC +
#
# MAGIC event_ts

# COMMAND ----------

window_spec = Window.partitionBy(
"session_id",
"event_ts"
).orderBy(
col("ingestion_timestamp").desc()
)

silver_df = (
silver_df
.withColumn(
"row_num",
row_number().over(window_spec)
)
.filter(
col("row_num") == 1
)
.drop("row_num")
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 9. Create Derived Columns

# COMMAND ----------

silver_df = (
silver_df
.withColumn(
"event_date",
to_date(col("event_ts"))
)
.withColumn(
"event_hour",
hour(col("event_ts"))
)
.withColumn(
"processing_timestamp",
current_timestamp()
)
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 10. Select Final Columns

# COMMAND ----------

silver_df = silver_df.select(
"session_id",
"customer_id",
"event_type",
"event_ts",
"event_date",
"event_hour",
"page",
"processing_timestamp",
"source_file"
)
display(silver_df.limit(20))

# COMMAND ----------
# MAGIC %md

# COMMAND ----------
# MAGIC %md

# MAGIC ## 11. Write Silver Delta Table
#
# MAGIC The cleansed dataframe is written to the Silver Delta table.
# MAGIC
# MAGIC For this capstone project we overwrite the table so the notebook can
# MAGIC be re-run easily. In a production project this would typically be
# MAGIC implemented using MERGE INTO for incremental processing.

# COMMAND ----------

(
    silver_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(SILVER_TABLE)
)

print(f"Successfully loaded Silver table : {SILVER_TABLE}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 12. Optimize Table
#
# MAGIC OPTIMIZE improves read performance.
# MAGIC ZORDER helps data skipping for frequently filtered columns.

# COMMAND ----------

spark.sql(f"""
OPTIMIZE {SILVER_TABLE}
ZORDER BY (event_date, customer_id)
""")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 13. Validate Silver Table

# COMMAND ----------

silver = spark.table(SILVER_TABLE)

display(silver.limit(20))

# COMMAND ----------
# MAGIC %md
# MAGIC ## 14. Record Count Comparison

# COMMAND ----------

silver_count = silver.count()

print("="*70)
print(f"Bronze Records : {bronze_count}")
print(f"Silver Records : {silver_count}")
print(f"Records Removed : {bronze_count - silver_count}")
print("="*70)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 15. Schema Validation

# COMMAND ----------

silver.printSchema()

# COMMAND ----------
# MAGIC %md
# MAGIC ## 16. Null Validation

# COMMAND ----------

display(

spark.sql(f"""
SELECT
SUM(CASE WHEN session_id IS NULL THEN 1 ELSE 0 END) session_nulls,
SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) customer_nulls,
SUM(CASE WHEN event_ts IS NULL THEN 1 ELSE 0 END) timestamp_nulls,
SUM(CASE WHEN event_type IS NULL THEN 1 ELSE 0 END) event_nulls,
SUM(CASE WHEN page IS NULL THEN 1 ELSE 0 END) page_nulls
FROM {SILVER_TABLE}
""")

)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 17. Event Type Distribution

# COMMAND ----------

display(
spark.sql(f"""
SELECT
event_type,
COUNT(*) total_events
FROM {SILVER_TABLE}
GROUP BY event_type
ORDER BY total_events DESC
""")
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 18. Page Distribution

# COMMAND ----------

display(
spark.sql(f"""
SELECT
page,
COUNT(*) visits
FROM {SILVER_TABLE}
GROUP BY page
ORDER BY visits DESC
""")
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 19. Daily Activity

# COMMAND ----------

display(
spark.sql(f"""
SELECT
event_date,
COUNT(*) total_events,
COUNT(DISTINCT customer_id) unique_customers,
COUNT(DISTINCT session_id) unique_sessions
FROM {SILVER_TABLE}
GROUP BY event_date
ORDER BY event_date
""")
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 20. Hourly Activity

# COMMAND ----------

display(
spark.sql(f"""
SELECT
event_hour,
COUNT(*) total_events
FROM {SILVER_TABLE}
GROUP BY event_hour
ORDER BY event_hour
""")
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 21. Top Customers by Activity

# COMMAND ----------

display(
spark.sql(f"""
SELECT
customer_id,
COUNT(*) total_events
FROM {SILVER_TABLE}
GROUP BY customer_id
ORDER BY total_events DESC
LIMIT 20
""")
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 22. Top Sessions

# COMMAND ----------

display(

spark.sql(f"""
SELECT
session_id,
COUNT(*) events_in_session
FROM {SILVER_TABLE}
GROUP BY session_id
ORDER BY events_in_session DESC
LIMIT 20
""")
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 23. Change Data Feed Validation
#
# MAGIC Verify that Change Data Feed has been enabled.

# COMMAND ----------

display(
spark.sql(f"""
SHOW TBLPROPERTIES {SILVER_TABLE}
""")
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 24. Sample Change Data Feed Query
#
# MAGIC Uncomment after multiple versions of the Silver table exist.
#
# MAGIC SELECT *
# MAGIC FROM table_changes('{SILVER_TABLE}',1);

# COMMAND ----------

# Example only
#
# display(
# spark.sql(f"""
#
# SELECT *
# FROM table_changes('{SILVER_TABLE}',1)
#
# """)
# )

# COMMAND ----------
# MAGIC %md
# MAGIC ## 25. Data Quality Summary

# COMMAND ----------

quality_summary = spark.sql(f"""
SELECT
COUNT(*) total_records,
COUNT(DISTINCT customer_id) unique_customers,
COUNT(DISTINCT session_id) unique_sessions,
MIN(event_ts) earliest_event,
MAX(event_ts) latest_event
FROM {SILVER_TABLE}
""")

display(quality_summary)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 26. Completion Summary

# COMMAND ----------

print("=" * 80)
print("SILVER LAYER PROCESSING COMPLETED")
print("=" * 80)

print(f"Source Table : {BRONZE_TABLE}")
print(f"Target Table : {SILVER_TABLE}")

print(f"Bronze Records : {bronze_count}")
print(f"Silver Records : {silver_count}")

print("")
print("Transformations Applied")
print("-----------------------")
print("✓ Null record removal")
print("✓ Event type standardization")
print("✓ Page standardization")
print("✓ Timestamp conversion")
print("✓ Duplicate removal")
print("✓ Event date derivation")
print("✓ Event hour derivation")
print("✓ Change Data Feed Enabled")
print("✓ Delta Optimization")
print("=" * 80)




