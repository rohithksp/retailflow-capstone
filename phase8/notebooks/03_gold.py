# Databricks notebook source
# =============================================================================
# CAPSTONE PROJECT
# Phase 8 - Databricks Lakehouse Track
#
# Notebook:
#     03_gold.py
#
# Purpose:
#     Create business-ready Gold Delta tables from the Silver clickstream layer.
#
# Source:
#     retail.silver.clickstream
#
# Target Tables:
#
#     retail.gold.daily_events
#     retail.gold.event_summary
#     retail.gold.page_summary
#     retail.gold.daily_active_customers
#
#
# Business KPIs:
#
#     - Daily traffic trends
#     - Event type analysis
#     - Page popularity
#     - Daily active customers
#
# Assignment Requirement:
#     Requirement 45
#
# =============================================================================


# COMMAND ----------

from pyspark.sql.functions import *

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Runtime Parameters

# COMMAND ----------

dbutils.widgets.text("catalog", "retail")
dbutils.widgets.text("silver_schema", "silver")
dbutils.widgets.text("gold_schema", "gold")


CATALOG = dbutils.widgets.get("catalog")
SILVER_SCHEMA = dbutils.widgets.get("silver_schema")
GOLD_SCHEMA = dbutils.widgets.get("gold_schema")
SILVER_TABLE = f"{CATALOG}.{SILVER_SCHEMA}.clickstream"


# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Create Gold Schema

# COMMAND ----------

spark.sql(f"""
CREATE SCHEMA IF NOT EXISTS
{CATALOG}.{GOLD_SCHEMA}
""")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Read Silver Data

# COMMAND ----------

silver_df = spark.table(SILVER_TABLE)

display(
    silver_df.limit(20)
)


# COMMAND ----------

silver_count = silver_df.count()

print(f"Silver Records Available : {silver_count}")


# COMMAND ----------
# MAGIC %md
# MAGIC # GOLD TABLE 1
# MAGIC
# MAGIC ## Daily Events
# MAGIC
# MAGIC Business Purpose:
# MAGIC
# MAGIC Shows total website activity per day.

# COMMAND ----------

daily_events = (
    silver_df
    .groupBy(
        "event_date"
    )
    .agg(
        count("*")
        .alias("total_events")

    )
    .orderBy(
        "event_date"
    )
)

display(daily_events)

# COMMAND ----------

daily_events.write \
.format("delta") \
.mode("overwrite") \
.saveAsTable(
    f"{CATALOG}.{GOLD_SCHEMA}.daily_events"
)


# COMMAND ----------
# MAGIC %md
# MAGIC # GOLD TABLE 2
# MAGIC
# MAGIC ## Event Summary
# MAGIC
# MAGIC Business Purpose:
# MAGIC
# MAGIC Understand customer interaction behaviour.
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC Search events vs Checkout events.

# COMMAND ----------

event_summary = (
    silver_df
    .groupBy(
        "event_type"
    )
    .agg(
        count("*")
        .alias("total_events")
    )
    .orderBy(
        desc("total_events")
    )
)

display(event_summary)

# COMMAND ----------

event_summary.write \
.format("delta") \
.mode("overwrite") \
.saveAsTable(
    f"{CATALOG}.{GOLD_SCHEMA}.event_summary"
)


# COMMAND ----------
# MAGIC %md
# MAGIC # GOLD TABLE 3
# MAGIC
# MAGIC ## Page Summary
# MAGIC
# MAGIC Business Purpose:
# MAGIC
# MAGIC Identify the most visited website pages.

# COMMAND ----------

page_summary = (
    silver_df
    .groupBy(
        "page"
    )
    .agg(
        count("*")
        .alias("page_visits")
    )
    .orderBy(
        desc("page_visits")
    )
)

display(page_summary)

# COMMAND ----------

page_summary.write \
.format("delta") \
.mode("overwrite") \
.saveAsTable(
    f"{CATALOG}.{GOLD_SCHEMA}.page_summary"
)


# COMMAND ----------
# MAGIC %md
# MAGIC # GOLD TABLE 4
# MAGIC
# MAGIC ## Daily Active Customers
# MAGIC
# MAGIC Business Purpose:
# MAGIC
# MAGIC Measures unique customers visiting the platform each day.

# COMMAND ----------


