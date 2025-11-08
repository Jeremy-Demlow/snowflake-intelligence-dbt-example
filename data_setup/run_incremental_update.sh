#!/bin/bash
# Quick script to run incremental data updates for ACME Intelligence
# This keeps your demo data fresh and up-to-date

echo "🔄 ACME Intelligence - Incremental Data Update"
echo "=============================================="
echo ""

# Activate conda environment
echo "📦 Activating service_titan conda environment..."
eval "$(conda shell.bash hook)"
conda activate service_titan

# Check if activation was successful
if [ $? -ne 0 ]; then
    echo "❌ Error: Could not activate service_titan conda environment"
    echo "Please run: conda env create -f environment.yml"
    exit 1
fi

echo "✅ Environment activated"
echo ""

# Run the incremental update script
echo "🚀 Running incremental data update..."
echo ""
cd "$(dirname "$0")"
python update_incremental_data.py

# Check if update was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Incremental update completed successfully!"
    echo ""
    echo "Next steps:"
    echo "  1. Run dbt models: cd ../acme_intelligence && dbt run"
    echo "  2. Test your agent with the latest data"
    echo "  3. Run this script again anytime to add more data"
else
    echo ""
    echo "❌ Update failed. Check the error messages above."
    exit 1
fi


