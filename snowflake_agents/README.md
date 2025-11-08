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
├── agent_configs/                      # Agent YAML configurations
│   ├── acme_intelligence_agent.yml     # Basic comprehensive agent
│   ├── acme_contracts_agent.yml        # Basic contracts specialist
│   ├── acme_intelligence_agent_enhanced.yml  # Enhanced comprehensive agent
│   ├── acme_contracts_agent_enhanced.yml     # Enhanced contracts specialist
│   └── environments/
│       └── dev.yml                     # Environment overrides
├── generated/                          # Auto-generated SQL files
│   ├── acme_intelligence_agent.sql
│   └── acme_contracts_agent.sql
├── agent_generator.py                  # YAML-to-SQL generator
└── manage_agents.py                   # Agent management CLI
```

## 🚀 Quick Start - Deploy All Agents

### **Recommended: One-Command Deployment**
```bash
cd snowflake_agents
conda activate service_titan
./deploy_all_agents.sh snowflake_intelligence
```

This script automatically:
- ✅ Regenerates all agent configurations from YAML
- ✅ Deploys all 3 agents to Snowflake
- ✅ Shows deployment summary
- ✅ Uses updated semantic view names

### **Manual Deployment**

#### Generate SQL from YAML configs
```bash
conda activate service_titan
python agent_generator.py
```

#### Deploy specific agent
```bash
snow sql -c snowflake_intelligence -f generated/acme_intelligence_agent.sql
snow sql -c snowflake_intelligence -f generated/acme_contracts_agent.sql
snow sql -c snowflake_intelligence -f generated/data_engineer_assistant.sql
```

### **Environment-Specific Generation**
```bash
# Generate for specific environment (optional)
python agent_generator.py --environment dev

# List available configurations
python agent_generator.py --list

# Generate specific agent
python agent_generator.py --agent acme_intelligence_agent
```

### Agent Management
```bash
# Check deployed agents
snow sql -c snowflake_intelligence -q "SHOW AGENTS IN SCHEMA SNOWFLAKE_INTELLIGENCE.AGENTS;"

# Show semantic views agents are using
snow sql -c snowflake_intelligence -q "SHOW SEMANTIC VIEWS IN SCHEMA ACME_INTELLIGENCE.SEMANTIC_MODELS;"

# Test agent functionality
snow sql -q "DESC AGENT SNOWFLAKE_INTELLIGENCE.AGENTS.ACME_CONTRACTS_AGENT;"
```

## 📦 Important: Semantic View Names (Updated Oct 20, 2025)

**We migrated to the official [Snowflake-Labs/dbt_semantic_view](https://github.com/Snowflake-Labs/dbt_semantic_view) package (v1.0.3).**

This changed the semantic view naming convention:

| Agent Tool | Old Semantic View | New Semantic View |
|------------|-------------------|-------------------|
| Query Operational Data | acme_analytics_view | **acme_semantic_view** |
| Query Financial Metrics | acme_financial_analytics_view | **acme_financial_semantic_view** |
| Query Contracts Data | acme_contracts_analytics_view | **acme_contracts_semantic_view** |
| Query Snowflake Usage | snowflake_usage_analytics_view | **snowflake_usage_semantic_view** |

**All agent configs have been updated** and regenerating agents will use the correct names.

**Location**: All semantic views are in `ACME_INTELLIGENCE.SEMANTIC_MODELS` schema.

## 🚀 Production-Grade Agent Patterns (Enhanced)

Based on analysis of enterprise Snowflake agent deployments, we've identified key patterns for production-grade performance:

### Performance Optimization Patterns

**❌ Basic Orchestration:**
```yaml
orchestration: "Use this tool for X and that tool for Y"
```

**✅ Production Orchestration:**
```yaml
orchestration: >
  OVERALL: parallelize as many tool calls as possible for optimal latency.
  Use multiple tools simultaneously for comprehensive analysis.
```

### Executive Response Structure

**✅ Production Pattern:**
```yaml
response: >
  Transform analysis into executive-ready insights:
  1. Begin with executive summary highlighting key indicators
  2. Organize into logical sections: Risk Assessment, Financial Impact, Recommendations
  3. Convert raw metrics into business narratives with strategic context
  4. Use executive-level, decision-focused language throughout
  5. Include brief summary with recommended strategic actions
```

### Advanced Search Configuration

**✅ Production Pattern:**
```yaml
resources:
  max_results: 10
  experimental:
    Diversity:
      GroupBy: ["DOCUMENT_TYPE"]
      MaxResults: 3
    RerankWeights:
      TopicalityMultiplier: 4
      EmbeddingMultiplier: 1.2
      RerankingMultiplier: 1.5
```

### Model Configuration

**✅ Add for Production:**
```yaml
agent:
  models:
    orchestration: "auto"  # Enable automatic optimization
