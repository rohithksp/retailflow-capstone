# RetailFlow Capstone Project

## 📌 Overview
RetailFlow is a fictional mid-size e-commerce company.  
This capstone project demonstrates how to build a **cloud data platform** on AWS, taking raw messy order data through a governed data lake, into two parallel analytics engines (Amazon Redshift and Databricks), and out to business-ready dashboards.

---

## 🎯 Objectives
- Build a **three-zone S3 data lake** (Bronze, Silver, Gold).
- Implement **data ingestion utilities** with Boto3, logging, and retry logic.
- Apply **data quality rules** and schema evolution handling in AWS Glue.
- Model a **star schema** in Amazon Redshift Serverless.
- Build a **Delta Lake medallion pipeline** in Databricks with Unity Catalog governance.
- Deliver **BI-ready dashboards** on both Redshift and Databricks.

---

## 🗂 Project Phases
- **Phase 0 – Environment Setup**  
  AWS Budget, Databricks workspace, GitHub repo initialized  
- **Phase 1 – Synthetic Data Generation**  
  Faker datasets, profiling, charts  
- **Phase 2 – Boto3 Ingestion Utility**  
  S3 ingestion package with retry + logging  
- **Phase 3 – S3 Data Lake Foundations**  
  Bronze/Silver/Gold zones, partitioning, lifecycle rules  
- **Phase 4 – Glue Catalog & Athena**  
  Crawlers, partition projection, cost comparison  
- **Phase 5 – Lake Formation Governance**  
  LF-Tags, role-based access, masking  
- **Phase 6 – Glue ETL with Data Quality**  
  PySpark ETL, schema evolution, DQDL rules  
- **Phase 7 – Redshift Serverless**  
  Star schema, COPY load, Spectrum, materialized views  
- **Phase 8 – Databricks Lakehouse**  
  Delta tables, Auto Loader, DLT pipeline, dashboard  
- **Phase 9 – Final Integration Report**  
  Architecture diagram, cost review, reflection  

---

## 📂 Deliverables
- Data generation notebook + profiling report + charts  
- S3 ingestion package + logs  
- S3 bucket screenshots + ARCHITECTURE.md  
- Athena cost comparison report  
- Lake Formation governance proof  
- Glue ETL job + DQDL rules + CloudWatch metrics  
- Redshift scripts + performance notes  
- Databricks notebooks + pipeline/workflow JSON + dashboard screenshot  
- Final integration report  

---

## ⚙️ Tech Stack
- **AWS**: S3, Glue, Lake Formation, Athena, Redshift Serverless, CloudWatch  
- **Databricks**: Delta Lake, Auto Loader, Delta Live Tables, Unity Catalog, Workflows  
- **Python**: Faker, Pandas, NumPy, Matplotlib, Seaborn, Boto3  
- **VS Code / Colab**: Development environments  
- **GitHub**: Version control & deliverables  

---

## 🚀 Getting Started
1. Clone this repo:
   ```bash
   git clone https://github.com/rohithksp/retailflow-capstone.git
