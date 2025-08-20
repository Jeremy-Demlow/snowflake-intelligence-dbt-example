-- =====================================================
-- EMAIL TOOL PERMISSIONS
-- =====================================================
-- Required permissions for the email sending tool
-- Run as ACCOUNTADMIN before deploying the tool

-- Create email integration (if not exists)
CREATE OR REPLACE NOTIFICATION INTEGRATION ai_email_int
  TYPE = EMAIL
  ENABLED = TRUE
  ALLOWED_RECIPIENTS = ('*');  -- Restrict as needed for production

-- Grant usage to intelligence role
GRANT USAGE ON INTEGRATION ai_email_int TO ROLE SNOWFLAKE_INTELLIGENCE;

-- Grant warehouse usage (tools need a warehouse to execute)
GRANT USAGE ON WAREHOUSE HOL_WAREHOUSE TO ROLE SNOWFLAKE_INTELLIGENCE;
-- GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE SNOWFLAKE_INTELLIGENCE;

-- Grant procedure creation rights (if deploying to specific database/schema)
-- GRANT CREATE PROCEDURE ON SCHEMA your_database.your_schema TO ROLE SNOWFLAKE_INTELLIGENCE;
