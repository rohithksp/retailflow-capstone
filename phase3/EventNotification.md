# Event Notification Setup

## Overview

To automate metadata discovery for newly uploaded datasets, **Amazon EventBridge** rules were configured to monitor object creation events in the Amazon S3 bucket.

**Bucket Name:** `capstone-project-bucket-12345`

Two EventBridge rules were created based on the data format and S3 folder structure:

| Rule Name | Monitored Prefixes | Intended Target |
|------------|--------------------|-----------------|
| `RawCsvArrivalRule` | `raw/customers/`, `raw/products/` | `csv_crawler_customers_products` |
| `RawJsonArrivalRule` | `raw/orders/`, `raw/order_items/` | `json_crawler_orders_items` |

> **Note:** For the scope of this capstone project, the EventBridge rules are created and documented. Live target integration with AWS Glue crawlers is not required.

---

# EventBridge Rule 1 – CSV Files

**Rule Name:** `RawCsvArrivalRule`

This rule detects object creation events for CSV datasets uploaded to the following S3 prefixes:

- `raw/customers/`
- `raw/products/`

### AWS CLI Command

```bash
aws events put-rule \
  --name RawCsvArrivalRule \
  --event-pattern '{
    "source": ["aws.s3"],
    "detail-type": ["Object Created"],
    "detail": {
      "bucket": {
        "name": ["capstone-project-bucket-12345"]
      },
      "object": {
        "key": [
          { "prefix": "raw/customers/" },
          { "prefix": "raw/products/" }
        ]
      }
    }
  }'
```

### Event Pattern

```json
{
  "source": ["aws.s3"],
  "detail-type": ["Object Created"],
  "detail": {
    "bucket": {
      "name": ["capstone-project-bucket-12345"]
    },
    "object": {
      "key": [
        {
          "prefix": "raw/customers/"
        },
        {
          "prefix": "raw/products/"
        }
      ]
    }
  }
}
```

---

# EventBridge Rule 2 – JSON Files

**Rule Name:** `RawJsonArrivalRule`

This rule detects object creation events for JSON datasets uploaded to the following S3 prefixes:

- `raw/orders/`
- `raw/order_items/`

### AWS CLI Command

```bash
aws events put-rule \
  --name RawJsonArrivalRule \
  --event-pattern '{
    "source": ["aws.s3"],
    "detail-type": ["Object Created"],
    "detail": {
      "bucket": {
        "name": ["capstone-project-bucket-12345"]
      },
      "object": {
        "key": [
          { "prefix": "raw/orders/" },
          { "prefix": "raw/order_items/" }
        ]
      }
    }
  }'
```

### Event Pattern

```json
{
  "source": ["aws.s3"],
  "detail-type": ["Object Created"],
  "detail": {
    "bucket": {
      "name": ["capstone-project-bucket-12345"]
    },
    "object": {
      "key": [
        {
          "prefix": "raw/orders/"
        },
        {
          "prefix": "raw/order_items/"
        }
      ]
    }
  }
}
```

---

# Intended Glue Crawler Targets

The EventBridge rules are designed to trigger the appropriate AWS Glue crawler after new files are uploaded.

| EventBridge Rule | Glue Crawler |
|------------------|--------------|
| `RawCsvArrivalRule` | `csv_crawler_customers_products` |
| `RawJsonArrivalRule` | `json_crawler_orders_items` |

---

# Architecture Flow

```text
S3 Bucket
(capstone-project-bucket-12345)
│
├── raw/customers/
├── raw/products/
│        │
│        └── RawCsvArrivalRule
│                 │
│                 └── csv_crawler_customers_products
│
├── raw/orders/
└── raw/order_items/
         │
         └── RawJsonArrivalRule
                  │
                  └── json_crawler_orders_items
```

---

# Summary

- Created two Amazon EventBridge rules.
- Monitored S3 object creation events for CSV and JSON datasets.
- Configured separate rules based on S3 prefixes.
- Intended targets are AWS Glue crawlers for automated metadata discovery.
- For this capstone project, the rules are created and documented; live EventBridge-to-Glue target wiring is not implemented.
