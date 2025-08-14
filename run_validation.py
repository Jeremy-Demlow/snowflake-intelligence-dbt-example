#!/usr/bin/env python3
"""
Quick Validation Script - Test individual components
This script allows you to test specific parts of the pipeline
"""

import subprocess
import sys
from pathlib import Path

def run_snowcli_test():
    """Test SNOWCLI connection and basic queries"""
    print("🔍 Testing SNOWCLI connection...")
    
    # Test basic connection
    result = subprocess.run([
        "snow", "sql", "-q", 
        "SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE();"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ SNOWCLI connection successful")
        print(f"Output: {result.stdout[:200]}...")
        return True
    else:
        print("❌ SNOWCLI connection failed")
        print(f"Error: {result.stderr}")
        return False

def test_conda_env():
    """Test conda acme environment"""
    print("🔍 Testing conda acme environment...")
    
    # Test conda environment
    result = subprocess.run([
        "conda", "run", "-n", "acme", "python", "--version"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ conda acme environment working")
        print(f"Python version: {result.stdout.strip()}")
        return True
    else:
        print("❌ conda acme environment failed")
        print(f"Error: {result.stderr}")
        return False

def test_dbt_connection():
    """Test dbt connection in conda environment"""
    print("🔍 Testing dbt connection...")
    
    if not Path("acme_intelligence").exists():
        print("❌ acme_intelligence directory not found")
        return False
    
    # Test dbt debug
    result = subprocess.run([
        "conda", "run", "-n", "acme", "dbt", "debug"
    ], cwd="acme_intelligence", capture_output=True, text=True)
    
    if result.returncode == 0 and "All checks passed!" in result.stdout:
        print("✅ dbt connection successful")
        return True
    else:
        print("❌ dbt connection failed") 
        print(f"Output: {result.stdout[-300:]}")
        print(f"Error: {result.stderr}")
        return False

def test_database_access():
    """Test database and table access"""
    print("🔍 Testing database access...")
    
    # Test database access
    result = subprocess.run([
        "snow", "sql", "-q",
        "USE DATABASE acme_INTELLIGENCE; SELECT COUNT(*) FROM RAW.CUSTOMERS;"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Database access successful")
        return True
    else:
        print("❌ Database access failed")
        print(f"Error: {result.stderr}")
        return False

def main():
    """Run quick validation tests"""
    print("🚀 acme Intelligence - Quick Validation")
    print("=" * 50)
    
    tests = [
        ("SNOWCLI Connection", run_snowcli_test),
        ("conda acme Environment", test_conda_env), 
        ("dbt Connection", test_dbt_connection),
        ("Database Access", test_database_access)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for full deployment.")
        print("\nRun full validation with:")
        print("   python validate_end_to_end.py")
    else:
        print("⚠️  Some tests failed. Please fix issues before deploying.")
        
        if passed == 0:
            print("\n🛠️  Setup suggestions:")
            print("   1. Install Snowflake CLI: pip install snowflake-cli-labs")
            print("   2. Configure connection: snow connection add")
            print("   3. Create conda env: conda create -n acme python=3.9 dbt-snowflake")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
