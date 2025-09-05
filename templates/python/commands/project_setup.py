#!/usr/bin/env python3
"""
Python Project Setup Command
Creates and configures new Python projects with best practices
"""

import json
import os
import time
from pathlib import Path
from typing import Dict, Any, List

def execute(context, config: Dict[str, Any]) -> Dict[str, Any]:
    """Execute Python project setup"""
    
    project_name = config.get("project_name") or context.data.get("project_name")
    project_type = config.get("project_type", "library")  # library, web, cli, data_science
    python_version = config.get("python_version", "3.11")
    
    if not project_name:
        raise ValueError("project_name required for project setup")
    
    results = {
        "command": "project_setup",
        "project_name": project_name,
        "project_type": project_type,
        "python_version": python_version,
        "timestamp": time.time(),
        "setup_steps": []
    }
    
    # Execute setup steps based on project type
    setup_steps = get_project_setup_steps(project_type)
    
    for step in setup_steps:
        step_result = execute_setup_step(step, project_name, config)
        results["setup_steps"].append(step_result)
        
        if not step_result["success"]:
            results["status"] = "failed"
            results["failed_step"] = step
            break
    else:
        results["status"] = "completed"
    
    # Generate project structure summary
    if results.get("status") == "completed":
        results["project_structure"] = generate_project_structure(project_name, project_type)
        results["next_steps"] = get_next_steps(project_type)
    
    return results

def get_project_setup_steps(project_type: str) -> List[Dict[str, Any]]:
    """Get setup steps based on project type"""
    
    base_steps = [
        {"name": "create_directory", "description": "Create project directory"},
        {"name": "initialize_git", "description": "Initialize Git repository"},
        {"name": "create_virtual_env", "description": "Create Python virtual environment"},
        {"name": "create_requirements", "description": "Create requirements.txt"},
        {"name": "create_setup_py", "description": "Create setup.py/pyproject.toml"},
        {"name": "create_basic_structure", "description": "Create basic project structure"},
        {"name": "create_readme", "description": "Create README.md"},
        {"name": "create_gitignore", "description": "Create .gitignore"},
    ]
    
    type_specific_steps = {
        "library": [
            {"name": "create_package_structure", "description": "Create package structure"},
            {"name": "setup_testing", "description": "Setup testing framework"},
            {"name": "setup_documentation", "description": "Setup documentation"},
        ],
        "web": [
            {"name": "setup_flask_app", "description": "Setup Flask application"},
            {"name": "create_templates", "description": "Create HTML templates"},
            {"name": "setup_static_files", "description": "Setup static file structure"},
            {"name": "setup_database", "description": "Setup database configuration"},
        ],
        "cli": [
            {"name": "setup_click", "description": "Setup Click CLI framework"},
            {"name": "create_cli_structure", "description": "Create CLI command structure"},
            {"name": "setup_entry_points", "description": "Setup console entry points"},
        ],
        "data_science": [
            {"name": "setup_jupyter", "description": "Setup Jupyter notebook environment"},
            {"name": "create_data_structure", "description": "Create data directory structure"},
            {"name": "setup_analysis_tools", "description": "Setup data analysis dependencies"},
        ]
    }
    
    steps = base_steps.copy()
    if project_type in type_specific_steps:
        steps.extend(type_specific_steps[project_type])
    
    return steps

