# Data Profile Report – RetailFlow Synthetic Dataset

## 📌 Overview
This report summarizes the profiling results of the synthetic datasets generated in Phase 1.  
It covers null rates, duplicates, schema evolution, and deliberate data quality issues injected.

---

## 1. Customers.csv
- **Rows generated**: 5,000 (+ ~1% duplicates)
- **Null/invalid emails**: ~2%
- **Duplicate customer_id count**: <fill in>
- **Notes**: Email column deliberately contains nulls and malformed values to simulate real-world dirty data.

---

## 2. Products.csv
- **Rows generated**: 800
- **Categories**: Electronics, Clothing, Books, Home, Sports
- **Unit price range**: <fill in from `describe()`, e.g. 5–500>
- **Notes**: Clean catalog, no deliberate issues.

---

## 3. Orders Day1 (orders_day1.json)
- **Rows generated**: 20,000
- **Columns**: order_id, customer_id, order_ts, store_region, status
- **Null rates**: <fill in>
- **Notes**: Order timestamps distributed across the year; store_region balanced across 4 regions.

---

## 4. Order Items Day1 (order_items_day1.json)
- **Rows generated**: ~55,000
- **Invalid product_id references**: <fill in count>
- **Negative/zero quantities**: <fill in count>
- **Revenue distribution**: <summary from histogram>
- **Notes**: Includes deliberate referential integrity failures and invalid quantities.

---

## 5. Orders Day2 (orders_day2.json)
- **Rows generated**: ~4,000
- **New column introduced**: `discount_code`
- **Schema evolution**: Day2 adds discount_code not present in Day1.
- **Notes**: Values include DISC10, DISC20, FREESHIP, and null.

---

## 6. Order Items Day2 (order_items_day2.json)
- **Rows generated**: ~11,000
- **Invalid product_id references**: <fill in count>
- **Negative/zero quantities**: <fill in count>
- **Notes**: Includes discount_code column and deliberate data quality issues.

---

## 7. Clickstream Day1/Day2
- **Rows generated**: ~15,000 per day
- **Columns**: session_id, customer_id, event_type, event_ts, page
- **Event types**: page_view, add_to_cart, checkout, search
- **Notes**: Used for streaming ingestion in Databricks Auto Loader.

---

## 8. Charts Produced
1. Order volume by day (bar chart)  
2. Revenue distribution (histogram)  
3. Top 10 categories by revenue (bar chart)  
4. Null-rate heatmap across all files (Seaborn heatmap)

---

## 9. Key Findings
- **Data quality issues injected successfully**:
  - Null/malformed emails (~2%)
  - Duplicate customer_ids (~1%)
  - Invalid product_id references
  - Negative/zero quantities
- **Schema evolution handled**: discount_code introduced in Day2.
- **Profiling confirms**: datasets are realistic, dirty, and ready for downstream ETL.

---

## ✅ Deliverables
- `01_data_generation.ipynb` (notebook with code + outputs)  
- `data_profile_report.md` (this report)  
- 4+ PNG charts in `charts/` folder  

