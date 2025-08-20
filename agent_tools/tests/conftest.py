"""
Pytest configuration and fixtures for agent tools testing
"""

import pytest
from unittest.mock import Mock, MagicMock
from snowflake.snowpark import Session
from pathlib import Path
import sys
import os

# Add the agent_tools directory to the Python path
agent_tools_dir = Path(__file__).parent.parent
sys.path.insert(0, str(agent_tools_dir))

from snowflake_connection import ConnectionConfig, SnowflakeConnection

@pytest.fixture
def mock_session():
    """Mock Snowpark session for testing"""
    session = Mock(spec=Session)
    session.get_current_database.return_value = "TEST_DB"
    session.get_current_schema.return_value = "TEST_SCHEMA" 
    session.get_current_warehouse.return_value = "TEST_WH"
    session.sql.return_value = Mock()
    session.call.return_value = "Success"
    return session

@pytest.fixture
def mock_connection_config():
    """Mock connection configuration"""
    return ConnectionConfig(
        account="test_account",
        user="test_user",
        password="test_password",
        role="TEST_ROLE",
        warehouse="TEST_WH",
        database="TEST_DB",
        schema="TEST_SCHEMA"
    )

@pytest.fixture
def mock_snowflake_connection(mock_session, mock_connection_config):
    """Mock SnowflakeConnection for testing"""
    with pytest.mock.patch('snowflake_connection.Session') as mock_session_class:
        mock_session_class.builder.configs.return_value.create.return_value = mock_session
        connection = SnowflakeConnection.from_config(mock_connection_config)
        return connection

@pytest.fixture
def email_test_data():
    """Test data for email functionality"""
    return {
        "valid_email": "test@example.com",
        "invalid_email": "invalid-email",
        "subject": "Test Email Subject",
        "body": "<h1>Test Email Body</h1><p>This is a test email.</p>",
        "content_type": "text/html"
    }

@pytest.fixture(scope="session")
def test_output_dir():
    """Create test output directory"""
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir

# Skip tests that require real Snowflake connection unless explicitly enabled
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "snowflake: mark test as requiring real Snowflake connection"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )

def pytest_collection_modifyitems(config, items):
    """Skip Snowflake tests unless --snowflake flag is provided"""
    if not config.getoption("--snowflake", default=False):
        skip_snowflake = pytest.mark.skip(reason="need --snowflake option to run")
        for item in items:
            if "snowflake" in item.keywords:
                item.add_marker(skip_snowflake)

def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--snowflake",
        action="store_true",
        default=False,
        help="run tests that require real Snowflake connection"
    )
    parser.addoption(
        "--connection-name",
        action="store",
        default=None,
        help="Snowflake connection name to use for integration tests"
    )
