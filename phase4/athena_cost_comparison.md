# Athena Cost Comparison: Pruned vs. Un‑Pruned Queries

## Context
- Tables: `customers`, `products`, `orders`, `order_items`
- Each table currently has **only one file in a single partition**.
- Goal: Compare Athena query cost (bytes scanned) between full table scans and partition‑filtered queries.

## Queries Executed

### 1. Un‑Pruned Query

SELECT COUNT(*) FROM orders; -- 3.09mb
SELECT COUNT(*)  FROM customers; -- 513.30kb
SELECT COUNT(*)  FROM products; -- 20.80kb

### 2. Pruned Query

select count(*) from products where dt = '2026-07-11'; -- 20.80kb
select count(*) from orders where dt = '2026-07-11'; -- 3.09mb
select count(*) from customers where dt = '2026-07-11'; -- 513.30kb

## **Observations**
No difference in bytes scanned between pruned and un‑pruned queries.
Reason: Each table has only one partition with one file. Athena must read the same file regardless of filters.

Partition pruning benefits appear only when:
Multiple partitions exist in the Glue Data Catalog.
Queries filter on the actual partition column.

## **Conclusion**
Current setup does not demonstrate cost savings from partition pruning.
To show impact, we can restructure S3 data into multiple partitioned folders (e.g., order_date=YYYY-MM-DD/) and reload partitions in Athena.
