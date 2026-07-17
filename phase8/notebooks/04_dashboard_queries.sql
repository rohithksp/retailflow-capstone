-- ============================================================================
-- CAPSTONE PROJECT
-- Phase 8 - Databricks Lakehouse Track
--
-- File:
--     04_dashboard_queries.sql
--
-- Purpose:
--     SQL queries used by Databricks SQL Dashboard.
--
-- Source:
--     Gold Delta Tables
--
-- Dashboard Tiles:
--
--     1. Daily Website Traffic
--     2. Event Type Distribution
--     3. Most Visited Pages
--     4. Daily Active Customers
--
-- Requirement Covered:
--     Requirement 50
--
-- ============================================================================



-- ============================================================================
-- TILE 1
-- DAILY WEBSITE TRAFFIC TREND
--
-- Visualization:
-- Line Chart
--
-- X Axis:
-- event_date
--
-- Y Axis:
-- total_events
-- ============================================================================


SELECT
event_date,
total_events
FROM retail.gold.daily_events
ORDER BY event_date;



-- ============================================================================
-- TILE 2
-- CUSTOMER EVENT BEHAVIOUR
--
-- Visualization:
-- Bar Chart / Pie Chart
--
-- Shows:
-- search
-- click
-- cart
-- checkout
--
-- ============================================================================


SELECT
event_type,
total_events,
ROUND((total_events * 100.0)/SUM(total_events) OVER(),2) AS percentage
FROM retail.gold.event_summary
ORDER BY total_events DESC;



-- ============================================================================
-- TILE 3
-- MOST VISITED PAGES
--
-- Visualization:
-- Horizontal Bar Chart
--
-- ============================================================================


SELECT
page,
page_visits
FROM retail.gold.page_summary
ORDER BY page_visits DESC
LIMIT 10;



-- ============================================================================
-- TILE 4
-- DAILY ACTIVE CUSTOMERS
--
-- Visualization:
-- KPI + Trend Line
--
-- ============================================================================


SELECT
event_date,
active_customers
FROM retail.gold.daily_active_customers
ORDER BY event_date;



-- ============================================================================
-- ALERT QUERY
--
-- KPI:
-- Total Daily Events
--
-- Example Alert:
--
-- Trigger when today's events < 100
--
-- Databricks SQL Alert:
--
-- Schedule:
-- Daily
--
-- Condition:
-- value < 100
--
-- ============================================================================


SELECT
SUM(total_events) AS today_events
FROM retail.gold.daily_events
WHERE event_date = current_date();


-- ============================================================================
-- OPTIONAL BUSINESS KPI QUERY
--
-- Useful for dashboard header cards
--
-- ============================================================================


SELECT
COUNT(DISTINCT customer_id) AS total_customers,
COUNT(DISTINCT session_id) AS total_sessions,
COUNT(*) AS total_events
FROM retail.silver.clickstream;