daily_active_customers = (
    silver_df
    .groupBy(
        "event_date"
    )
    .agg(
        countDistinct("customer_id")
        .alias("active_customers")
    )
    .orderBy(
        "event_date"
    )
)

display(daily_active_customers)


# COMMAND ----------


daily_active_customers.write \
.format("delta") \
.mode("overwrite") \
.saveAsTable(
    f"{CATALOG}.{GOLD_SCHEMA}.daily_active_customers"
)


# MAGIC ## 4. Validate Gold Tables
#
# MAGIC Validate that all business-ready tables have been created successfully.

# COMMAND ----------

GOLD_DAILY_EVENTS = f"{CATALOG}.{GOLD_SCHEMA}.daily_events"
GOLD_EVENT_SUMMARY = f"{CATALOG}.{GOLD_SCHEMA}.event_summary"
GOLD_PAGE_SUMMARY = f"{CATALOG}.{GOLD_SCHEMA}.page_summary"
GOLD_DAU = f"{CATALOG}.{GOLD_SCHEMA}.daily_active_customers"


# COMMAND ----------

gold_tables = [
    GOLD_DAILY_EVENTS,
    GOLD_EVENT_SUMMARY,
    GOLD_PAGE_SUMMARY,
    GOLD_DAU
]

for table in gold_tables:
    print("-----------------------------------")
    print(f"Checking table: {table}")
    count = spark.table(table).count()
    print(f"Records: {count}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 5. Daily Events Validation

# COMMAND ----------

display(
spark.sql(f"""
SELECT
event_date,
total_events
FROM {GOLD_DAILY_EVENTS}
ORDER BY event_date
""")
)


# COMMAND ----------
# MAGIC %md
# MAGIC ## 6. Event Behaviour Analysis

# COMMAND ----------

display(
spark.sql(f"""
SELECT
event_type,
total_events,
ROUND((total_events * 100.0) /SUM(total_events) OVER(),2) AS event_percentage
FROM {GOLD_EVENT_SUMMARY}
ORDER BY total_events DESC
""")
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 7. Most Popular Pages

# COMMAND ----------

display(
spark.sql(f"""
SELECT
page,
page_visits
FROM {GOLD_PAGE_SUMMARY}
ORDER BY page_visits DESC
LIMIT 10
""")
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 8. Daily Active Customer Trend

# COMMAND ----------

display(
spark.sql(f"""
SELECT
event_date,
active_customers
FROM {GOLD_DAU}
ORDER BY event_date
""")
)


# COMMAND ----------
# MAGIC %md
# MAGIC ## 9. Business KPI Summary

# COMMAND ----------

kpi_summary = spark.sql(f"""
SELECT
COUNT(DISTINCT customer_id)
AS total_customers,
COUNT(DISTINCT session_id)
AS total_sessions,
COUNT(*)
AS total_events,
COUNT(DISTINCT event_date)
AS active_days
FROM {SILVER_TABLE}
""")

display(kpi_summary)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 10. Session Engagement Analysis
#
# MAGIC Although not stored as a Gold table,
# MAGIC this query helps validate user engagement.

# COMMAND ----------


display(
spark.sql(f"""
SELECT
AVG(event_count)
AS avg_events_per_session
FROM
(
SELECT
session_id,
COUNT(*) event_count
FROM {SILVER_TABLE}
GROUP BY session_id
)
""")
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 11. Optimize Gold Tables
#
# MAGIC Improves dashboard query performance.

# COMMAND ----------


for table in gold_tables:
    spark.sql(f"""
    OPTIMIZE {table}
    """)
    print(f"Optimized {table}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 12. Verify Delta Tables

# COMMAND ----------


for table in gold_tables:
    print("="*70)
    print(table)
    spark.sql(
        f"DESCRIBE DETAIL {table}"
    ).show(truncate=False)


# COMMAND ----------
# MAGIC %md
# MAGIC ## 13. Final Gold Layer Summary

# COMMAND ----------

print("="*80)

print("GOLD LAYER PROCESSING COMPLETED")

print("="*80)

print("")
print("Source Layer")
print("----------------")
print(SILVER_TABLE)
print("")
print("Created Gold Tables")
print("-------------------")

for table in gold_tables:
    print("✓", table)


print("")

print("Business KPIs Available")

print("-----------------------")

print("✓ Daily Website Traffic")

print("✓ Event Behaviour Analysis")

print("✓ Popular Pages")

print("✓ Daily Active Customers")

print("="*80)
