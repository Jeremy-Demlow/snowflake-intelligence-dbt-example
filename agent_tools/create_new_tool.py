#!/usr/bin/env python3
"""
Tool Creator - Easily create new agent tools from template

Usage: python create_new_tool.py <tool_name> [--with-integration] [--with-deployment]
"""

import sys
import shutil
from pathlib import Path

def create_tool(tool_name: str, with_integration: bool = False, with_deployment: bool = False):
    """Create a new tool from template"""
    
    # Validate tool name
    if not tool_name.isidentifier():
        print(f"❌ Invalid tool name: {tool_name}")
        print("Tool name must be a valid Python identifier (letters, numbers, underscore)")
        return False
    
    tools_dir = Path("tools")
    template_path = tools_dir / "tool_template.py"
    new_tool_path = tools_dir / f"{tool_name}.py"
    
    if not template_path.exists():
        print(f"❌ Template not found: {template_path}")
        return False
    
    if new_tool_path.exists():
        print(f"❌ Tool already exists: {new_tool_path}")
        return False
    
    # Read template
    with open(template_path, 'r') as f:
        content = f.read()
    
    # Customize template
    class_name = ''.join(word.capitalize() for word in tool_name.split('_'))
    
    replacements = {
        'MyNewTool': class_name,
        'my_new_tool': tool_name,
        'my_new_function': f"{tool_name}_function",
        'my_integration': f"{tool_name}_integration",
        'Your new tool description here': f"{class_name} for Snowflake Intelligence",
        'TEMPLATE: New Agent Tool for Snowflake Intelligence': f"{class_name} for Snowflake Intelligence"
    }
    
    # Apply integration settings
    if with_integration:
        content = content.replace('REQUIRES_INTEGRATION = False', 'REQUIRES_INTEGRATION = True')
        content = content.replace('INTEGRATION_TYPE = None', 'INTEGRATION_TYPE = "EXTERNAL_ACCESS"')
    
    # Apply replacements
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Write new tool file
    with open(new_tool_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Created new tool: {new_tool_path}")
    print()
    print("📝 Next steps:")
    print(f"1. Edit {new_tool_path} to implement your tool logic")
    print(f"2. Test locally: python tool_manager.py test {tool_name}")
    if with_deployment:
        print(f"3. Deploy: python tool_manager.py deploy {tool_name}")
    if with_integration:
        print(f"3. Setup integration: python tool_manager.py setup {tool_name}")
    print(f"4. Check status: python tool_manager.py status")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_new_tool.py <tool_name> [--with-integration] [--with-deployment]")
        print()
        print("Examples:")
        print("  python create_new_tool.py web_scraper --with-integration")
        print("  python create_new_tool.py data_processor --with-deployment") 
        print("  python create_new_tool.py file_uploader --with-integration --with-deployment")
        sys.exit(1)
    
    tool_name = sys.argv[1]
    with_integration = '--with-integration' in sys.argv
    with_deployment = '--with-deployment' in sys.argv
    
    create_tool(tool_name, with_integration, with_deployment)
