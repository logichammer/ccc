#!/usr/bin/env python3
"""
Workflow Markdown Parser
Parses draft and suggested workflow markdown files.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class WorkflowStage:
    """Represents a workflow stage"""
    name: str
    description: str
    dependencies: List[str]
    recommended_agents: List[str]
    suggested_mcps: List[str]
    parallel_tasks: List[str]
    success_criteria: List[str]
    expected_outputs: List[str]
    expected_correlations: List[str]
    warnings: List[str]

@dataclass
class WorkflowDefinition:
    """Complete workflow definition"""
    name: str
    description: str
    goal: str
    context: str
    requirements: List[str]
    expected_challenges: List[str]
    parameters: Dict[str, Any]
    inputs: Dict[str, str]
    stages: List[WorkflowStage]
    expected_outputs: List[str]
    template_selection: Optional[str]
    client_slug: Optional[str]
    estimated_time: Optional[int]  # minutes

class WorkflowParser:
    """Parses workflow markdown files"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        
    def parse_draft(self, file_path: Path) -> WorkflowDefinition:
        """Parse a draft workflow markdown file"""
        
        if not file_path.exists():
            raise FileNotFoundError(f"Draft workflow file not found: {file_path}")
            
        # Check for workflow-config.json in inputs directory
        inputs_dir = file_path.parent / "inputs" 
        config_file = inputs_dir / "workflow-config.json"
        config_data = self._load_config_if_exists(config_file)
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract workflow name from filename or first header
        workflow_name = file_path.stem
        
        # Parse main sections
        sections = self._parse_markdown_sections(content)
        
        # Build workflow definition from draft
        workflow = WorkflowDefinition(
            name=workflow_name,
            description=sections.get('description', ''),
            goal=sections.get('goal', ''),
            context=sections.get('context', ''),
            requirements=self._parse_list_items(sections.get('requirements', '')),
            expected_challenges=self._parse_list_items(sections.get('expected challenges', '')),
            parameters={},  # Drafts don't have structured parameters yet
            inputs={},      # Drafts don't have structured inputs yet
            stages=[],      # Drafts don't have stages yet
            expected_outputs=[],  # Will be determined during interview
            template_selection=None,
            client_slug=None,
            estimated_time=None
        )
        
        # Apply config data if available
        if config_data:
            workflow = self._apply_config_to_workflow(workflow, config_data)
        
        return workflow
        
    def parse_suggested(self, file_path: Path) -> WorkflowDefinition:
        """Parse a suggested workflow markdown file (more structured)"""
        
        if not file_path.exists():
            raise FileNotFoundError(f"Suggested workflow file not found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        workflow_name = file_path.stem
        sections = self._parse_markdown_sections(content)
        
        # Parse parameters section
        parameters = self._parse_parameters(sections.get('parameters', ''))
        
        # Parse inputs section
        inputs = self._parse_inputs(sections.get('inputs', ''))
        
        # Parse stages
        stages = self._parse_stages(sections.get('stages', ''))
        
        # Parse expected outputs
        expected_outputs = self._parse_list_items(sections.get('expected outputs', ''))
        
        # Extract metadata
        template_selection = self._extract_template_selection(content)
        client_slug = parameters.get('client_slug')
        estimated_time = self._extract_estimated_time(content)
        
        workflow = WorkflowDefinition(
            name=workflow_name,
            description=sections.get('description', ''),
            goal=sections.get('goal', ''),
            context=sections.get('context', ''),
            requirements=self._parse_list_items(sections.get('requirements', '')),
            expected_challenges=self._parse_list_items(sections.get('expected challenges', '')),
            parameters=parameters,
            inputs=inputs,
            stages=stages,
            expected_outputs=expected_outputs,
            template_selection=template_selection,
            client_slug=client_slug,
            estimated_time=estimated_time
        )
        
        return workflow
        
    def _parse_markdown_sections(self, content: str) -> Dict[str, str]:
        """Parse markdown content into sections"""
        
        sections = {}
        current_section = None
        current_content = []
        
        lines = content.split('\n')
        
        for line in lines:
            # Check for headers (## Section Name)
            header_match = re.match(r'^##\s+(.+)$', line.strip())
            if header_match:
                # Save previous section
                if current_section:
                    sections[current_section.lower()] = '\n'.join(current_content).strip()
                    
                # Start new section
                current_section = header_match.group(1)
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
                    
        # Save final section
        if current_section:
            sections[current_section.lower()] = '\n'.join(current_content).strip()
            
        return sections
        
    def _parse_list_items(self, text: str) -> List[str]:
        """Parse markdown list items"""
        items = []
        
        for line in text.split('\n'):
            line = line.strip()
            # Match both - and * list items
            if line.startswith('- ') or line.startswith('* '):
                items.append(line[2:].strip())
                
        return items
        
    def _parse_parameters(self, text: str) -> Dict[str, Any]:
        """Parse parameters section"""
        parameters = {}
        
        for line in text.split('\n'):
            line = line.strip()
            if ':' in line and (line.startswith('- ') or line.startswith('* ')):
                # Remove list marker
                param_line = line[2:].strip()
                
                # Split on first colon
                parts = param_line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value_desc = parts[1].strip()
                    
                    # For suggested workflows, extract the actual value before parentheses
                    # Format: "- key: actual_value (metadata)"
                    paren_match = re.search(r'^([^(]+)', value_desc)
                    if paren_match:
                        actual_value = paren_match.group(1).strip()
                        
                        # Try to parse as Python literal for lists, etc.
                        try:
                            import ast
                            parsed_value = ast.literal_eval(actual_value)
                            parameters[key] = parsed_value
                        except (ValueError, SyntaxError):
                            # If it's not a valid Python literal, use as string
                            parameters[key] = actual_value
                    else:
                        parameters[key] = value_desc
                    
        return parameters
        
    def _parse_inputs(self, text: str) -> Dict[str, str]:
        """Parse inputs section"""
        inputs = {}
        
        for line in text.split('\n'):
            line = line.strip()
            if ':' in line and (line.startswith('- ') or line.startswith('* ')):
                # Remove list marker
                input_line = line[2:].strip()
                
                # Split on first colon
                parts = input_line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    inputs[key] = value
                    
        return inputs
        
    def _parse_stages(self, text: str) -> List[WorkflowStage]:
        """Parse stages section"""
        stages = []
        current_stage = None
        
        lines = text.split('\n')
        
        for line in lines:
            # Check for stage headers (### Stage N: Name)
            stage_match = re.match(r'^###\s+Stage\s+\d+:\s*(.+)$', line.strip())
            if stage_match:
                # Save previous stage
                if current_stage:
                    stages.append(current_stage)
                    
                # Start new stage
                stage_name = stage_match.group(1)
                current_stage = WorkflowStage(
                    name=stage_name,
                    description='',
                    dependencies=[],
                    recommended_agents=[],
                    suggested_mcps=[],
                    parallel_tasks=[],
                    success_criteria=[],
                    expected_outputs=[],
                    expected_correlations=[],
                    warnings=[]
                )
            elif current_stage:
                # Parse stage attributes
                line = line.strip()
                
                if line.startswith('**Description**:'):
                    current_stage.description = line.replace('**Description**:', '').strip()
                elif line.startswith('**Dependencies**:'):
                    deps_text = line.replace('**Dependencies**:', '').strip()
                    if deps_text.lower() == 'none':
                        current_stage.dependencies = []
                    else:
                        current_stage.dependencies = [d.strip() for d in deps_text.split(',') if d.strip()]
                elif line.startswith('**Recommended Agents**:'):
                    # Parse agent list
                    agents_text = line.replace('**Recommended Agents**:', '').strip()
                    current_stage.recommended_agents = self._parse_agent_list(agents_text)
                elif line.startswith('**Suggested MCPs**:'):
                    mcps_text = line.replace('**Suggested MCPs**:', '').strip()
                    current_stage.suggested_mcps = self._parse_mcp_list(mcps_text)
                elif line.startswith('**Parallel Tasks**:') or line.startswith('**Parallel Execution**:'):
                    parallel_text = re.sub(r'\*\*(Parallel Tasks|Parallel Execution)\*\*:', '', line).strip()
                    current_stage.parallel_tasks = [p.strip() for p in parallel_text.split(',') if p.strip()]
                elif line.startswith('**Success Criteria**:'):
                    # This might be followed by a list, handle it
                    current_stage.success_criteria.append(line.replace('**Success Criteria**:', '').strip())
                elif line.startswith('**Expected Correlations**:'):
                    correlations_text = line.replace('**Expected Correlations**:', '').strip()
                    current_stage.expected_correlations = [c.strip() for c in correlations_text.split(',') if c.strip()]
                elif line.startswith('- ') and current_stage.success_criteria:
                    # Success criteria list item
                    current_stage.success_criteria.append(line[2:].strip())
                    
        # Save final stage
        if current_stage:
            stages.append(current_stage)
            
        return stages
        
    def _parse_agent_list(self, text: str) -> List[str]:
        """Parse agent list with priorities"""
        agents = []
        
        # Handle both comma-separated and line-by-line formats
        if '\n' in text:
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('- ') or line.startswith('* '):
                    agent_info = line[2:].strip()
                    # Extract agent name (before any parentheses or dashes)
                    agent_name = re.split(r'[\(\-]', agent_info)[0].strip()
                    if agent_name:
                        agents.append(agent_name)
        else:
            # Comma-separated format
            for agent in text.split(','):
                agent = agent.strip()
                if agent:
                    # Extract agent name
                    agent_name = re.split(r'[\(\-]', agent)[0].strip()
                    if agent_name:
                        agents.append(agent_name)
                        
        return agents
        
    def _parse_mcp_list(self, text: str) -> List[str]:
        """Parse MCP list"""
        mcps = []
        
        # Similar to agent parsing
        if '\n' in text:
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('- ') or line.startswith('* '):
                    mcp_info = line[2:].strip()
                    mcp_name = mcp_info.split(' ')[0]  # Get first word
                    if mcp_name:
                        mcps.append(mcp_name)
        else:
            for mcp in text.split(','):
                mcp = mcp.strip()
                if mcp:
                    mcp_name = mcp.split(' ')[0]
                    if mcp_name:
                        mcps.append(mcp_name)
                        
        return mcps
        
    def _extract_template_selection(self, content: str) -> Optional[str]:
        """Extract template selection from content"""
        
        template_match = re.search(r'\*\*Template\*\*:\s*`([^`]+)`', content)
        if template_match:
            return template_match.group(1)
            
        template_match = re.search(r'\*\*Template Selection\*\*:\s*([^\n]+)', content)
        if template_match:
            return template_match.group(1).strip()
            
        return None
        
    def _extract_estimated_time(self, content: str) -> Optional[int]:
        """Extract estimated execution time in minutes"""
        
        time_match = re.search(r'\*\*Estimated Duration\*\*:\s*(\d+)[-\s]*(\d+)?\s*minutes?', content)
        if time_match:
            # If range given, use the higher estimate
            if time_match.group(2):
                return int(time_match.group(2))
            else:
                return int(time_match.group(1))
                
        return None
        
    def validate_workflow_syntax(self, file_path: Path) -> List[str]:
        """Validate workflow markdown syntax and return issues"""
        
        issues = []
        
        try:
            workflow = self.parse_suggested(file_path)
            
            # Check required sections
            if not workflow.goal:
                issues.append("Missing Goal section")
                
            if not workflow.stages:
                issues.append("Missing Stages section")
                
            # Check stage validity
            for i, stage in enumerate(workflow.stages):
                if not stage.name:
                    issues.append(f"Stage {i+1} missing name")
                    
                if not stage.recommended_agents:
                    issues.append(f"Stage '{stage.name}' missing recommended agents")
                    
            return issues
            
        except Exception as e:
            issues.append(f"Parse error: {str(e)}")
            return issues
    
    def _load_config_if_exists(self, config_file: Path) -> Optional[Dict[str, Any]]:
        """Load workflow config JSON if it exists"""
        if not config_file.exists():
            return None
            
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
            return None
    
    def _apply_config_to_workflow(self, workflow: WorkflowDefinition, config_data: Dict[str, Any]) -> WorkflowDefinition:
        """Apply JSON config data to workflow definition"""
        
        # Extract variables and apply them to workflow
        if 'variables' in config_data:
            variables = config_data['variables']
            
            # Update workflow parameters with config variables
            updated_parameters = workflow.parameters.copy()
            for key, value in variables.items():
                updated_parameters[key] = value
            workflow.parameters = updated_parameters
        
        # Apply client settings if present
        if 'client_settings' in config_data:
            client_settings = config_data['client_settings']
            if 'client_slug' in client_settings:
                workflow.client_slug = client_settings['client_slug']
        
        # Apply workflow metadata if present
        if 'workflow_name' in config_data:
            workflow.name = config_data['workflow_name']
            
        return workflow
    
    def extract_variables_from_content(self, content: str) -> List[str]:
        """Extract all {{VARIABLE}} patterns from markdown content"""
        pattern = r'\{\{([A-Z_]+)\}\}'
        matches = re.findall(pattern, content)
        return list(set(matches))  # Remove duplicates
    
    def generate_config_template(self, workflow_file: Path) -> Dict[str, Any]:
        """Generate a JSON config template for a workflow"""
        
        if not workflow_file.exists():
            return {}
            
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract variables from content
        variables = self.extract_variables_from_content(content)
        
        # Create template config
        config_template = {
            "workflow_name": workflow_file.stem,
            "variables": {},
            "client_settings": {
                "client_slug": "example-client",
                "output_directory": "reports/client-example/",
                "archive_previous": True
            }
        }
        
        # Add variables with example values
        for var in variables:
            if var == "SITE_URL":
                config_template["variables"][var] = "https://example.com"
            elif var == "MAIN_KEYWORD":
                config_template["variables"][var] = "target keyword phrase"
            elif "DEPTH" in var or "MODE" in var:
                config_template["variables"][var] = "standard"
            elif "COUNT" in var or "LIMIT" in var:
                config_template["variables"][var] = 5
            else:
                config_template["variables"][var] = f"value_for_{var.lower()}"
                
        return config_template