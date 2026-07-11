# Lake Formation Governance — Phase 5 Deliverable

## 24. Register S3 Bucket & Switch Database to LF‑Managed
- **Bucket registered:** `s3://capstone-project-bucket-12345/raw/`
- **Service role used:** `AWSServiceRoleForLakeFormationDataAccess`
- **Database:** `capstone-project-bucket-12345`
- **Permissions mode:** Lake Formation (converted from IAM/Glue policies)

✅ Result: Database now governed by Lake Formation permissions.

---

## 25. Create LF‑Tags
- **LF‑Tag Key:** `data_sensitivity`
  - Values: `PII`, `Confidential`, `Public`
- **LF‑Tag Key:** `department`
  - Values: `analytics`, `engineering`

✅ Result: Classification framework established.

---

## 26. Apply LF‑Tags
- **Table:** `customers`
  - Column: `email`,`phone` → `data_sensitivity = PII`
- **Curated/Gold tables (Phase 6)**  
  - Entire table → `data_sensitivity = Confidential`

✅ Result: Fine‑grained column‑level control ready.

---

## 27. Create IAM Personas & Grant Permissions
- **Role:** `data_analyst`
  - Granted: `SELECT` where `data_sensitivity = Confidential`
  - Denied: `PII` (no grant for PII values)
- **Role:** `data_engineer`
  - Granted: `SELECT` where `data_sensitivity IN (Confidential, PII)`

✅ Result: Roles have differentiated access boundaries.

---

## 28. Access Proof via Athena
- **Test Query:** `SELECT * FROM customers;`

### Screenshot 1 — Analyst Role
- Role assumed: `data_analyst`
- Result: `email` column **not visible** (blocked by LF‑Tag governance)

### Screenshot 2 — Engineer Role
- Role assumed: `data_engineer`
- Result: `email` column **visible** (granted via LF‑Tag expression)

✅ Result: Governance boundary proven.

---

## Observations
- Removing broad IAMAllowedPrincipals grants was necessary to enforce LF‑Tags.
- LF‑Tag expressions now control access at both table and column level.
- Analyst vs. Engineer personas demonstrate clear separation of duties.

---

## Deliverables
- **LF‑Tag assignments:** documented above.
- **Screenshots:**  
  - Athena query as `data_analyst` (email hidden).  
  - Athena query as `data_engineer` (email visible).
