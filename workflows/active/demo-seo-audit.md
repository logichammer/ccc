# demo-seo-audit

## Description
Comprehensive workflow generated from user requirements

## Goal
I need to perform a quick SEO technical audit for a client's website to identify key improvement opportunities.

## Context
- Small business e-commerce website
- Client wants to improve organic search rankings
- I have access to Google Search Console data
- Need results within 2 hours for client presentation

## Interview Configuration
Generated on: 2025-09-05 10:52:37
Client: acme-corp
Project Type: seo
Timeline: standard

## Parameters
- client_slug: acme-corp (required)
- timeline: standard (quality vs speed preference)
- output_formats: ['html']
- detail_level: standard
- parallelization: conservative
- error_handling: retry

## Input Files
- competitor.urls.txt: inputs/competitor_urls.txt (List of competitor websites to analyze)

## Stages

### Stage 1: Data Collection
**Description**: Gather SEO data from multiple sources
**Dependencies**: None
**Recommended Agents**: 
- DatabaseOptimizerAgent
**Suggested MCPs**: 
- firecrawl
- firecrawl-mcp
**Success Criteria**:
- Search data retrieved
- Site crawl completed
- Competitor data collected
**Expected Outputs**: search_data.json, crawl_results.json, competitor_analysis.json

### Stage 2: Analysis & Correlation Discovery
**Description**: Analyze data and discover unexpected correlations
**Dependencies**: Stage 1
**Recommended Agents**: 
- DataPipelineAgent
- DatabaseOptimizerAgent
**Suggested MCPs**: 
- data-explorer-mcp
- chart-mcp
**Success Criteria**:
- Statistical analysis completed
- Correlations identified
- Anomalies flagged
**Expected Outputs**: correlation_analysis.json, insights_summary.json

### Stage 3: Report Generation
**Description**: Generate comprehensive reports and visualizations
**Dependencies**: Stage 2
**Recommended Agents**: 
- MetricsReporterAgent
**Suggested MCPs**: 
- chart-mcp
**Success Criteria**:
- Reports generated
- Visualizations created
- Action items prioritized
**Expected Outputs**: seo_dashboard.html, executive_summary.pdf, recommendations.xlsx

## Parallelization Analysis
**Strategy**: conservative

**SAFE Parallelization Opportunities**:
- Stage 1 can run independently
- Stage 2: Multiple agents (DataPipelineAgent, DatabaseOptimizerAgent) can work on different aspects
- Stage 2: Multiple MCPs (data-explorer-mcp, chart-mcp) access different data sources

**POTENTIAL CONFLICTS**:
- DatabaseOptimizerAgent needed by both Stage 1 and Stage 2
- chart-mcp might have rate limits affecting Stage 2 and Stage 3

**RECOMMENDATIONS**:
- Execute stages sequentially to ensure stability
- Only parallelize within-stage tasks that use different resources

## Expected Outputs
- **Primary Report**: Interactive standard-level report
- **Data Export**: html formats
- **Analysis Files**: Correlation analysis and insights
- **Raw Data**: Included

## Estimated Execution Time
60-90 minutes

## Configuration File
This workflow will generate a configuration file at:
`/workflows/configs/demo-seo-audit.yaml`

## Next Steps
1. Review this suggested workflow
2. Edit stages, agents, or parameters as needed  
3. Validate technical feasibility: `workflow-system validate demo-seo-audit`
4. Execute: `workflow-system execute demo-seo-audit`
