#!/usr/bin/env python3
"""
YAML-based Agent Configuration Generator
Scalable approach for multiple agents with environment support
"""

import yaml
import json
import os
import argparse
from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Template

class AgentGenerator:
    def __init__(self, config_dir: str = "agent_configs"):
        self.config_dir = Path(config_dir)
        
    def load_yaml_config(self, config_file: str) -> Dict[str, Any]:
        """Load and parse YAML configuration file"""
        config_path = self.config_dir / f"{config_file}.yml"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Agent config not found: {config_path}")
        
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def apply_environment_overrides(self, config: Dict[str, Any], environment: str = None) -> Dict[str, Any]:
        """Apply environment-specific overrides"""
        if not environment:
            return config
            
        env_file = self.config_dir / "environments" / f"{environment}.yml"
        if env_file.exists():
            with open(env_file, 'r') as f:
                env_overrides = yaml.safe_load(f)
            
            # Simple deep merge for environment overrides
            config = self._deep_merge(config, env_overrides)
        
        return config
    
    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge dictionaries"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    def convert_to_agent_spec(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Convert YAML config to Snowflake Agent JSON specification"""
        
        # Build tools array
        tools = []
        tool_resources = {}
        
        for tool_config in config.get('tools', []):
            # Build tool spec
            tool_spec = {
                "type": tool_config['type'],
                "name": tool_config['name'],
                "description": tool_config['description']
            }
            
            # Add input schema for generic tools
            if 'input_schema' in tool_config:
                tool_spec['input_schema'] = tool_config['input_schema']
            
            tools.append({"tool_spec": tool_spec})
            
            # Build tool resources
            if 'resources' in tool_config:
                tool_resources[tool_config['name']] = tool_config['resources']
        
        # Build agent specification
        spec = {
            "models": {"orchestration": ""},
            "instructions": {
                "response": config['instructions']['response'].strip(),
                "orchestration": config['instructions']['orchestration'].strip(),
                "sample_questions": [
                    {"question": q} for q in config['instructions']['sample_questions']
                ]
            },
            "tools": tools,
            "tool_resources": tool_resources
        }
        
        return spec
    
    def generate_agent_sql(self, config: Dict[str, Any]) -> str:
        """Generate SQL for agent deployment"""
        
        agent_info = config['agent']
        spec = self.convert_to_agent_spec(config)
        
        # Pretty print JSON with proper indentation
        json_spec = json.dumps(spec, indent=2)
        
        sql_template = Template("""-- {{ agent.display_name }} - Generated from YAML Configuration
-- Scalable, maintainable agent deployment

CREATE OR REPLACE AGENT {{ agent.database }}.{{ agent.schema }}.{{ agent.name }}
WITH PROFILE = '{"display_name": "{{ agent.display_name }}"}'  
COMMENT = '{{ agent.comment }}'
FROM SPECIFICATION $${{ json_spec }}$$;""")
        
        return sql_template.render(
            agent=agent_info,
            json_spec=json_spec
        )
    
    def generate_all_agents(self, environment: str = None, output_dir: str = "generated") -> List[str]:
        """Generate SQL for all agent configurations"""
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        generated_files = []
        
        # Find all YAML config files
        for config_file in self.config_dir.glob("*.yml"):
            if config_file.stem == "environments":  # Skip environment configs
                continue
                
            try:
                print(f"🔄 Processing agent: {config_file.stem}")
                
                # Load and process configuration
                config = self.load_yaml_config(config_file.stem)
                config = self.apply_environment_overrides(config, environment)
                
                # Generate SQL
                sql = self.generate_agent_sql(config)
                
                # Save to file
                env_suffix = f"_{environment}" if environment else ""
                output_file = output_path / f"{config_file.stem}{env_suffix}.sql"
                
                with open(output_file, 'w') as f:
                    f.write(sql)
                
                generated_files.append(str(output_file))
                print(f"✅ Generated: {output_file}")
                
            except Exception as e:
                print(f"❌ Error processing {config_file.stem}: {e}")
        
        return generated_files

def main():
    parser = argparse.ArgumentParser(description='Generate Snowflake Agent configurations from YAML')
    parser.add_argument('--agent', help='Specific agent to generate (optional)')
    parser.add_argument('--environment', help='Environment (dev/staging/prod)')
    parser.add_argument('--output-dir', default='generated', help='Output directory')
    parser.add_argument('--list', action='store_true', help='List available agents')
    
    args = parser.parse_args()
    
    generator = AgentGenerator()
    
    if args.list:
        print("📋 Available Agent Configurations:")
        for config_file in Path("agent_configs").glob("*.yml"):
            print(f"  • {config_file.stem}")
        return
    
    if args.agent:
        # Generate single agent
        config = generator.load_yaml_config(args.agent)
        config = generator.apply_environment_overrides(config, args.environment)
        sql = generator.generate_agent_sql(config)
        
        env_suffix = f"_{args.environment}" if args.environment else ""
        output_file = f"{args.output_dir}/{args.agent}{env_suffix}.sql"
        
        os.makedirs(args.output_dir, exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(sql)
        
        print(f"✅ Generated: {output_file}")
        print(f"📊 Lines: {len(sql.splitlines())}")
    else:
        # Generate all agents
        files = generator.generate_all_agents(args.environment, args.output_dir)
        print(f"\n🎉 Generated {len(files)} agent configurations!")

if __name__ == "__main__":
    main()