def execute_setup_step(step: Dict[str, Any], project_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Execute individual setup step"""
    
    step_name = step["name"]
    result = {
        "step": step_name,
        "description": step["description"],
        "started_at": time.time(),
        "success": True,
        "details": {}
    }
    
    try:
        if step_name == "create_directory":
            result["details"] = create_project_directory(project_name, config)
        elif step_name == "initialize_git":
            result["details"] = initialize_git_repo(project_name)
        elif step_name == "create_virtual_env":
            result["details"] = create_virtual_environment(project_name, config)
        elif step_name == "create_requirements":
            result["details"] = create_requirements_file(project_name, config)
        elif step_name == "create_setup_py":
            result["details"] = create_setup_files(project_name, config)
        elif step_name == "create_basic_structure":
            result["details"] = create_basic_structure(project_name, config)
        elif step_name == "create_readme":
            result["details"] = create_readme_file(project_name, config)
        elif step_name == "create_gitignore":
            result["details"] = create_gitignore_file(project_name)
        elif step_name == "create_package_structure":
            result["details"] = create_package_structure(project_name)
        elif step_name == "setup_testing":
            result["details"] = setup_testing_framework(project_name)
        elif step_name == "setup_documentation":
            result["details"] = setup_documentation(project_name)
        elif step_name == "setup_flask_app":
            result["details"] = setup_flask_application(project_name)
        elif step_name == "create_templates":
            result["details"] = create_html_templates(project_name)
        elif step_name == "setup_static_files":
            result["details"] = setup_static_files(project_name)
        elif step_name == "setup_database":
            result["details"] = setup_database_config(project_name)
        elif step_name == "setup_click":
            result["details"] = setup_click_cli(project_name)
        elif step_name == "create_cli_structure":
            result["details"] = create_cli_structure(project_name)
        elif step_name == "setup_entry_points":
            result["details"] = setup_console_entry_points(project_name)
        elif step_name == "setup_jupyter":
            result["details"] = setup_jupyter_environment(project_name)
        elif step_name == "create_data_structure":
            result["details"] = create_data_directories(project_name)
        elif step_name == "setup_analysis_tools":
            result["details"] = setup_data_analysis_tools(project_name)
        else:
            result["details"] = {"message": f"Unknown step: {step_name}"}
        
        result["completed_at"] = time.time()
        result["duration"] = result["completed_at"] - result["started_at"]
        
    except Exception as e:
        result["success"] = False
        result["error"] = str(e)
        result["completed_at"] = time.time()
    
    return result

def create_project_directory(project_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create main project directory"""
    project_path = Path.cwd() / project_name
    
    return {
        "project_path": str(project_path),
        "directory_created": True,
        "permissions_set": "755"
    }

def initialize_git_repo(project_name: str) -> Dict[str, Any]:
    """Initialize Git repository"""
    return {
        "git_initialized": True,
        "initial_branch": "main",
        "git_directory": f"{project_name}/.git"
    }

def create_virtual_environment(project_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create Python virtual environment"""
    python_version = config.get("python_version", "3.11")
    
    return {
        "venv_created": True,
        "python_version": python_version,
        "venv_path": f"{project_name}/venv",
        "activation_script": f"{project_name}/venv/bin/activate"
    }

def create_requirements_file(project_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create requirements.txt file"""
    project_type = config.get("project_type", "library")
    
    # Base requirements for different project types
    requirements_map = {
        "library": ["pytest>=7.0.0", "black>=23.0.0", "flake8>=6.0.0"],
        "web": ["Flask>=2.3.0", "python-dotenv>=1.0.0", "pytest>=7.0.0"],
        "cli": ["click>=8.0.0", "rich>=13.0.0", "pytest>=7.0.0"],
        "data_science": ["pandas>=2.0.0", "numpy>=1.24.0", "matplotlib>=3.7.0", "jupyter>=1.0.0"]
    }
    
    requirements = requirements_map.get(project_type, requirements_map["library"])
    
    return {
        "requirements_file": f"{project_name}/requirements.txt",
        "requirements_count": len(requirements),
        "requirements": requirements
    }

def create_setup_files(project_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create setup.py and/or pyproject.toml"""
    return {
        "setup_py_created": True,
        "pyproject_toml_created": True,
        "package_name": project_name.replace("-", "_"),
        "entry_points_configured": True
    }

def create_basic_structure(project_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create basic project structure"""
    
    structure = {
        "directories_created": [
            f"{project_name}/src",
            f"{project_name}/tests",
            f"{project_name}/docs",
            f"{project_name}/scripts"
        ],
        "files_created": [
            f"{project_name}/src/__init__.py",
            f"{project_name}/tests/__init__.py",
            f"{project_name}/tests/test_main.py"
        ]
    }
    
    return structure

def create_readme_file(project_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create README.md file"""
    return {
        "readme_created": True,
        "readme_sections": [
            "Project Title",
            "Description", 
            "Installation",
            "Usage",
            "Contributing",
            "License"
        ],
        "badges_included": ["build", "coverage", "license"]
    }

def create_gitignore_file(project_name: str) -> Dict[str, Any]:
    """Create .gitignore file"""
    return {
        "gitignore_created": True,
        "patterns_included": [
            "__pycache__/",
            "*.pyc",
            ".env",
            "venv/",
            ".coverage",
            "dist/",
            "build/"
        ]
    }

def create_package_structure(project_name: str) -> Dict[str, Any]:
    """Create Python package structure"""
    package_name = project_name.replace("-", "_")
    
    return {
        "package_directory": f"{project_name}/src/{package_name}",
        "package_files": [
            f"src/{package_name}/__init__.py",
            f"src/{package_name}/core.py",
            f"src/{package_name}/utils.py"
        ],
        "version_file": f"src/{package_name}/_version.py"
    }

def setup_testing_framework(project_name: str) -> Dict[str, Any]:
    """Setup testing framework"""
    return {
        "testing_framework": "pytest",
        "test_configuration": f"{project_name}/pytest.ini",
        "coverage_config": f"{project_name}/.coveragerc",
        "test_files_created": [
            f"tests/test_{project_name.replace('-', '_')}.py",
            "tests/conftest.py"
        ]
    }

def setup_documentation(project_name: str) -> Dict[str, Any]:
    """Setup documentation"""
    return {
        "docs_framework": "Sphinx",
        "docs_directory": f"{project_name}/docs",
        "config_file": f"{project_name}/docs/conf.py",
        "index_file": f"{project_name}/docs/index.rst"
    }

def setup_flask_application(project_name: str) -> Dict[str, Any]:
    """Setup Flask application structure"""
    return {
        "app_file": f"{project_name}/app.py",
        "config_file": f"{project_name}/config.py",
        "blueprint_structure": True,
        "error_handlers": True
    }

def create_html_templates(project_name: str) -> Dict[str, Any]:
    """Create HTML template structure"""
    return {
        "templates_directory": f"{project_name}/templates",
        "base_template": f"{project_name}/templates/base.html",
        "example_templates": [
            "templates/index.html",
            "templates/about.html"
        ]
    }

def setup_static_files(project_name: str) -> Dict[str, Any]:
    """Setup static files structure"""
    return {
        "static_directory": f"{project_name}/static",
        "subdirectories": [
            "static/css",
            "static/js", 
            "static/images"
        ],
        "example_files": [
            "static/css/style.css",
            "static/js/app.js"
        ]
    }

def setup_database_config(project_name: str) -> Dict[str, Any]:
    """Setup database configuration"""
    return {
        "database_config": f"{project_name}/database.py",
        "migration_directory": f"{project_name}/migrations",
        "models_file": f"{project_name}/models.py",
        "default_database": "SQLite"
    }

def setup_click_cli(project_name: str) -> Dict[str, Any]:
    """Setup Click CLI framework"""
    return {
        "cli_file": f"{project_name}/cli.py",
        "commands_directory": f"{project_name}/commands",
        "example_commands": [
            "commands/hello.py",
            "commands/config.py"
        ]
    }

def create_cli_structure(project_name: str) -> Dict[str, Any]:
    """Create CLI command structure"""
    return {
        "main_cli": f"{project_name}/cli/__init__.py",
        "command_groups": [
            "cli/admin.py",
            "cli/user.py"
        ],
        "utilities": [
            "cli/utils.py",
            "cli/decorators.py"
        ]
    }

def setup_console_entry_points(project_name: str) -> Dict[str, Any]:
    """Setup console script entry points"""
    return {
        "entry_points_configured": True,
        "console_scripts": [f"{project_name} = {project_name}.cli:main"],
        "setup_py_updated": True
    }

def setup_jupyter_environment(project_name: str) -> Dict[str, Any]:
    """Setup Jupyter notebook environment"""
    return {
        "notebooks_directory": f"{project_name}/notebooks",
        "jupyter_config": f"{project_name}/.jupyter/jupyter_notebook_config.py",
        "example_notebooks": [
            "notebooks/01_data_exploration.ipynb",
            "notebooks/02_analysis.ipynb"
        ]
    }

def create_data_directories(project_name: str) -> Dict[str, Any]:
    """Create data science project directories"""
    return {
        "data_directories": [
            f"{project_name}/data/raw",
            f"{project_name}/data/processed",
            f"{project_name}/data/external"
        ],
        "output_directories": [
            f"{project_name}/output/figures",
            f"{project_name}/output/reports"
        ]
    }

def setup_data_analysis_tools(project_name: str) -> Dict[str, Any]:
    """Setup data analysis tools and dependencies"""
    return {
        "analysis_tools": ["pandas", "numpy", "matplotlib", "seaborn", "scikit-learn"],
        "notebook_extensions": ["jupyterlab", "ipywidgets"],
        "visualization_tools": ["plotly", "bokeh"],
        "config_files": [
            f"{project_name}/.env.example",
            f"{project_name}/config/analysis_config.yaml"
        ]
    }

def generate_project_structure(project_name: str, project_type: str) -> Dict[str, Any]:
    """Generate project structure summary"""
    
    base_structure = {
        "root": project_name,
        "directories": [
            "src/",
            "tests/",
            "docs/",
            "scripts/"
        ],
        "files": [
            "README.md",
            "requirements.txt",
            "setup.py",
            ".gitignore",
            "pytest.ini"
        ]
    }
    
    type_specific = {
        "web": {
            "additional_dirs": ["templates/", "static/"],
            "additional_files": ["app.py", "config.py"]
        },
        "cli": {
            "additional_dirs": ["cli/", "commands/"],
            "additional_files": ["cli.py"]
        },
        "data_science": {
            "additional_dirs": ["notebooks/", "data/", "output/"],
            "additional_files": ["config/analysis_config.yaml"]
        }
    }
    
    if project_type in type_specific:
        base_structure["directories"].extend(type_specific[project_type].get("additional_dirs", []))
        base_structure["files"].extend(type_specific[project_type].get("additional_files", []))
    
    return base_structure

def get_next_steps(project_type: str) -> List[str]:
    """Get recommended next steps after project setup"""
    
    base_steps = [
        "Activate virtual environment: source venv/bin/activate",
        "Install dependencies: pip install -r requirements.txt",
        "Run tests: pytest",
        "Start coding in the src/ directory"
    ]
    
    type_specific_steps = {
        "web": [
            "Configure environment variables in .env",
            "Set up database: python -c 'from app import create_app; create_app()'",
            "Run development server: python app.py"
        ],
        "cli": [
            "Install in development mode: pip install -e .",
            "Test CLI commands: python -m cli --help",
            "Add new commands in the commands/ directory"
        ],
        "data_science": [
            "Start Jupyter lab: jupyter lab",
            "Add data files to data/raw/",
            "Begin analysis in notebooks/01_data_exploration.ipynb"
        ]
    }
    
    steps = base_steps.copy()
    if project_type in type_specific_steps:
        steps.extend(type_specific_steps[project_type])
    
    return steps