# ACME Intelligence Semantic Models

This directory contains semantic views and related artifacts for enabling natural language queries through Snowflake Cortex Analyst.

## Files in this directory

- **`acme_semantic_view.sql`**: Main semantic view model that calls the macro
- **`create_semantic_view.sql`** (in macros/): Contains the actual semantic view SQL and utilities
- **`schema.yml`**: DBT schema documentation for semantic models
- **`README.md`**: This file

## Semantic View Overview

The `acme_analytics_view` provides a comprehensive business model for ACME Services analytics, enabling both SQL queries and natural language queries through Cortex Analyst.

### Business Entities

- **TECHNICIAN_PERFORMANCE**: Core technician profiles with performance metrics, ratings, and revenue data
- **JOBS**: Individual job records with service details (planned for future expansion)

### Key Metrics Available

- **Revenue Metrics**: Total revenue, 2025 revenue, average job revenue
- **Performance Metrics**: Average ratings, positive/negative reviews, technician counts
- **Operational Metrics**: Total jobs, completed jobs, underperforming technician counts

## Deployment Methods

### Method 1: Full dbt Run (Recommended - Simplified!)
```bash
# Deploy all models including semantic views automatically!
dbt deps
dbt run  # Handles all 15 models in correct dependency order
```

### Method 2: Individual Model Deployment  
```bash
# Deploy just the semantic view (after dependencies exist)
dbt run --select acme_semantic_view
```

### Method 3: Compile + Snowflake CLI
```bash
# Step 1: Compile to resolve dbt variables
dbt compile --select acme_semantic_view

# Step 2: Execute with Snowflake CLI
snow sql -f target/compiled/acme_intelligence/models/semantic/acme_semantic_view.sql
```

## Dependencies

**dbt handles dependencies automatically!** The semantic view depends on:
- `fct_technician_performance` (marts layer)
- `fct_jobs` (marts layer)

**No need for manual dependency management:**
```bash
# ❌ Old complex approach
dbt run --models staging
dbt run --models marts  
dbt run --models semantic

# ✅ New simplified approach  
dbt run  # Builds staging → marts → semantic automatically!
```

## Example Natural Language Queries

Once deployed, you can ask Cortex Analyst questions like:

**Technician Performance:**
- "Which technicians are underperforming?"
- "Show me top performers by specialization"
- "What's the average rating for HVAC technicians?"

**Revenue Analysis:**
- "What's our total revenue by company size?"
- "Which specializations generate the most revenue?"
- "Show me revenue trends for 2025"

**Operational Insights:**
- "How many technicians do we have by certification level?"
- "Which companies have the most underperforming technicians?"
- "What's our positive review rate by industry?"

## SQL Query Examples

### Basic Technician Count
```sql
SELECT * FROM SEMANTIC_VIEW(
    [DATABASE].SEMANTIC_MODELS.acme_analytics_view
    METRICS technician_count
);
```

### Revenue by Specialization
```sql
SELECT * FROM SEMANTIC_VIEW(
    [DATABASE].SEMANTIC_MODELS.acme_analytics_view
    DIMENSIONS specialization
    METRICS total_revenue_sum, technician_count
) ORDER BY total_revenue_sum DESC;
```

### Performance Analysis
```sql
SELECT * FROM SEMANTIC_VIEW(
    [DATABASE].SEMANTIC_MODELS.acme_analytics_view
    DIMENSIONS performance_category, specialization
    METRICS technician_count, avg_rating_avg
) ORDER BY technician_count DESC;
```

## Validation & Testing

### 1. Check Deployment
```sql
-- Verify the semantic view exists
SHOW SEMANTIC VIEWS IN SCHEMA [DATABASE].SEMANTIC_MODELS;

-- Get detailed structure
DESCRIBE SEMANTIC VIEW [DATABASE].SEMANTIC_MODELS.acme_analytics_view;
```

### 2. Basic Functionality Test
```sql
-- Simple metric test
SELECT * FROM SEMANTIC_VIEW(
    [DATABASE].SEMANTIC_MODELS.acme_analytics_view
    METRICS technician_count
);
```

### 3. Test with Cortex Analyst
- Open Snowsight
- Navigate to AI & ML > Cortex Analyst
- Select the semantic view
- Try the example questions listed above

## Troubleshooting

### Common Issues

1. **"Semantic view not found"**
   - Check deployment: `SHOW SEMANTIC VIEWS IN SCHEMA schema_name`
   - Verify permissions: Ensure CREATE SEMANTIC VIEW privileges

2. **"Column not found"**
   - Verify source tables exist: `DESCRIBE TABLE fct_technician_performance`
   - Check column names match exactly (case-sensitive)

3. **DBT compilation errors**
   - Verify variables are set: `dbt debug`
   - Check syntax in the macro file

### Best Practices

1. **Business-Friendly Names**: Use synonyms that match how users naturally speak about technicians and performance
2. **Rich Comments**: Provide context that helps Cortex Analyst understand business meaning
3. **Test Thoroughly**: Validate both SQL queries and natural language questions
4. **Version Control**: Track changes like any other DBT model

---

This semantic view enables powerful business intelligence queries for ACME Services data through natural language, making analytics accessible to non-technical users while maintaining the flexibility for advanced SQL queries.

