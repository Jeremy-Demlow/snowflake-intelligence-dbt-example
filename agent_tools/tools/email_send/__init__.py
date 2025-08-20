"""
Email Send Tool Package
"""

# Tool metadata for tool_manager.py discovery
TOOL_CONFIG = {
    "name": "email_send",
    "description": "Agent-compatible email sender tool for Snowflake Intelligence agents",
    "requires_integration": True,
    "integration_type": "EMAIL",
    "has_local_testing": True,
    "has_deployment": True
}

# Import required functions only when needed by tool_manager
def __getattr__(name):
    if name in ["send_email_for_agent", "deploy_to_snowflake", "setup_integration", "test_local", "get_required_permissions"]:
        from .agent import send_email_for_agent, deploy_to_snowflake, setup_integration, test_local, get_required_permissions
        return locals()[name]
    raise AttributeError(f"module {__name__} has no attribute {name}")
