#!/bin/bash

# acme Intelligence - Quick Setup Test
# Tests that all required tools and environments are properly configured

echo "🚀 acme Intelligence - Setup Test"
echo "=========================================="

# Test 1: Check if we're in the right directory
echo ""
echo "📋 Test 1: Project Directory"
if [ -d "acme_intelligence" ] && [ -d "sql_scripts" ] && [ -d "data_setup" ]; then
    echo "✅ Project structure found"
else
    echo "❌ Error: Run this script from the project root directory"
    exit 1
fi

# Test 2: Check Snowflake CLI
echo ""
echo "📋 Test 2: Snowflake CLI"
if command -v snow &> /dev/null; then
    echo "✅ Snowflake CLI found"
    snow --version | head -1
else
    echo "❌ Snowflake CLI not found"
    echo "   Install with: pip install snowflake-cli-labs"
    echo "   Configure with: snow connection add"
fi

# Test 3: Check conda
echo ""
echo "📋 Test 3: conda Environment"
if command -v conda &> /dev/null; then
    echo "✅ conda found"
    
    # Check if acme environment exists
    if conda env list | grep -q "acme"; then
        echo "✅ acme environment exists"
        
        # Test the environment
        if conda run -n acme python --version &> /dev/null; then
            echo "✅ acme environment working"
            conda run -n acme python --version
        else
            echo "❌ acme environment not working"
        fi
    else
        echo "❌ acme environment not found"
        echo "   Create with: conda create -n acme python=3.9 dbt-snowflake"
    fi
else
    echo "❌ conda not found"
    echo "   Install Miniconda or Anaconda first"
fi

# Test 4: Check dbt in conda environment  
echo ""
echo "📋 Test 4: dbt Installation"
if conda run -n acme dbt --version &> /dev/null; then
    echo "✅ dbt found in acme environment"
    conda run -n acme dbt --version | head -1
else
    echo "❌ dbt not found in acme environment"
    echo "   Install with: conda activate acme && pip install dbt-snowflake"
fi

# Test 5: Check Python scripts exist
echo ""
echo "📋 Test 5: Validation Scripts"
scripts=("validate_end_to_end.py" "run_validation.py" "deploy_acme_intelligence.py")
for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        echo "✅ Found: $script"
    else
        echo "❌ Missing: $script"
    fi
done

# Test 6: Check SQL scripts
echo ""
echo "📋 Test 6: SQL Scripts"
sql_scripts=("sql_scripts/setup_complete_infrastructure.sql" "sql_scripts/validate_dbt_solution.sql")
for script in "${sql_scripts[@]}"; do
    if [ -f "$script" ]; then
        echo "✅ Found: $script"
    else
        echo "❌ Missing: $script"
    fi
done

echo ""
echo "=========================================="
echo "🎯 Setup Test Complete!"
echo ""
echo "Next steps:"
echo "1. Quick validation:    python run_validation.py"
echo "2. Full validation:     python validate_end_to_end.py"  
echo "3. Complete deployment: python deploy_acme_intelligence.py"
echo ""
echo "For detailed instructions, see: README_VALIDATION.md"
