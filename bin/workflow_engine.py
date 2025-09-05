#!/usr/bin/env python3
"""
CCC Workflow Engine - Core orchestration system for multi-agent workflows
"""

import json
import os
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path

class WorkflowEngine:
    """Main workflow orchestration engine for CCC system"""
    
    def __init__(self, template_path: str = None):
        self.template_path = template_path
        self.current_template = None
        self.workflow_config = self._load_global_config()
        
        if template_path:
            self.current_template = self._load_template_config(template_path)
    
    def _load_global_config(self) -> Dict[str, Any]:
        """Load global workflow configuration"""
        config_path = Path(__file__).parent.parent / "templates" / "config" / "workflow_config.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        return {"global_workflows": {}, "agent_definitions": {}}
    
    def _load_template_config(self, template_path: str) -> Dict[str, Any]:
        """Load template-specific configuration"""
        config_file = Path(template_path) / "template-config.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def list_available_workflows(self) -> List[str]:
        """List all available workflows for current template"""
        workflows = []
        
        # Global workflows
        workflows.extend(self.workflow_config.get("global_workflows", {}).keys())
        
        # Template-specific workflows
        if self.current_template and "workflows" in self.current_template:
            workflows.extend(self.current_template["workflows"].keys())
        
        return workflows
    
    def get_workflow_definition(self, workflow_name: str) -> Optional[Dict[str, Any]]:
        """Get workflow definition by name"""
        # Check template-specific first
        if self.current_template and "workflows" in self.current_template:
            if workflow_name in self.current_template["workflows"]:
                return self.current_template["workflows"][workflow_name]
        
        # Check global workflows
        if workflow_name in self.workflow_config.get("global_workflows", {}):
            return self.workflow_config["global_workflows"][workflow_name]
        
        return None
    
    def execute_workflow(self, workflow_name: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a workflow by name"""
        workflow = self.get_workflow_definition(workflow_name)
        if not workflow:
            raise ValueError(f"Workflow '{workflow_name}' not found")
        
        context = context or {}
        results = {
            "workflow_name": workflow_name,
            "steps": [],
            "status": "running",
            "context": context
        }
        
        try:
            for step in workflow.get("steps", []):
                step_result = self._execute_step(step, context)
                results["steps"].append(step_result)
                
                # Update context with step results
                if step_result.get("output"):
                    context.update(step_result["output"])
            
            results["status"] = "completed"
            
        except Exception as e:
            results["status"] = "failed"
            results["error"] = str(e)
        
        return results
    
    def _execute_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        agent_name = step.get("agent")
        command = step.get("command")
        step_config = step.get("config", {})
        
        result = {
            "agent": agent_name,
            "command": command,
            "status": "running",
            "input": step_config
        }
        
        try:
            # Import and execute command module
            if self.current_template and "commands" in self.current_template:
                command_path = self.current_template["commands"].get(command)
                if command_path:
                    output = self._run_command(command_path, context, step_config)
                    result["output"] = output
                    result["status"] = "completed"
                else:
                    result["status"] = "skipped"
                    result["message"] = f"Command '{command}' not found in template"
            else:
                result["status"] = "skipped"
                result["message"] = "No commands defined for template"
                
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
        
        return result
    
    def _run_command(self, command_path: str, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Run a command module"""
        # This would integrate with the actual command execution
        # For now, return mock structure
        return {
            "command_executed": command_path,
            "context_used": list(context.keys()),
            "config_applied": config
        }
    
    def validate_workflow(self, workflow_name: str) -> Dict[str, Any]:
        """Validate workflow definition"""
        workflow = self.get_workflow_definition(workflow_name)
        if not workflow:
            return {"valid": False, "error": f"Workflow '{workflow_name}' not found"}
        
        validation = {"valid": True, "issues": []}
        
        # Check required fields
        if "steps" not in workflow:
            validation["issues"].append("Missing 'steps' field")
        
        # Validate steps
        for i, step in enumerate(workflow.get("steps", [])):
            if "agent" not in step:
                validation["issues"].append(f"Step {i}: Missing 'agent' field")
            if "command" not in step:
                validation["issues"].append(f"Step {i}: Missing 'command' field")
        
        validation["valid"] = len(validation["issues"]) == 0
        return validation


def main():
    """CLI interface for workflow engine"""
    if len(sys.argv) < 2:
        print("Usage: workflow_engine.py <template_path> [workflow_name]")
        sys.exit(1)
    
    template_path = sys.argv[1]
    workflow_engine = WorkflowEngine(template_path)
    
    if len(sys.argv) == 3:
        # Execute specific workflow
        workflow_name = sys.argv[2]
        result = workflow_engine.execute_workflow(workflow_name)
        print(json.dumps(result, indent=2))
    else:
        # List available workflows
        workflows = workflow_engine.list_available_workflows()
        print("Available workflows:")
        for workflow in workflows:
            print(f"  - {workflow}")


if __name__ == "__main__":
    main()