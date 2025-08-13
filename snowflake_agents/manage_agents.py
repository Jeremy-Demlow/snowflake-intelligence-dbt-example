#!/usr/bin/env python3
"""
Snowflake Agents Management Script
Manages Snowflake Intelligence Agents independently from dbt pipeline
"""

import subprocess
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SnowflakeAgentManager:
    """Manages Snowflake Intelligence Agents"""
    
    def __init__(self, agents_dir: str = "."):
        self.agents_dir = Path(agents_dir)
        
    def list_agents(self) -> List[str]:
        """List all available agent SQL files"""
        agent_files = list(self.agents_dir.glob("*agent*.sql"))
        return [f.stem for f in agent_files]
    
    def deploy_agent(self, agent_name: str) -> bool:
        """Deploy a specific agent"""
        agent_file = self.agents_dir / f"{agent_name}.sql"
        
        if not agent_file.exists():
            logger.error(f"Agent file not found: {agent_file}")
            return False
        
        try:
            logger.info(f"Deploying agent: {agent_name}")
            result = subprocess.run(
                ["snow", "sql", "-f", str(agent_file)],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Agent {agent_name} deployed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to deploy agent {agent_name}: {e}")
            logger.error(f"Error output: {e.stderr}")
            return False
    
    def deploy_all_agents(self) -> Dict[str, bool]:
        """Deploy all agents"""
        agents = self.list_agents()
        results = {}
        
        for agent in agents:
            results[agent] = self.deploy_agent(agent)
        
        return results
    
    def test_agent(self, agent_name: str, database: str = "acme_INTELLIGENCE", schema: str = "STAGING") -> bool:
        """Test if an agent exists and is accessible"""
        try:
            test_query = f"SHOW AGENTS LIKE '{agent_name.upper()}' IN SCHEMA {database}.{schema};"
            result = subprocess.run(
                ["snow", "sql", "-q", test_query],
                capture_output=True,
                text=True,
                check=True
            )
            
            if agent_name.upper() in result.stdout:
                logger.info(f"Agent {agent_name} is active and accessible")
                return True
            else:
                logger.warning(f"Agent {agent_name} not found or not accessible")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to test agent {agent_name}: {e}")
            return False
    
    def add_tool_to_agent(self, agent_name: str, tool_spec: Dict[str, Any]) -> bool:
        """Add a new tool to an existing agent (placeholder for future implementation)"""
        logger.info(f"Adding tool to agent {agent_name}: {tool_spec}")
        # This would require reading the current agent spec, modifying it, and redeploying
        # For now, this is a placeholder for the concept
        logger.warning("Tool addition not implemented yet - would require agent spec modification")
        return False
    
    def get_agent_status(self, database: str = "acme_INTELLIGENCE") -> Dict[str, Any]:
        """Get status of all agents in the database"""
        try:
            query = f"SHOW AGENTS IN DATABASE {database};"
            result = subprocess.run(
                ["snow", "sql", "-q", query],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the output to extract agent information
            agents_info = {}
            if "acme_INTELLIGENCE_AGENT" in result.stdout:
                agents_info["acme_intelligence_agent"] = {
                    "status": "active",
                    "database": database,
                    "last_checked": "now"
                }
            
            return agents_info
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get agent status: {e}")
            return {}

def main():
    """Main CLI interface"""
    manager = SnowflakeAgentManager()
    
    if len(sys.argv) < 2:
        print("Usage: python manage_agents.py <command> [agent_name]")
        print("Commands:")
        print("  list                    - List all available agents")
        print("  deploy <agent_name>     - Deploy a specific agent")
        print("  deploy-all             - Deploy all agents")
        print("  test <agent_name>      - Test if agent is working")
        print("  status                 - Show status of all agents")
        return
    
    command = sys.argv[1]
    
    if command == "list":
        agents = manager.list_agents()
        print("Available agents:")
        for agent in agents:
            print(f"  - {agent}")
    
    elif command == "deploy" and len(sys.argv) > 2:
        agent_name = sys.argv[2]
        success = manager.deploy_agent(agent_name)
        sys.exit(0 if success else 1)
    
    elif command == "deploy-all":
        results = manager.deploy_all_agents()
        failed = [name for name, success in results.items() if not success]
        if failed:
            print(f"Failed to deploy: {failed}")
            sys.exit(1)
        else:
            print("All agents deployed successfully!")
    
    elif command == "test" and len(sys.argv) > 2:
        agent_name = sys.argv[2]
        success = manager.test_agent(agent_name)
        sys.exit(0 if success else 1)
    
    elif command == "status":
        status = manager.get_agent_status()
        print("Agent Status:")
        for name, info in status.items():
            print(f"  {name}: {info['status']}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
