-- acme Intelligence Demo - User Access Management
-- This script shows how to grant access to additional users

USE ROLE ACCOUNTADMIN;

-- ========================================
-- OPTION 1: GRANT DEMO ROLE TO USER
-- ========================================
-- This gives the user the same permissions as the demo role
-- Recommended for most use cases

GRANT ROLE acme_INTELLIGENCE_DEMO TO USER JDEMLOW;

-- Optionally set it as their default role
-- ALTER USER JDEMLOW SET DEFAULT_ROLE = acme_INTELLIGENCE_DEMO;

-- ========================================
-- OPTION 2: CREATE USER-SPECIFIC ROLE
-- ========================================
-- This creates a dedicated role for the user with custom permissions
-- Useful when you want to limit or customize access

CREATE OR REPLACE ROLE JDEMLOW_acme_ACCESS 
COMMENT = 'Custom acme Intelligence access for JDEMLOW';

-- Grant basic warehouse access
GRANT USAGE ON WAREHOUSE HOL_WAREHOUSE TO ROLE JDEMLOW_acme_ACCESS;
GRANT USAGE ON DATABASE acme_INTELLIGENCE TO ROLE JDEMLOW_acme_ACCESS;

-- Grant schema access (choose what they need)
GRANT USAGE ON SCHEMA acme_INTELLIGENCE.RAW TO ROLE JDEMLOW_acme_ACCESS;
GRANT USAGE ON SCHEMA acme_INTELLIGENCE.STAGING TO ROLE JDEMLOW_acme_ACCESS;
GRANT USAGE ON SCHEMA acme_INTELLIGENCE.MARTS TO ROLE JDEMLOW_acme_ACCESS;
GRANT USAGE ON SCHEMA acme_INTELLIGENCE.SEMANTIC_MODELS TO ROLE JDEMLOW_acme_ACCESS;
GRANT USAGE ON SCHEMA acme_INTELLIGENCE.SEARCH TO ROLE JDEMLOW_acme_ACCESS;
GRANT USAGE ON SCHEMA acme_INTELLIGENCE.AGENTS TO ROLE JDEMLOW_acme_ACCESS;

-- Grant table access (read-only for safety)
GRANT SELECT ON ALL TABLES IN SCHEMA acme_INTELLIGENCE.RAW TO ROLE JDEMLOW_acme_ACCESS;
GRANT SELECT ON ALL TABLES IN SCHEMA acme_INTELLIGENCE.STAGING TO ROLE JDEMLOW_acme_ACCESS;
GRANT SELECT ON ALL TABLES IN SCHEMA acme_INTELLIGENCE.MARTS TO ROLE JDEMLOW_acme_ACCESS;

-- Grant Intelligence component access
GRANT USAGE ON SEMANTIC VIEW acme_INTELLIGENCE.SEMANTIC_MODELS.acme_ANALYTICS_VIEW TO ROLE JDEMLOW_acme_ACCESS;
GRANT USAGE ON CORTEX SEARCH SERVICE acme_INTELLIGENCE.SEARCH.acme_DOCUMENT_SEARCH TO ROLE JDEMLOW_acme_ACCESS;
GRANT USAGE ON AGENT acme_INTELLIGENCE.AGENTS.acme_INTELLIGENCE_AGENT TO ROLE JDEMLOW_acme_ACCESS;

-- Grant the role to the user
GRANT ROLE JDEMLOW_acme_ACCESS TO USER JDEMLOW;

-- ========================================
-- OPTION 3: READ-ONLY ACCESS
-- ========================================
-- This creates a read-only role for users who just need to view data
-- Good for analysts, executives, or external stakeholders

CREATE OR REPLACE ROLE acme_INTELLIGENCE_READONLY 
COMMENT = 'Read-only access to acme Intelligence demo';

-- Basic access
GRANT USAGE ON WAREHOUSE HOL_WAREHOUSE TO ROLE acme_INTELLIGENCE_READONLY;
GRANT USAGE ON DATABASE acme_INTELLIGENCE TO ROLE acme_INTELLIGENCE_READONLY;

-- Schema access
GRANT USAGE ON SCHEMA acme_INTELLIGENCE.MARTS TO ROLE acme_INTELLIGENCE_READONLY;
GRANT USAGE ON SCHEMA acme_INTELLIGENCE.SEMANTIC_MODELS TO ROLE acme_INTELLIGENCE_READONLY;
GRANT USAGE ON SCHEMA acme_INTELLIGENCE.AGENTS TO ROLE acme_INTELLIGENCE_READONLY;

-- Read-only table access
GRANT SELECT ON ALL TABLES IN SCHEMA acme_INTELLIGENCE.MARTS TO ROLE acme_INTELLIGENCE_READONLY;

-- Intelligence component access (read-only)
GRANT USAGE ON SEMANTIC VIEW acme_INTELLIGENCE.SEMANTIC_MODELS.acme_ANALYTICS_VIEW TO ROLE acme_INTELLIGENCE_READONLY;
GRANT USAGE ON AGENT acme_INTELLIGENCE.AGENTS.acme_INTELLIGENCE_AGENT TO ROLE acme_INTELLIGENCE_READONLY;

-- Grant to user
-- GRANT ROLE acme_INTELLIGENCE_READONLY TO USER JDEMLOW;

-- ========================================
-- VERIFICATION QUERIES
-- ========================================

-- Check what roles the user has
SHOW GRANTS TO USER JDEMLOW;

-- Check what the demo role can access
SHOW GRANTS TO ROLE acme_INTELLIGENCE_DEMO;

-- Test user access (run as the user)
-- USE ROLE acme_INTELLIGENCE_DEMO;
-- SELECT * FROM SEMANTIC_VIEW(
--     acme_INTELLIGENCE.SEMANTIC_MODELS.acme_analytics_view
--     METRICS technician_count, total_revenue_sum
-- );

-- ========================================
-- CLEANUP (if needed)
-- ========================================

-- To remove access:
-- REVOKE ROLE acme_INTELLIGENCE_DEMO FROM USER JDEMLOW;
-- REVOKE ROLE JDEMLOW_acme_ACCESS FROM USER JDEMLOW;
-- DROP ROLE IF EXISTS JDEMLOW_acme_ACCESS;

SELECT '=== USER ACCESS GRANTED ===' as status;
SELECT 'User JDEMLOW now has access to acme Intelligence demo' as message;
