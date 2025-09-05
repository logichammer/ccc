#!/usr/bin/env python3
"""
Workflow Runner - Execution runtime for CCC workflows
Integrates with existing TodoWrite and Agent switching mechanisms
"""

import json
import time
import importlib.util
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from dataclasses import dataclass

@dataclass
class WorkflowContext:
    """Context object passed between workflow steps"""
    template_path: str
    data: Dict[str, Any]
    results: Dict[str, Any]
    current_agent: Optional[str] = None
    todo_list: List[Dict[str, Any]] = None

class WorkflowRunner:
    """Runtime for executing workflow steps with agent coordination"""
    
    def __init__(self, template_path: str):
        self.template_path = Path(template_path)
        self.agent_handlers = {}
        self.command_cache = {}
        
    def register_agent_handler(self, agent_name: str, handler: Callable):
        """Register handler for specific agent"""
        self.agent_handlers[agent_name] = handler
    
    def execute_workflow_step(self, step: Dict[str, Any], context: WorkflowContext) -> Dict[str, Any]:
        """Execute single workflow step with agent coordination"""
        agent_name = step.get("agent")
        command = step.get("command")
        step_config = step.get("config", {})
        
        result = {
            "step_id": step.get("id", f"{agent_name}_{command}"),
            "agent": agent_name,
            "command": command,
            "started_at": time.time(),
            "status": "running"
        }
        
        try:
            # Update context for current agent
            context.current_agent = agent_name
            
            # Execute agent-specific handler if registered
            if agent_name in self.agent_handlers:
                output = self.agent_handlers[agent_name](command, context, step_config)
            else:
                # Default command execution
                output = self._execute_command(command, context, step_config)
            
            result["output"] = output
            result["status"] = "completed"
            result["completed_at"] = time.time()
            result["duration"] = result["completed_at"] - result["started_at"]
            
            # Update workflow context with results
            context.results[result["step_id"]] = output
            
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            result["completed_at"] = time.time()
        
        return result
    
    def _execute_command(self, command: str, context: WorkflowContext, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute command module from template"""
        # Look for command in template commands directory
        commands_dir = self.template_path / "commands"
        command_file = commands_dir / f"{command}.py"
        
        if not command_file.exists():
            raise FileNotFoundError(f"Command file not found: {command_file}")
        
        # Load and execute command module
        if str(command_file) in self.command_cache:
            module = self.command_cache[str(command_file)]
        else:
            spec = importlib.util.spec_from_file_location(command, command_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.command_cache[str(command_file)] = module
        
        # Execute command function
        if hasattr(module, 'execute'):
            return module.execute(context, config)
        elif hasattr(module, 'main'):
            return module.main(context, config)
        else:
            raise AttributeError(f"Command module {command} missing execute() or main() function")
    
    def create_todo_integration(self, workflow_steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert workflow steps to TodoWrite format"""
        todos = []
        
        for step in workflow_steps:
            agent_name = step.get("agent", "Unknown")
            command = step.get("command", "unknown")
            description = step.get("description", f"{agent_name}: {command}")
            
            todo = {
                "content": description,
                "status": "pending", 
                "activeForm": f"Running {description}",
                "agent": agent_name,
                "command": command
            }
            todos.append(todo)
        
        return todos
    
    def execute_with_todo_tracking(self, workflow_steps: List[Dict[str, Any]], context: WorkflowContext) -> List[Dict[str, Any]]:
        """Execute workflow with TodoWrite integration"""
        results = []
        
        # Create todo list for workflow
        todos = self.create_todo_integration(workflow_steps)
        context.todo_list = todos
        
        for i, step in enumerate(workflow_steps):
            # Update todo status to in_progress
            if i < len(todos):
                todos[i]["status"] = "in_progress"
            
            # Execute step
            step_result = self.execute_workflow_step(step, context)
            results.append(step_result)
            
            # Update todo status based on result
            if i < len(todos):
                if step_result["status"] == "completed":
                    todos[i]["status"] = "completed"
                elif step_result["status"] == "failed":
                    todos[i]["status"] = "pending"  # Keep as pending for retry
                    todos[i]["error"] = step_result.get("error", "Unknown error")
        
        return results

class AgentWorkflowIntegration:
    """Integration layer between workflows and existing CCC agent system"""
    
    def __init__(self, workflow_runner: WorkflowRunner):
        self.runner = workflow_runner
        self.agent_mappings = self._load_agent_mappings()
    
    def _load_agent_mappings(self) -> Dict[str, str]:
        """Load agent name mappings for workflow integration"""
        return {
            "TechnicalSEOAgent": "🔧",
            "KeywordStrategyAgent": "🔑", 
            "MetricsReporterAgent": "📊",
            "PerformanceProfilerAgent": "⚡",
            "QualityTesterAgent": "🧪",
            "InterfaceDesignerAgent": "🎨",
            "FrontendImplementerAgent": "🖼️",
            "InteractionEnhancerAgent": "🎯",
            "ResponsiveAdapterAgent": "📱",
            "SecurityAuditorAgent": "🔒"
        }
    
    def format_agent_switch(self, current_agent: str, next_agent: str, reason: str) -> str:
        """Format agent handoff message"""
        current_emoji = self.agent_mappings.get(current_agent, "🏗️")
        next_emoji = self.agent_mappings.get(next_agent, "🔧")
        
        return f"""
🔄 AGENT HANDOFF: {current_emoji} [{current_agent}] → {next_emoji} [{next_agent}]
Reason: {reason}
Context: Workflow step execution
Expected Output: Step completion with results
Return Trigger: Step completion or error
"""
    
    def execute_workflow_with_agents(self, workflow_name: str, steps: List[Dict[str, Any]], context: WorkflowContext) -> Dict[str, Any]:
        """Execute workflow with proper agent switching"""
        results = {
            "workflow_name": workflow_name,
            "steps": [],
            "agent_switches": [],
            "status": "running",
            "started_at": time.time()
        }
        
        current_agent = "SystemArchitectAgent"
        
        try:
            for step in steps:
                next_agent = step.get("agent")
                
                # Handle agent switch if needed
                if next_agent != current_agent:
                    switch_msg = self.format_agent_switch(
                        current_agent, 
                        next_agent, 
                        f"Execute {step.get('command', 'unknown')} command"
                    )
                    results["agent_switches"].append({
                        "from": current_agent,
                        "to": next_agent,
                        "message": switch_msg,
                        "timestamp": time.time()
                    })
                    current_agent = next_agent
                
                # Execute step
                step_result = self.runner.execute_workflow_step(step, context)
                results["steps"].append(step_result)
                
                if step_result["status"] == "failed":
                    results["status"] = "failed"
                    results["failed_step"] = step_result
                    break
            
            if results["status"] != "failed":
                results["status"] = "completed"
        
        except Exception as e:
            results["status"] = "failed" 
            results["error"] = str(e)
        
        results["completed_at"] = time.time()
        results["total_duration"] = results["completed_at"] - results["started_at"]
        
        return results


def create_workflow_context(template_path: str, initial_data: Dict[str, Any] = None) -> WorkflowContext:
    """Helper function to create workflow context"""
    return WorkflowContext(
        template_path=template_path,
        data=initial_data or {},
        results={}
    )