#!/usr/bin/env python3
"""
Core Workflow System Implementation
Handles workflow creation, validation, and execution.
"""

import os
import sys
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from workflow_parser import WorkflowParser
from workflow_interview import WorkflowInterview
from workflow_validator import WorkflowValidator
from workflow_executor import WorkflowExecutor
from config_manager import ConfigManager

@dataclass
class WorkflowInfo:
    """Information about a workflow"""
    name: str
    stage: str  # draft, suggested, active, archive
    file_path: Path
    created: datetime
    modified: datetime
    client_slug: Optional[str] = None

class WorkflowSystem:
    """Main workflow system orchestrator"""
    
    def __init__(self, config_file: Optional[str] = None, client_slug: Optional[str] = None, verbose: bool = False):
        self.verbose = verbose
        self.client_slug = client_slug
        
        # Get CCC root directory
        self.ccc_root = Path(__file__).parent.parent.parent
        self.workflows_dir = self.ccc_root / "workflows"
        
        # Ensure workflow directories exist
        self._ensure_directories()
        
        # Initialize components
        self.config_manager = ConfigManager(config_file, client_slug)
        self.parser = WorkflowParser(self.config_manager)
        self.interview = WorkflowInterview(self.config_manager)
        self.validator = WorkflowValidator(self.config_manager)
        self.executor = WorkflowExecutor(self.config_manager)
        
    def _ensure_directories(self):
        """Create workflow directories if they don't exist"""
        for stage in ['draft', 'suggested', 'active', 'archive']:
            (self.workflows_dir / stage).mkdir(parents=True, exist_ok=True)
            
        # Create config directories
        (self.workflows_dir / 'configs').mkdir(parents=True, exist_ok=True)
        (self.ccc_root / 'client-configs').mkdir(parents=True, exist_ok=True)
        
    def _log(self, message: str, level: str = "INFO"):
        """Log message if verbose mode enabled"""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {level}: {message}")
            
    def create_workflow(self, workflow_name: str):
        """Create a new workflow from a draft markdown file"""
        
        # Remove .md extension if provided
        if workflow_name.endswith('.md'):
            workflow_name = workflow_name[:-3]
            
        draft_path = self.workflows_dir / 'draft' / f'{workflow_name}.md'
        
        if not draft_path.exists():
            print(f"Error: Draft file not found: {draft_path}")
            print(f"Please create your initial workflow draft at: {draft_path}")
            print(f"See: /docs/workflow/format-specification.html for format details")
            return False
            
        self._log(f"Starting workflow creation from draft: {draft_path}")
        
        try:
            # Step 1: Parse the draft file
            self._log("Parsing draft workflow...")
            draft_content = self.parser.parse_draft(draft_path)
            
            # Step 2: Analyze available capabilities
            self._log("Analyzing available agents and MCPs...")
            capabilities = self.validator.analyze_capabilities()
            
            # Step 3: Conduct interactive interview
            print(f"\n🎯 Starting workflow creation interview for: {workflow_name}")
            print("=" * 60)
            
            interview_responses = self.interview.conduct_interview(draft_content, capabilities)
            
            # Step 4: Generate suggested workflow
            self._log("Generating workflow recommendations...")
            suggested_workflow = self.interview.generate_suggested_workflow(
                draft_content, 
                interview_responses, 
                capabilities
            )
            
            # Step 5: Save suggested workflow
            suggested_path = self.workflows_dir / 'suggested' / f'{workflow_name}.md'
            with open(suggested_path, 'w') as f:
                f.write(suggested_workflow)
                
            print(f"\n✅ Suggested workflow created: {suggested_path}")
            print(f"\nNext steps:")
            print(f"1. Review and edit the suggested workflow: {suggested_path}")
            print(f"2. Validate technical feasibility: workflow-system validate {workflow_name}")
            print(f"3. Execute approved workflow: workflow-system execute {workflow_name}")
            
            return True
            
        except Exception as e:
            print(f"Error creating workflow: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False
            
    def validate_workflow(self, workflow_name: str):
        """Validate a suggested workflow for technical feasibility"""
        
        suggested_path = self.workflows_dir / 'suggested' / f'{workflow_name}.md'
        
        if not suggested_path.exists():
            print(f"Error: Suggested workflow not found: {suggested_path}")
            print(f"Use 'workflow-system create {workflow_name}' to create it first")
            return False
            
        self._log(f"Validating workflow: {suggested_path}")
        
        try:
            validation_results = self.validator.validate_workflow(suggested_path)
            
            if validation_results.is_valid:
                # Move to active directory
                active_path = self.workflows_dir / 'active' / f'{workflow_name}.md'
                suggested_path.rename(active_path)
                
                print(f"✅ Workflow validation successful!")
                print(f"✅ Workflow moved to active: {active_path}")
                print(f"\nValidation Summary:")
                print(f"- All agents available: {validation_results.agents_available}")
                print(f"- All MCPs accessible: {validation_results.mcps_available}")
                print(f"- Input files validated: {validation_results.input_files_valid}")
                print(f"- No conflicts detected: {validation_results.no_conflicts}")
                
                if validation_results.warnings:
                    print(f"\nWarnings:")
                    for warning in validation_results.warnings:
                        print(f"⚠️  {warning}")
                        
                print(f"\nReady to execute: workflow-system execute {workflow_name}")
                return True
            else:
                print(f"❌ Workflow validation failed!")
                print(f"\nErrors found:")
                for error in validation_results.errors:
                    print(f"❌ {error}")
                    
                if validation_results.suggestions:
                    print(f"\nSuggestions:")
                    for suggestion in validation_results.suggestions:
                        print(f"💡 {suggestion}")
                        
                print(f"\nPlease fix the issues and validate again.")
                return False
                
        except Exception as e:
            print(f"Error validating workflow: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False
            
    def execute_workflow(self, workflow_name: str, dry_run: bool = False):
        """Execute an active workflow"""
        
        active_path = self.workflows_dir / 'active' / f'{workflow_name}.md'
        
        if not active_path.exists():
            print(f"Error: Active workflow not found: {active_path}")
            print(f"Use 'workflow-system validate {workflow_name}' first")
            return False
            
        if dry_run:
            print(f"🔍 DRY RUN MODE - No actual execution")
            
        self._log(f"Executing workflow: {active_path}")
        
        try:
            execution_result = self.executor.execute_workflow(active_path, dry_run=dry_run)
            
            if execution_result.success:
                if not dry_run:
                    print(f"✅ Workflow execution completed successfully!")
                    print(f"📁 Results saved to: {execution_result.output_directory}")
                    print(f"📊 Execution time: {execution_result.execution_time:.1f} seconds")
                    print(f"📈 Stages completed: {execution_result.stages_completed}/{execution_result.total_stages}")
                    
                    if execution_result.correlations_found:
                        print(f"🔍 Correlations discovered: {len(execution_result.correlations_found)}")
                        
                    # Offer to archive the workflow
                    archive_choice = input(f"\nArchive this completed workflow? [Y/n]: ").strip().lower()
                    if archive_choice in ['', 'y', 'yes']:
                        self.archive_workflow(workflow_name)
                else:
                    print(f"✅ Dry run completed - workflow appears executable")
                    print(f"📋 Planned stages: {execution_result.total_stages}")
                    print(f"⏱️  Estimated time: {execution_result.estimated_time:.1f} seconds")
                    
                return True
            else:
                print(f"❌ Workflow execution failed!")
                print(f"Error: {execution_result.error_message}")
                
                if execution_result.partial_results:
                    print(f"💾 Partial results saved to: {execution_result.output_directory}")
                    
                return False
                
        except Exception as e:
            print(f"Error executing workflow: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False
            
    def list_workflows(self):
        """List all workflows in the system"""
        
        workflows = []
        
        for stage in ['draft', 'suggested', 'active', 'archive']:
            stage_dir = self.workflows_dir / stage
            for md_file in stage_dir.glob('*.md'):
                stat = md_file.stat()
                workflows.append(WorkflowInfo(
                    name=md_file.stem,
                    stage=stage,
                    file_path=md_file,
                    created=datetime.fromtimestamp(stat.st_ctime),
                    modified=datetime.fromtimestamp(stat.st_mtime)
                ))
                
        if not workflows:
            print("No workflows found.")
            print(f"Create your first workflow draft in: {self.workflows_dir / 'draft'}")
            return
            
        # Sort by stage priority and name
        stage_order = {'draft': 0, 'suggested': 1, 'active': 2, 'archive': 3}
        workflows.sort(key=lambda w: (stage_order[w.stage], w.name))
        
        print(f"CCC Workflow System - Found {len(workflows)} workflows")
        print("=" * 70)
        
        current_stage = None
        for workflow in workflows:
            if workflow.stage != current_stage:
                current_stage = workflow.stage
                print(f"\n📁 {current_stage.upper()} WORKFLOWS:")
                
            age = datetime.now() - workflow.modified
            if age.days > 0:
                age_str = f"{age.days}d ago"
            elif age.seconds > 3600:
                age_str = f"{age.seconds // 3600}h ago"
            else:
                age_str = f"{age.seconds // 60}m ago"
                
            print(f"  • {workflow.name:<30} (modified {age_str})")
            
    def archive_workflow(self, workflow_name: str):
        """Archive a completed workflow"""
        
        active_path = self.workflows_dir / 'active' / f'{workflow_name}.md'
        
        if not active_path.exists():
            print(f"Error: Active workflow not found: {active_path}")
            return False
            
        try:
            archive_path = self.workflows_dir / 'archive' / f'{workflow_name}.md'
            active_path.rename(archive_path)
            
            print(f"📦 Workflow archived: {archive_path}")
            return True
            
        except Exception as e:
            print(f"Error archiving workflow: {e}")
            return False
            
    def show_status(self):
        """Show system status and configuration"""
        
        print("CCC Workflow Definition & Execution System")
        print("=" * 50)
        print(f"🏠 CCC Root: {self.ccc_root}")
        print(f"📁 Workflows: {self.workflows_dir}")
        print(f"👤 Client: {self.client_slug or 'None'}")
        print(f"🔧 Verbose: {self.verbose}")
        
        # Count workflows by stage
        for stage in ['draft', 'suggested', 'active', 'archive']:
            count = len(list((self.workflows_dir / stage).glob('*.md')))
            print(f"📊 {stage.capitalize()}: {count} workflows")
            
        # Show configuration status
        config_status = self.config_manager.get_status()
        print(f"\n🔧 Configuration Status:")
        print(f"  • Global config: {config_status['global_config']}")
        print(f"  • Client config: {config_status['client_config']}")
        print(f"  • Available agents: {config_status['agents_count']}")
        print(f"  • Available MCPs: {config_status['mcps_count']}")
    
    def generate_config_template(self, workflow_name: str) -> bool:
        """Generate a JSON config template for a draft workflow"""
        
        try:
            # Look for the workflow in draft directory
            draft_path = self.workflows_dir / "draft" / f"{workflow_name}.md"
            
            if not draft_path.exists():
                print(f"❌ Draft workflow not found: {workflow_name}")
                print(f"Available drafts: {[f.stem for f in (self.workflows_dir / 'draft').glob('*.md')]}")
                return False
            
            # Generate config template
            config_template = self.parser.generate_config_template(draft_path)
            
            # Save config template to inputs directory
            inputs_dir = self.workflows_dir / "draft" / "inputs"
            inputs_dir.mkdir(exist_ok=True)
            
            config_path = inputs_dir / "workflow-config.json"
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_template, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Config template generated!")
            print(f"📁 Location: {config_path}")
            print(f"📝 Edit this file to provide actual values for:")
            
            if config_template.get('variables'):
                for var, example in config_template['variables'].items():
                    print(f"  • {var}: {example}")
            
            print(f"\n💡 Place the configured file at: inputs/workflow-config.json")
            print(f"💡 The system will automatically detect and use it")
            
            return True
            
        except Exception as e:
            print(f"Error generating config template: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False