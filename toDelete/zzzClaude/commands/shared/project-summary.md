# /project-summary

**Purpose**  
Generate comprehensive project summary with architecture analysis, progress tracking, and recommendations.

**Tags**: analysis, documentation, architecture, project-management, reporting

**Arguments**
- `depth` (optional): Analysis depth - quick, standard, detailed (default: standard)
- `include_metrics` (optional): Include performance and quality metrics - true/false (default: true)
- `output_format` (optional): Output format - markdown, html, json (default: markdown)

**Usage Example**
```
/project-summary depth=detailed include_metrics=true output_format=html
```

**MCPs Used**
- sequential-thinking: Analysis planning
- chart-mcp: Metrics visualization

**Output**
Comprehensive project analysis report with architecture overview, progress summary, and actionable recommendations.

---

## Arguments

- Provide arguments inline as `key=value` pairs.
- Booleans: `true`/`false`. Lists: comma‑separated (no spaces) unless noted.

depth (optional): Analysis depth level - quick,standard,detailed (default: standard)
include_metrics (boolean, default: true): Include performance and quality metrics
output_format (optional): Report format - markdown,html,json (default: markdown)
focus_areas (optional): Specific areas to analyze - architecture,code,tests,docs,performance
include_todos (boolean, default: true): Include current todos and task analysis
generate_charts (boolean, default: true): Create visual charts for metrics

---

## Runbook

### Phase 1: Project Discovery
1. **Codebase Analysis**:
   - Identify project type and technologies
   - Analyze directory structure and organization
   - Count files, lines of code, and complexity metrics
   - Identify main entry points and critical paths

2. **Configuration Assessment**:
   - Review configuration files and settings
   - Analyze dependencies and versions
   - Check for environment-specific configs
   - Identify potential configuration issues

### Phase 2: Architecture Analysis
1. **Code Structure Review**:
   - Analyze module organization and separation of concerns
   - Identify design patterns and architectural decisions
   - Review database schema and data models
   - Assess API design and integration points

2. **Quality Assessment**:
   - Code quality metrics (complexity, duplication)
   - Test coverage and test quality analysis
   - Documentation coverage and quality
   - Security considerations review

### Phase 3: Progress and Status Analysis
1. **Development Status**:
   - Feature completion analysis
   - Current todos and task breakdown
   - Recent changes and development velocity
   - Milestone progress tracking

2. **Technical Debt Assessment**:
   - Code debt identification
   - Performance bottlenecks
   - Maintenance burden analysis
   - Refactoring opportunities

### Phase 4: Metrics and Visualization
1. **Quantitative Analysis**:
   - Lines of code by language/module
   - Complexity distribution
   - Test coverage percentages
   - Performance benchmarks

2. **Visual Reporting**:
   - Architecture diagrams
   - Metrics charts and graphs
   - Progress visualization
   - Trend analysis

### Phase 5: Recommendations and Action Items
1. **Priority Recommendations**:
   - Critical issues requiring immediate attention
   - Performance optimization opportunities
   - Code quality improvements
   - Architecture enhancements

2. **Implementation Roadmap**:
   - Short-term action items (next sprint)
   - Medium-term improvements (next quarter)
   - Long-term strategic initiatives
   - Resource requirements and timeline estimates

## Report Sections

### Executive Summary
- Project overview and current status
- Key achievements and milestones
- Critical issues and blockers
- Overall health score

### Technical Overview
- Technology stack and architecture
- Key components and their relationships
- Data flow and integration points
- Security and performance considerations

### Code Quality Analysis
- Code organization and structure
- Quality metrics and trends
- Test coverage and effectiveness
- Documentation completeness

### Progress Tracking
- Feature development status
- Todo/task completion rates
- Recent achievements
- Upcoming milestones

### Performance Metrics
- Application performance benchmarks
- Resource utilization analysis
- Scalability considerations
- Optimization opportunities

### Recommendations
- Immediate action items
- Strategic improvements
- Best practices implementation
- Tool and process enhancements

## Output Templates

### Quick Analysis (5-minute overview)
- Project type and technology stack
- Directory structure overview
- Basic metrics (files, LOC, tests)
- Top 3 recommendations

### Standard Analysis (15-minute deep dive)
- Complete architecture analysis
- Quality metrics with visualization
- Progress tracking and todos
- Prioritized recommendations

### Detailed Analysis (comprehensive report)
- In-depth code analysis
- Performance profiling
- Security assessment
- Complete implementation roadmap

## Error Handling

- Handle missing files or directories gracefully
- Provide meaningful analysis even with incomplete information
- Include confidence levels for recommendations
- Offer alternative analysis approaches when tools are unavailable

## Notes

- Analysis adapts to project type (Python, WordPress, SEO, etc.)
- Uses appropriate tools and metrics for each technology stack
- Provides actionable insights rather than just raw data
- Includes visual elements to make reports more digestible
- Supports multiple output formats for different audiences
- Can be run regularly to track progress over time
- Integrates with existing project management workflows