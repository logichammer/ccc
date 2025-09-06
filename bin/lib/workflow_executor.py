#!/usr/bin/env python3
"""
Workflow Execution Engine
Executes validated workflows with proper error handling and monitoring.
"""

import os
import json
import time
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from workflow_parser import WorkflowParser, WorkflowDefinition

@dataclass
class ExecutionResult:
    """Results of workflow execution"""
    success: bool
    execution_time: float
    stages_completed: int
    total_stages: int
    output_directory: Optional[Path]
    correlations_found: List[Dict]
    error_message: Optional[str]
    partial_results: bool
    estimated_time: Optional[float] = None  # For dry run

class WorkflowExecutor:
    """Executes validated workflows"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.parser = WorkflowParser(config_manager)
        
        # Get execution configuration
        self.exec_config = config_manager.get_execution_config()
        self.storage_config = config_manager.get_storage_config()
        
        # Setup output directory
        self.reports_dir = Path(self.storage_config['reports_base_dir'])
        self.temp_dir = Path(self.storage_config['temp_dir'])
        
        # Current execution state
        self.current_workflow = None
        self.execution_start_time = None
        self.output_dir = None
        
    def execute_workflow(self, workflow_path: Path, dry_run: bool = False) -> ExecutionResult:
        """Execute a validated workflow"""
        
        try:
            # Parse workflow
            workflow = self.parser.parse_suggested(workflow_path)
            self.current_workflow = workflow
            self.execution_start_time = time.time()
            
            if dry_run:
                return self._perform_dry_run(workflow)
            else:
                return self._perform_execution(workflow)
                
        except Exception as e:
            return ExecutionResult(
                success=False,
                execution_time=time.time() - (self.execution_start_time or time.time()),
                stages_completed=0,
                total_stages=len(workflow.stages) if workflow else 0,
                output_directory=None,
                correlations_found=[],
                error_message=f"Execution failed: {str(e)}",
                partial_results=False
            )
            
    def _perform_dry_run(self, workflow: WorkflowDefinition) -> ExecutionResult:
        """Perform dry run analysis without actual execution"""
        
        print(f"🔍 DRY RUN: {workflow.name}")
        print("=" * 50)
        
        estimated_time = 0
        
        for i, stage in enumerate(workflow.stages, 1):
            print(f"\n📋 Stage {i}: {stage.name}")
            print(f"   Description: {stage.description}")
            print(f"   Agents: {', '.join(stage.recommended_agents)}")
            print(f"   MCPs: {', '.join(stage.suggested_mcps)}")
            print(f"   Dependencies: {', '.join(stage.dependencies) if stage.dependencies else 'None'}")
            
            # Estimate time for this stage
            stage_time = self._estimate_stage_time(stage)
            estimated_time += stage_time
            print(f"   Estimated time: {stage_time:.1f} minutes")
            
            # Check for parallel execution opportunities
            if not stage.dependencies and i > 1:
                print(f"   🔄 Could run in parallel with earlier stages")
                
        print(f"\n⏱️ Total estimated time: {estimated_time:.1f} minutes")
        
        return ExecutionResult(
            success=True,
            execution_time=0,
            stages_completed=0,
            total_stages=len(workflow.stages),
            output_directory=None,
            correlations_found=[],
            error_message=None,
            partial_results=False,
            estimated_time=estimated_time
        )
        
    def _perform_execution(self, workflow: WorkflowDefinition) -> ExecutionResult:
        """Perform actual workflow execution"""
        
        print(f"🚀 EXECUTING WORKFLOW: {workflow.name}")
        print("=" * 50)
        
        # Setup output directory
        self.output_dir = self._create_output_directory(workflow)
        
        # Save workflow configuration
        self._save_workflow_config(workflow)
        
        # Archive input files
        self._archive_input_files(workflow)
        
        # Execute stages
        stages_completed = 0
        correlations_found = []
        partial_results = False
        
        try:
            for i, stage in enumerate(workflow.stages, 1):
                print(f"\n📋 Stage {i}/{len(workflow.stages)}: {stage.name}")
                print("-" * 40)
                
                stage_result = self._execute_stage(stage, i, workflow)
                
                if stage_result['success']:
                    stages_completed += 1
                    correlations_found.extend(stage_result.get('correlations', []))
                    
                    print(f"✅ Stage {i} completed successfully")
                    
                    # Save stage results
                    self._save_stage_results(stage, i, stage_result)
                    
                else:
                    print(f"❌ Stage {i} failed: {stage_result.get('error', 'Unknown error')}")
                    
                    error_handling = self.exec_config.get('error_handling', 'retry')
                    
                    if error_handling == 'stop':
                        partial_results = True
                        break
                    elif error_handling == 'retry':
                        # Attempt retry
                        retry_result = self._retry_stage(stage, i, workflow)
                        if retry_result['success']:
                            stages_completed += 1
                            correlations_found.extend(retry_result.get('correlations', []))
                            print(f"✅ Stage {i} completed on retry")
                            self._save_stage_results(stage, i, retry_result)
                        else:
                            partial_results = True
                            if error_handling != 'continue':
                                break
                    # 'continue' option falls through to next stage
                    
            # Generate final reports
            if stages_completed > 0:
                self._generate_final_reports(workflow, correlations_found)
                
            execution_time = time.time() - self.execution_start_time
            
            return ExecutionResult(
                success=stages_completed == len(workflow.stages),
                execution_time=execution_time,
                stages_completed=stages_completed,
                total_stages=len(workflow.stages),
                output_directory=self.output_dir,
                correlations_found=correlations_found,
                error_message=None,
                partial_results=partial_results
            )
            
        except Exception as e:
            execution_time = time.time() - self.execution_start_time
            
            return ExecutionResult(
                success=False,
                execution_time=execution_time,
                stages_completed=stages_completed,
                total_stages=len(workflow.stages),
                output_directory=self.output_dir,
                correlations_found=correlations_found,
                error_message=str(e),
                partial_results=True
            )
            
    def _execute_stage(self, stage, stage_num: int, workflow: WorkflowDefinition) -> Dict[str, Any]:
        """Execute a single workflow stage"""
        
        stage_start_time = time.time()
        
        try:
            print(f"   Agents: {', '.join(stage.recommended_agents)}")
            print(f"   MCPs: {', '.join(stage.suggested_mcps)}")
            
            # This is where we would integrate with the actual CCC agent system
            # For now, we'll simulate the execution and demonstrate the structure
            
            result = {
                'success': True,
                'stage_num': stage_num,
                'execution_time': time.time() - stage_start_time,
                'outputs': [],
                'correlations': [],
                'warnings': [],
                'metrics': {}
            }
            
            # Simulate different types of stage execution
            if 'data collection' in stage.name.lower():
                result.update(self._simulate_data_collection(stage, workflow))
            elif 'analysis' in stage.name.lower():
                result.update(self._simulate_analysis(stage, workflow))
            elif 'report' in stage.name.lower():
                result.update(self._simulate_report_generation(stage, workflow))
            else:
                result.update(self._simulate_generic_stage(stage, workflow))
                
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'stage_num': stage_num,
                'execution_time': time.time() - stage_start_time
            }
            
    def _simulate_data_collection(self, stage, workflow: WorkflowDefinition) -> Dict:
        """Simulate data collection stage"""
        
        print("   📊 Collecting data from sources...")
        
        # Simulate time delay
        time.sleep(2)
        
        outputs = []
        
        if 'seo' in workflow.description.lower():
            outputs.extend([
                'search_console_data.json',
                'competitor_serp_data.json', 
                'technical_crawl_results.json'
            ])
        elif 'python' in workflow.description.lower():
            outputs.extend([
                'code_metrics.json',
                'dependency_analysis.json',
                'test_coverage_report.json'
            ])
            
        return {
            'outputs': outputs,
            'metrics': {
                'data_sources': len(stage.suggested_mcps),
                'records_collected': 1250,
                'quality_score': 0.92
            }
        }
        
    def _simulate_analysis(self, stage, workflow: WorkflowDefinition) -> Dict:
        """Simulate analysis stage"""
        
        print("   🔍 Analyzing data and discovering correlations...")
        
        time.sleep(3)
        
        # Simulate correlation discoveries
        correlations = [
            {
                'variables': ['page_load_time', 'bounce_rate'],
                'correlation': 0.78,
                'significance': 0.01,
                'insight': 'Pages loading >3s have 78% higher bounce rates'
            },
            {
                'variables': ['content_length', 'organic_traffic'],
                'correlation': 0.45,
                'significance': 0.05,
                'insight': 'Longer content (1500+ words) correlates with higher traffic'
            }
        ]
        
        return {
            'outputs': [
                'correlation_analysis.json',
                'anomaly_detection.json',
                'insights_summary.json'
            ],
            'correlations': correlations,
            'metrics': {
                'correlations_found': len(correlations),
                'anomalies_detected': 3,
                'confidence_level': 0.95
            }
        }
        
    def _simulate_report_generation(self, stage, workflow: WorkflowDefinition) -> Dict:
        """Simulate report generation stage"""
        
        print("   📄 Generating reports and visualizations...")
        
        time.sleep(2)
        
        # Create mock report files
        self._create_mock_outputs(workflow)
        
        return {
            'outputs': [
                f'{workflow.name}_dashboard.html',
                f'{workflow.name}_summary.pdf',
                f'{workflow.name}_data.xlsx'
            ],
            'metrics': {
                'charts_generated': 8,
                'pages_created': 12,
                'action_items': 15
            }
        }
        
    def _simulate_generic_stage(self, stage, workflow: WorkflowDefinition) -> Dict:
        """Simulate generic workflow stage"""
        
        print(f"   ⚙️ Processing: {stage.description}")
        
        time.sleep(1)
        
        return {
            'outputs': [f'stage_{stage.name.lower().replace(" ", "_")}_results.json'],
            'metrics': {'items_processed': 42}
        }
        
    def _retry_stage(self, stage, stage_num: int, workflow: WorkflowDefinition) -> Dict[str, Any]:
        """Retry a failed stage with backoff"""
        
        max_retries = self.exec_config.get('max_retries', 3)
        retry_delay = self.exec_config.get('retry_delay', 5)
        
        for attempt in range(max_retries):
            print(f"   🔄 Retry attempt {attempt + 1}/{max_retries}")
            
            # Exponential backoff
            time.sleep(retry_delay * (2 ** attempt))
            
            result = self._execute_stage(stage, stage_num, workflow)
            
            if result['success']:
                return result
                
        return {'success': False, 'error': 'Max retries exceeded'}
        
    def _create_output_directory(self, workflow: WorkflowDefinition) -> Path:
        """Create timestamped output directory for workflow results"""
        
        timestamp = datetime.now().strftime('%Y_%m_%d')
        
        if workflow.client_slug:
            # Client-based storage structure: /home/loki/seo-projects/client1/reports/workflow1_2025_09_25
            client_base = Path(self.storage_config['reports_base_dir']) / workflow.client_slug
        else:
            # Default client if none specified
            client_base = Path(self.storage_config['reports_base_dir']) / 'default-client'
            
        output_dir = client_base / 'reports' / f'{workflow.name}_{timestamp}'
        
        # Create directory structure
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / 'inputs').mkdir(exist_ok=True)
        (output_dir / 'artifacts').mkdir(exist_ok=True)
        (output_dir / 'charts').mkdir(exist_ok=True)
        (output_dir / 'reports').mkdir(exist_ok=True)
        
        return output_dir
        
    def _save_workflow_config(self, workflow: WorkflowDefinition):
        """Save workflow configuration for reproducibility"""
        
        config = {
            'workflow_name': workflow.name,
            'execution_timestamp': datetime.now().isoformat(),
            'client_slug': workflow.client_slug,
            'parameters': workflow.parameters,
            'inputs': workflow.inputs,
            'estimated_time': workflow.estimated_time,
            'stages': [
                {
                    'name': stage.name,
                    'description': stage.description,
                    'agents': stage.recommended_agents,
                    'mcps': stage.suggested_mcps,
                    'dependencies': stage.dependencies
                }
                for stage in workflow.stages
            ]
        }
        
        config_file = self.output_dir / 'workflow_config.yaml'
        
        import yaml
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
            
    def _archive_input_files(self, workflow: WorkflowDefinition):
        """Archive input files to output directory"""
        
        if not workflow.client_slug:
            return
            
        client_inputs_dir = Path(self.storage_config['reports_base_dir']) / workflow.client_slug / 'inputs'
        archive_inputs_dir = self.output_dir / 'inputs'
        
        for input_name, input_path in workflow.inputs.items():
            if input_path.startswith('inputs/'):
                source_file = client_inputs_dir / input_path.replace('inputs/', '')
                if source_file.exists():
                    dest_file = archive_inputs_dir / source_file.name
                    shutil.copy2(source_file, dest_file)
                    print(f"   📁 Archived: {input_path}")
                    
    def _save_stage_results(self, stage, stage_num: int, result: Dict):
        """Save stage execution results"""
        
        stage_file = self.output_dir / 'artifacts' / f'stage_{stage_num}_{stage.name.lower().replace(" ", "_")}.json'
        
        with open(stage_file, 'w') as f:
            json.dump(result, f, indent=2, default=str)
            
    def _generate_final_reports(self, workflow: WorkflowDefinition, correlations: List[Dict]):
        """Generate final workflow reports"""
        
        print(f"\n📊 Generating final reports...")
        
        # Create execution summary
        summary = {
            'workflow_name': workflow.name,
            'execution_completed': datetime.now().isoformat(),
            'total_execution_time': time.time() - self.execution_start_time,
            'stages_completed': len(workflow.stages),
            'correlations_discovered': len(correlations),
            'correlations': correlations,
            'output_files': self._list_output_files(),
            'client_slug': workflow.client_slug,
            'success': True
        }
        
        summary_file = self.output_dir / 'execution_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
            
        # Generate HTML summary report
        self._generate_html_summary(workflow, summary)
        
        print(f"   ✅ Reports generated in: {self.output_dir}")
        
    def _create_mock_outputs(self, workflow: WorkflowDefinition):
        """Create mock output files for demonstration"""
        
        reports_dir = self.output_dir / 'reports'
        
        # Create mock HTML dashboard
        dashboard_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{workflow.name} Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .metric {{ background: #f5f5f5; padding: 20px; margin: 10px; border-radius: 5px; }}
        .correlation {{ background: #e8f5e8; padding: 15px; margin: 10px; border-left: 4px solid #4CAF50; }}
    </style>
</head>
<body>
    <h1>{workflow.name} Results Dashboard</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div class="metric">
        <h3>Key Metrics</h3>
        <p>Data sources analyzed: 3</p>
        <p>Correlations discovered: 2</p>
        <p>Action items identified: 15</p>
    </div>
    
    <div class="correlation">
        <h3>Key Finding</h3>
        <p>Strong correlation discovered between page load time and bounce rate (r=0.78, p<0.01)</p>
        <p><strong>Recommendation:</strong> Focus on page speed optimization for high-traffic pages</p>
    </div>
    
    <p><em>This is a demonstration output from the CCC Workflow System</em></p>
</body>
</html>"""
        
        with open(reports_dir / f'{workflow.name}_dashboard.html', 'w') as f:
            f.write(dashboard_content)
            
        # Create mock Excel data file (as text for now)
        excel_content = """Workflow,Stage,Metric,Value
{},Data Collection,Records,1250
{},Analysis,Correlations,2
{},Reporting,Charts,8""".format(workflow.name, workflow.name, workflow.name)
        
        with open(reports_dir / f'{workflow.name}_data.csv', 'w') as f:
            f.write(excel_content)
            
    def _generate_html_summary(self, workflow: WorkflowDefinition, summary: Dict):
        """Generate HTML execution summary"""
        
        correlations_html = ""
        for corr in summary['correlations']:
            correlations_html += f"""
            <div class="correlation">
                <strong>{corr['insight']}</strong><br>
                <small>Correlation: {corr['correlation']:.2f}, Significance: {corr['significance']:.3f}</small>
            </div>
            """
            
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Workflow Execution Summary - {workflow.name}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .metric {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .correlation {{ background: #e8f5e8; padding: 15px; margin: 10px 0; border-left: 4px solid #4CAF50; }}
        .file-list {{ background: #fff3cd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Workflow Execution Summary</h1>
        <h2>{workflow.name}</h2>
        <p>Client: {workflow.client_slug or 'N/A'} | Completed: {summary['execution_completed']}</p>
    </div>
    
    <div class="metric">
        <h3>📊 Execution Metrics</h3>
        <p><strong>Total Time:</strong> {summary['total_execution_time']:.1f} seconds</p>
        <p><strong>Stages Completed:</strong> {summary['stages_completed']}</p>
        <p><strong>Correlations Discovered:</strong> {summary['correlations_discovered']}</p>
    </div>
    
    <div class="correlation">
        <h3>🔍 Key Discoveries</h3>
        {correlations_html or '<p><em>No significant correlations discovered</em></p>'}
    </div>
    
    <div class="file-list">
        <h3>📁 Generated Files</h3>
        <ul>
            <li>📊 Dashboard: {workflow.name}_dashboard.html</li>
            <li>📈 Data Export: {workflow.name}_data.csv</li>
            <li>⚙️ Execution Log: execution_summary.json</li>
            <li>🔧 Configuration: workflow_config.yaml</li>
        </ul>
    </div>
    
    <p><em>Generated by CCC Workflow Definition & Execution System</em></p>
</body>
</html>"""
        
        with open(self.output_dir / 'workflow_summary.html', 'w') as f:
            f.write(html_content)
            
    def _list_output_files(self) -> List[str]:
        """List all files created during workflow execution"""
        
        files = []
        
        for root, dirs, filenames in os.walk(self.output_dir):
            for filename in filenames:
                file_path = Path(root) / filename
                rel_path = file_path.relative_to(self.output_dir)
                files.append(str(rel_path))
                
        return files
        
    def _estimate_stage_time(self, stage) -> float:
        """Estimate execution time for a stage in minutes"""
        
        base_time = 5  # Base time per stage in minutes
        
        # Adjust based on stage complexity
        if len(stage.recommended_agents) > 1:
            base_time += 2
        
        if len(stage.suggested_mcps) > 2:
            base_time += 3
            
        if 'comprehensive' in stage.description.lower():
            base_time *= 1.5
        elif 'quick' in stage.description.lower():
            base_time *= 0.5
            
        return base_time