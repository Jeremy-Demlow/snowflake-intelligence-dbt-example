#!/usr/bin/env python3
"""
Scalable Tool Manager for Snowflake Intelligence Agent Tools

This makes it easy to:
1. Add new tools following the same pattern
2. Automatically discover and manage tools
3. Set up integrations via Python (not just manual SQL)
4. Scale to many tools without touching existing code
"""

import importlib
import pkgutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging
from snowflake_connection import SnowflakeConnection

logger = logging.getLogger(__name__)

@dataclass
class ToolInfo:
    """Information about an agent tool"""
    name: str
    module_name: str
    description: str
    has_local_test: bool = False
    has_deployment: bool = False
    has_integration_setup: bool = False
    requires_integration: bool = False
    integration_type: Optional[str] = None

class ToolManager:
    """Manages discovery, deployment, and testing of agent tools"""
    
    def __init__(self, connection_name: str = 'snowflake_intelligence'):
        self.connection_name = connection_name
        self.tools: Dict[str, ToolInfo] = {}
        self._discover_tools()
    
    def _discover_tools(self):
        """Automatically discover all tools in the tools/ directory"""
        tools_dir = Path(__file__).parent / "tools"
        if not tools_dir.exists():
            return
            
        # Import all modules in tools/ directory
        for finder, name, ispkg in pkgutil.iter_modules([str(tools_dir)]):
            if name.startswith('__'):
                continue
                
            try:
                module = importlib.import_module(f"tools.{name}")
                tool_info = self._analyze_tool_module(name, module)
                if tool_info:
                    self.tools[name] = tool_info
                    logger.debug(f"Discovered tool: {name}")
            except Exception as e:
                logger.warning(f"Failed to import tool {name}: {e}")
    
    def _analyze_tool_module(self, name: str, module) -> Optional[ToolInfo]:
        """Analyze a tool module to determine its capabilities"""
        tool_info = ToolInfo(
            name=name,
            module_name=f"tools.{name}",
            description=getattr(module, '__doc__', f"{name} tool").strip().split('\n')[0]
        )
        
        # Check for standard functions
        if hasattr(module, 'deploy_to_snowflake'):
            tool_info.has_deployment = True
        
        if hasattr(module, 'setup_integration'):
            tool_info.has_integration_setup = True
            
        # Check if it requires integration (email, external access, etc.)
        if hasattr(module, 'REQUIRES_INTEGRATION'):
            tool_info.requires_integration = module.REQUIRES_INTEGRATION
            tool_info.integration_type = getattr(module, 'INTEGRATION_TYPE', None)
        
        # Check for test functions
        for attr_name in dir(module):
            if attr_name.endswith('_local') or 'test' in attr_name.lower():
                tool_info.has_local_test = True
                break
                
        return tool_info
    
    def list_tools(self) -> List[ToolInfo]:
        """List all discovered tools"""
        return list(self.tools.values())
    
    def get_tool(self, name: str) -> Optional[ToolInfo]:
        """Get information about a specific tool"""
        return self.tools.get(name)
    
    def test_tool_local(self, tool_name: str, **kwargs) -> bool:
        """Test a tool locally"""
        tool_info = self.get_tool(tool_name)
        if not tool_info:
            print(f"❌ Tool '{tool_name}' not found")
            return False
            
        try:
            module = importlib.import_module(tool_info.module_name)
            
            # Look for test functions
            if hasattr(module, 'test_local'):
                result = module.test_local(**kwargs)
                return result
            elif tool_name == 'email_sender':
                # Email tool specific test
                from tools.email_sender import EmailSender
                sender = EmailSender()
                result = sender.send_email_local("test@example.com", "Test", "Body")
                print(f"✅ Local test: {result.success} - {result.message}")
                return result.success
            else:
                print(f"⚠️  No local test available for {tool_name}")
                return True
                
        except Exception as e:
            print(f"❌ Local test failed for {tool_name}: {e}")
            return False
    
    def deploy_tool(self, tool_name: str) -> bool:
        """Deploy a tool to Snowflake"""
        tool_info = self.get_tool(tool_name)
        if not tool_info:
            print(f"❌ Tool '{tool_name}' not found")
            return False
            
        if not tool_info.has_deployment:
            print(f"❌ Tool '{tool_name}' doesn't have deployment capability")
            return False
            
        try:
            conn = SnowflakeConnection.from_snow_cli(self.connection_name)
            module = importlib.import_module(tool_info.module_name)
            
            success = module.deploy_to_snowflake(conn.session)
            if success:
                print(f"✅ {tool_name} deployed to Snowflake")
            else:
                print(f"❌ {tool_name} deployment failed")
            return success
            
        except Exception as e:
            print(f"❌ Deployment failed for {tool_name}: {e}")
            return False
    
    def setup_integration(self, tool_name: str, **kwargs) -> bool:
        """Set up required integration for a tool"""
        tool_info = self.get_tool(tool_name)
        if not tool_info:
            print(f"❌ Tool '{tool_name}' not found")
            return False
            
        if not tool_info.requires_integration:
            print(f"✅ {tool_name} doesn't require integration setup")
            return True
            
        try:
            conn = SnowflakeConnection.from_snow_cli(self.connection_name)
            module = importlib.import_module(tool_info.module_name)
            
            if hasattr(module, 'setup_integration'):
                success = module.setup_integration(conn.session, **kwargs)
                if success:
                    print(f"✅ Integration set up for {tool_name}")
                else:
                    print(f"❌ Integration setup failed for {tool_name}")
                return success
            else:
                # Fallback to manual SQL display
                if hasattr(module, 'get_required_permissions'):
                    print(f"Run this SQL as ACCOUNTADMIN for {tool_name}:")
                    print("=" * 50)
                    print(module.get_required_permissions())
                    print("=" * 50)
                return True
                
        except Exception as e:
            print(f"❌ Integration setup failed for {tool_name}: {e}")
            return False
    
    def deploy_all_tools(self) -> Dict[str, bool]:
        """Deploy all tools that have deployment capability"""
        results = {}
        for tool_name, tool_info in self.tools.items():
            if tool_info.has_deployment:
                print(f"🚀 Deploying {tool_name}...")
                results[tool_name] = self.deploy_tool(tool_name)
            else:
                print(f"⏭️  Skipping {tool_name} (no deployment)")
                results[tool_name] = None
        return results
    
    def setup_all_integrations(self, **kwargs) -> Dict[str, bool]:
        """Set up integrations for all tools that require them"""
        results = {}
        for tool_name, tool_info in self.tools.items():
            if tool_info.requires_integration:
                print(f"🔧 Setting up integration for {tool_name}...")
                results[tool_name] = self.setup_integration(tool_name, **kwargs)
            else:
                results[tool_name] = True  # No integration needed
        return results
    
    def status_report(self):
        """Generate a status report of all tools"""
        print("\n🔧 AGENT TOOLS STATUS REPORT")
        print("=" * 50)
        
        if not self.tools:
            print("❌ No tools discovered")
            return
            
        for name, info in self.tools.items():
            print(f"\n📧 {name.upper()}")
            print(f"   Description: {info.description}")
            print(f"   Local Testing: {'✅' if info.has_local_test else '❌'}")
            print(f"   Deployment: {'✅' if info.has_deployment else '❌'}")
            print(f"   Requires Integration: {'✅' if info.requires_integration else '❌'}")
            if info.integration_type:
                print(f"   Integration Type: {info.integration_type}")

