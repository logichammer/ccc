#!/usr/bin/env python3
"""
Interactive Workflow Interview System
Conducts chat-based interviews to create detailed workflow specifications.
"""

import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from workflow_parser import WorkflowDefinition

@dataclass
class InterviewResponse:
    """Stores user response to interview question"""
    question: str
    response: str
    suggested_options: List[str]
    selected_option: Optional[str] = None

class WorkflowInterview:
    """Conducts interactive workflow creation interviews"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        
    def conduct_interview(self, draft_workflow: WorkflowDefinition, capabilities: Dict) -> Dict[str, Any]:
        """Auto-parse draft and confirm understanding (Claude Code compatible)"""
        
        print(f"\n🎯 Auto-analyzing workflow draft: '{draft_workflow.name}'")
        print(f"Goal: {draft_workflow.goal}")
        print("\n🤖 Intelligent Analysis & Auto-Configuration")
        print("=" * 60)
        
        # Auto-parse everything intelligently
        responses = self._intelligent_auto_parse(draft_workflow, capabilities)
        
        # Present understanding for confirmation
        self._present_understanding(responses, draft_workflow)
        
        # Enhanced Claude Code compatible confirmation
        confirmation = self._get_confirmation_with_natural_language(responses, draft_workflow)
        responses.update(confirmation)
        
        return responses
        
    def _get_confirmation_with_natural_language(self, responses: Dict, workflow: WorkflowDefinition) -> Dict:
        """Enhanced confirmation interface supporting natural language input"""
        
        print("\n" + "="*60)
        print("🤖 CLAUDE CODE COMPATIBLE CONFIRMATION")
        print("="*60)
        print("✅ Type 'yes' or 'looks good' to proceed")
        print("🔧 Type 'change X to Y' for specific modifications")
        print("📝 Type 'modify' for guided modification menu")
        print("❌ Type 'no' or 'restart' to restart the process")
        print("="*60)
        
        user_input = input("\n💬 Your response: ").strip()
        
        modifications = {}
        
        # Parse natural language confirmation
        if self._is_positive_confirmation(user_input):
            print("\n✅ Configuration confirmed. Proceeding with workflow creation.")
            modifications['confirmed'] = True
            
        elif self._is_negative_confirmation(user_input):
            print("\n🔄 Restarting auto-analysis with your feedback...")
            modifications = self._restart_with_feedback(user_input)
            
        elif 'modify' in user_input.lower():
            print("\n🔧 Opening guided modification menu...")
            modifications.update(self._quick_modify_interview(responses))
            modifications['confirmed'] = True
            
        elif self._contains_change_request(user_input):
            print("\n🤖 Processing your change request...")
            modifications.update(self._process_natural_language_changes(user_input, responses))
            modifications['confirmed'] = True
            
        else:
            print("\n❓ I didn't understand that. Let me show you the guided menu...")
            modifications.update(self._quick_modify_interview(responses))
            modifications['confirmed'] = True
            
        return modifications
        
    def _is_positive_confirmation(self, text: str) -> bool:
        """Detect positive confirmation in natural language"""
        text = text.lower()
        positive_phrases = [
            'yes', 'y', 'looks good', 'perfect', 'correct', 'right', 'good', 
            'proceed', 'continue', 'go ahead', 'that works', 'sounds good',
            'agreed', 'approve', 'confirmed', 'ok', 'okay'
        ]
        return any(phrase in text for phrase in positive_phrases)
        
    def _is_negative_confirmation(self, text: str) -> bool:
        """Detect negative confirmation in natural language"""
        text = text.lower()
        negative_phrases = [
            'no', 'n', 'wrong', 'incorrect', 'restart', 'start over', 
            'not right', 'not good', 'disagree', 'deny', 'reject'
        ]
        return any(phrase in text for phrase in negative_phrases)
        
    def _contains_change_request(self, text: str) -> bool:
        """Detect change requests in natural language"""
        text = text.lower()
        change_indicators = [
            'change', 'modify', 'update', 'switch', 'replace', 'use',
            'add', 'remove', 'delete', 'include', 'exclude', 'set'
        ]
        return any(indicator in text for indicator in change_indicators)
        
    def _process_natural_language_changes(self, text: str, responses: Dict) -> Dict:
        """Process natural language change requests"""
        
        modifications = {}
        text = text.lower()
        
        # Simple pattern matching for common change requests
        if 'project type' in text or 'type' in text:
            for project_type in ['seo', 'python', 'data_analysis', 'wordpress', 'general']:
                if project_type in text:
                    modifications['project_type'] = project_type
                    print(f"✅ Changed project type to: {project_type}")
                    break
                    
        if 'agent' in text:
            # Extract agent names from text (basic pattern)
            words = text.split()
            for i, word in enumerate(words):
                if 'agent' in word and i > 0:
                    potential_agent = words[i-1].title() + 'Agent'
                    current_agents = responses.get('selected_agents', [])
                    if 'add' in text and potential_agent not in current_agents:
                        current_agents.append(potential_agent)
                        modifications['selected_agents'] = current_agents
                        print(f"✅ Added agent: {potential_agent}")
                    elif 'remove' in text and potential_agent in current_agents:
                        current_agents.remove(potential_agent)
                        modifications['selected_agents'] = current_agents
                        print(f"✅ Removed agent: {potential_agent}")
                        
        if 'format' in text:
            for fmt in ['html', 'excel', 'pdf', 'json']:
                if fmt in text:
                    current_formats = responses.get('output_formats', [])
                    if 'add' in text and fmt not in current_formats:
                        current_formats.append(fmt)
                        modifications['output_formats'] = current_formats
                        print(f"✅ Added output format: {fmt}")
                    elif 'remove' in text and fmt in current_formats:
                        current_formats.remove(fmt)
                        modifications['output_formats'] = current_formats
                        print(f"✅ Removed output format: {fmt}")
                        
        # If no specific changes were detected, save the raw feedback
        if not modifications:
            modifications['user_modifications'] = text
            print(f"✅ Recorded your feedback: {text}")
            
        return modifications
        
    def _restart_with_feedback(self, feedback: str) -> Dict:
        """Restart the process incorporating user feedback"""
        
        print("\\n🔄 RESTART WITH FEEDBACK")
        print("To restart the interview process, please:")
        print("1. Edit your draft workflow markdown file with clearer requirements")
        print("2. Run the workflow-system create command again")
        print("3. The enhanced auto-parsing will incorporate your feedback")
        
        return {
            'restart_requested': True,
            'feedback': feedback,
            'confirmed': False
        }
        
    def _intelligent_auto_parse(self, workflow: WorkflowDefinition, capabilities: Dict) -> Dict:
        """Intelligently parse workflow and auto-configure everything"""
        
        responses = {}
        
        # Auto-detect project context
        project_types = self._detect_project_type(workflow)
        responses['project_type'] = project_types[0] if project_types else 'general'
        responses['timeline'] = self._auto_detect_timeline(workflow)
        responses['client_slug'] = workflow.client_slug or 'default'
        
        # Auto-determine input requirements
        responses.update(self._auto_detect_inputs(workflow))
        
        # Auto-select optimal agents and MCPs
        responses.update(self._auto_select_agents(workflow, capabilities))
        
        # Auto-configure output preferences
        responses.update(self._auto_configure_outputs(workflow))
        
        # Auto-set execution parameters
        responses.update(self._auto_configure_execution(workflow))
        
        return responses
    
    def _present_understanding(self, responses: Dict, workflow: WorkflowDefinition):
        """Present parsed understanding to user for confirmation"""
        
        print(f"\n📋 AUTO-PARSED CONFIGURATION")
        print("=" * 40)
        print(f"🎯 Workflow: {workflow.name}")
        print(f"📁 Project Type: {responses.get('project_type', 'general')}")
        print(f"⏱️  Timeline: {responses.get('timeline', 'standard')}")
        print(f"👤 Client: {responses.get('client_slug', 'default')}")
        
        if 'selected_agents' in responses:
            print(f"\n🤖 Selected Agents:")
            for agent in responses['selected_agents']:
                print(f"   • {agent}")
                
        if 'selected_mcps' in responses:
            print(f"\n🔌 Selected MCPs:")
            for mcp in responses['selected_mcps']:
                print(f"   • {mcp}")
                
        if 'input_files' in responses:
            print(f"\n📂 Expected Inputs:")
            for input_file, details in responses['input_files'].items():
                print(f"   • {input_file}: {details.get('description', 'Auto-detected')}")
                
        print(f"\n📊 Output: {responses.get('output_format', 'Standard report + visualizations')}")
        
    def _auto_detect_inputs(self, workflow: WorkflowDefinition) -> Dict:
        """Auto-detect required input files based on workflow analysis"""
        
        project_type = workflow.context.lower() if hasattr(workflow, 'context') else 'general'
        goal_text = workflow.goal.lower()
        
        input_files = {}
        
        # SEO workflow inputs
        if 'seo' in project_type or any(term in goal_text for term in ['audit', 'keyword', 'serp', 'competitor']):
            input_files.update({
                'target_urls.txt': {'description': 'URLs to analyze', 'optional': False},
                'competitors.txt': {'description': 'Competitor domains', 'optional': True},
                'keywords.csv': {'description': 'Target keywords', 'optional': True}
            })
            
        # Data analysis inputs
        if any(term in goal_text for term in ['data', 'analysis', 'csv', 'excel']):
            input_files.update({
                'data.csv': {'description': 'Primary dataset', 'optional': False},
                'config.json': {'description': 'Analysis configuration', 'optional': True}
            })
            
        # WordPress inputs
        if 'wordpress' in project_type or any(term in goal_text for term in ['wp', 'theme', 'plugin']):
            input_files.update({
                'requirements.md': {'description': 'Project requirements', 'optional': False},
                'design_assets/': {'description': 'Design files and assets', 'optional': True}
            })
        
        return {'input_files': input_files}
    
    def _auto_select_agents(self, workflow: WorkflowDefinition, capabilities: Dict) -> Dict:
        """Automatically select optimal agents based on workflow analysis"""
        
        project_types = self._detect_project_type(workflow)
        available_agents = capabilities.get('agents', [])
        
        selected_agents = []
        
        # Primary agents based on project type
        for project_type in project_types:
            if project_type == 'seo':
                seo_agents = [a for a in available_agents if any(term in a.lower() for term in ['seo', 'keyword'])]
                selected_agents.extend(seo_agents[:2])  # Limit to top 2
            elif project_type == 'python':
                code_agents = [a for a in available_agents if any(term in a.lower() for term in ['codebase', 'feature', 'quality'])]
                selected_agents.extend(code_agents[:2])
            elif project_type == 'data_analysis':
                data_agents = [a for a in available_agents if any(term in a.lower() for term in ['data', 'metrics', 'analysis'])]
                selected_agents.extend(data_agents[:2])
        
        # Always include reporting agent
        reporting_agents = [a for a in available_agents if 'metrics' in a.lower() or 'report' in a.lower()]
        if reporting_agents:
            selected_agents.append(reporting_agents[0])
            
        # Remove duplicates and limit total
        selected_agents = list(dict.fromkeys(selected_agents))[:5]
        
        return {'selected_agents': selected_agents}
        
    def _auto_select_mcps(self, workflow: WorkflowDefinition, capabilities: Dict) -> Dict:
        """Automatically select optimal MCPs based on workflow analysis"""
        
        project_types = self._detect_project_type(workflow)
        available_mcps = capabilities.get('mcps', [])
        
        selected_mcps = []
        
        # MCPs based on project type
        for project_type in project_types:
            if project_type == 'seo':
                seo_mcps = [m for m in available_mcps if any(term in m.lower() for term in ['dataforseo', 'gsc', 'firecrawl'])]
                selected_mcps.extend(seo_mcps[:3])
            elif project_type == 'data_analysis':
                data_mcps = [m for m in available_mcps if any(term in m.lower() for term in ['data', 'chart', 'explorer'])]
                selected_mcps.extend(data_mcps[:2])
        
        # Always include chart MCP for visualizations
        chart_mcps = [m for m in available_mcps if 'chart' in m.lower()]
        if chart_mcps:
            selected_mcps.append(chart_mcps[0])
            
        # Remove duplicates and limit total
        selected_mcps = list(dict.fromkeys(selected_mcps))[:4]
        
        return {'selected_mcps': selected_mcps}
        
    def _auto_configure_outputs(self, workflow: WorkflowDefinition) -> Dict:
        """Auto-configure output preferences based on workflow analysis"""
        
        goal_text = workflow.goal.lower()
        
        # Default to HTML dashboard + Excel export
        output_formats = ['html', 'excel']
        detail_level = 'standard'
        include_raw_data = True
        
        # Adjust based on goal keywords
        if any(term in goal_text for term in ['executive', 'summary', 'overview']):
            detail_level = 'executive'
            output_formats = ['html', 'pdf']
        elif any(term in goal_text for term in ['detailed', 'comprehensive', 'thorough']):
            detail_level = 'comprehensive'
            output_formats = ['html', 'excel', 'json']
            
        return {
            'output_formats': output_formats,
            'detail_level': detail_level,
            'include_raw_data': include_raw_data
        }
        
    def _auto_configure_execution(self, workflow: WorkflowDefinition) -> Dict:
        """Auto-configure execution parameters based on workflow analysis"""
        
        goal_text = workflow.goal.lower()
        
        # Default conservative settings
        parallelization = 'conservative'
        error_handling = 'retry'
        
        # Adjust based on urgency indicators
        if any(term in goal_text for term in ['quick', 'fast', 'immediate', 'urgent']):
            parallelization = 'balanced'
        elif any(term in goal_text for term in ['comprehensive', 'thorough', 'detailed']):
            parallelization = 'conservative'
            
        return {
            'parallelization': parallelization,
            'error_handling': error_handling
        }
        
    def _auto_detect_timeline(self, workflow: WorkflowDefinition) -> str:
        """Auto-detect timeline preference from workflow content"""
        
        goal_text = workflow.goal.lower()
        
        if any(term in goal_text for term in ['quick', 'fast', 'immediate']):
            return 'immediate'
        elif any(term in goal_text for term in ['comprehensive', 'thorough', 'detailed']):
            return 'comprehensive'
        else:
            return 'standard'
            
    def _quick_modify_interview(self, responses: Dict) -> Dict:
        """Quick modification interface for parsed configuration"""
        
        print("\n🔧 Quick Modification Options:")
        print("1. Change project type")
        print("2. Add/remove agents")
        print("3. Add/remove MCPs")
        print("4. Change output formats")
        print("5. Other (specify)")
        
        choice = input("\nWhat would you like to modify? (1-5): ").strip()
        
        modifications = {}
        
        if choice == '1':
            new_type = input("Enter new project type (seo/python/data_analysis/wordpress/general): ").strip().lower()
            if new_type in ['seo', 'python', 'data_analysis', 'wordpress', 'general']:
                modifications['project_type'] = new_type
                
        elif choice == '2':
            action = input("Add or remove agents? (add/remove): ").strip().lower()
            agent_name = input("Enter agent name: ").strip()
            
            current_agents = responses.get('selected_agents', [])
            if action == 'add' and agent_name not in current_agents:
                current_agents.append(agent_name)
            elif action == 'remove' and agent_name in current_agents:
                current_agents.remove(agent_name)
                
            modifications['selected_agents'] = current_agents
            
        elif choice == '3':
            action = input("Add or remove MCPs? (add/remove): ").strip().lower()
            mcp_name = input("Enter MCP name: ").strip()
            
            current_mcps = responses.get('selected_mcps', [])
            if action == 'add' and mcp_name not in current_mcps:
                current_mcps.append(mcp_name)
            elif action == 'remove' and mcp_name in current_mcps:
                current_mcps.remove(mcp_name)
                
            modifications['selected_mcps'] = current_mcps
            
        elif choice == '4':
            print("Available formats: html, excel, pdf, json")
            formats = input("Enter desired formats (comma-separated): ").strip().split(',')
            modifications['output_formats'] = [f.strip() for f in formats if f.strip()]
            
        elif choice == '5':
            other_changes = input("Describe your changes: ").strip()
            modifications['user_modifications'] = other_changes
            
        return modifications
        
    def _interview_agent_selection(self, workflow: WorkflowDefinition, capabilities: Dict) -> Dict:
        """Interview about agent and MCP preferences"""
        
        responses = {}
        
        print(f"\n🤖 AGENT & MCP CONFIGURATION")
        print("=" * 40)
        
        # Get available agents
        available_agents = capabilities.get('agents', [])
        available_mcps = capabilities.get('mcps', [])
        
        # Suggest agents based on workflow type
        suggested_agents = self._suggest_agents(workflow, available_agents)
        
        if suggested_agents:
            print(f"\n1. Recommended Agents:")
            for role, agents in suggested_agents.items():
                print(f"   {role.title()}:")
                
                if len(agents) > 1:
                    for i, agent in enumerate(agents):
                        print(f"   {i+1}. {agent}")
                        
                    choice = input(f"   Select preferred agent for {role} (1-{len(agents)}) [1]: ").strip()
                    try:
                        selected_agent = agents[int(choice) - 1] if choice else agents[0]
                    except (ValueError, IndexError):
                        selected_agent = agents[0]
                else:
                    selected_agent = agents[0]
                    print(f"   Using: {selected_agent}")
                    
                responses[f'agent_{role}'] = selected_agent
                
        # MCP preferences
        suggested_mcps = self._suggest_mcps(workflow, available_mcps)
        
        if suggested_mcps:
            print(f"\n2. MCP Selection:")
            for purpose, mcps in suggested_mcps.items():
                print(f"   For {purpose}:")
                
                if len(mcps) > 1:
                    for i, mcp in enumerate(mcps):
                        print(f"   {i+1}. {mcp}")
                        
                    choice = input(f"   Select MCP for {purpose} (1-{len(mcps)}) [1]: ").strip()
                    try:
                        selected_mcp = mcps[int(choice) - 1] if choice else mcps[0]
                    except (ValueError, IndexError):
                        selected_mcp = mcps[0]
                else:
                    selected_mcp = mcps[0]
                    print(f"   Using: {selected_mcp}")
                    
                responses[f'mcp_{purpose}'] = selected_mcp
                
        return responses
        
    def _interview_output_preferences(self, workflow: WorkflowDefinition, capabilities: Dict) -> Dict:
        """Interview about output format and reporting preferences"""
        
        responses = {}
        
        print(f"\n📊 OUTPUT PREFERENCES")
        print("=" * 40)
        
        # Output formats
        print(f"\n1. Output Formats:")
        format_options = [
            ("html", "Interactive HTML dashboard"),
            ("excel", "Excel spreadsheet with data"),
            ("pdf", "PDF report (executive summary)"),
            ("json", "Raw JSON data for further analysis")
        ]
        
        print(f"   Select desired output formats (space-separated numbers):")
        for i, (fmt, desc) in enumerate(format_options):
            print(f"   {i+1}. {fmt.upper()}: {desc}")
            
        format_choice = input(f"   Formats [1 2]: ").strip()
        if format_choice:
            try:
                selected_indices = [int(i) - 1 for i in format_choice.split()]
                selected_formats = [format_options[i][0] for i in selected_indices if 0 <= i < len(format_options)]
                responses['output_formats'] = selected_formats
            except ValueError:
                responses['output_formats'] = ['html', 'excel']  # Default
        else:
            responses['output_formats'] = ['html', 'excel']  # Default
            
        # Report detail level
        print(f"\n2. Report Detail Level:")
        detail_options = [
            ("executive", "High-level summary with key insights"),
            ("standard", "Balanced detail with analysis and recommendations"),
            ("comprehensive", "Full technical details with all data")
        ]
        
        for i, (level, desc) in enumerate(detail_options):
            print(f"   {i+1}. {level.title()}: {desc}")
            
        detail_choice = input(f"   Select detail level (1-3) [2]: ").strip()
        try:
            detail_index = int(detail_choice) - 1 if detail_choice else 1
            responses['detail_level'] = detail_options[detail_index][0]
        except (ValueError, IndexError):
            responses['detail_level'] = 'standard'
            
        # Include raw data
        include_raw = input(f"\n3. Include raw data files for further analysis? [Y/n]: ").strip().lower()
        responses['include_raw_data'] = include_raw in ['', 'y', 'yes']
        
        return responses
        
    def _interview_execution_parameters(self, workflow: WorkflowDefinition, capabilities: Dict) -> Dict:
        """Interview about execution settings and parallelization"""
        
        responses = {}
        
        print(f"\n⚙️ EXECUTION PARAMETERS")
        print("=" * 40)
        
        # Parallelization preference
        print(f"\n1. Parallelization:")
        parallel_options = [
            ("conservative", "Only run clearly independent tasks in parallel"),
            ("balanced", "Use parallelization where safe and beneficial"),
            ("aggressive", "Maximize parallelization (higher risk of conflicts)")
        ]
        
        for i, (level, desc) in enumerate(parallel_options):
            print(f"   {i+1}. {level.title()}: {desc}")
            
        parallel_choice = input(f"   Select parallelization level (1-3) [1]: ").strip()
        try:
            parallel_index = int(parallel_choice) - 1 if parallel_choice else 0
            responses['parallelization'] = parallel_options[parallel_index][0]
        except (ValueError, IndexError):
            responses['parallelization'] = 'conservative'
            
        # Error handling
        print(f"\n2. Error Handling:")
        error_options = [
            ("stop", "Stop workflow on first error"),
            ("continue", "Continue with warnings, skip failed stages"),
            ("retry", "Retry failed stages up to 3 times")
        ]
        
        for i, (strategy, desc) in enumerate(error_options):
            print(f"   {i+1}. {strategy.title()}: {desc}")
            
        error_choice = input(f"   Select error handling (1-3) [3]: ").strip()
        try:
            error_index = int(error_choice) - 1 if error_choice else 2
            responses['error_handling'] = error_options[error_index][0]
        except (ValueError, IndexError):
            responses['error_handling'] = 'retry'
            
        return responses
        
    def _detect_project_type(self, workflow: WorkflowDefinition) -> List[str]:
        """Enhanced project type detection using context inference"""
        
        # Start with workflow content analysis
        text = f"{workflow.goal} {workflow.context} {workflow.description}".lower()
        types = []
        
        # Analyze workflow text content
        text_types = self._analyze_workflow_text(text)
        types.extend(text_types)
        
        # Enhance with codebase context inference
        context_types = self._infer_project_context()
        types.extend(context_types)
        
        # Remove duplicates while preserving order
        unique_types = list(dict.fromkeys(types))
        
        return unique_types or ['general']
        
    def _analyze_workflow_text(self, text: str) -> List[str]:
        """Analyze workflow text for project type indicators"""
        
        types = []
        
        # SEO indicators
        if any(term in text for term in ['seo', 'search engine', 'ranking', 'serp', 'keyword', 'competitor', 'google search console', 'analytics']):
            types.append('seo')
            
        # Python/Development indicators  
        if any(term in text for term in ['python', 'code', 'api', 'flask', 'django', 'repository', 'pip', 'pytest', 'virtual environment']):
            types.append('python')
            
        # Data analysis indicators
        if any(term in text for term in ['data', 'analysis', 'correlation', 'csv', 'analytics', 'pandas', 'numpy', 'visualization', 'dataset']):
            types.append('data_analysis')
            
        # WordPress indicators
        if any(term in text for term in ['wordpress', 'wp', 'elementor', 'plugin', 'theme', 'wp-admin', 'woocommerce']):
            types.append('wordpress')
            
        return types
        
    def _infer_project_context(self) -> List[str]:
        """Infer project type from current directory context"""
        
        import os
        from pathlib import Path
        
        types = []
        current_dir = Path.cwd()
        
        try:
            # Check for Python project indicators
            if any(f.exists() for f in [
                current_dir / 'requirements.txt',
                current_dir / 'pyproject.toml', 
                current_dir / 'setup.py',
                current_dir / 'Pipfile'
            ]):
                types.append('python')
                
            # Check for Node.js/JavaScript project
            if (current_dir / 'package.json').exists():
                # Could be a Node.js based tool
                with open(current_dir / 'package.json', 'r') as f:
                    package_content = f.read().lower()
                    if any(term in package_content for term in ['wordpress', 'wp', 'elementor']):
                        types.append('wordpress')
                        
            # Check for WordPress indicators
            if any(f.exists() for f in [
                current_dir / 'wp-config.php',
                current_dir / 'wp-content',
                current_dir / 'functions.php',
                current_dir / 'style.css'
            ]):
                types.append('wordpress')
                
            # Check for data analysis indicators
            data_files = list(current_dir.glob('*.csv')) + list(current_dir.glob('*.xlsx')) + list(current_dir.glob('*.json'))
            if data_files and len(data_files) > 2:
                types.append('data_analysis')
                
            # Check for Jupyter notebooks
            if list(current_dir.glob('*.ipynb')):
                types.append('data_analysis')
                
            # Check for SEO project indicators
            seo_files = list(current_dir.glob('*seo*')) + list(current_dir.glob('*keyword*')) + list(current_dir.glob('*analytics*'))
            if seo_files:
                types.append('seo')
                
            # Check directory names for context
            dir_name = current_dir.name.lower()
            if any(term in dir_name for term in ['seo', 'analytics', 'keyword']):
                types.append('seo')
            elif any(term in dir_name for term in ['wp', 'wordpress', 'theme', 'plugin']):
                types.append('wordpress')
            elif any(term in dir_name for term in ['data', 'analysis', 'research']):
                types.append('data_analysis')
                
        except (PermissionError, OSError):
            # If we can't read the directory, fall back to text analysis only
            pass
            
        return types
        
    def _suggest_input_files(self, project_type: str, goal: str) -> Dict[str, str]:
        """Suggest likely input files based on project type"""
        
        suggestions = {}
        
        if 'seo' in project_type or 'seo' in goal:
            suggestions.update({
                'gsc_search_analytics.csv': 'Google Search Console export with query performance',
                'competitor_urls.txt': 'List of competitor websites to analyze',
                'target_keywords.csv': 'Priority keywords to focus analysis on'
            })
            
        if 'python' in project_type or 'code' in goal:
            suggestions.update({
                'requirements.txt': 'Python dependencies list',
                'test_config.ini': 'Testing configuration file',
                'codebase.zip': 'Source code archive for analysis'
            })
            
        if 'data' in goal or 'correlation' in goal:
            suggestions.update({
                'primary_dataset.csv': 'Main data file for analysis',
                'supplementary_data.json': 'Additional data source',
                'data_dictionary.txt': 'Column definitions and data descriptions'
            })
            
        return suggestions
        
    def _suggest_fallback_method(self, input_file: str, capabilities: Dict) -> Optional[str]:
        """Suggest fallback method when input file is not available"""
        
        mcps = capabilities.get('mcps', [])
        
        if 'gsc_' in input_file and 'gsc-mcp' in mcps:
            return "Retrieve data directly from Google Search Console API"
        elif 'competitor' in input_file and 'dataforseo-mcp' in mcps:
            return "Auto-discover competitors using DataForSEO API"
        elif 'crawl' in input_file and 'firecrawl-mcp' in mcps:
            return "Perform live website crawl using Firecrawl"
            
        return None
        
    def _suggest_agents(self, workflow: WorkflowDefinition, available_agents: List[str]) -> Dict[str, List[str]]:
        """Suggest agents based on workflow content"""
        
        suggestions = {}
        text = f"{workflow.goal} {workflow.context}".lower()
        
        # Primary analysis agents
        if 'seo' in text:
            seo_agents = [agent for agent in available_agents if 'seo' in agent.lower()]
            if seo_agents:
                suggestions['primary_analysis'] = seo_agents
                
        if 'code' in text or 'python' in text:
            code_agents = [agent for agent in available_agents if any(term in agent.lower() for term in ['codebase', 'feature', 'quality'])]
            if code_agents:
                suggestions['code_analysis'] = code_agents
                
        # Reporting agents
        reporting_agents = [agent for agent in available_agents if 'metrics' in agent.lower() or 'report' in agent.lower()]
        if reporting_agents:
            suggestions['reporting'] = reporting_agents
            
        return suggestions
        
    def _suggest_mcps(self, workflow: WorkflowDefinition, available_mcps: List[str]) -> Dict[str, List[str]]:
        """Suggest MCPs based on workflow content"""
        
        suggestions = {}
        text = f"{workflow.goal} {workflow.context}".lower()
        
        # Data collection MCPs
        if 'seo' in text:
            seo_mcps = [mcp for mcp in available_mcps if any(term in mcp.lower() for term in ['dataforseo', 'gsc', 'firecrawl'])]
            if seo_mcps:
                suggestions['data_collection'] = seo_mcps
                
        # Visualization MCPs
        chart_mcps = [mcp for mcp in available_mcps if 'chart' in mcp.lower()]
        if chart_mcps:
            suggestions['visualization'] = chart_mcps
            
        return suggestions
        
    def generate_suggested_workflow(self, draft: WorkflowDefinition, responses: Dict, capabilities: Dict) -> str:
        """Generate detailed workflow markdown from interview responses"""
        
        workflow_md = f"""# {draft.name}

