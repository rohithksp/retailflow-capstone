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

Architecture
                         AWS S3
                           |
                           |
                           v

                  Databricks Auto Loader

                           |
                           |
                           v

                 Bronze Delta Table

              retail.bronze.clickstream

                           |
                           |
                           v

                 Silver Delta Table

              retail.silver.clickstream

                           |
                           |
                           v

                  Gold Delta Tables

              retail.gold.*

                           |
                           |
                           v

              Databricks SQL Warehouse

                           |
                           |
                           v

                    Dashboard
Bronze Layer

Table:

retail.bronze.clickstream

Purpose:

Store raw clickstream events
Maintain ingestion history
Support incremental processing

Technology:

Databricks Auto Loader
Delta Lake
Checkpointing

Notebook:

notebooks/01_bronze_autoloader.py
Silver Layer

Table:

retail.silver.clickstream

Purpose:

Creates cleansed and conformed data.

Transformations:

Remove invalid records
Standardize fields
Convert timestamps
Deduplicate events
Create derived columns
Enable Change Data Feed

Notebook:

notebooks/02_silver.py
Gold Layer

The Gold layer contains business-ready analytical tables.

Daily Events

Table:

retail.gold.daily_events

Purpose:

Daily website traffic analysis.

Event Summary

Table:

retail.gold.event_summary

Purpose:

Customer behaviour analysis:

Search
Click
Cart
Checkout
Page Summary

Table:

retail.gold.page_summary

Purpose:

Identify most visited pages.

Daily Active Customers

Table:

retail.gold.daily_active_customers

Purpose:

Track daily customer engagement.

Notebook:

notebooks/03_gold.py
Delta Live Tables Pipeline

The Silver transformation is recreated using Delta Live Tables.

Features:

Managed pipeline execution
Data quality expectations
Automatic monitoring

Expectations:

Expectation	Type	Rule
valid_customer	expect	customer_id is not null
valid_page	expect_or_drop	Drop invalid pages
valid_event_type	expect_or_fail	Fail invalid events

Notebook:

notebooks/dlt_pipeline.py
Unity Catalog

Catalog:

retail

Schemas:

retail.bronze

retail.silver

retail.gold

Implemented:

External Location
Storage Credential
Three-level namespace
Column masking
Automatic lineage

Lineage:

Bronze
   |
   v
Silver
   |
   v
Gold

Configuration:

sql/unity_catalog.sql
Delta Sharing

Gold data is shared with an external analytics partner.

Shared table:

retail.gold.daily_events

Purpose:

Provide aggregated business metrics without exposing raw customer data.

Configuration:

sql/delta_share.sql
Workflow Orchestration

Databricks Workflow execution:

01_bronze_autoloader.py

        |
        v

Delta Live Tables Pipeline

        |
        v

03_gold.py

Features:

Multi-task workflow
Task dependencies
Retry handling
Failure notifications

Configuration:

workflow/workflow.json
Dashboard

Created using Databricks SQL Warehouse.

Dashboard tiles:

1. Daily Traffic Trend

Visualization:

Line Chart

Source:

retail.gold.daily_events
2. Event Distribution

Visualization:

Pie Chart

Source:

retail.gold.event_summary
3. Popular Pages

Visualization:

Bar Chart

Source:

retail.gold.page_summary
4. Active Customers

Visualization:

KPI / Line Chart

Source:

retail.gold.daily_active_customers

Screenshot:

screenshots/dashboard.png
Repository Structure
databricks-capstone/

│
├── notebooks/
│   ├── 01_bronze_autoloader.py
│   ├── 02_silver.py
│   ├── 03_gold.py
│   ├── dlt_pipeline.py
│   └── 04_dashboard_queries.sql
│
├── workflow/
│   └── workflow.json
│
├── dlt/
│   └── pipeline_settings.json
│
├── sql/
│   ├── unity_catalog.sql
│   └── delta_share.sql
│
├── screenshots/
│   └── dashboard.png
│
└── README.md

Technologies Used
Technology	Purpose
Databricks	Lakehouse platform
Delta Lake	Transaction storage
Auto Loader	Incremental ingestion
Unity Catalog	Governance
Delta Live Tables	Pipeline management
AWS S3	Data storage
SQL Warehouse	Analytics
Delta Sharing	External sharing
