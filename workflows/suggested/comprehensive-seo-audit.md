# Comprehensive SEO Technical Audit Workflow

## Workflow Metadata
- **Type**: seo
- **Complexity**: advanced
- **Duration**: 2-4 hours
- **Agents**: 4 specialized agents with orchestrated handoffs
- **MCPs**: firecrawl, dataforseo, chart-mcp
- **Parallelization**: Stage 1-2 concurrent execution

## Agent Orchestration Plan

### 🏗️ SystemArchitectAgent (Coordinator)
**Role**: Workflow orchestration, quality gates, final integration
**Duration**: Full workflow supervision
**Handoffs**: 
- → TechnicalSEOAgent (Stage 1: Technical Analysis)
- → BenchmarkResearchAgent (Stage 2: Competitive Intelligence) 
- ← Integration and final reporting

### 🔧 TechnicalSEOAgent (Primary Executor)
**Role**: Site crawling, technical issue identification, performance analysis
**Duration**: Stages 1, 3, 4 (70% of workflow)
**Tools**: firecrawl, lighthouse analysis, schema validation
**Handoffs**:
- Parallel execution with BenchmarkResearchAgent in Stage 2
- → PerformanceProfilerAgent for Core Web Vitals deep dive
- → MetricsReporterAgent for dashboard generation

### 🔍 BenchmarkResearchAgent (Competitive Intelligence)
**Role**: SERP analysis, competitor crawling, market positioning
**Duration**: Stage 2 (parallel with TechnicalSEOAgent)
**Tools**: dataforseo, competitive analysis algorithms
**Handoffs**: 
- ← Receives target data from TechnicalSEOAgent
- → Provides competitor data to MetricsReporterAgent

### ⚡ PerformanceProfilerAgent (Performance Specialist)
**Role**: Core Web Vitals analysis, performance bottleneck identification
**Duration**: Stage 4 focused execution
**Tools**: Performance monitoring, correlation analysis
**Handoffs**:
- ← Receives site data from TechnicalSEOAgent
- → Provides performance insights to MetricsReporterAgent

### 📊 MetricsReporterAgent (Reporting & Visualization)
**Role**: Dashboard creation, data visualization, executive summary
**Duration**: Stage 5 (after data collection complete)
**Tools**: chart-mcp, reporting templates, Excel generation
**Handoffs**:
- ← Receives data from all specialized agents
- → Returns final deliverables to SystemArchitectAgent

## Execution Stages

### Stage 1: Site Discovery & Technical Crawling (TechnicalSEOAgent)
```yaml
agent: TechnicalSEOAgent
duration: 30-45 minutes
parallel: false
tools:
  - firecrawl_crawl:
      url: "{{TARGET_URL}}"
      maxDepth: "{{CRAWL_DEPTH}}"
      allowExternalLinks: false
  - lighthouse_analysis:
      pages: top_20_from_crawl
      device: "{{DEVICE}}"
success_criteria:
  - crawl_completion_rate: ">95%"
  - lighthouse_scores: "collected_for_top_pages"
  - technical_issues: "categorized_by_severity"
outputs:
  - artifacts/crawl_results.json
  - artifacts/lighthouse_scores.json  
  - artifacts/technical_issues.csv
handoff_trigger: "crawl_data_ready"
```

### Stage 2: Competitive Intelligence (BenchmarkResearchAgent) [PARALLEL]
```yaml
agent: BenchmarkResearchAgent
duration: 25-40 minutes
parallel: true  # Runs concurrent with Stage 1
tools:
  - dataforseo_serp_analysis:
      keyword: "{{MAIN_KEYWORD}}"
      location: "{{LOCALE}}"
      device: "{{DEVICE}}"
  - firecrawl_competitor_crawling:
      urls: top_competitors_from_serp
      depth: 2
success_criteria:
  - serp_data: "top_10_results_collected"
  - competitor_crawl: "{{COMPETITOR_COUNT}}_sites_analyzed"
  - competitive_gaps: "identified_and_prioritized"
outputs:
  - artifacts/serp_competitors.csv
  - artifacts/competitor_analysis.json
  - artifacts/competitive_gaps.json
handoff_trigger: "competitive_analysis_complete"
```

### Stage 3: Keyword & Content Strategy (TechnicalSEOAgent)
```yaml
agent: TechnicalSEOAgent  
duration: 20-30 minutes
parallel: false
dependencies: [stage_1_complete]
tools:
  - dataforseo_keyword_research:
      seed_keyword: "{{MAIN_KEYWORD}}"
      site_analysis: "{{TARGET_URL}}"
  - content_gap_analysis:
      target_content: from_crawl_results
      competitor_content: from_stage_2
success_criteria:
  - keyword_opportunities: ">100_researched_terms"
  - content_gaps: "themes_identified_with_volume_data"
  - keyword_difficulty: "assessed_for_opportunity_terms"
outputs:
  - artifacts/keyword_opportunities.csv
  - artifacts/content_gaps.json
  - artifacts/keyword_strategy.xlsx
handoff_trigger: "content_strategy_ready"
```

