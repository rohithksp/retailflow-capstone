This document demonstrates how AWS Glue job bookmarks and schema evolution were configured and validated in the capstone pipeline.

---

## Step 29 — Enable Job Bookmarks
- In the Glue job parameters, set:
  ```json
  {
    "job-bookmark-option": "job-bookmark-enable"
  }

This ensures Glue tracks processed data and avoids re‑processing the same files.

**Step 30 — Schema Evolution
**
- Source tables (Orders, Order Items, Customers, Products) may evolve over time.
- Glue DynamicFrames were converted to DataFrames and reconciled with the latest schema.

Example:

- df = dyf.toDF()
- df = df.withColumn("new_column", F.lit(None).cast("string"))
- This guarantees downstream queries don’t break when new columns are introduced.

**Step 31 — Data Quality Rules
**
- Ruleset stored in S3 (config/dqdl_rules.json).
- Checks applied:
  - Completeness: Required fields not null.
  - Uniqueness: Primary keys deduplicated.
  - Referential Integrity: Foreign keys validated against parent tables.
  - Valid records written to curated layer.
  - Invalid records routed to quarantine layer.

**Step 32 — Quarantine Routing
**
- Invalid records are written to:
- s3://capstone-project-bucket-12345/quarantine/<table>/
- Partitioned by dt for traceability.

Example:
- s3://.../quarantine/orders/dt=2026-07-11/part-0000.parquet

**Step 33 — CloudWatch Metrics
**
Custom metrics published for:
- Count of valid vs. quarantined records.
- Rule violations per table.

**Example metric:
**
dq_valid_orders = orders_valid.count()
dq_quarantine_orders = orders_quarantine.count()
cloudwatch.put_metric_data(
    Namespace="CapstoneDQ",
    MetricData=[{
        "MetricName": "OrdersValidCount",
        "Value": dq_valid_orders
    }]
)

**Proof of Execution
**
- Job bookmarks confirmed by Glue logs: only new files processed.
- Schema evolution tested by adding a new column (discount_code) to Orders.
- DQ rules validated: missing customer_id in Orders correctly routed to quarantine.
- CloudWatch metrics visible in the CapstoneDQ namespace.

**Conclusion
**
This pipeline demonstrates:

- Bookmarking for incremental loads.
- Schema evolution handling.
- Config‑driven data quality enforcement.
- Quarantine routing for invalid records.

Operational metrics in CloudWatch.

