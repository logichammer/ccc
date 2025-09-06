#!/usr/bin/env python3
"""
Workflow Technical Validation System
Validates workflow technical feasibility and dependencies.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from workflow_parser import WorkflowParser, WorkflowDefinition

@dataclass
class ValidationResult:
    """Results of workflow validation"""
    is_valid: bool
    agents_available: bool
    mcps_available: bool
    input_files_valid: bool
    no_conflicts: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]

class WorkflowValidator:
    """Validates workflow technical feasibility"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.parser = WorkflowParser(config_manager)
        
        # Get CCC root for accessing system resources
        self.ccc_root = Path(__file__).parent.parent.parent
        
    def validate_workflow(self, workflow_path: Path) -> ValidationResult:
        """Validate a workflow for technical feasibility"""
        
        errors = []
        warnings = []
        suggestions = []
        
        try:
            # Parse the workflow
            workflow = self.parser.parse_suggested(workflow_path)
            
            # Check all validation aspects
            agents_valid = self._validate_agents(workflow, errors, warnings, suggestions)
            mcps_valid = self._validate_mcps(workflow, errors, warnings, suggestions)
            inputs_valid = self._validate_input_files(workflow, errors, warnings, suggestions)
            no_conflicts = self._validate_no_conflicts(workflow, errors, warnings, suggestions)
            
            # Additional validations
            self._validate_workflow_structure(workflow, errors, warnings, suggestions)
            self._validate_dependencies(workflow, errors, warnings, suggestions)
            
            is_valid = len(errors) == 0
            
            return ValidationResult(
                is_valid=is_valid,
                agents_available=agents_valid,
                mcps_available=mcps_valid,
                input_files_valid=inputs_valid,
                no_conflicts=no_conflicts,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions
            )
            
        except Exception as e:
            errors.append(f"Failed to parse workflow: {str(e)}")
            return ValidationResult(
                is_valid=False,
                agents_available=False,
                mcps_available=False,
                input_files_valid=False,
                no_conflicts=False,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions
            )
            
    def analyze_capabilities(self) -> Dict[str, Any]:
        """Analyze available system capabilities"""
        
        capabilities = {
            'agents': self._discover_available_agents(),
            'mcps': self._discover_available_mcps(),
            'commands': self._discover_available_commands(),
            'templates': self._discover_available_templates()
        }
        
        return capabilities
        
    def _validate_agents(self, workflow: WorkflowDefinition, errors: List[str], warnings: List[str], suggestions: List[str]) -> bool:
        """Validate that all required agents are available"""
        
        available_agents = self._discover_available_agents()
        required_agents = set()
        
        # Collect all agents from workflow stages
        for stage in workflow.stages:
            required_agents.update(stage.recommended_agents)
            
        missing_agents = required_agents - set(available_agents)
        
        if missing_agents:
            for agent in missing_agents:
                errors.append(f"Agent not available: {agent}")
                
                # Suggest alternatives
                alternatives = self._suggest_agent_alternatives(agent, available_agents)
                if alternatives:
                    suggestions.append(f"Alternative agents for {agent}: {', '.join(alternatives)}")
                    
            return False
            
        # Check agent capabilities
        for stage in workflow.stages:
            for agent in stage.recommended_agents:
                capabilities = self._get_agent_capabilities(agent)
                if not capabilities:
                    warnings.append(f"Could not verify capabilities for agent: {agent}")
                    
        return True
        
    def _validate_mcps(self, workflow: WorkflowDefinition, errors: List[str], warnings: List[str], suggestions: List[str]) -> bool:
        """Validate that all required MCPs are available"""
        
        available_mcps = self._discover_available_mcps()
        required_mcps = set()
        
        # Collect all MCPs from workflow stages
        for stage in workflow.stages:
            required_mcps.update(stage.suggested_mcps)
            
        missing_mcps = required_mcps - set(available_mcps)
        
        if missing_mcps:
            for mcp in missing_mcps:
                errors.append(f"MCP not available: {mcp}")
                
                # Suggest alternatives
                alternatives = self._suggest_mcp_alternatives(mcp, available_mcps)
                if alternatives:
                    suggestions.append(f"Alternative MCPs for {mcp}: {', '.join(alternatives)}")
                    
            return False
            
        return True
        
    def _validate_input_files(self, workflow: WorkflowDefinition, errors: List[str], warnings: List[str], suggestions: List[str]) -> bool:
        """Validate input file requirements"""
        
        all_valid = True
        
        # Check for client data directory if client_slug is specified
        if workflow.client_slug:
            client_data_dir = self.ccc_root / 'seo-projects' / workflow.client_slug / 'inputs'
            if not client_data_dir.exists():
                warnings.append(f"Client data directory does not exist: {client_data_dir}")
                suggestions.append(f"Create client directory: mkdir -p {client_data_dir}")
                
        # Validate each input file
        for input_name, input_info in workflow.inputs.items():
            # Handle both string and dict input specifications
            if isinstance(input_info, dict):
                input_path = input_info.get('location', '')
            else:
                input_path = input_info
                
            if input_path and input_path.startswith('inputs/'):
                # Check if file exists relative to client directory
                if workflow.client_slug:
                    full_path = self.ccc_root / 'seo-projects' / workflow.client_slug / input_path
                else:
                    full_path = Path(input_path)
                    
                if not full_path.exists():
                    if 'required' in input_name.lower() or (isinstance(input_info, dict) and not input_info.get('fallback_method')):
                        warnings.append(f"Input file not found: {input_path}")
                        suggestions.append(f"Create input file or specify fallback method for: {input_name}")
                    else:
                        warnings.append(f"Optional input file not found: {input_path}")
                        
        return all_valid
        
    def _validate_no_conflicts(self, workflow: WorkflowDefinition, errors: List[str], warnings: List[str], suggestions: List[str]) -> bool:
        """Validate that there are no resource conflicts"""
        
        agent_usage = {}
        mcp_usage = {}
        no_conflicts = True
        
        # Track agent usage across stages
        for i, stage in enumerate(workflow.stages):
            for agent in stage.recommended_agents:
                if agent in agent_usage:
                    prev_stage = agent_usage[agent]
                    # Check if stages have dependencies that prevent conflict
                    if not self._stages_are_sequential(workflow.stages, prev_stage, i):
                        warnings.append(f"Agent {agent} may be needed by multiple parallel stages")
                        suggestions.append(f"Consider using alternative agents or making stages sequential")
                        
                agent_usage[agent] = i
                
            # Check MCP rate limiting potential
            for mcp in stage.suggested_mcps:
                if mcp in mcp_usage:
                    warnings.append(f"MCP {mcp} used in multiple stages - check rate limits")
                mcp_usage[mcp] = i
                
        return no_conflicts
        
    def _validate_workflow_structure(self, workflow: WorkflowDefinition, errors: List[str], warnings: List[str], suggestions: List[str]):
        """Validate overall workflow structure"""
        
        if not workflow.stages:
            errors.append("Workflow has no stages defined")
            
        if not workflow.goal:
            warnings.append("Workflow goal is not clearly defined")
            
        # Check for circular dependencies
        if self._has_circular_dependencies(workflow.stages):
            errors.append("Circular dependencies detected in workflow stages")
            
        # Check for unrealistic time estimates
        if workflow.estimated_time and workflow.estimated_time > 480:  # 8 hours
            warnings.append(f"Estimated time ({workflow.estimated_time} min) seems excessive")
            suggestions.append("Consider breaking workflow into smaller parts")
            
    def _validate_dependencies(self, workflow: WorkflowDefinition, errors: List[str], warnings: List[str], suggestions: List[str]):
        """Validate stage dependencies"""
        
        stage_names = {f"Stage {i+1}" for i in range(len(workflow.stages))}
        
        for stage in workflow.stages:
            for dep in stage.dependencies:
                if dep not in stage_names:
                    errors.append(f"Stage '{stage.name}' depends on non-existent stage: {dep}")
                    
    def _discover_available_agents(self) -> List[str]:
        """Discover available CCC agents"""
        
        agents = []
        agents_dir = self.ccc_root / 'agents'
        
        if agents_dir.exists():
            for agent_file in agents_dir.glob('*Agent.json'):
                agents.append(agent_file.stem)
                
        return agents
        
    def _discover_available_mcps(self) -> List[str]:
        """Discover available MCPs"""
        
        # This would ideally connect to the MCP system to get available MCPs
        # For now, return the ones mentioned in CCC documentation
        mcps = [
            'sequential_thinking',
            'firecrawl',
            'fetch',
            'dataforseo',
            'chart-mcp',
            'data-explorer',
            'Context7',
            'ref-tools-mcp',
            'screenshot-website-fast',
            'perplexity-ask',
            'gsc-mcp',  # Assumed based on workflow examples
            'pylint-mcp',  # Assumed for Python workflows
            'bandit-mcp',  # Assumed for security
            'lighthouse-mcp'  # Assumed for performance
        ]
        
        return mcps
        
    def _discover_available_commands(self) -> List[str]:
        """Discover available CCC commands"""
        
        commands = []
        commands_dir = self.ccc_root / 'commands'
        
        if commands_dir.exists():
            for cmd_dir in commands_dir.iterdir():
                if cmd_dir.is_dir():
                    commands.extend([f.stem for f in cmd_dir.glob('*.py')])
                    
        return commands
        
    def _discover_available_templates(self) -> List[str]:
        """Discover available report templates"""
        
        templates = []
        templates_dir = self.ccc_root / 'templates'
        
        if templates_dir.exists():
            for template_file in templates_dir.rglob('*.html'):
                # Get relative path from templates directory
                rel_path = template_file.relative_to(templates_dir)
                templates.append(str(rel_path))
                
        return templates
        
    def _suggest_agent_alternatives(self, missing_agent: str, available_agents: List[str]) -> List[str]:
        """Suggest alternative agents for missing one"""
        
        alternatives = []
        
        # Simple keyword matching for alternatives
        if 'SEO' in missing_agent:
            alternatives.extend([agent for agent in available_agents if 'SEO' in agent or 'Benchmark' in agent])
        elif 'Codebase' in missing_agent:
            alternatives.extend([agent for agent in available_agents if 'Feature' in agent or 'Quality' in agent])
        elif 'Metrics' in missing_agent:
            alternatives.extend([agent for agent in available_agents if 'Report' in agent or 'Data' in agent])
            
        return alternatives[:3]  # Limit to top 3
        
    def _suggest_mcp_alternatives(self, missing_mcp: str, available_mcps: List[str]) -> List[str]:
        """Suggest alternative MCPs for missing one"""
        
        alternatives = []
        
        # Simple keyword matching
        if 'dataforseo' in missing_mcp.lower():
            alternatives.extend([mcp for mcp in available_mcps if 'firecrawl' in mcp.lower() or 'perplexity' in mcp.lower()])
        elif 'chart' in missing_mcp.lower():
            alternatives.extend([mcp for mcp in available_mcps if 'visual' in mcp.lower()])
        elif 'gsc' in missing_mcp.lower():
            alternatives.extend([mcp for mcp in available_mcps if 'dataforseo' in mcp.lower()])
            
        return alternatives[:3]
        
    def _get_agent_capabilities(self, agent_name: str) -> Optional[Dict]:
        """Get agent capabilities from agent JSON file"""
        
        agent_file = self.ccc_root / 'agents' / f'{agent_name}.json'
        
        if agent_file.exists():
            try:
                with open(agent_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return None
                
        return None
        
    def _stages_are_sequential(self, stages: List, stage1_idx: int, stage2_idx: int) -> bool:
        """Check if two stages are forced to be sequential by dependencies"""
        
        if stage1_idx >= len(stages) or stage2_idx >= len(stages):
            return False
            
        stage2 = stages[stage2_idx]
        
        # Check if stage2 depends on stage1
        stage1_name = f"Stage {stage1_idx + 1}"
        
        return stage1_name in stage2.dependencies
        
    def _has_circular_dependencies(self, stages: List) -> bool:
        """Check for circular dependencies in stages"""
        
        # Build dependency graph
        graph = {}
        
        for i, stage in enumerate(stages):
            stage_name = f"Stage {i+1}"
            graph[stage_name] = stage.dependencies
            
        # Simple cycle detection using DFS
        def has_cycle(node, visited, rec_stack):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True
                    
            rec_stack.remove(node)
            return False
            
        visited = set()
        
        for node in graph:
            if node not in visited:
                if has_cycle(node, visited, set()):
                    return True
                    
        return False