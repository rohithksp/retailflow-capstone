-- ============================================================================
-- CAPSTONE PROJECT
-- Phase 8 - Databricks Lakehouse Track
--
-- File:
--     unity_catalog.sql
--
-- Purpose:
--     Configure Unity Catalog objects.
--
-- Features:
--
--     - Catalog creation
--     - Schema creation
--     - External location
--     - Storage credential
--     - Three-level namespace
--     - Column masking
--     - Lineage support
--
-- Requirement Covered:
--     Requirement 47
--
-- ============================================================================


-- ============================================================================
-- 1. CREATE CATALOG
-- ============================================================================

CREATE CATALOG IF NOT EXISTS retail;

-- ============================================================================
-- 2. CREATE SCHEMAS
--
-- Three-layer Medallion Architecture
--
-- retail.bronze
-- retail.silver
-- retail.gold
--
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS retail.bronze;
CREATE SCHEMA IF NOT EXISTS retail.silver;
CREATE SCHEMA IF NOT EXISTS retail.gold;

-- ============================================================================
-- 3. CREATE STORAGE CREDENTIAL
--
-- NOTE:
-- Replace IAM role ARN with your AWS IAM role.
--
-- No instance profile shortcut is used.
--
-- ============================================================================

CREATE STORAGE CREDENTIAL IF NOT EXISTS retail_storage_credential
WITH AWS IAM ROLE
'arn:aws:iam::<ACCOUNT_ID>:role/databricks-retail-role';


-- ============================================================================
-- 4. CREATE EXTERNAL LOCATION
--
-- Source:
--
-- s3://databricks-capstone-retail-bucket/
--
-- ============================================================================

CREATE EXTERNAL LOCATION IF NOT EXISTS retail_external_location
URL
's3://databricks-capstone-retail-bucket/'
WITH STORAGE CREDENTIAL retail_storage_credential;

-- ============================================================================
-- 5. GRANT ACCESS
--
-- Example permissions
--
-- ============================================================================

GRANT
READ FILES
ON EXTERNAL LOCATION retail_external_location
TO `data_engineers`;


GRANT
USE CATALOG
ON CATALOG retail
TO `data_engineers`;

GRANT
USE SCHEMA
ON SCHEMA retail.bronze
TO `data_engineers`;

GRANT
USE SCHEMA
ON SCHEMA retail.silver
TO `data_engineers`;


GRANT
USE SCHEMA
ON SCHEMA retail.gold
TO `data_engineers`;


-- ============================================================================
-- 6. THREE LEVEL NAMESPACE EXAMPLES
--
-- Databricks naming convention:
--
-- catalog.schema.table
--
-- Examples:
--
-- retail.bronze.clickstream
-- retail.silver.clickstream
-- retail.gold.daily_events
--
-- ============================================================================

SHOW TABLES IN retail.bronze;
SHOW TABLES IN retail.silver;
SHOW TABLES IN retail.gold;



-- ============================================================================
-- 7. CUSTOMER TABLE FOR COLUMN MASKING DEMONSTRATION
--
-- The provided clickstream data does not contain email.
--
-- This demonstrates Unity Catalog masking capability.
--
-- ============================================================================


CREATE TABLE IF NOT EXISTS retail.silver.customers
(
customer_id STRING,
customer_email STRING
)
USING DELTA;



-- ============================================================================
-- 8. CREATE EMAIL MASKING FUNCTION
--
-- Admin users see real email.
-- Other users see masked value.
--
-- ============================================================================

CREATE FUNCTION IF NOT EXISTS retail.silver.mask_email
(email STRING)
RETURN
CASE
WHEN
is_account_group_member('admins')
THEN email
ELSE
CONCAT(
LEFT(email,2),
'*****',
SUBSTRING(email,LOCATE('@',email))
)
END;


-- ============================================================================
-- 9. APPLY COLUMN MASK
--
-- ============================================================================

ALTER TABLE retail.silver.customers
ALTER COLUMN customer_email
SET MASK retail.silver.mask_email;

-- ============================================================================
-- 10. VERIFY MASKING
-- ============================================================================

DESCRIBE TABLE retail.silver.customers;

-- ============================================================================
-- 11. LINEAGE
--
-- Unity Catalog automatically captures lineage.
--
-- Expected lineage:
--
--
-- S3 JSON
--    |
--    |
--    v
-- retail.bronze.clickstream
--    |
--    |
--    v
-- retail.silver.clickstream
--    |
--    |
--    v
-- retail.gold.daily_events
--
--
-- No additional code required.
--
-- View from:
--
-- Catalog Explorer
--      |
--      Table
--      |
--      Lineage
--
-- ============================================================================



-- ============================================================================
-- END OF UNITY CATALOG CONFIGURATION
-- ============================================================================
