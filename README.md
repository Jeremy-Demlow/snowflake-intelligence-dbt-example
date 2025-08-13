# ACME Intelligence - Snowflake Demo

A comprehensive business intelligence demo using **ACME Services** as a fake customer, showcasing:

## 🎯 **What This Demonstrates**

- **Modern Data Stack**: dbt + Snowflake + Cortex AI
- **Intelligence Components**: Semantic views, search services, and AI agents  
- **Tool Integration**: SNOWCLI + conda environments
- **Complete Pipeline**: Raw data → Analytics → Intelligence
- **Simplified dbt Pipeline**: Single `dbt run` handles all dependencies automatically

## 🚀 **Quick Start**

### Prerequisites

1. **Snowflake Account** with ACCOUNTADMIN privileges
2. **Snowflake CLI**: 
   ```bash
   pip install snowflake-cli-labs
   ```
3. **conda environment**:
   ```bash
   conda create -n service_titan python=3.9 dbt-snowflake
   conda activate service_titan
   pip install dbt-snowflake
   ```
4. **Snowflake connection setup**:
   ```bash
   snow connection add
   ```
   Configure with your account details and ACCOUNTADMIN role.

### ⚡ One-Command Deployment
```bash
python deploy_acme_intelligence.py
```

### 🔧 Manual Step-by-Step (Optional)
If you prefer to understand each step:

```bash
# 1. Setup Infrastructure
snow sql -f sql_scripts/setup_complete_infrastructure.sql

# 2. Generate Sample Data  
cd data_setup && conda run -n service_titan python generate_acme_data.py && cd ..

# 3. Upload Documents
snow stage copy data_setup/acme_annual_report.txt @ACME_INTELLIGENCE.RAW.ACME_STG

# 4. Run dbt Pipeline (simplified!)
cd acme_intelligence
conda run -n service_titan dbt deps
conda run -n service_titan dbt run  # Handles all dependencies automatically!
cd ..

# 5. Deploy Intelligence Agent
snow sql -f snowflake_agents/acme_intelligence_agent_scalable.sql
```

### ✅ Validation & Testing
```bash
# Quick validation
snow sql -q "SELECT * FROM SEMANTIC_VIEW(ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_analytics_view METRICS technician_count, total_revenue_sum)"

# Test Cortex Search
snow sql -q "SHOW CORTEX SEARCH SERVICES IN SCHEMA ACME_INTELLIGENCE.SEARCH"

# Test Agent
snow sql -q "SHOW AGENTS IN SCHEMA SNOWFLAKE_INTELLIGENCE.AGENTS"
```

### User Access Management
```bash
# Grant full demo access
python manage_user_access.py grant-demo <USERNAME>

# Create custom role
python manage_user_access.py create-custom <USERNAME> readonly

# List user permissions
python manage_user_access.py list <USERNAME>
```

## 📊 **What Gets Built**

### Infrastructure
- **Database**: `ACME_INTELLIGENCE`
- **Schemas**: `RAW`, `STAGING`, `MARTS`, `SEMANTIC_MODELS`, `SEARCH` 
- **Role**: `ACME_INTELLIGENCE_DEMO` with proper permissions
- **Sample Data**: 50 customers, 25 technicians, 525+ jobs, 233+ reviews

### Data Pipeline (dbt) - **15 Models Total**
- **Raw Data**: Customers, technicians, jobs, reviews, documents (8 tables)
- **Staging**: Clean, typed data models (6 views) 
- **Marts**: Business logic and fact tables (4 tables)
- **Semantic**: Intelligence-ready analytics (2 semantic views + 1 summary)

### Intelligence Components
- **Semantic Views**: 
  - `acme_analytics_view` - Operational data for Cortex Analyst
  - `acme_financial_analytics_view` - Financial metrics (NDR, ARR)
- **Search Service**: `acme_document_search` for document retrieval
- **AI Agent**: `acme_intelligence_agent` (deployed in `SNOWFLAKE_INTELLIGENCE.AGENTS`)

## 🧪 **Sample Business Questions**

