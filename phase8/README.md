# Databricks Lakehouse Retail Clickstream Analytics Platform

**Phase 8 — Databricks Lakehouse Track**

A complete end-to-end retail clickstream analytics platform built using the Databricks Lakehouse architecture.

## Overview

This project demonstrates:

- Data ingestion from Amazon S3
- Auto Loader incremental ingestion
- Delta Lake Bronze/Silver/Gold architecture
- Delta Live Tables (DLT) pipeline
- Unity Catalog governance
- Delta Sharing
- Databricks Workflow orchestration
- SQL Warehouse dashboard analytics

The goal of this project is to process retail clickstream JSON data stored in Amazon S3 and transform it into business-ready analytics datasets, following the **Medallion Architecture**:

```
Amazon S3
    │
    ▼
Bronze Delta Layer
    │
    ▼
Silver Delta Layer
    │
    ▼
Gold Delta Layer
    │
    ▼
Databricks SQL Dashboard
```

The platform provides insights into:

- Website traffic trends
- Customer activity
- Event behaviour
- Popular website pages

## Source Data

**S3 Location**

```
s3://databricks-capstone-retail-bucket/raw/clickstream/
```

**Files**

- `clickstream_day1.json`
- `clickstream_day2.json`

**Dataset size**

- ~15,000 records per file
- ~30,000 total clickstream events

**Source Schema**

| Column        | Description             |
|---------------|--------------------------|
| `session_id`  | Unique browsing session |
| `customer_id` | Customer identifier      |
| `event_type`  | Customer action          |
| `event_ts`    | Event timestamp          |
| `page`        | Website page visited     |

**Example record**

```json
{
  "session_id": "3626008a-46f0-4ad4-bdba-95ddd06b2ada",
  "customer_id": "421595b3-8d5e-4b07-8e2a-7f89085d057d",
  "event_type": "search",
  "event_ts": "2026-06-30T13:27:14.625469",
  "page": "home"
}
```

## Architecture

```
                    AWS S3
                      │
                      ▼
            Databricks Auto Loader
                      │
                      ▼
              Bronze Delta Table
            retail.bronze.clickstream
                      │
                      ▼
              Silver Delta Table
            retail.silver.clickstream
                      │
                      ▼
               Gold Delta Tables
                 retail.gold.*
                      │
                      ▼
            Databricks SQL Warehouse
                      │
                      ▼
                   Dashboard
```

## Bronze Layer

- **Table:** `retail.bronze.clickstream`
- **Notebook:** `notebooks/01_bronze_autoloader.py`

**Purpose**

- Store raw clickstream events
- Maintain ingestion history
- Support incremental processing

**Technology**

- Databricks Auto Loader
- Delta Lake
- Checkpointing

## Silver Layer

- **Table:** `retail.silver.clickstream`
- **Notebook:** `notebooks/02_silver.py`

**Purpose:** Creates cleansed and conformed data.

**Transformations**

- Remove invalid records
- Standardize fields
- Convert timestamps
- Deduplicate events
- Create derived columns
- Enable Change Data Feed

## Gold Layer

The Gold layer contains business-ready analytical tables.

**Notebook:** `notebooks/03_gold.py`

| Table                                 | Purpose                              |
|----------------------------------------|---------------------------------------|
| `retail.gold.daily_events`             | Daily website traffic analysis        |
| `retail.gold.event_summary`            | Customer behaviour analysis (search, click, cart, checkout) |
| `retail.gold.page_summary`             | Identify most visited pages           |
| `retail.gold.daily_active_customers`   | Track daily customer engagement       |

## Delta Live Tables Pipeline

The Silver transformation is recreated using Delta Live Tables.

**Notebook:** `notebooks/dlt_pipeline.py`

**Features**

- Managed pipeline execution
- Data quality expectations
- Automatic monitoring

**Expectations**

| Expectation          | Type              | Rule                          |
|-----------------------|-------------------|--------------------------------|
| `valid_customer`      | `expect`          | `customer_id` is not null      |
| `valid_page`          | `expect_or_drop`  | Drop invalid pages             |
| `valid_event_type`    | `expect_or_fail`  | Fail invalid events            |

## Unity Catalog

**Catalog:** `retail`

**Schemas**

- `retail.bronze`
- `retail.silver`
- `retail.gold`

**Implemented**

- External Location
- Storage Credential
- Three-level namespace
- Column masking
- Automatic lineage

**Lineage**

```
Bronze → Silver → Gold
```

**Configuration:** `sql/unity_catalog.sql`

## Delta Sharing

Gold data is shared with an external analytics partner.

- **Shared table:** `retail.gold.daily_events`
- **Purpose:** Provide aggregated business metrics without exposing raw customer data
- **Configuration:** `sql/delta_share.sql`

## Workflow Orchestration

Databricks Workflow execution order:

```
01_bronze_autoloader.py
        │
        ▼
Delta Live Tables Pipeline
        │
        ▼
03_gold.py
```

**Features**

- Multi-task workflow
- Task dependencies
- Retry handling
- Failure notifications

**Configuration:** `workflow/workflow.json`

## Dashboard

Created using Databricks SQL Warehouse.

| # | Tile                  | Visualization      | Source                                |
|---|------------------------|---------------------|-----------------------------------------|
| 1 | Daily Traffic Trend    | Line Chart          | `retail.gold.daily_events`             |
| 2 | Event Distribution     | Pie Chart           | `retail.gold.event_summary`            |
| 3 | Popular Pages          | Bar Chart           | `retail.gold.page_summary`             |
| 4 | Active Customers       | KPI / Line Chart    | `retail.gold.daily_active_customers`   |

**Screenshot:** `screenshots/dashboard.png`

## Repository Structure

```
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
```

## Technologies Used

| Technology         | Purpose                  |
|----------------------|---------------------------|
| Databricks           | Lakehouse platform        |
| Delta Lake            | Transaction storage       |
| Auto Loader           | Incremental ingestion     |
| Unity Catalog         | Governance                |
| Delta Live Tables     | Pipeline management       |
| AWS S3                | Data storage               |
| SQL Warehouse         | Analytics                  |
| Delta Sharing         | External sharing           |

## Requirement Mapping

| Requirement | Implementation                              |
|-------------|-----------------------------------------------|
| 42          | Databricks cluster and Git repo               |
| 43          | Bronze Delta tables with External Location    |
| 44          | Auto Loader ingestion                          |
| 45          | Silver and Gold Delta tables                   |
| 46          | Delta Live Tables expectations                 |
| 47          | Unity Catalog and masking                      |
| 48          | Delta Sharing                                   |
| 49          | Workflow orchestration                          |
| 50          | SQL Warehouse dashboard                         |

## Future Enhancements

- Add product transaction data
- Customer segmentation
- Recommendation engine
- Real-time streaming analytics
- Machine learning models
- CI/CD deployment
