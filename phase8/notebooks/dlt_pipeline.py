# Databricks notebook source
# =============================================================================
# CAPSTONE PROJECT
# Phase 8 - Databricks Lakehouse Track
#
# File:
#     dlt_pipeline.py
#
# Purpose:
#     Implement Silver transformation using Delta Live Tables.
#
# Source:
#     retail.bronze.clickstream
#
# Target:
#     retail_dlt.silver_clickstream
#
# Features:
#
#     - Delta Live Tables
#     - Data Quality Expectations
#     - Cleansing
#     - Deduplication
#     - Timestamp Conversion
#
# Assignment Requirement:
#
#     Requirement 46
#
# =============================================================================

# COMMAND ----------

import dlt
from pyspark.sql.functions import *
from pyspark.sql.window import Window

# COMMAND ----------
# MAGIC %md
# MAGIC ## Configuration


# COMMAND ----------

CATALOG = "retail"
BRONZE_TABLE = (
    f"{CATALOG}.bronze.clickstream"
)


# COMMAND ----------
# MAGIC %md
# MAGIC # DLT Bronze Layer
#
# MAGIC Reads the existing Bronze Delta table.
#
# MAGIC Bronze remains the raw ingestion layer created by Auto Loader.


# COMMAND ----------

@dlt.table(
    name="dlt_bronze_clickstream",
    comment="Bronze clickstream data consumed from Auto Loader"
)

def bronze_clickstream():
    return (
        spark.table(BRONZE_TABLE)
    )



# COMMAND ----------
# MAGIC %md
# MAGIC # DLT Silver Layer
#
# MAGIC Transformations:
#
# MAGIC - Remove invalid records
# MAGIC - Standardize fields
# MAGIC - Convert timestamps
# MAGIC - Deduplicate events


# COMMAND ----------

@dlt.table(
    name="dlt_silver_clickstream",
    comment="Cleaned and conformed clickstream Silver table"
)


# -------------------------------------------------------------------
# Data Quality Expectations
#
# 1. expect
#    Warning only
#
# 2. expect_or_drop
#    Removes invalid records
#
# 3. expect_or_fail
#    Stops pipeline execution
# -------------------------------------------------------------------


@dlt.expect(
    "valid_customer",
    "customer_id IS NOT NULL"
)


@dlt.expect_or_drop(
    "valid_page",
    "page IS NOT NULL"
)

@dlt.expect_or_fail(
    "valid_event_type",
    """
    event_type IN
    (
        'search',
        'click',
        'cart',
        'checkout'
    )
    """
)

def silver_clickstream():

    df = dlt.read(
        "dlt_bronze_clickstream"
    )

    # Standardize columns

    df = (
        df
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


    # Remove duplicate events

    window = Window.partitionBy(
        "session_id",
        "event_ts"
    ).orderBy(
        col("ingestion_timestamp").desc()
    )


    df = (
        df
        .withColumn(
            "row_number",
            row_number().over(window)
        )
        .filter(
            col("row_number") == 1
        )
        .drop(
            "row_number"
        )
    )


    # Derived columns

    df = (
        df
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

    return (
        df.select(
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
    )
