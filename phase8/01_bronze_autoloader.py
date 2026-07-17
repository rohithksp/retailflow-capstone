# Databricks notebook source
# =============================================================================
# CAPSTONE PROJECT
# Phase 8 - Databricks Lakehouse Track
#
# Notebook:
#     01_bronze_autoloader.py
#
# Purpose:
#     Incrementally ingest clickstream JSON files from Amazon S3 into a
#     Bronze Delta table using Databricks Auto Loader.
#
# Source:
#     s3://databricks-capstone-retail-bucket/raw/clickstream/
#
# Target:
#     retail.bronze.clickstream
#
# Technologies:
#     - Databricks Auto Loader
#     - Delta Lake
#     - Unity Catalog
#     - Structured Streaming
#     - Amazon S3
#
# Assignment Requirements Covered:
#     ✔ Requirement 43
#     ✔ Requirement 44
#
# =============================================================================

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *

import logging

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Runtime Parameters
#
# MAGIC Configure notebook parameters using Databricks widgets.
# MAGIC These values can be overridden when the notebook is called from a
# MAGIC Databricks Workflow.

# COMMAND ----------

dbutils.widgets.text("catalog", "retail")
dbutils.widgets.text("schema", "bronze")
dbutils.widgets.text("table", "clickstream")

CATALOG = dbutils.widgets.get("catalog")
SCHEMA = dbutils.widgets.get("schema")
TABLE = dbutils.widgets.get("table")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Storage Configuration
#
# MAGIC External Location and Storage Credential are assumed to have already
# MAGIC been created using Unity Catalog.
#
# MAGIC Requirement 43 specifically states NOT to use Instance Profiles.

# COMMAND ----------

SOURCE_PATH = "s3://databricks-capstone-retail-bucket/raw/clickstream/"

SCHEMA_LOCATION = "dbfs:/capstone/autoloader/schema/clickstream"

CHECKPOINT_LOCATION = "dbfs:/capstone/autoloader/checkpoints/clickstream"

TARGET_TABLE = f"{CATALOG}.{SCHEMA}.{TABLE}"

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Create Catalog & Schema

# COMMAND ----------

spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOG}")

spark.sql(f"""
CREATE SCHEMA IF NOT EXISTS
{CATALOG}.{SCHEMA}
""")

print(f"Catalog  : {CATALOG}")
print(f"Schema   : {SCHEMA}")
print(f"Table    : {TABLE}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. Read Files Using Auto Loader
#
# MAGIC Auto Loader Configuration
#
# MAGIC * JSON Source
# MAGIC * Directory Listing Mode
# MAGIC * Schema Inference
# MAGIC * Incremental Processing
# MAGIC * Schema Evolution

# COMMAND ----------

clickstream_df = (
    spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option(
            "cloudFiles.schemaLocation",
            SCHEMA_LOCATION
        )
        .option(
            "cloudFiles.useNotifications",
            "false"
        )
        .option(
            "cloudFiles.includeExistingFiles",
            "true"
        )
        .option(
            "cloudFiles.schemaEvolutionMode",
            "addNewColumns"
        )
        .load(SOURCE_PATH)
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 5. Bronze Transformations
#
# MAGIC Bronze should preserve the raw data while adding ingestion metadata.

# COMMAND ----------

bronze_df = (
    clickstream_df
    .withColumn(
        "ingestion_timestamp",
        current_timestamp()
    )
    .withColumn(
        "source_file",
        input_file_name()
    )
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 6. Write Bronze Delta Table

# COMMAND ----------

query = (
    bronze_df.writeStream
        .format("delta")
        .outputMode("append")
        .option(
            "checkpointLocation",
            CHECKPOINT_LOCATION
        )
        .trigger(availableNow=True)
        .toTable(TARGET_TABLE)
)

# COMMAND ----------

query.awaitTermination()

print("Bronze ingestion completed successfully.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 7. Validate Bronze Data

# COMMAND ----------

display(
    spark.table(TARGET_TABLE)
)

# COMMAND ----------

display(
spark.sql(f"""
SELECT
COUNT(*) AS total_records
FROM {TARGET_TABLE}
""")
)

# COMMAND ----------

display(
spark.sql(f"""
SELECT
event_type,
COUNT(*) AS total_events
FROM {TARGET_TABLE}
GROUP BY event_type
ORDER BY total_events DESC
""")
)

# COMMAND ----------

display(

spark.sql(f"""
SELECT
page,
COUNT(*) AS page_visits
FROM {TARGET_TABLE}
GROUP BY page
ORDER BY page_visits DESC
""")
)

# COMMAND ----------

display(
spark.sql(f"""
SELECT
MIN(event_ts) AS earliest_event,
MAX(event_ts) AS latest_event
FROM {TARGET_TABLE}
""")

)

# COMMAND ----------

spark.table(TARGET_TABLE).printSchema()

# COMMAND ----------
# MAGIC %md
# MAGIC ## 8. Bronze Summary

# COMMAND ----------

total = spark.table(TARGET_TABLE).count()

print("=" * 80)
print("BRONZE LAYER INGESTION COMPLETED")
print("=" * 80)

print(f"Target Table      : {TARGET_TABLE}")
print(f"Source Path       : {SOURCE_PATH}")
print(f"Checkpoint Path   : {CHECKPOINT_LOCATION}")
print(f"Schema Path       : {SCHEMA_LOCATION}")
print(f"Total Records     : {total}")

print("=" * 80)
