# ACME Intelligence - Snowflake Demo

A comprehensive business intelligence demo showcasing **modern data stack architecture** with **Snowflake Intelligence Agents** and **custom tool integration**.

## 🎯 **What This Demonstrates**

- **Modern Data Stack**: dbt + Snowflake + Cortex AI + Intelligence Agents
- **Tool Integration**: Custom email and web scraping tools via Snowpark
- **YAML-Driven Architecture**: Scalable agent configuration system
- **Complete Pipeline**: Raw data → Analytics → Intelligence → Action

## 🏗️ **Architecture Overview**

```
📊 ACME Intelligence Demo
├── 🛠️  agent_tools/          # Reusable Tool Library
│   ├── src/email_tools/       # Email sender (Snowpark procedure)
│   ├── src/web_tools/         # Web scraper w/ Claude-3.5-Sonnet AI
│   ├── snowflake.yml          # Snowpark deployment config
│   └── tests/                 # Local testing framework
│
├── 🤖 snowflake_agents/       # Agent Management System  
│   ├── agent_configs/*.yml    # YAML agent definitions
│   ├── agent_generator.py     # YAML → SQL converter
│   ├── manage_agents.py       # SQL → Snowflake deployer
│   └── generated/*.sql        # Auto-generated agent SQL
│
├── 📊 acme_intelligence/      # dbt Data Pipeline
│   ├── models/staging/        # Clean data transformations
│   ├── models/marts/          # Business logic layer
│   └── models/semantic/       # Intelligence-ready analytics
│
└── 🚀 Root Level              # Deployment & Management
    ├── deploy_acme_intelligence.py  # One-command deployment
    ├── manage_user_access.py        # Role & permission management
    └── validate_end_to_end.py       # Complete validation suite
```

## 🚀 **Quick Start**

### Prerequisites

1. **Snowflake Account** with ACCOUNTADMIN privileges
2. **Snowflake CLI v3.7+**: 
   ```bash
   pip install snowflake-cli-labs
   snow connection add  # Configure with ACCOUNTADMIN
   ```
3. **conda environment**:
   ```bash
   conda create -n acme python=3.9 
   conda activate acme
   pip install dbt-snowflake
   ```

### ⚡ One-Command Demo Deployment
```bash
python deploy_acme_intelligence.py
```

This single command:
- ✅ Sets up all Snowflake infrastructure  
- ✅ Generates and loads sample data (50+ customers, 525+ jobs)
- ✅ Runs complete dbt transformation pipeline
- ✅ Deploys semantic views and Cortex Search
- ✅ Creates intelligence agent with custom tools
- ✅ Validates entire deployment

## 🛠️ **Custom Tool Development**

### Deploy Enhanced Tools
```bash
# Deploy email sender & web scraper to Snowflake
cd agent_tools
snow snowpark deploy

# Tools deploy to: AGENT_TOOLS_CENTRAL.AGENT_TOOLS.*
# - SEND_MAIL(recipient, subject, html_content)  
# - WEB_SCRAPE(url) -> AI-powered competitive analysis
```

### Local Tool Testing
```bash
cd agent_tools
python test_local_scraper.py  # Test web scraper with real data
python -m pytest tests/       # Run full test suite
```

### Web Scraper Features
- **Claude-3.5-Sonnet AI**: 10k token limit for deep analysis
- **Real Competitor Detection**: Industry-specific competitor databases
- **Rich HTML Reports**: Formatted output for agent consumption
- **External Access**: Configured for secure web access

## 🤖 **Scalable Agent Management**

### YAML-Based Agent Configuration
```yaml
# snowflake_agents/agent_configs/acme_intelligence_agent.yml
agent_name: "ACME_INTELLIGENCE_AGENT"
profile:
  display_name: "ACME Intelligence Agent"

tools:
  - name: "Send_Email"
    type: "generic" 
    resource:
      identifier: "AGENT_TOOLS_CENTRAL.AGENT_TOOLS.SEND_MAIL"
  - name: "Web_scrape"  
    type: "generic"
    resource:
      identifier: "AGENT_TOOLS_CENTRAL.AGENT_TOOLS.WEB_SCRAPE"
```

### Deploy Agents
```bash
cd snowflake_agents

# Step 1: Generate SQL from YAML (single responsibility)
python agent_generator.py --agent acme_intelligence_agent

# Step 2: Deploy SQL to Snowflake (single responsibility)  
python manage_agents.py deploy acme_intelligence_agent

# Environment-specific deployment
python agent_generator.py --agent acme_intelligence_agent --environment dev
python manage_agents.py deploy acme_intelligence_agent_dev
```

## 📊 **What Gets Built**

