# Agent Tools Architecture

## Overview
The Agent Tools library provides a scalable, organized way to build and deploy tools for Snowflake Intelligence agents. Tools are organized in dedicated folders with clean separation of concerns.

## Folder Structure
```
agent_tools/
├── tools/
│   ├── email_send/                    # Email tool package
│   │   ├── __init__.py               # Package config & exports
│   │   └── agent.py                  # @sproc implementation  
│   └── web_scraper/                  # Web scraper tool package
│       ├── __init__.py               # Package config & exports
│       ├── core.py                   # Core scraping logic
│       ├── ai.py                     # Claude AI analysis
│       └── agent.py                  # @sproc implementation
├── tool_manager.py                   # Central tool management
├── create_new_tool.py               # Tool creation utility
├── snowflake_connection.py          # Connection utilities
└── README.md                        # Usage documentation
```

## Design Principles

### 1. **Folder-Based Organization**
- Each tool gets its own folder under `tools/`
- No more flat file structure confusion
- Easy to find and maintain specific tool code

### 2. **Clean Separation of Concerns**
- `core.py`: Business logic, validation, utilities
- `ai.py`: AI analysis and Claude integration  
- `agent.py`: Snowflake @sproc wrapper for agents
- `__init__.py`: Tool configuration and exports

### 3. **Scalable Architecture**
- Adding new tools: just create a new folder
- Consistent interface across all tools
- Centralized deployment and management

### 4. **@sproc First Approach**
- Uses Snowflake stored procedures (@sproc) for better performance
- HTML responses for rich agent output
- Proper error handling and logging

## Current Tools

### Email Send (`tools/email_send/`)
- **Purpose**: Send HTML emails from agents
- **Deployment**: `AGENT_TOOLS_CENTRAL.AGENT_TOOLS.SEND_MAIL`
- **Integration**: EMAIL notification integration
- **Usage**: `Send_Email` tool in agents

### Web Scraper (`tools/web_scraper/`)  
- **Purpose**: AI-powered competitive analysis and market research
- **Deployment**: `AGENT_TOOLS_CENTRAL.AGENT_TOOLS.WEB_SCRAPE`
- **Integration**: EXTERNAL_ACCESS for web requests
- **AI Features**: 
  - Claude suggests competitor URLs
  - AI analysis of competitive landscape
  - Price extraction and comparison
  - Beautiful HTML reports
- **Usage**: `Web_scrape` tool in agents

## Tool Manager Commands

```bash
# View all tools
python tool_manager.py status

# Test a tool locally  
python tool_manager.py test web_scraper url=https://example.com

# Deploy a tool to Snowflake
python tool_manager.py deploy web_scraper

# Set up integrations (email, external access, etc.)
python tool_manager.py setup web_scraper
```

## Creating New Tools

### Option 1: Use the Generator
```bash
python create_new_tool.py my_new_tool "Description of my tool"
```

### Option 2: Manual Creation
1. Create folder: `tools/my_new_tool/`
2. Add `__init__.py` with `TOOL_CONFIG`
3. Add `agent.py` with required functions:
   - `main_handler_function()` - Entry point for agents
   - `deploy_to_snowflake()` - Snowflake deployment
   - `setup_integration()` - Integration setup  
   - `test_local()` - Local testing
   - `get_required_permissions()` - SQL permissions

## Agent Integration

Tools automatically appear in agents when:
1. Deployed to `AGENT_TOOLS_CENTRAL.AGENT_TOOLS`
2. Added to agent's `tool_resources` section
3. Proper permissions granted to `SNOWFLAKE_INTELLIGENCE_*_RL` roles

Example agent configuration:
```json
"tool_resources": {
  "Web_scrape": {
    "type": "procedure",
    "identifier": "AGENT_TOOLS_CENTRAL.AGENT_TOOLS.WEB_SCRAPE",
    "name": "WEB_SCRAPE(VARCHAR)",
    "execution_environment": {
      "type": "warehouse",
      "warehouse": "HOL_WAREHOUSE"
    }
  }
}
```

## Benefits of This Architecture

✅ **Organized**: Clear folder structure, easy to navigate  
✅ **Scalable**: Add tools without refactoring existing code  
✅ **Modular**: Reusable components (core logic, AI analysis)  
✅ **Maintainable**: Each tool is self-contained  
✅ **Testable**: Local testing built into every tool  
✅ **Powerful**: Claude AI integration for intelligent analysis  
✅ **Beautiful**: HTML responses for rich agent interactions  
✅ **Secure**: URL validation and access controls  

This architecture makes it easy to build sophisticated agent tools while maintaining clean, scalable code.
