# AWS Glue Pipeline Validation

This document demonstrates how AWS Glue job bookmarks and schema evolution were configured and validated in the capstone pipeline.

---

## Step 29 — Enable Job Bookmarks

In the Glue job parameters, set the option to enable bookmarking:

```json
{
  "--job-bookmark-option": "job-bookmark-enable"
}
```

This ensures Glue tracks processed data and avoids re‑processing the same files.

## Step 30 — Schema Evolution

* Source tables (`Orders`, `Order Items`, `Customers`, `Products`) may evolve over time.
* Glue `DynamicFrames` were converted to `DataFrames` and reconciled with the latest schema.

### Example Evolution Code:

```python
# Convert DynamicFrame to DataFrame
df = dyf.toDF()

# Reconcile schema by adding a new column with null values
df = df.withColumn("new_column", F.lit(None).cast("string"))
```

This guarantees downstream queries do not break when new columns are introduced.

## Step 31 — Data Quality Rules

The DQDL ruleset is stored in Amazon S3 at `s3://capstone-project-bucket-12345/config/dqdl_rules.json`.

### Checks Applied:
* **Completeness:** Required fields must not be null.
* **Uniqueness:** Primary keys are thoroughly deduplicated.
* **Referential Integrity:** Foreign keys are validated against parent tables.
* **Routing:** Valid records are written to the curated layer, while invalid records are routed to the quarantine layer.

## Step 32 — Quarantine Routing

Invalid records are written to a dedicated S3 location partitioned by date (`dt`) for traceability:

* **S3 Path:** `s3://capstone-project-bucket-12345/quarantine/<table>/`
* **File Example:** `s3://capstone-project-bucket-12345/quarantine/orders/dt=2026-07-11/part-0000.parquet`

## Step 33 — CloudWatch Metrics

Custom metrics are published to Amazon CloudWatch to track data quality performance:
* Count of valid vs. quarantined records.
* Rule violations per table.
* As of now, we could see 100% valid hence we can observe straight line in a image.

### Example Metric Implementation:

```python
dq_valid_orders = orders_valid.count()
dq_quarantine_orders = orders_quarantine.count()

cloudwatch.put_metric_data(
    Namespace="CapstoneDQ",
    MetricData=[
        {
            "MetricName": "OrdersValidCount",
            "Value": dq_valid_orders,
            "Unit": "Count"
        },
        {
            "MetricName": "OrdersQuarantineCount",
            "Value": dq_quarantine_orders,
            "Unit": "Count"
        }
    ]
)
```

## Proof of Execution

* **Job Bookmarks:** Confirmed by Glue logs showing only new files were processed.
* **Schema Evolution:** Tested successfully by adding a new column (`discount_code`) to the `Orders` table.
* **DQ Rules:** Validated by verifying that records missing a `customer_id` in `Orders` were correctly routed to quarantine.
* **CloudWatch Metrics:** Verified as fully visible and updating in the `CapstoneDQ` namespace.

## Conclusion

This pipeline successfully demonstrates:
* **Bookmarking:** Efficient incremental data loads.
* **Schema Evolution:** Resilient handling of schema changes.
* **Data Quality:** Config‑driven enforcement rules.
* **Quarantine Routing:** Isolation of invalid records.
* **Observability:** Operational metrics monitored in CloudWatch.
