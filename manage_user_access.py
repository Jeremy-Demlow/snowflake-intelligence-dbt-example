#!/usr/bin/env python3
"""
acme Intelligence Demo - User Access Management
This script helps manage user access to the acme Intelligence demo.
"""

import subprocess
import sys
from typing import List

def run_sql_command(sql: str, description: str) -> bool:
    """Execute a SQL command via SnowCLI"""
    print(f"\n🔄 {description}")
    
    # Escape quotes for shell execution
    escaped_sql = sql.replace('"', '\\"').replace("'", "\\'")
    cmd = f'snow sql -q "{escaped_sql}"'
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} - SUCCESS")
        return True
    else:
        print(f"❌ {description} - FAILED")
        print(f"Error: {result.stderr}")
        return False

def grant_demo_role(username: str) -> bool:
    """Grant the main demo role to a user (recommended approach)"""
    sql = f"GRANT ROLE acme_INTELLIGENCE_DEMO TO USER {username};"
    return run_sql_command(sql, f"Granting demo role to {username}")

def create_custom_role(username: str, access_level: str = "full") -> bool:
    """Create a custom role for the user"""
    role_name = f"{username}_acme_ACCESS"
    
    # Create role
    sql_create = f"""
    USE ROLE ACCOUNTADMIN;
    CREATE OR REPLACE ROLE {role_name} 
    COMMENT = 'Custom acme Intelligence access for {username}';
    """
    
    if not run_sql_command(sql_create, f"Creating custom role {role_name}"):
        return False
    
    # Grant basic permissions
    permissions = [
        f"GRANT USAGE ON WAREHOUSE HOL_WAREHOUSE TO ROLE {role_name};",
        f"GRANT USAGE ON DATABASE acme_INTELLIGENCE TO ROLE {role_name};",
        f"GRANT USAGE ON SCHEMA acme_INTELLIGENCE.MARTS TO ROLE {role_name};",
        f"GRANT USAGE ON SCHEMA acme_INTELLIGENCE.SEMANTIC_MODELS TO ROLE {role_name};",
        f"GRANT USAGE ON SCHEMA acme_INTELLIGENCE.AGENTS TO ROLE {role_name};",
        f"GRANT SELECT ON ALL TABLES IN SCHEMA acme_INTELLIGENCE.MARTS TO ROLE {role_name};",
        f"GRANT USAGE ON SEMANTIC VIEW acme_INTELLIGENCE.SEMANTIC_MODELS.acme_ANALYTICS_VIEW TO ROLE {role_name};",
        f"GRANT USAGE ON AGENT acme_INTELLIGENCE.AGENTS.acme_INTELLIGENCE_AGENT TO ROLE {role_name};"
    ]
    
    if access_level == "full":
        permissions.extend([
            f"GRANT USAGE ON SCHEMA acme_INTELLIGENCE.RAW TO ROLE {role_name};",
            f"GRANT USAGE ON SCHEMA acme_INTELLIGENCE.STAGING TO ROLE {role_name};",
            f"GRANT USAGE ON SCHEMA acme_INTELLIGENCE.SEARCH TO ROLE {role_name};",
            f"GRANT SELECT ON ALL TABLES IN SCHEMA acme_INTELLIGENCE.RAW TO ROLE {role_name};",
            f"GRANT SELECT ON ALL TABLES IN SCHEMA acme_INTELLIGENCE.STAGING TO ROLE {role_name};",
            f"GRANT USAGE ON CORTEX SEARCH SERVICE acme_INTELLIGENCE.SEARCH.acme_DOCUMENT_SEARCH TO ROLE {role_name};"
        ])
    
    # Apply permissions
    for perm in permissions:
        if not run_sql_command(perm, f"Granting permission: {perm.split()[1]}"):
            return False
    
    # Grant role to user
    sql_grant = f"GRANT ROLE {role_name} TO USER {username};"
    return run_sql_command(sql_grant, f"Granting {role_name} to {username}")

def revoke_access(username: str) -> bool:
    """Revoke access for a user"""
    commands = [
        f"REVOKE ROLE acme_INTELLIGENCE_DEMO FROM USER {username};",
        f"REVOKE ROLE {username}_acme_ACCESS FROM USER {username};"
    ]
    
    success = True
    for cmd in commands:
        if not run_sql_command(cmd, f"Revoking access: {cmd}"):
            success = False
    
    return success

def list_user_access(username: str) -> bool:
    """Show what access a user currently has"""
    sql = f"SHOW GRANTS TO USER {username};"
    return run_sql_command(sql, f"Showing grants for {username}")

def test_user_access(username: str) -> bool:
    """Test if user can access the semantic view"""
    sql = f"""
    USE ROLE acme_INTELLIGENCE_DEMO;
    SELECT * FROM SEMANTIC_VIEW(
        acme_INTELLIGENCE.SEMANTIC_MODELS.acme_analytics_view
        METRICS technician_count, total_revenue_sum
    );
    """
    return run_sql_command(sql, f"Testing {username} access to semantic view")

def main():
    """Main CLI interface"""
    if len(sys.argv) < 3:
        print("Usage: python manage_user_access.py <action> <username> [access_level]")
        print("\nActions:")
        print("  grant-demo     - Grant main demo role (recommended)")
        print("  create-custom  - Create custom role [full|readonly]")
        print("  revoke         - Revoke all access")
        print("  list           - List current access")
        print("  test           - Test access")
        print("\nExamples:")
        print("  python manage_user_access.py grant-demo JDEMLOW")
        print("  python manage_user_access.py create-custom JDEMLOW readonly")
        print("  python manage_user_access.py list JDEMLOW")
        sys.exit(1)
    
    action = sys.argv[1]
    username = sys.argv[2].upper()
    access_level = sys.argv[3] if len(sys.argv) > 3 else "full"
    
    print(f"🚀 acme Intelligence - User Access Management")
    print(f"Action: {action}")
    print(f"User: {username}")
    print("=" * 60)
    
    if action == "grant-demo":
        success = grant_demo_role(username)
    elif action == "create-custom":
        success = create_custom_role(username, access_level)
    elif action == "revoke":
        success = revoke_access(username)
    elif action == "list":
        success = list_user_access(username)
    elif action == "test":
        success = test_user_access(username)
    else:
        print(f"❌ Unknown action: {action}")
        sys.exit(1)
    
    if success:
        print(f"\n🎉 Action '{action}' completed successfully for user {username}!")
    else:
        print(f"\n❌ Action '{action}' failed for user {username}")
        sys.exit(1)

if __name__ == "__main__":
    main()
