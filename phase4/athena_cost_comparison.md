# Athena Cost Comparison: Pruned vs. Un-Pruned Queries

## Context

- Tables: `customers`, `products`, `orders`, `order_items`
- `customers` and `products` currently contain **only one partition with a single data file**.
- The `orders` table contains **multiple partitions**, allowing Athena to demonstrate **partition pruning**.
- Goal: Compare Athena query cost (bytes scanned) and execution time between full table scans and partition-filtered queries.

---

# Queries Executed

## 1. Un-Pruned Queries

```sql
SELECT COUNT(*) FROM orders;
-- Data scanned: 3.84 MB
-- Runtime: 1.237 sec

SELECT COUNT(*) FROM customers;
-- Data scanned: 513.30 KB

SELECT COUNT(*) FROM products;
-- Data scanned: 20.80 KB
```

---

## 2. Partition-Pruned Queries

```sql
SELECT COUNT(*) FROM orders
WHERE dt = '2026-07-11';
-- Data scanned: 764.66 KB
-- Runtime: 853 ms

SELECT COUNT(*) FROM customers
WHERE dt = '2026-07-11';
-- Data scanned: 513.30 KB

SELECT COUNT(*) FROM products
WHERE dt = '2026-07-11';
-- Data scanned: 20.80 KB
```

---

# Results Comparison

| Table | Query Type | Data Scanned | Runtime | Observation |
|--------|------------|-------------:|---------:|-------------|
| `orders` | Un-Pruned | **3.84 MB** | **1.237 sec** | Full table scan across all partitions. |
| `orders` | Pruned (`WHERE dt='2026-07-11'`) | **764.66 KB** | **853 ms** | Athena scanned only the required partition, reducing both data scanned and execution time. |
| `customers` | Un-Pruned | 513.30 KB | — | Single partition; full scan required. |
| `customers` | Pruned | 513.30 KB | — | No reduction because only one partition exists. |
| `products` | Un-Pruned | 20.80 KB | — | Single partition; full scan required. |
| `products` | Pruned | 20.80 KB | — | No reduction because only one partition exists. |

---

# Observations

### Orders Table

The `orders` table contains multiple partitions, enabling Athena's **partition pruning** feature.

Applying the partition filter (`WHERE dt = '2026-07-11'`):

- Reduced data scanned from **3.84 MB** to **764.66 KB**.
- Reduced query runtime from **1.237 sec** to **853 ms**.
- Athena read only the matching partition instead of scanning all available partitions.

### Customers and Products Tables

No difference was observed between pruned and un-pruned queries because each table currently contains only a single partition with one data file. Since there are no additional partitions to eliminate, Athena scans the same amount of data regardless of the partition filter.

---

# Conclusion

The results demonstrate the effectiveness of **partition pruning** on the `orders` table. By filtering on the partition column (`dt`), Athena scanned approximately **80% less data** (3.84 MB → 764.66 KB) and completed the query faster (1.237 sec → 853 ms).

For the `customers` and `products` tables, partition pruning provides no measurable benefit because each table currently consists of only one partition. As additional partitions are added over time, queries that filter on the partition column will similarly benefit from reduced data scanning, lower query costs, and improved execution performance.
