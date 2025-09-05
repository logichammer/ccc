#!/usr/bin/env python3
"""
Test script for CCC Workflow System
Validates workflow engine functionality and integration
"""

import sys
import json
from pathlib import Path

# Add CCC to path
sys.path.insert(0, str(Path(__file__).parent.parent / "bin"))

from workflow_engine import WorkflowEngine
from lib.workflow_runner import WorkflowRunner, create_workflow_context
from lib.workflow_runner import AgentWorkflowIntegration

def test_workflow_engine():
    """Test workflow engine basic functionality"""
    print("Testing WorkflowEngine...")
    
    # Test with SEO template
    seo_template_path = Path(__file__).parent.parent / "templates" / "seo"
    engine = WorkflowEngine(str(seo_template_path))
    
    # Test workflow listing
    workflows = engine.list_available_workflows()
    print(f"Available workflows: {workflows}")
    
    # Test workflow definition retrieval
    if "full_seo_audit" in workflows:
        workflow = engine.get_workflow_definition("full_seo_audit")
        print(f"Full SEO Audit workflow: {json.dumps(workflow, indent=2)}")
    
    # Test workflow validation
    validation = engine.validate_workflow("full_seo_audit")
    print(f"Workflow validation: {validation}")
    
    return len(workflows) > 0

def test_workflow_runner():
    """Test workflow runner execution"""
    print("\nTesting WorkflowRunner...")
    
    # Create workflow runner for Python template
    python_template_path = Path(__file__).parent.parent / "templates" / "python"
    runner = WorkflowRunner(str(python_template_path))
    
    # Create workflow context
    context = create_workflow_context(
        str(python_template_path),
        {"project_name": "test_project", "project_type": "library"}
    )
    
    # Test step execution simulation
    test_step = {
        "agent": "FeatureDeveloperAgent",
        "command": "project_setup",
        "config": {"project_type": "library", "python_version": "3.11"}
    }
    
    try:
        result = runner.execute_workflow_step(test_step, context)
        print(f"Step execution result: {json.dumps(result, indent=2)}")
        return result["status"] in ["completed", "skipped"]
    except Exception as e:
        print(f"Step execution error: {e}")
        return False

def test_agent_integration():
    """Test agent workflow integration"""
    print("\nTesting AgentWorkflowIntegration...")
    
    # Create runner and integration layer
    template_path = Path(__file__).parent.parent / "templates" / "seo"
    runner = WorkflowRunner(str(template_path))
    integration = AgentWorkflowIntegration(runner)
    
    # Test agent handoff formatting
    handoff_msg = integration.format_agent_switch(
        "SystemArchitectAgent",
        "TechnicalSEOAgent", 
        "Execute technical analysis"
    )
    print(f"Agent handoff message:\n{handoff_msg}")
    
    return "AGENT HANDOFF" in handoff_msg

def test_template_configurations():
    """Test template configuration loading"""
    print("\nTesting template configurations...")
    
    templates = ["seo", "wordpress", "python"]
    results = {}
    
    for template in templates:
        template_path = Path(__file__).parent.parent / "templates" / template
        config_file = template_path / "template-config.json"
        
        if config_file.exists():
            try:
                with open(config_file) as f:
                    config = json.load(f)
                workflows = list(config.get("workflows", {}).keys())
                commands = list(config.get("commands", {}).keys())
                
                results[template] = {
                    "workflows": workflows,
                    "commands": commands,
                    "workflow_count": len(workflows),
                    "command_count": len(commands)
                }
                
                print(f"{template} template: {len(workflows)} workflows, {len(commands)} commands")
                
            except Exception as e:
                print(f"Error loading {template} config: {e}")
                results[template] = {"error": str(e)}
        else:
            print(f"Config file not found for {template} template")
            results[template] = {"error": "Config file not found"}
    
    return all("error" not in result for result in results.values())

def test_global_configuration():
    """Test global workflow configuration"""
    print("\nTesting global configuration...")
    
    config_path = Path(__file__).parent.parent / "templates" / "config" / "workflow_config.json"
    
    if config_path.exists():
        try:
            with open(config_path) as f:
                config = json.load(f)
            
            global_workflows = list(config.get("global_workflows", {}).keys())
            agent_definitions = list(config.get("agent_definitions", {}).keys())
            
            print(f"Global workflows: {global_workflows}")
            print(f"Agent definitions: {len(agent_definitions)} agents")
            
            return len(global_workflows) > 0 and len(agent_definitions) > 0
            
        except Exception as e:
            print(f"Error loading global config: {e}")
            return False
    else:
        print("Global config file not found")
        return False

def run_comprehensive_test():
    """Run comprehensive workflow system test"""
    print("=" * 60)
    print("CCC Workflow System Comprehensive Test")
    print("=" * 60)
    
    tests = [
        ("Workflow Engine", test_workflow_engine),
        ("Workflow Runner", test_workflow_runner),
        ("Agent Integration", test_agent_integration),
        ("Template Configurations", test_template_configurations),
        ("Global Configuration", test_global_configuration)
    ]
    
    results = {}
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
            if result:
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            results[test_name] = False
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Summary: {passed}/{total} tests passed")
    print("=" * 60)
    
    # Detailed results
    if passed == total:
        print("🎉 All tests passed! Workflow system is ready.")
        return True
    else:
        print("⚠️  Some tests failed. Review implementation.")
        for test_name, result in results.items():
            if not result:
                print(f"  - {test_name}: needs attention")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)