### Stage 4: Performance Deep Dive (PerformanceProfilerAgent)
```yaml
agent: PerformanceProfilerAgent
duration: 15-25 minutes
parallel: false
dependencies: [stage_1_complete]
tools:
  - core_web_vitals_analysis:
      source: lighthouse_scores
      device_breakdown: true
  - performance_correlation:
      metrics: [load_time, organic_traffic, rankings]
  - bottleneck_identification:
      focus: [images, scripts, server_response]
success_criteria:
  - cwv_baseline: "established_for_all_page_types"
  - performance_issues: "prioritized_by_impact"
  - correlation_analysis: "traffic_vs_performance"
outputs:
  - artifacts/performance_baseline.csv
  - artifacts/cwv_analysis.json
  - artifacts/performance_issues.csv
handoff_trigger: "performance_analysis_complete"
```

### Stage 5: Reporting & Deliverables (MetricsReporterAgent)
```yaml
agent: MetricsReporterAgent
duration: 20-30 minutes
parallel: false
dependencies: [all_previous_stages_complete]
tools:
  - chart_mcp:
      types: [heatmap, comparison_charts, opportunity_matrix]
  - dashboard_generation:
      template: seo_audit_dashboard
  - excel_export:
      sheets: [issues, keywords, performance, competitors]
success_criteria:
  - dashboard: "interactive_html_with_charts"
  - executive_summary: "top_10_issues_prioritized"
  - implementation_roadmap: "6_week_plan_with_owners"
outputs:
  - reports/seo_audit_dashboard.html
  - reports/executive_summary.pdf
  - exports/technical_issues.xlsx
  - exports/keyword_strategy.xlsx
  - exports/performance_baseline.csv
  - reports/optimization_roadmap.md
handoff_trigger: "deliverables_complete"
```

## Input Parameters

### Required Variables
```yaml
TARGET_URL:
  description: "Primary website to audit"
  type: string
  validation: "valid_url"
  example: "https://example.com"

MAIN_KEYWORD:
  description: "Primary target keyword for competitive analysis"
  type: string
  validation: "non_empty"
  example: "digital marketing services"
```

### Optional Variables (with defaults)
```yaml
DEVICE:
  description: "Device type for analysis"
  type: enum
  options: [mobile, desktop, both]
  default: "both"

LOCALE:
  description: "Country code for SERP analysis"
  type: string
  default: "US"
  validation: "iso_country_code"

CRAWL_DEPTH:
  description: "Site crawling depth"
  type: enum
  options: [quick, standard, comprehensive]
  default: "standard"
  mapping:
    quick: 2
    standard: 4
    comprehensive: 8

COMPETITOR_COUNT:
  description: "Number of top competitors to analyze"
  type: integer
  default: 5
  range: [3, 10]
```

## MCP Integration & Fallbacks

### Primary MCP Stack
```yaml
firecrawl:
  purpose: "Site crawling and competitor analysis"
  fallback: "manual_sitemap_parsing + lighthouse_cli"
  
dataforseo:
  purpose: "SERP analysis and keyword research"
  fallback: "google_search_console + manual_serp_analysis"
  
chart-mcp:
  purpose: "Data visualization and reporting"
  fallback: "matplotlib_static_charts"
```

### Error Handling Strategy
```yaml
crawl_failures:
  action: "retry_with_reduced_depth"
  max_retries: 3
  
api_rate_limits:
  action: "exponential_backoff"
  max_wait: "300_seconds"
  
mcp_unavailable:
  action: "switch_to_fallback_method"
  notify_user: true
```

## Quality Gates & Success Validation

### Stage Completion Criteria
1. **Technical Analysis**: 95%+ page crawl success, technical issues categorized
2. **Competitive Intelligence**: Top competitors identified and analyzed
3. **Content Strategy**: 100+ keyword opportunities with difficulty scores
4. **Performance Analysis**: Core Web Vitals baseline established
5. **Reporting**: Interactive dashboard and actionable roadmap generated

### Final Deliverable Validation
```yaml
completeness_check:
  - all_artifacts_generated: true
  - dashboard_functional: true
  - issues_prioritized: true
  - roadmap_actionable: true

quality_assurance:
  - data_accuracy: "spot_check_10_sample_issues"
  - chart_readability: "visual_validation"
  - recommendation_feasibility: "technical_review"
```

## Estimated Resource Requirements
- **Duration**: 2-4 hours depending on site size and complexity
- **API Calls**: ~500-1000 (DataForSEO), ~50-100 (Firecrawl)
- **Storage**: 100-500MB for artifacts and reports
- **Compute**: Moderate (parallel processing reduces total time)

## Success Metrics & KPIs
- **Technical Issues Identified**: Target 20+ actionable improvements
- **Keyword Opportunities**: Target 100+ researched terms with volume data
- **Competitive Insights**: Top 5 competitor analysis with gap identification  
- **Performance Baseline**: Core Web Vitals scores for all major page types
- **Actionable Roadmap**: 6-week implementation plan with clear owners and metrics

---

*Generated by CCC Intelligent Workflow System*  
*Agent Orchestration Pattern: Lead-SubAgent with Parallel Processing*  
*Compatible with: Claude Code slash commands and autonomous execution*