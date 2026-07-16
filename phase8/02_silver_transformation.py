# Databricks notebook source
# MAGIC %md
# MAGIC # Step 45: Silver Layer Transformation & CDF Enrichment
# MAGIC - Cleanses and conforms column types.
# MAGIC - Deduplicates data based on unique session/event keys.
# MAGIC - Enforces and enables Change Data Feed (CDF).

# COMMAND ----------

from pyspark.sql.functions import col, to_timestamp, row_number
from pyspark.sql.window import Window

CATALOG = "main"
SCHEMA = "clickstream_analytics"
SOURCE_TABLE = f"{CATALOG}.{SCHEMA}.bronze_clickstream"
TARGET_TABLE = f"{CATALOG}.{SCHEMA}.silver_clickstream"

# COMMAND ----------

# Read new Bronze data
df_bronze = spark.read.table(SOURCE_TABLE)

# Cleanse and conform data types
df_cleansed = df_bronze.select(
    col("user_id").cast("string"),
    col("session_id").cast("string"),
    col("email").cast("string"),
    to_timestamp(col("event_timestamp")).alias("event_timestamp"),
    col("event_type").cast("string"),
    col("page_url").cast("string"),
    col("ingested_at")
).filter(col("user_id").isNotNull())

# Deduplicate events using window functions
window_spec = Window.partitionBy("session_id", "event_timestamp").orderBy(col("ingested_at").desc())

df_deduplicated = df_cleansed.withColumn("row_num", row_number().over(window_spec)) \
                             .filter(col("row_num") == 1) \
                             .drop("row_num")

# COMMAND ----------

# Create target table with CDF enabled if it doesn't exist
spark.sql(f"""
  CREATE TABLE IF NOT EXISTS {TARGET_TABLE}
  USING DELTA
  TBLPROPERTIES (delta.enableChangeDataFeed = true)
  AS SELECT * FROM {SOURCE_TABLE} WHERE 1=0
""")

# Merge or Append data into Silver
# For this workflow pattern, we overwrite/append the processed batch safely
df_deduplicated.write.format("delta").mode("append").saveAsTable(TARGET_TABLE)
