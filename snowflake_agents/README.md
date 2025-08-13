# Snowflake Agents Management

This directory manages Snowflake Intelligence Agents independently from the dbt data pipeline.

## Why Separate from dbt?

Agents are **operational entities** that:
- Can have tools added/removed dynamically
- Need configuration updates independent of data models
- Have different deployment lifecycles than data transformations
- Require operational management (start/stop/modify)

## Directory Structure

```
snowflake_agents/
├── README.md                           # This file
├── agent_config.yml                    # Agent configurations
├── manage_agents.py                    # Agent management CLI
├── acme_intelligence_agent.sql # acme agent definition
└── [future_agent].sql                 # Additional agents
```

## Usage

### Deploy Agents
```bash
# Deploy specific agent
python manage_agents.py deploy acme_intelligence_agent

# Deploy all agents
python manage_agents.py deploy-all
```

### Manage Agents
```bash
# List available agents
python manage_agents.py list

# Test agent functionality
python manage_agents.py test acme_intelligence_agent

# Check agent status
python manage_agents.py status
```

### Direct SQL Deployment
```bash
# Deploy using SnowCLI directly
snow sql -f acme_intelligence_agent.sql
```

## Agent Configuration

Agents are configured in `agent_config.yml` with:
- **Tools**: Cortex Analyst, Cortex Search, custom functions
- **Instructions**: Response behavior and orchestration logic
- **Sample Questions**: Example queries for users
- **Resources**: Semantic views, search services, databases

## Adding New Tools

To add a new tool to an existing agent:

1. **Update the SQL file** with new tool specification
2. **Redeploy the agent** using the management script
3. **Test the new functionality**

Example tool addition:
```sql
{
  "tool_spec": {
    "type": "generic",
    "name": "Custom Analysis Tool",
    "description": "Performs custom business analysis",
    "input_schema": {
      "type": "object",
      "properties": {
        "analysis_type": {"type": "string"}
      }
    }
  }
}
```

## Integration with dbt

The dbt pipeline creates the **data foundation**:
- ✅ Semantic views (for Cortex Analyst)
- ✅ Cortex Search services (for document search)
- ✅ Parsed documents and data models

Agents **consume** these resources but are managed separately for operational flexibility.

## Current Agents

### ACME Intelligence Agent
- **Purpose**: Analyze technician performance and business metrics
- **Tools**: Cortex Analyst + Cortex Search
- **Data Sources**: 
  - Semantic View: `ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_analytics_view`
  - Financial View: `ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_financial_analytics_view`  
  - Search Service: `ACME_INTELLIGENCE.SEARCH.acme_document_search`
- **Deployment**: `SNOWFLAKE_INTELLIGENCE.AGENTS.acme_intelligence_agent`

## Future Agents

The configuration supports adding new agents for different business domains:
- **HR Intelligence Agent**: Employee performance and workforce analytics
- **Finance Intelligence Agent**: Financial performance and budgeting
- **Operations Intelligence Agent**: Operational efficiency and process optimization

Each agent can have its own tools, instructions, and data sources while sharing the same management infrastructure.
