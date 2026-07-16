# Databricks notebook source
# MAGIC %md
# MAGIC # Step 43 & 44: Bronze Layer Ingestion via Auto Loader
# MAGIC - Utilizes Unity Catalog External Locations (no instance profiles).
# MAGIC - Uses Auto Loader in directory-listing mode with schema inference and checkpointing.

# COMMAND ----------

# Define source and target paths using Unity Catalog Catalog and Schema
CATALOG = "main"
SCHEMA = "clickstream_analytics"
VOLUME_SOURCE_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/raw/clickstream/"
CHECKPOINT_PATH = f"dbfs:/pipelines/{CATALOG}_{SCHEMA}/_checkpoints/bronze_clickstream/"
TARGET_TABLE = f"{CATALOG}.{SCHEMA}.bronze_clickstream"

# COMMAND ----------

# Configure Auto Loader Stream
df_stream = (spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.useNotifications", "false")  # Enforces directory-listing mode
  .option("cloudFiles.inferColumnTypes", "true")
  .option("cloudFiles.schemaLocation", f"{CHECKPOINT_PATH}/schema")
  .load(VOLUME_SOURCE_PATH)
)

# COMMAND ----------

# Add ingestion metadata
from pyspark.sql.functions import current_timestamp, input_file_name

df_bronze = (df_stream
  .withColumn("ingested_at", current_timestamp())
  .withColumn("source_file", input_file_name())
)

# COMMAND ----------

# Write stream to Unity Catalog Delta Table
query = (df_bronze.writeStream
  .format("delta")
  .outputMode("append")
  .option("checkpointLocation", f"{CHECKPOINT_PATH}/data")
  .trigger(availableNow=True)  # Processes day1/day2 files incrementally in batch mode
  .toTable(TARGET_TABLE)
)

query.awaitTermination()