### Infrastructure
- **Databases**: `ACME_INTELLIGENCE`, `AGENT_TOOLS_CENTRAL`, `SNOWFLAKE_INTELLIGENCE`
- **Sample Data**: 50 customers, 25 technicians, 525+ jobs, 233+ reviews
- **Business Metrics**: $195,768 total revenue, 4.04 avg satisfaction

### Intelligence Components
- **Semantic Views**: Operational & financial analytics for Cortex Analyst
- **Cortex Search**: `acme_document_search` for document retrieval  
- **AI Agent**: Full business analyst with custom tools
- **Custom Tools**: Email sender + AI-powered web scraper

### Data Pipeline (dbt) - 15 Models
- **Staging (8)**: Clean, typed source data
- **Marts (4)**: Business logic and fact tables  
- **Semantic (3)**: Intelligence-ready analytics with NDR calculations

## 🧪 **Sample Business Questions**

Ask the deployed agent:
- *"Which technicians have ratings below 3 stars?"*
- *"What's our total revenue this year?"*
- *"Send a performance report to jeremy.demlow@snowflake.com"*
- *"Analyze our competitor amce's website"*  
- *"What does our annual report say about customer trust?"*
- *"Which customer segments have the highest NDR?"*

## 👥 **User Access Management**

```bash
# Grant complete demo access
python manage_user_access.py grant-demo <USERNAME>

# Create custom role with specific permissions
python manage_user_access.py create-custom <USERNAME> readonly

# List all user permissions  
python manage_user_access.py list <USERNAME>
```

## ✅ **Validation & Testing**

```bash
# Quick infrastructure validation
snow sql -q "SELECT * FROM SEMANTIC_VIEW(ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_analytics_view METRICS technician_count)"

# Test custom tools
snow sql -q "CALL AGENT_TOOLS_CENTRAL.AGENT_TOOLS.SEND_MAIL('test@example.com', 'Test', 'Hello!')"  
snow sql -q "CALL AGENT_TOOLS_CENTRAL.AGENT_TOOLS.WEB_SCRAPE('https://amce.com')"

# Complete validation suite
python validate_end_to_end.py
python run_validation.py  # Quick validation tests
```

## 🛠️ **Development Philosophy**

### Unix Philosophy: Do One Thing Well
- **`agent_tools/`**: Tool development and deployment (one responsibility)
- **`snowflake_agents/`**: Agent configuration and management (one responsibility)  
- **`agent_generator.py`**: YAML → SQL conversion (one job)
- **`manage_agents.py`**: SQL → Snowflake deployment (one job)

### Clean Architecture Principles
- ✅ **No string escaping hell**: Python → SQL, not manual JSON
- ✅ **Modular design**: Each component is independently testable
- ✅ **Clear separation**: Tools ≠ Agents ≠ Data Pipeline  
- ✅ **Easy debugging**: Know exactly where issues occur
- ✅ **Scalable**: Add tools and agents without complexity

## 🎯 **Business Value Demonstrated**

- **$195,768 total revenue** tracked with real-time analytics
- **2 underperforming technicians** automatically identified  
- **Natural language** business intelligence via AI agent
- **Automated workflows**: Email reports, competitive analysis
- **Document integration**: Semantic search with structured data
- **Financial analytics**: NDR, ARR expansion, customer segmentation

## 📋 **Troubleshooting**

### Common Issues
1. **"Object does not exist"**: Ensure ACCOUNTADMIN privileges
2. **dbt failures**: Check `conda activate acme` and connection settings
3. **Tool deployment fails**: Verify Snowflake CLI connection with `snow connection list`
4. **Agent access issues**: Tools deploy to `AGENT_TOOLS_CENTRAL.AGENT_TOOLS.*`

### Prerequisites Check
```bash  
snow connection list                    # Verify CLI setup
conda env list | grep acme             # Check conda environment
snow sql -q "SELECT CURRENT_ROLE()"    # Verify privileges
```

## 🔧 **Advanced Configuration**

### Environment-Specific Deployments
```yaml
# snowflake_agents/agent_configs/environments/dev.yml
agent:
  database: "DEV_ACME_INTELLIGENCE"
default_execution_environment:  
  warehouse: "DEV_WAREHOUSE"
```

### Adding New Tools
1. Create tool in `agent_tools/src/your_tool/`
2. Add to `agent_tools/snowflake.yml` 
3. Deploy: `cd agent_tools && snow snowpark deploy`
4. Reference in agent YAML: `AGENT_TOOLS_CENTRAL.AGENT_TOOLS.YOUR_TOOL`

### Adding New Agents
1. Create `snowflake_agents/agent_configs/your_agent.yml`
2. Generate: `python agent_generator.py --agent your_agent`  
3. Deploy: `python manage_agents.py deploy your_agent`

---

🏢 **ACME Services** - *Your Trusted Partner for Snowflake Intelligence Demonstrations*

*This demo showcases production-ready patterns for Snowflake Intelligence with custom tool integration*