# Redshift Performance Analysis

## Query 1: Daily Revenue by Category (Single Date)

### SQL
```sql
EXPLAIN
SELECT
    p.category,
    SUM(f.amount) AS total_revenue
FROM fact_orders_items f
JOIN dim_product p
    ON f.product_id = p.product_id
WHERE CAST(f.order_date AS DATE) = '2026-07-11'
GROUP BY p.category;
```

### Execution Plan
```text
XN HashAggregate
  -> XN Seq Scan on mv_tbl__mv_daily_revenue_by_category__0
       Filter: (date((grvar_1)::text) = '2026-07-11'::date)
```

### Execution Plan Interpretation

| Operation | Description |
|----------|-------------|
| **XN Seq Scan** | Performs a sequential scan of the materialized view. Every row is read before applying the filter. |
| **Filter** | Restricts rows where `order_date = '2026-07-11'`. |
| **XN HashAggregate** | Groups rows by `category` and computes `SUM(amount)` efficiently using a hash table. |

### Performance Analysis

**Advantages**
- Query automatically uses the materialized view instead of scanning the base fact table.
- Hash aggregation is efficient for grouped aggregations.
- Local aggregation minimizes intermediate data movement.

**Potential Bottleneck**
- Sequential scan reads the entire materialized view before filtering.
- For very large materialized views, this increases disk I/O.

---

## Query 2: Daily Revenue by Category (Date Range with Sorting)

### SQL
```sql
EXPLAIN
SELECT
    p.category,
    SUM(f.amount) AS total_revenue
FROM fact_orders_items f
JOIN dim_product p
    ON f.product_id = p.product_id
WHERE CAST(f.order_date AS DATE)
      BETWEEN '2026-07-11' AND '2026-07-12'
GROUP BY p.category
ORDER BY total_revenue DESC;
```

### Execution Plan
```text
XN Merge
  Merge Key: sum(derived_table1.aggvar_1)
    -> XN Network
         Send to leader
           -> XN Sort
                Sort Key: sum(derived_table1.aggvar_1)
                  -> XN HashAggregate
                       -> XN Seq Scan on mv_tbl__mv_daily_revenue_by_category__0
                            Filter:
                            ((date((grvar_1)::text) <= '2026-07-12'::date)
                             AND
                             (date((grvar_1)::text) >= '2026-07-11'::date))
```

### Execution Plan Interpretation

| Operation | Description |
|----------|-------------|
| **XN Seq Scan** | Sequentially scans the materialized view and applies the date-range filter. |
| **XN HashAggregate** | Aggregates revenue grouped by product category. |
| **XN Sort** | Sorts aggregated results by `SUM(amount)` in descending order. |
| **XN Network** | Sends sorted results from compute nodes to the leader node. |
| **XN Merge** | Merges sorted streams from multiple nodes into the final ordered result. |

### Performance Analysis

**Advantages**
- Materialized view significantly reduces processing compared to the base fact table.
- Parallel aggregation improves scalability.
- Distributed sorting enables efficient processing across compute nodes.

**Potential Bottlenecks**
- Sequential scan still reads all rows in the materialized view.
- Sorting large aggregated datasets can consume additional memory and CPU.
- Network transfer introduces overhead before final merging.

---

# Optimization Recommendations

## 1. Distribution Keys

### Current Configuration

- **fact_orders_items**
  - `DISTSTYLE KEY`
  - `DISTKEY(product_id)`

- **dim_product**
  - `DISTSTYLE ALL`

### Analysis

This configuration is well optimized because:

- `dim_product` is replicated to every compute node.
- Joins on `product_id` occur locally without data redistribution.
- Network traffic during joins is minimized.

### Recommendation

If queries frequently join with other dimensions, consider matching distribution keys.

Example:

- `customer_id` for customer analytics
- `store_id` for store-level reporting

---

## 2. Sort Keys

### Current Sort Key

```text
(order_id, dt)
```

### Analysis

Current benefits:

- Efficient retrieval of individual orders.
- Some benefit for date filtering.

### Recommendation

If most analytical queries filter by date, use the date column as the leading sort key.

Example:

```text
(dt, order_id)
```

Benefits:

- Better zone-map pruning.
- Less disk I/O.
- Faster date-range scans.

---

## 3. Materialized View Refresh

Current configuration:

```sql
AUTO REFRESH YES
```

### Benefits

- Automatically keeps query results up to date.
- No manual intervention required.

### Considerations

For very large datasets:

- Automatic refresh may increase ETL overhead.
- Refresh operations can consume cluster resources.

### Recommendation

Use manual refresh during off-peak hours.

```sql
REFRESH MATERIALIZED VIEW mv_daily_revenue_by_category;
```

Monitor refresh status using:

```sql
SELECT *
FROM svv_mv_info;
```

---

## 4. COPY Performance

### Recommended File Format

Use **Parquet** whenever possible because it provides:

- Columnar storage
- Better compression
- Lower disk I/O
- Faster query performance

### CSV Best Practices

Always include:

```sql
IGNOREHEADER 1
```

Validate manifests before loading to avoid schema mismatches.

Monitor load failures:

```sql
SELECT *
FROM stl_load_errors;
```

---

## 5. Query Tuning

### Avoid Unnecessary Casting

Current query:

```sql
CAST(order_date AS DATE)
```

Repeated casting prevents optimal predicate evaluation.

### Recommendation

Store dates using the native **DATE** data type whenever possible.

Instead of:

```sql
VARCHAR
```

Use:

```sql
DATE
```

Benefits:

- Faster filtering
- Reduced CPU usage
- Better optimizer decisions

### Pre-Aggregation

For frequently executed reports:

- Create summary tables.
- Use incremental materialized views.
- Reduce repeated aggregation work.

---


## 6. Governance and Security

### Data Masking

Protect sensitive information using masking policies.

Example:

- Email masking
- Phone number masking

### Row-Level Security (RLS)

Apply RLS when users should only access specific subsets of data.

Example:

- Region-based access
- Department-based access
- Business unit restrictions

### Audit Permissions

Regularly review database roles and permissions.

Useful system tables:

```sql
SELECT *
FROM pg_roles;

SELECT *
FROM pg_group;
```

---

# Overall Assessment

### Strengths

- Efficient use of materialized views.
- Local joins using appropriate distribution styles.
- Parallel hash aggregation.
- Distributed sorting for ordered results.
- Good foundation for analytical workloads.

### Areas for Improvement

- Reduce sequential scans by optimizing sort keys.
- Store dates using native `DATE` data types.
- Schedule manual materialized view refreshes for large workloads.
- Use Parquet for bulk data loading.
- Introduce additional distribution keys where join patterns justify them.
- Implement row-level security and regular permission audits.

---

# Conclusion

The execution plans show that Amazon Redshift efficiently leverages **materialized views**, **parallel hash aggregation**, and **distributed query execution** to process analytical workloads. While the current implementation performs well, additional optimizations—such as improving sort key design, using native data types, optimizing distribution strategies, and managing materialized view refreshes—can further reduce query execution time, improve scalability, and lower resource consumption for large-scale data warehouse environments.
