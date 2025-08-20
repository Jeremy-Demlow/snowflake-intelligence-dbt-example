-- =====================================================
-- BASIC ROLE SETUP FOR SNOWFLAKE INTELLIGENCE
-- =====================================================
-- One-time setup for the main intelligence role
-- Run as ACCOUNTADMIN

-- Create the intelligence role
CREATE ROLE IF NOT EXISTS SNOWFLAKE_INTELLIGENCE;
GRANT ROLE SNOWFLAKE_INTELLIGENCE TO ROLE ACCOUNTADMIN;

-- Basic permissions for agent development
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE SNOWFLAKE_INTELLIGENCE;
GRANT CREATE DATABASE ON ACCOUNT TO ROLE SNOWFLAKE_INTELLIGENCE;

-- Create a database for intelligence tools (optional)
CREATE DATABASE IF NOT EXISTS SNOWFLAKE_INTELLIGENCE;
GRANT ALL ON DATABASE SNOWFLAKE_INTELLIGENCE TO ROLE SNOWFLAKE_INTELLIGENCE;

CREATE SCHEMA IF NOT EXISTS SNOWFLAKE_INTELLIGENCE.TOOLS;
GRANT ALL ON SCHEMA SNOWFLAKE_INTELLIGENCE.TOOLS TO ROLE SNOWFLAKE_INTELLIGENCE;

-- Note: Individual tools will have their own permission files
-- See: email_tool_permissions.sql, web_scraper_permissions.sql, etc.
