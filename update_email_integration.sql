/*
Update Email Integration - Add Sean Guillen
============================================
This script adds sean.guillen@snowflake.com to the allowed recipients 
for the ai_email_int notification integration.
*/

USE ROLE ACCOUNTADMIN;

-- Option 1: ALTER existing integration to add Sean's email (RECOMMENDED)
-- This preserves the existing setup and just adds the new recipient
ALTER NOTIFICATION INTEGRATION ai_email_int 
SET ALLOWED_RECIPIENTS = ('jeremy.demlow@snowflake.com', 'sean.guillen@snowflake.com')
COMMENT = 'Email integration for ACME Intelligence agents - Updated to include Sean Guillen';

-- Verify the integration was updated
DESC NOTIFICATION INTEGRATION ai_email_int;

-- Test the updated integration
SELECT 'Email integration updated successfully - both Jeremy and Sean can now receive emails' as status;

/*
Alternative Option 2: Create new integration with broader email list
====================================================================
Uncomment below if you prefer a new integration instead:

CREATE OR REPLACE NOTIFICATION INTEGRATION acme_team_email_int
    TYPE = EMAIL
    ENABLED = TRUE
    ALLOWED_RECIPIENTS = (
        'jeremy.demlow@snowflake.com',
        'sean.guillen@snowflake.com'
        -- Add more team members as needed:
        -- 'other.teammate@snowflake.com'
    )
    COMMENT = 'Email integration for ACME Intelligence team';

-- To use the new integration, update sender.py line 20:
-- Change 'ai_email_int' to 'acme_team_email_int'
*/

/*
Future Team Management:
======================
To add more team members later, run:

ALTER NOTIFICATION INTEGRATION ai_email_int 
SET ALLOWED_RECIPIENTS = (
    'jeremy.demlow@snowflake.com', 
    'sean.guillen@snowflake.com',
    'new.teammate@snowflake.com'
);
*/