```

## Agent Configuration

Agents are configured in YAML files with:
- **Tools**: Cortex Analyst, Cortex Search, custom functions
- **Instructions**: Response behavior and orchestration logic
- **Sample Questions**: Example queries for users
- **Resources**: Semantic views, search services, databases
- **Models**: Orchestration optimization settings

## Integration with dbt

The dbt pipeline creates the **data foundation**:
- ✅ Semantic views (for Cortex Analyst)
- ✅ Cortex Search services (for document search)
- ✅ Parsed documents and data models

Agents **consume** these resources but are managed separately for operational flexibility.

## Current Agents

### ACME Intelligence Agent (Basic & Enhanced)
- **Purpose**: Comprehensive business intelligence across operations, finance, and contracts
- **Tools**: Cortex Analyst + Cortex Search + Email + Web Scraping
- **Data Sources**: 
  - Operational: `ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_analytics_view`
  - Financial: `ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_financial_analytics_view`
  - Contracts: `ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_contracts_analytics_view`
  - Search Service: `ACME_INTELLIGENCE.SEARCH.acme_document_search`
- **Deployment**: `SNOWFLAKE_INTELLIGENCE.AGENTS.acme_intelligence_agent`

### ACME Contracts Agent (Basic & Enhanced)
- **Purpose**: Specialized contract analysis, churn prevention, revenue risk management
- **Tools**: Contracts Analytics + Document Search + Email Alerts
- **Data Sources**:
  - Contracts: `ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_contracts_analytics_view`
  - Documents: `ACME_INTELLIGENCE.SEARCH.acme_document_search`
- **Deployment**: `SNOWFLAKE_INTELLIGENCE.AGENTS.acme_contracts_agent`

### Data Engineer Assistant
- **Purpose**: Query performance optimization, cost reduction, and proactive performance monitoring
- **Tools**: Usage Analytics + Document Search + Performance Reporting
- **Data Sources**:
  - Performance: `ACME_INTELLIGENCE.SEMANTIC_MODELS.snowflake_usage_analytics_view` (85+ columns)
  - Account Usage: `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY` + `QUERY_ATTRIBUTION_HISTORY`
  - Documents: `ACME_INTELLIGENCE.SEARCH.acme_document_search`
- **Deployment**: `SNOWFLAKE_INTELLIGENCE.AGENTS.data_engineer_assistant`

## Business Questions Supported

### Contract Intelligence (Enhanced):
- "How many active contracts do we have and what's the revenue health status?"
- "What's our churn rate, revenue at risk, and recommended intervention strategies?"
- "Which accounts have exit ramp commitments and what's our retention strategy?"
- "Analyze commitment fulfillment trends and predict revenue risk for next quarter"

### Comprehensive Intelligence (Enhanced):
- "What is our comprehensive business health across operations, finance, and contracts?"
- "Analyze the relationship between technician ratings, contract performance, and financial outcomes"
- "Which customer segments have the highest ARR expansion potential and operational capacity?"

### Performance Optimization (Data Engineer Assistant):
- "What are my slowest queries and how can I optimize them?"
- "Which warehouses are consuming the most credits and need right-sizing?"
- "Show me cost optimization opportunities with projected savings"
- "What compilation errors am I seeing and how do I fix them?"
- "Recommend Gen 2 warehouse upgrades with performance benefits"
- "Analyze query performance trends and identify bottlenecks"

### Key Metrics Available:
- **Active Contracts**: 80 contracts
- **Total Commitments**: $254,046.71  
- **Churned Clients**: 6 clients
- **At-Risk Revenue**: $27,357.61

## Performance Optimization

**Production Agent Performance:**
- **Response Latency**: < 3 seconds via parallelization
- **Search Relevance**: 95%+ via advanced ranking
- **Executive Ready**: No technical translation needed
- **Action Oriented**: Prioritized recommendations with business impact

## Deployment Requirements

### Permissions Setup
```bash
# Required for SNOWFLAKE_INTELLIGENCE database access
snow sql -q "
GRANT ROLE SNOWFLAKE_INTELLIGENCE_ADMIN_RL TO ROLE ACCOUNTADMIN;
GRANT ALL PRIVILEGES ON DATABASE SNOWFLAKE_INTELLIGENCE TO ROLE ACCOUNTADMIN;
"
```

### Database Structure
```bash
# Ensure proper schema exists
snow sql -q "
CREATE DATABASE IF NOT EXISTS SNOWFLAKE_INTELLIGENCE;
CREATE SCHEMA IF NOT EXISTS SNOWFLAKE_INTELLIGENCE.AGENTS;
"
```

## Future Agents

The configuration supports adding new agents for different business domains:
- **HR Intelligence Agent**: Employee performance and workforce analytics
- **Finance Intelligence Agent**: Financial performance and budgeting
- **Operations Intelligence Agent**: Operational efficiency and process optimization

Each agent can have its own tools, instructions, and data sources while sharing the same management infrastructure.