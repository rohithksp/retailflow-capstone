-- ============================================================================
-- CAPSTONE PROJECT
-- Phase 8 - Databricks Lakehouse Track
--
-- File:
--     delta_share.sql
--
-- Purpose:
--     Configure Delta Sharing to expose Gold data to an external partner.
--
-- Shared Dataset:
--
--     retail.gold.daily_events
--
-- Business Scenario:
--
--     External retail analytics partner receives aggregated
--     website traffic metrics.
--
-- Requirement Covered:
--
--     Requirement 48
--
-- ============================================================================

-- ============================================================================
-- 1. CREATE DELTA SHARE
-- ============================================================================

CREATE SHARE IF NOT EXISTS retail_analytics_partner_share;

-- ============================================================================
-- 2. ADD GOLD TABLE TO SHARE
--
-- Only business-ready aggregated data is exposed.
--
-- ============================================================================

ALTER SHARE retail_analytics_partner_share
ADD TABLE retail.gold.daily_events;


-- ============================================================================
-- 3. CREATE EXTERNAL RECIPIENT
--
-- In a real implementation this would generate a sharing activation link.
--
-- ============================================================================

CREATE RECIPIENT IF NOT EXISTS external_retail_partner;

-- ============================================================================
-- 4. GRANT SHARE ACCESS
--
-- ============================================================================


GRANT SELECT
ON SHARE retail_analytics_partner_share
TO RECIPIENT external_retail_partner;

-- ============================================================================
-- 5. VERIFY SHARE CONTENTS
-- ============================================================================

SHOW ALL IN SHARE retail_analytics_partner_share;

-- ============================================================================
-- 6. VERIFY RECIPIENT
-- ============================================================================

SHOW RECIPIENTS;


-- ============================================================================
-- 7. PARTNER ACCESS INFORMATION
--
-- External partner receives:
--
--     Share Name:
--          retail_analytics_partner_share
--
--     Table:
--          retail.gold.daily_events
--
--
-- They can consume this using:
--
--     Databricks-to-Databricks Sharing
--     Open Delta Sharing Client
--
--
-- ============================================================================



-- ============================================================================
-- END OF DELTA SHARE CONFIGURATION
-- ============================================================================