## Description
{draft.description or 'Comprehensive workflow generated from user requirements'}

## Goal
{draft.goal}

## Context
{draft.context}

## Interview Configuration
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Client: {responses.get('client_slug', 'Not specified')}
Project Type: {responses.get('project_type', 'general')}
Timeline: {responses.get('timeline', 'standard')}

## Parameters
- client_slug: {responses.get('client_slug', 'required-client-name')} (required)
- timeline: {responses.get('timeline', 'standard')} (quality vs speed preference)
- output_formats: {responses.get('output_formats', ['html', 'excel'])}
- detail_level: {responses.get('detail_level', 'standard')}
- parallelization: {responses.get('parallelization', 'conservative')}
- error_handling: {responses.get('error_handling', 'retry')}

## Input Files
"""
        
        # Add input files section
        input_files = []
        for key, value in responses.items():
            if key.startswith('input_') and isinstance(value, dict):
                file_name = key.replace('input_', '').replace('_', '.')
                if value.get('available'):
                    workflow_md += f"- {file_name}: {value['location']} ({value['description']})\n"
                    input_files.append(file_name)
                elif value.get('fallback_method'):
                    workflow_md += f"- {file_name}: *fallback: {value['fallback_method']}* ({value['description']})\n"
                elif value.get('optional'):
                    workflow_md += f"- {file_name}: *optional* ({value['description']})\n"
                    
        # Generate stages based on workflow type and responses
        stages = self._generate_workflow_stages(draft, responses, capabilities)
        
        workflow_md += f"\n## Stages\n\n"
        
        for i, stage in enumerate(stages, 1):
            workflow_md += f"""### Stage {i}: {stage['name']}
