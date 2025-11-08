#!/bin/bash
# Deploy All ACME Intelligence Agents
# Regenerates agent SQL and deploys to Snowflake in one command

set -e  # Exit on error

echo "🤖 ACME Intelligence - Agent Deployment"
echo "=========================================="
echo ""

# Check if connection name is provided
CONNECTION="${1:-snowflake_intelligence}"
echo "📡 Using connection: $CONNECTION"
echo ""

# Step 1: Regenerate agent configurations
echo "📝 Step 1: Regenerating agent configurations..."
conda run -n service_titan python agent_generator.py
echo ""

# Step 2: Deploy each agent
echo "🚀 Step 2: Deploying agents to Snowflake..."
echo ""

AGENTS=(
    "acme_intelligence_agent"
    "acme_contracts_agent"
    "data_engineer_assistant"
)

SUCCESS_COUNT=0
FAIL_COUNT=0

for agent in "${AGENTS[@]}"; do
    echo "  Deploying: $agent..."
    if snow sql -c "$CONNECTION" -f "generated/${agent}.sql" > /dev/null 2>&1; then
        echo "  ✅ $agent deployed successfully"
        ((SUCCESS_COUNT++))
    else
        echo "  ❌ $agent deployment failed"
        ((FAIL_COUNT++))
    fi
done

echo ""
echo "=========================================="
echo "📊 Deployment Summary:"
echo "  ✅ Successful: $SUCCESS_COUNT"
if [ $FAIL_COUNT -gt 0 ]; then
    echo "  ❌ Failed: $FAIL_COUNT"
fi
echo "=========================================="
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo "🎉 All agents deployed successfully!"
    echo ""
    echo "🔍 Verify deployment:"
    echo "  snow sql -c $CONNECTION -q 'SHOW AGENTS IN SCHEMA SNOWFLAKE_INTELLIGENCE.AGENTS;'"
    echo ""
    echo "📝 Test an agent:"
    echo "  Use Snowflake UI or API to test ACME_INTELLIGENCE_AGENT"
else
    echo "⚠️  Some agents failed to deploy. Check the errors above."
    exit 1
fi

