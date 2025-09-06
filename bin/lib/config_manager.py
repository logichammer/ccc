#!/usr/bin/env python3
"""
Configuration Management System
Handles YAML configuration hierarchy and merging.
"""

import os
import yaml
import toml
from pathlib import Path
from typing import Dict, List, Optional, Any

class ConfigManager:
    """Manages configuration hierarchy and merging"""
    
    def __init__(self, config_file: Optional[str] = None, client_slug: Optional[str] = None):
        self.client_slug = client_slug
        self.custom_config_file = config_file
        
        # Get CCC root directory
        self.ccc_root = Path(__file__).parent.parent.parent
        
        # Configuration paths
        self.global_config_path = self.ccc_root / "config.toml"
        self.client_configs_dir = self.ccc_root / "client-configs"
        self.workflow_configs_dir = self.ccc_root / "workflows" / "configs"
        
        # Load and merge configurations
        self._load_configurations()
        
    def _load_configurations(self):
        """Load and merge all configuration sources"""
        
        # Start with empty config
        self.config = {}
        
        # 1. Load global CCC config (config.toml) - lowest priority
        if self.global_config_path.exists():
            try:
                with open(self.global_config_path, 'r') as f:
                    global_config = toml.load(f)
                self._merge_config(self.config, global_config)
            except Exception as e:
                print(f"Warning: Could not load global config: {e}")
                
        # 2. Load client-specific config - medium priority
        if self.client_slug:
            client_config_path = self.client_configs_dir / f"{self.client_slug}.yaml"
            if client_config_path.exists():
                try:
                    with open(client_config_path, 'r') as f:
                        client_config = yaml.safe_load(f)
                    if client_config:
                        self._merge_config(self.config, client_config)
                except Exception as e:
                    print(f"Warning: Could not load client config: {e}")
                    
        # 3. Load custom config file - highest priority
        if self.custom_config_file:
            custom_path = Path(self.custom_config_file)
            if custom_path.exists():
                try:
                    with open(custom_path, 'r') as f:
                        if custom_path.suffix.lower() == '.yaml':
                            custom_config = yaml.safe_load(f)
                        elif custom_path.suffix.lower() == '.toml':
                            custom_config = toml.load(f)
                        else:
                            custom_config = yaml.safe_load(f)  # Default to YAML
                    if custom_config:
                        self._merge_config(self.config, custom_config)
                except Exception as e:
                    print(f"Warning: Could not load custom config: {e}")
                    
    def _merge_config(self, base: Dict, update: Dict):
        """Recursively merge configuration dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
                
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation (e.g., 'agents.seo.primary')"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
        
    def set_workflow_config(self, workflow_name: str, config: Dict):
        """Set workflow-specific configuration"""
        config_path = self.workflow_configs_dir / f"{workflow_name}.yaml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise Exception(f"Could not save workflow config: {e}")
            
    def load_workflow_config(self, workflow_name: str) -> Dict:
        """Load workflow-specific configuration"""
        config_path = self.workflow_configs_dir / f"{workflow_name}.yaml"
        
        if not config_path.exists():
            return {}
            
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load workflow config: {e}")
            return {}
            
    def get_agent_config(self, agent_name: str) -> Dict:
        """Get configuration for a specific agent"""
        return self.get(f'agents.{agent_name}', {})
        
    def get_mcp_config(self, mcp_name: str) -> Dict:
        """Get configuration for a specific MCP"""
        return self.get(f'mcps.{mcp_name}', {})
        
    def get_client_config(self) -> Dict:
        """Get client-specific configuration"""
        return self.get('client', {})
        
    def get_execution_config(self) -> Dict:
        """Get workflow execution configuration"""
        return self.get('execution', {
            'max_parallel_tasks': 3,
            'timeout_seconds': 300,
            'max_retries': 3,
            'retry_delay': 5
        })
        
    def get_storage_config(self) -> Dict:
        """Get storage and output configuration"""
        return self.get('storage', {
            'reports_base_dir': '/home/loki/seo-projects',
            'temp_dir': '/tmp/ccc-workflows',
            'cleanup_temp_files': True,
            'archive_completed': True
        })
        
    def get_status(self) -> Dict:
        """Get configuration status for diagnostics"""
        agents_count = 0
        mcps_count = 0
        
        # Count available agents
        agents_dir = self.ccc_root / 'agents'
        if agents_dir.exists():
            agents_count = len(list(agents_dir.glob('*Agent.json')))
            
        # Count available MCPs (this would need to be enhanced to actually detect MCPs)
        mcps_count = len(self.get('mcps', {}))
        
        return {
            'global_config': str(self.global_config_path) if self.global_config_path.exists() else 'Not found',
            'client_config': f'{self.client_slug}.yaml' if self.client_slug else 'None',
            'agents_count': agents_count,
            'mcps_count': mcps_count,
            'workflow_configs_dir': str(self.workflow_configs_dir),
            'client_configs_dir': str(self.client_configs_dir)
        }
        
    def create_default_client_config(self, client_slug: str) -> Path:
        """Create a default client configuration file"""
        
        config_path = self.client_configs_dir / f"{client_slug}.yaml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        default_config = {
            'client_name': client_slug.replace('-', ' ').title(),
            'client_slug': client_slug,
            'created': Path(__file__).name,  # Track creation source
            
            'default_settings': {
                'crawl_depth': 'standard',  # quick, standard, comprehensive
                'timeout_seconds': 300,
                'max_pages': 1000,
                'respect_robots': True
            },
            
            'preferred_agents': {
                'seo_primary': 'TechnicalSEOAgent',
                'seo_secondary': 'BenchmarkResearchAgent',
                'analysis_primary': 'DataPipelineAgent',
                'reporting_primary': 'MetricsReporterAgent'
            },
            
            'mcp_preferences': {
                'seo_data': 'dataforseo-mcp',  # Primary choice for SEO data
                'crawling': 'firecrawl-mcp',   # Primary choice for crawling
                'charts': 'chart-mcp',         # Visualization
                'search': 'perplexity-ask'     # Research and search
            },
            
            'output_settings': {
                'template_preference': 'professional',  # professional, minimal, detailed
                'export_formats': ['html', 'excel'],
                'include_raw_data': True,
                'client_branding': True
            },
            
            'storage_settings': {
                'archive_inputs': True,
                'retention_days': 365,
                'cleanup_temp': True
            }
        }
        
        try:
            with open(config_path, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False, sort_keys=False)
                
            return config_path
            
        except Exception as e:
            raise Exception(f"Could not create client config: {e}")
            
    def validate_config(self) -> List[str]:
        """Validate current configuration and return any issues"""
        issues = []
        
        # Check if agents directory exists
        agents_dir = self.ccc_root / 'agents'
        if not agents_dir.exists():
            issues.append("Agents directory not found")
            
        # Check for required configuration sections
        required_sections = ['execution', 'storage']
        for section in required_sections:
            if not self.get(section):
                issues.append(f"Missing configuration section: {section}")
                
        # Validate storage paths
        storage_config = self.get_storage_config()
        reports_dir = Path(storage_config['reports_base_dir'])
        if not reports_dir.parent.exists():
            issues.append(f"Reports base directory parent does not exist: {reports_dir.parent}")
            
        return issues