**Description**: {stage['description']}
**Dependencies**: {', '.join(stage.get('dependencies', [])) or 'None'}
**Recommended Agents**: 
{self._format_agent_list(stage.get('agents', []))}
**Suggested MCPs**: 
{self._format_mcp_list(stage.get('mcps', []))}
**Success Criteria**:
{self._format_success_criteria(stage.get('success_criteria', []))}
**Expected Outputs**: {', '.join(stage.get('outputs', []))}

"""

        # Add parallelization analysis
        workflow_md += f"""## Parallelization Analysis
**Strategy**: {responses.get('parallelization', 'conservative')}

**SAFE Parallelization Opportunities**:
{self._analyze_safe_parallelization(stages)}

**POTENTIAL CONFLICTS**:
{self._analyze_parallelization_conflicts(stages)}

**RECOMMENDATIONS**:
{self._generate_parallelization_recommendations(stages, responses)}

## Expected Outputs
- **Primary Report**: Interactive {responses.get('detail_level', 'standard')}-level report
- **Data Export**: {', '.join(responses.get('output_formats', ['HTML', 'Excel']))} formats
- **Analysis Files**: Correlation analysis and insights
- **Raw Data**: {'Included' if responses.get('include_raw_data') else 'Not included'}

## Estimated Execution Time
{self._estimate_execution_time(stages, responses)} minutes

