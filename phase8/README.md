# Databricks Lakehouse Retail Clickstream Analytics Platform

## Phase 8 - Databricks Lakehouse Track

A complete end-to-end retail clickstream analytics platform built using the Databricks Lakehouse architecture.

This project demonstrates how raw JSON clickstream data from Amazon S3 can be transformed into business-ready analytics using:

- Delta Lake
- Auto Loader
- Unity Catalog
- Delta Live Tables
- Delta Sharing
- Databricks Workflows
- Databricks SQL Warehouse


---

# Project Architecture

                     AWS S3
                       |
                       |
                       ▼
          Databricks Auto Loader
                       |
                       |
                       ▼
                Bronze Delta Layer
              retail.bronze.clickstream
                       |
                       |
                       ▼
                Silver Delta Layer
             retail.silver.clickstream
                       |
          -----------------------------
          |                           |
          ▼                           ▼
    Gold Delta Tables          Delta Live Tables
          |
          |
          ▼
    Databricks SQL Warehouse
          |
          |
          ▼

         Dashboard

---

# Dataset Description

## Source Location

clickstream_day1.json

clickstream_day2.json

Approximately:

15,000 records per file

30,000 total events



---

# Source Schema

| Column | Data Type | Description |
|---|---|---|
| session_id | STRING | Unique browsing session |
| customer_id | STRING | Customer identifier |
| event_type | STRING | User action |
| event_ts | STRING | Event timestamp |
| page | STRING | Website page visited |


Example event:

```json
{
 "session_id":"3626008a-46f0-4ad4-bdba-95ddd06b2ada",
 "customer_id":"421595b3-8d5e-4b07-8e2a-7f89085d057d",
 "event_type":"search",
 "event_ts":"2026-06-30T13:27:14.625469",
 "page":"home"
}
