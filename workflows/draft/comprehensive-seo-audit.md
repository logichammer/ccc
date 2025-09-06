# Comprehensive SEO Technical Audit

## Goal
Full technical SEO audit for {{TARGET_URL}} on {{DEVICE}} in {{LOCALE}} with crawl depth {{CRAWL_DEPTH}}.
Compare against competitors and generate actionable optimization roadmap.

## Variables
- TARGET_URL: The primary website to audit (required)
- DEVICE: mobile | desktop | both (default: both)
- LOCALE: Country code for SERP analysis (default: US)
- CRAWL_DEPTH: quick | standard | comprehensive (default: standard)
- MAIN_KEYWORD: Primary target keyword for competitive analysis (required)
- COMPETITOR_COUNT: Number of top competitors to analyze (default: 5)

## Input Requirements
### Required Data Sources
- **Crawl Access**: Full site crawl permissions for TARGET_URL
- **Search Console**: GSC access for TARGET_URL (if available)
- **SERP Access**: API access for competitor research

### Expected Input Files (Optional)
- `inputs/target_keywords.csv` - Priority keywords list (columns: keyword, search_volume, priority)
- `inputs/competitors.txt` - Known competitor URLs (one per line)
- `inputs/gsc_pages.csv` - GSC page performance data (if manual export)

## Data Processing Pipeline

### Stage 1: Site Discovery & Crawling
1. **Firecrawl**: Deep crawl TARGET_URL with depth=CRAWL_DEPTH
   - Output: `artifacts/crawl_results.json`
   - Extract: URLs, status codes, page titles, meta descriptions, schema markup
   - Filter: Remove non-indexable pages, focus on content pages

2. **Lighthouse**: Performance audit on top 20 pages from crawl
   - Output: `artifacts/lighthouse_scores.json`
   - Metrics: Core Web Vitals, accessibility, SEO scores
   - Generate: `artifacts/cwv_summary.csv`

### Stage 2: Competitive Intelligence
3. **DataForSEO SERP Analysis**:
   - Query: `serp_google_organic_live(MAIN_KEYWORD, LOCALE)`
   - Output: `artifacts/serp_competitors.csv`
   - Extract: Top 10 organic results, titles, descriptions, URLs

4. **Competitor Crawling**:
   - Crawl top COMPETITOR_COUNT sites from SERP results
   - Output: `artifacts/competitor_analysis.json`
   - Compare: Page structure, content length, schema usage

### Stage 3: Keyword & Content Analysis
5. **Keyword Expansion**:
   - DataForSEO: `keywords_google_ads_keywords_for_site(TARGET_URL)`
   - DataForSEO: `labs_google_related_keywords(MAIN_KEYWORD)`
   - Output: `artifacts/keyword_opportunities.csv`
   - Columns: keyword, volume, kd_score, cpc, competition

6. **Content Gap Analysis**:
   - Compare TARGET_URL content themes vs competitors
   - Identify missing topic clusters
   - Output: `artifacts/content_gaps.json`

### Stage 4: Technical Analysis
7. **Schema & Structure Analysis**:
   - Parse structured data from crawl results
   - Validate schema markup completeness
   - Output: `artifacts/schema_report.md`

8. **Page Speed & Performance**:
   - Cross-reference Lighthouse + PageSpeed Insights
   - Identify performance bottlenecks
   - Output: `artifacts/performance_issues.csv`

## Expected Outputs

### Primary Deliverables
- **Technical Audit Dashboard** (`reports/seo_audit_dashboard.html`)
  - Core Web Vitals performance matrix
  - Technical issue priority heatmap  
  - Competitor comparison charts
  - Keyword opportunity visualization

- **Executive Summary** (`reports/executive_summary.pdf`)
  - Top 10 critical issues with impact scores
  - Competitor positioning analysis
  - ROI-prioritized recommendations

### Data Exports
- **Issue Tracking** (`exports/technical_issues.xlsx`)
  - Columns: url, issue_type, severity, impact_score, fix_effort, owner
  - Tabs: Critical, High, Medium, Low priority issues

- **Keyword Strategy** (`exports/keyword_strategy.xlsx`) 
  - Opportunity keywords with volume, difficulty, current ranking
  - Content gap themes with search volume potential
  - Competitor keyword overlaps and gaps

- **Performance Baseline** (`exports/performance_baseline.csv`)
  - Current Core Web Vitals scores by page type
  - Competitor performance benchmarks
  - Mobile vs desktop performance gaps

### Implementation Roadmap
- **6-Week Optimization Plan** (`reports/optimization_roadmap.md`)
  - Week-by-week implementation sequence
  - Resource requirements and owners per task
  - Success metrics and tracking plan

## Success Criteria
- Complete site crawl with >95% successful page analysis
- Competitive analysis of top 5 SERP competitors  
- Identification of 20+ actionable technical improvements
- Performance baseline established for all Core Web Vitals
- Keyword opportunity list with 100+ researched terms
- Clear ROI prioritization for all recommendations

## Correlation Discovery Targets
- Page load time vs organic traffic correlation
- Schema markup completeness vs SERP ranking position
- Content length vs engagement metrics  
- Mobile performance vs mobile organic visibility
- Internal linking density vs page authority scores