def create_tool_manager(connection_name: str = 'snowflake_intelligence') -> ToolManager:
    """Create a tool manager instance"""
    return ToolManager(connection_name)

# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python tool_manager.py list                    # List all tools")
        print("  python tool_manager.py test <tool>             # Test tool locally") 
        print("  python tool_manager.py deploy <tool>           # Deploy specific tool")
        print("  python tool_manager.py deploy-all              # Deploy all tools")
        print("  python tool_manager.py setup <tool>            # Setup tool integration")
        print("  python tool_manager.py setup-all               # Setup all integrations")
        print("  python tool_manager.py status                  # Status report")
        sys.exit(1)
    
    manager = create_tool_manager()
    command = sys.argv[1]
    
    if command == "list":
        tools = manager.list_tools()
        print(f"\n📦 Discovered {len(tools)} tools:")
        for tool in tools:
            print(f"  • {tool.name}: {tool.description}")
    
    elif command == "test" and len(sys.argv) > 2:
        tool_name = sys.argv[2]
        manager.test_tool_local(tool_name)
    
    elif command == "deploy" and len(sys.argv) > 2:
        tool_name = sys.argv[2]
        manager.deploy_tool(tool_name)
    
    elif command == "deploy-all":
        results = manager.deploy_all_tools()
        successful = sum(1 for r in results.values() if r is True)
        print(f"\n✅ Deployed {successful}/{len([r for r in results.values() if r is not None])} tools")
    
    elif command == "setup" and len(sys.argv) > 2:
        tool_name = sys.argv[2]
        manager.setup_integration(tool_name)
    
    elif command == "setup-all":
        results = manager.setup_all_integrations()
        successful = sum(1 for r in results.values() if r is True)
        print(f"\n✅ Set up {successful}/{len(results)} integrations")
    
    elif command == "status":
        manager.status_report()
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
