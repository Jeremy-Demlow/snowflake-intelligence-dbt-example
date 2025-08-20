"""
Web Scraper Tool Package
"""

# Tool metadata for tool_manager.py discovery
TOOL_CONFIG = {
    "name": "web_scraper", 
    "description": "AI-powered web scraper for competitive analysis with Claude integration",
    "requires_integration": True,
    "integration_type": "EXTERNAL_ACCESS",
    "has_local_testing": True,
    "has_deployment": True
}

# Import required functions only when needed by tool_manager
def __getattr__(name):
    if name in ["scrape_website_for_agent", "deploy_to_snowflake", "setup_integration", "test_local", "get_required_permissions"]:
        from .agent import scrape_website_for_agent, deploy_to_snowflake, setup_integration, test_local, get_required_permissions
        return locals()[name]
    raise AttributeError(f"module {__name__} has no attribute {name}")
