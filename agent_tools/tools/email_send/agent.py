"""
Agent-compatible email sender - clean implementation
"""

import logging
from typing import Optional

try:
    from snowflake.snowpark import Session
except ImportError:
    Session = None

logger = logging.getLogger(__name__)

def send_email_for_agent(session: Session, recipient: str, subject: str, text: str) -> str:
    """
    Main handler function for Snowflake stored procedure
    Returns success/failure message for the agent
    """
    try:
        session.call(
            'SYSTEM$SEND_EMAIL',
            'ai_email_int',
            recipient,
            subject,
            text,
            'text/html'
        )
        logger.info(f"Email sent successfully to {recipient} with subject: '{subject}'")
        return f'Email was sent to {recipient} with subject: "{subject}".'
    except Exception as e:
        logger.error(f"Failed to send email to {recipient} with subject '{subject}': {e}")
        return f'Failed to send email: {str(e)}'

# Snowflake stored procedure deployment
DEPLOYMENT_SQL = """
CREATE OR REPLACE PROCEDURE send_mail(recipient TEXT, subject TEXT, text TEXT)
RETURNS TEXT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'send_email_for_agent'
AS
$$
import logging
from snowflake.snowpark import Session

logger = logging.getLogger(__name__)

def send_email_for_agent(session: Session, recipient: str, subject: str, text: str) -> str:
    try:
        session.call(
            'SYSTEM$SEND_EMAIL',
            'ai_email_int',
            recipient,
            subject,
            text,
            'text/html'
        )
        logger.info(f"Email sent successfully to {recipient} with subject: '{subject}'")
        return f'Email was sent to {recipient} with subject: "{subject}".'
    except Exception as e:
        logger.error(f"Failed to send email to {recipient} with subject '{subject}': {e}")
        return f'Failed to send email: {str(e)}'
$$;
"""

def deploy_to_snowflake(session: Session) -> bool:
    """Deploy email sender to centralized location"""
    try:
        session.sql("USE DATABASE AGENT_TOOLS_CENTRAL").collect()
        session.sql("USE SCHEMA AGENT_TOOLS").collect()
        
        session.sql(DEPLOYMENT_SQL).collect()
        logger.info("Email sender deployed to AGENT_TOOLS_CENTRAL.AGENT_TOOLS")
        return True
        
    except Exception as e:
        logger.error(f"Email sender deployment failed: {e}")
        return False

def setup_integration(session: Session, **kwargs) -> bool:
    """Set up email integration"""
    try:
        session.sql("USE DATABASE AGENT_TOOLS_CENTRAL").collect()
        session.sql("USE SCHEMA AGENT_TOOLS").collect()
        
        # Create notification integration
        integration_sql = """
        CREATE OR REPLACE NOTIFICATION INTEGRATION ai_email_int
        TYPE=EMAIL
        ENABLED=TRUE
        ALLOWED_RECIPIENTS=('Jeremy.Demlow@snowflake.com')
        """
        
        session.sql(integration_sql).collect()
        logger.info("Email integration created")
        return True
        
    except Exception as e:
        logger.error(f"Failed to set up email integration: {e}")
        return False

def test_local(**kwargs) -> bool:
    """Test email sender locally"""
    recipient = kwargs.get('recipient', 'test@example.com')
    subject = kwargs.get('subject', 'Test Email')
    text = kwargs.get('text', '<h1>Test Email</h1><p>This is a test email from the agent tools.</p>')
    
    print(f"[LOCAL TEST] Would send email to: {recipient}")
    print(f"Subject: {subject}")
    print(f"Content: {text[:100]}...")
    return True

def get_required_permissions() -> str:
    """Required SQL permissions for email sender"""
    return """
-- Email Sender Tool Permissions - Centralized in AGENT_TOOLS_CENTRAL

-- 1. Database and schema permissions
GRANT USAGE ON DATABASE AGENT_TOOLS_CENTRAL TO ROLE SNOWFLAKE_INTELLIGENCE_ADMIN_RL;
GRANT USAGE ON SCHEMA AGENT_TOOLS_CENTRAL.AGENT_TOOLS TO ROLE SNOWFLAKE_INTELLIGENCE_ADMIN_RL;
GRANT USAGE ON PROCEDURE AGENT_TOOLS_CENTRAL.AGENT_TOOLS.SEND_MAIL(TEXT, TEXT, TEXT) TO ROLE SNOWFLAKE_INTELLIGENCE_ADMIN_RL;

-- 2. Email integration
GRANT USAGE ON INTEGRATION AI_EMAIL_INT TO ROLE SNOWFLAKE_INTELLIGENCE_ADMIN_RL;

-- 3. Also grant to modeling role
GRANT USAGE ON DATABASE AGENT_TOOLS_CENTRAL TO ROLE SNOWFLAKE_INTELLIGENCE_MODELING_RL;
GRANT USAGE ON SCHEMA AGENT_TOOLS_CENTRAL.AGENT_TOOLS TO ROLE SNOWFLAKE_INTELLIGENCE_MODELING_RL;
GRANT USAGE ON PROCEDURE AGENT_TOOLS_CENTRAL.AGENT_TOOLS.SEND_MAIL(TEXT, TEXT, TEXT) TO ROLE SNOWFLAKE_INTELLIGENCE_MODELING_RL;

-- 4. Warehouse usage
GRANT USAGE ON WAREHOUSE HOL_WAREHOUSE TO ROLE SNOWFLAKE_INTELLIGENCE_ADMIN_RL;
GRANT USAGE ON WAREHOUSE SNOW_INTELLIGENCE_DEMO_WH TO ROLE SNOWFLAKE_INTELLIGENCE_ADMIN_RL;
"""