The deployed agent can answer:
- "Which technicians have ratings below 3 stars?"
- "What's our total revenue this year?" 
- "Show me revenue from underperforming technicians"
- "What does our annual report say about customer trust?"

## 🛠️ **Tools & Architecture**

- **SNOWCLI**: Infrastructure, SQL scripts, intelligence deployments
- **conda service_titan**: Data generation, dbt transformations
- **dbt**: Modern data transformations and modeling
- **Snowflake Cortex**: AI-powered analytics and search
- **Scalable Schema**: Organized for multiple use cases

## 📁 **Project Structure**

```
acme-intelligence-demo/
├── 🔧 Deployment & Validation
│   ├── deploy_acme_intelligence.py      # Complete deployment
│   ├── validate_end_to_end.py          # Full validation
│   ├── run_validation.py               # Quick tests
│   └── test_setup.sh                   # Prerequisites check
│
├── 📊 Data & Models  
│   ├── data_setup/
│   │   ├── generate_acme_data.py       # Sample data generation
│   │   └── acme_annual_report.txt      # Document for search
│   └── acme_intelligence/              # dbt project
│       ├── models/staging/             # Clean data views
│       ├── models/marts/               # Business logic
│       └── models/semantic/            # Intelligence layer
│
├── 💾 Infrastructure
│   └── sql_scripts/
│       ├── setup_complete_infrastructure.sql
│       ├── validate_dbt_solution.sql
│       └── grant_user_access.sql
│
├── 🧠 Intelligence
│   └── snowflake_agents/
│       ├── acme_intelligence_agent_scalable.sql
│       └── manage_agents.py
│
└── 👥 User Management
    └── manage_user_access.py           # Role management
```

## 🎯 **Business Value Demonstrated**

- **$195,768 total revenue** tracked across 25 technicians  
- **$82,132 revenue in 2025** specifically 
- **4.04 average** customer satisfaction rating
- **2 underperforming technicians** automatically identified (< 3 star rating)
- **Natural language** business intelligence queries via AI agent
- **Document search** integration with structured data via Cortex Search
- **Financial analytics** including NDR (Net Dollar Retention) calculations

## 🔍 **Key Innovation: Simplified dbt Pipeline**

This project demonstrates that **complex staged dbt deployments are unnecessary** when dependencies are properly configured:

❌ **Old Complex Approach:**
```bash
dbt run --models staging
dbt run --models marts  
dbt run --models semantic
```

✅ **New Simple Approach:**  
```bash
dbt deps
dbt run  # Handles all 15 models in correct order automatically!
```

**Why it works:** dbt automatically resolves dependencies using `ref()` functions, building models in the correct order: `staging → marts → semantic`.

## 🛠️ **Troubleshooting**

### Common Issues

1. **"Object does not exist" errors**: Ensure your Snowflake connection has ACCOUNTADMIN privileges
2. **dbt connection issues**: Check `~/.dbt/profiles.yml` has correct account/warehouse settings
3. **conda environment**: Make sure you're using the `service_titan` environment for dbt commands
4. **Agent deployment fails**: Agent is deployed to `SNOWFLAKE_INTELLIGENCE.AGENTS` (requires admin privileges)

### Prerequisites Check
```bash
# Verify Snowflake CLI
snow connection list

# Verify conda environment
conda env list | grep service_titan

# Test Snowflake connection
snow sql -q "SELECT CURRENT_USER(), CURRENT_ROLE()"
```

## 📋 **Next Steps**

After deployment:
1. **Test semantic views** with Cortex Analyst queries
2. **Chat with the agent** using natural language business questions
3. **Explore document search** functionality with company reports  
4. **Scale** by adding more data sources and business domains

## 🧪 **Sample Business Questions for the Agent**

Once deployed, try asking the agent:
- *"Which technicians have ratings below 3 stars?"*
- *"What's our total revenue this year?"*
- *"Show me revenue from underperforming technicians"*  
- *"What is our latest NDR across all customers?"*
- *"Which customer segments have the highest ARR expansion?"*

---

🏢 **ACME Services** - *Your Trusted Fake Company for Demonstrations*