## Configuration File
This workflow will generate a configuration file at:
`/workflows/configs/{draft.name}.yaml`

## Next Steps
1. Review this suggested workflow
2. Edit stages, agents, or parameters as needed  
3. Validate technical feasibility: `workflow-system validate {draft.name}`
4. Execute: `workflow-system execute {draft.name}`
"""
        
        return workflow_md
        
    def _generate_workflow_stages(self, draft: WorkflowDefinition, responses: Dict, capabilities: Dict) -> List[Dict]:
        """Generate workflow stages based on project type and responses"""
        
        project_type = responses.get('project_type', 'general')
        stages = []
        
        if project_type == 'seo':
            stages = [
                {
                    'name': 'Data Collection',
                    'description': 'Gather SEO data from multiple sources',
                    'agents': [responses.get('agent_primary_analysis', 'TechnicalSEOAgent')],
                    'mcps': [responses.get('mcp_data_collection', 'dataforseo-mcp'), 'firecrawl-mcp'],
                    'success_criteria': ['Search data retrieved', 'Site crawl completed', 'Competitor data collected'],
                    'outputs': ['search_data.json', 'crawl_results.json', 'competitor_analysis.json']
                },
                {
                    'name': 'Analysis & Correlation Discovery', 
                    'description': 'Analyze data and discover unexpected correlations',
                    'dependencies': ['Stage 1'],
                    'agents': ['DataPipelineAgent', responses.get('agent_primary_analysis', 'TechnicalSEOAgent')],
                    'mcps': ['data-explorer-mcp', responses.get('mcp_visualization', 'chart-mcp')],
                    'success_criteria': ['Statistical analysis completed', 'Correlations identified', 'Anomalies flagged'],
                    'outputs': ['correlation_analysis.json', 'insights_summary.json']
                },
                {
                    'name': 'Report Generation',
                    'description': 'Generate comprehensive reports and visualizations',
                    'dependencies': ['Stage 2'],
                    'agents': [responses.get('agent_reporting', 'MetricsReporterAgent')],
                    'mcps': [responses.get('mcp_visualization', 'chart-mcp')],
                    'success_criteria': ['Reports generated', 'Visualizations created', 'Action items prioritized'],
                    'outputs': ['seo_dashboard.html', 'executive_summary.pdf', 'recommendations.xlsx']
                }
            ]
            
        elif project_type == 'python':
            stages = [
                {
                    'name': 'Code Analysis',
                    'description': 'Static analysis and security scanning',
                    'agents': [responses.get('agent_code_analysis', 'CodebaseAnalyzerAgent'), 'SecurityAuditorAgent'],
                    'mcps': ['pylint-mcp', 'bandit-mcp'],
                    'success_criteria': ['Code quality assessed', 'Security issues identified', 'Test coverage analyzed'],
                    'outputs': ['code_quality_report.json', 'security_audit.json']
                },
                {
                    'name': 'Performance Analysis',
                    'description': 'Performance profiling and bottleneck identification',
                    'dependencies': ['Stage 1'],
                    'agents': ['PerformanceProfilerAgent'],
                    'mcps': ['profiler-mcp'],
                    'success_criteria': ['Performance bottlenecks identified', 'Resource usage analyzed'],
                    'outputs': ['performance_report.json', 'optimization_recommendations.json']
                },
                {
                    'name': 'Report Generation',
                    'description': 'Comprehensive development report',
                    'dependencies': ['Stage 2'],
                    'agents': [responses.get('agent_reporting', 'MetricsReporterAgent')],
                    'mcps': [responses.get('mcp_visualization', 'chart-mcp')],
                    'success_criteria': ['Development report created', 'Action items prioritized'],
                    'outputs': ['code_analysis_dashboard.html', 'development_recommendations.xlsx']
                }
            ]
            
        else:  # General workflow
            stages = [
                {
                    'name': 'Data Collection & Preparation',
                    'description': 'Gather and validate input data',
                    'agents': ['DataPipelineAgent'],
                    'mcps': ['data-explorer-mcp'],
                    'success_criteria': ['Data validated', 'Quality checks passed'],
                    'outputs': ['prepared_data.json']
                },
                {
                    'name': 'Analysis',
                    'description': 'Perform requested analysis and discover insights',
                    'dependencies': ['Stage 1'],
                    'agents': ['DataPipelineAgent', responses.get('agent_primary_analysis', 'MetricsReporterAgent')],
                    'mcps': ['data-explorer-mcp', responses.get('mcp_visualization', 'chart-mcp')],
                    'success_criteria': ['Analysis completed', 'Insights generated'],
                    'outputs': ['analysis_results.json', 'insights.json']
                },
                {
                    'name': 'Report Generation',
                    'description': 'Generate final reports and visualizations',
                    'dependencies': ['Stage 2'], 
                    'agents': [responses.get('agent_reporting', 'MetricsReporterAgent')],
                    'mcps': [responses.get('mcp_visualization', 'chart-mcp')],
                    'success_criteria': ['Reports generated', 'Deliverables created'],
                    'outputs': ['final_report.html', 'data_export.xlsx']
                }
            ]
            
        return stages
        
    def _format_agent_list(self, agents: List[str]) -> str:
        """Format agent list for markdown"""
        if not agents:
            return "- *No specific agents required*"
        return '\n'.join([f"- {agent}" for agent in agents])
        
    def _format_mcp_list(self, mcps: List[str]) -> str:
        """Format MCP list for markdown"""
        if not mcps:
            return "- *No specific MCPs required*"
        return '\n'.join([f"- {mcp}" for mcp in mcps])
        
    def _format_success_criteria(self, criteria: List[str]) -> str:
        """Format success criteria for markdown"""
        if not criteria:
            return "- *Success criteria will be determined during execution*"
        return '\n'.join([f"- {criterion}" for criterion in criteria])
        
    def _analyze_safe_parallelization(self, stages: List[Dict]) -> str:
        """Analyze safe parallelization opportunities"""
        
        safe_parallel = []
        
        for i, stage in enumerate(stages, 1):
            if not stage.get('dependencies'):
                safe_parallel.append(f"- Stage {i} can run independently")
            else:
                # Check for tasks within the stage that could be parallel
                agents = stage.get('agents', [])
                mcps = stage.get('mcps', [])
                
                if len(agents) > 1:
                    safe_parallel.append(f"- Stage {i}: Multiple agents ({', '.join(agents)}) can work on different aspects")
                if len(mcps) > 1:
                    safe_parallel.append(f"- Stage {i}: Multiple MCPs ({', '.join(mcps)}) access different data sources")
                    
        return '\n'.join(safe_parallel) if safe_parallel else "- No clear parallelization opportunities identified"
        
    def _analyze_parallelization_conflicts(self, stages: List[Dict]) -> str:
        """Analyze potential parallelization conflicts"""
        
        conflicts = []
        agent_usage = {}
        mcp_usage = {}
        
        # Track agent and MCP usage across stages
        for i, stage in enumerate(stages, 1):
            for agent in stage.get('agents', []):
                if agent in agent_usage:
                    conflicts.append(f"- {agent} needed by both Stage {agent_usage[agent]} and Stage {i}")
                else:
                    agent_usage[agent] = i
                    
            for mcp in stage.get('mcps', []):
                if mcp in mcp_usage:
                    conflicts.append(f"- {mcp} might have rate limits affecting Stage {mcp_usage[mcp]} and Stage {i}")
                else:
                    mcp_usage[mcp] = i
                    
        return '\n'.join(conflicts) if conflicts else "- No obvious conflicts detected"
        
    def _generate_parallelization_recommendations(self, stages: List[Dict], responses: Dict) -> str:
        """Generate parallelization recommendations"""
        
        strategy = responses.get('parallelization', 'conservative')
        recommendations = []
        
        if strategy == 'conservative':
            recommendations.append("- Execute stages sequentially to ensure stability")
            recommendations.append("- Only parallelize within-stage tasks that use different resources")
            
        elif strategy == 'balanced':
            recommendations.append("- Parallelize independent stages where safe")
            recommendations.append("- Monitor for resource conflicts during execution")
            recommendations.append("- Fall back to sequential execution if conflicts detected")
            
        elif strategy == 'aggressive':
            recommendations.append("- Maximize parallelization even with potential conflicts")
            recommendations.append("- Use timeouts and retries to handle resource contention")
            recommendations.append("- Monitor system resources closely during execution")
            
        return '\n'.join(recommendations)
        
    def _estimate_execution_time(self, stages: List[Dict], responses: Dict) -> str:
        """Estimate total execution time"""
        
        timeline = responses.get('timeline', 'standard')
        base_time_per_stage = {'immediate': 10, 'standard': 20, 'comprehensive': 40}
        
        base_time = len(stages) * base_time_per_stage.get(timeline, 20)
        
        # Adjust for parallelization
        parallelization = responses.get('parallelization', 'conservative')
        if parallelization == 'balanced':
            base_time *= 0.7
        elif parallelization == 'aggressive':
            base_time *= 0.5
            
        return f"{int(base_time)}-{int(base_time * 1.5)}"