---
name: keyword-research
description: Comprehensive keyword research and analysis using multiple data sources
category: seo
tags: ["seo", "keywords", "research", "serp-analysis", "competition", "strategy"]
version: 1.0
---

# /keyword-research

**Purpose**  
Comprehensive keyword research and analysis using multiple data sources for SEO strategy development.

**Tags**: seo, keywords, research, serp-analysis, competition, strategy

**Arguments**
- `seed_keywords` (required): Initial keywords to expand from (comma-separated)
- `target_location` (optional): Geographic target - country code (default: US)
- `language` (optional): Target language code (default: en)
- `search_volume_min` (optional): Minimum monthly search volume (default: 100)

**Usage Example**
```
/keyword-research seed_keywords="digital marketing,seo services" target_location=US search_volume_min=500
```

**MCPs Used**
- dataforseo: Keyword data and search volumes
- perplexity-ask: Trend research and context
- chart-mcp: Keyword visualization and analysis
- firecrawl: Competitor keyword analysis

**Output**
Comprehensive keyword research report with search volumes, difficulty scores, and strategic recommendations.

---

## Arguments

- Provide arguments inline as `key=value` pairs.
- Booleans: `true`/`false`. Lists: comma‑separated (no spaces) unless noted.

seed_keywords (required): Starting keywords for expansion
target_location (optional): Geographic targeting - US,GB,CA,AU,etc (default: US)
language (optional): Language code - en,es,fr,de,etc (default: en)
search_volume_min (number, default: 100): Minimum monthly search volume threshold
difficulty_max (number, default: 70): Maximum keyword difficulty score
include_questions (boolean, default: true): Include question-based keywords
include_longtail (boolean, default: true): Include long-tail keyword variations
competitor_analysis (boolean, default: true): Analyze competitor keywords
serp_analysis (boolean, default: true): Analyze SERP features and competition

---

## Runbook

### Phase 1: Seed Keyword Expansion
1. **Initial Keyword Processing**:
   - Parse and clean seed keywords
   - Generate keyword variations and synonyms
   - Create semantic keyword groups
   - Build keyword taxonomy structure

2. **Keyword Discovery Methods**:
   - Autocomplete suggestions from search engines
   - Related searches and "People also ask"
   - Competitor keyword harvesting
   - Topic modeling for semantic expansion

3. **Question-Based Keywords**:
   - Generate who, what, when, where, why, how questions
   - Find "People also ask" opportunities
   - Identify informational search intent
   - Map questions to funnel stages

### Phase 2: Data Collection and Enrichment
1. **Search Volume and Trends**:
   ```python
   def get_keyword_metrics(keywords, location="US"):
       # Use DataForSEO API for accurate search volumes
       metrics = {}
       for keyword in keywords:
           data = dataforseo_keyword_data(
               keyword=keyword,
               location=location,
               language="en"
           )
           metrics[keyword] = {
               'search_volume': data.search_volume,
               'cpc': data.cpc,
               'competition': data.competition,
               'trend': data.trend_data
           }
       return metrics
   ```

2. **Keyword Difficulty Analysis**:
   - SERP analysis for top 10 results
   - Domain authority of ranking pages
   - Content quality assessment
   - Backlink profile analysis

3. **Search Intent Classification**:
   - Informational: Research and learning
   - Navigational: Brand and specific site searches
   - Commercial: Product research and comparison
   - Transactional: Purchase-ready keywords

### Phase 3: Competitor Keyword Analysis
1. **Competitor Identification**:
   - Find organic search competitors
   - Identify content competitors
   - Analyze paid search competitors
   - Map competitor keyword strategies

2. **Keyword Gap Analysis**:
   - Keywords competitors rank for but you don't
   - Keywords where you could outrank competitors
   - Untapped keyword opportunities
   - Seasonal keyword patterns

3. **Competitor Content Analysis**:
   - Content types ranking for target keywords
   - Content length and depth analysis
   - Content freshness and update frequency
   - User engagement signals

### Phase 4: SERP Feature Analysis
1. **Feature Detection**:
   - Featured snippets opportunities
   - "People also ask" boxes
   - Image and video results
   - Local pack presence
   - Shopping results

2. **Optimization Opportunities**:
   - Featured snippet optimization potential
   - Image SEO opportunities
   - Video content gaps
   - Local SEO potential

### Phase 5: Strategic Keyword Prioritization
1. **Scoring Algorithm**:
   ```python
   def calculate_keyword_priority(keyword_data):
       # Priority = (Search Volume * Intent Score * Relevance) / (Difficulty * Competition + 1)
       search_volume = keyword_data['search_volume']
       difficulty = keyword_data['difficulty']
       intent_score = map_intent_to_score(keyword_data['intent'])
       relevance = calculate_relevance_score(keyword_data)
       
       priority_score = (search_volume * intent_score * relevance) / (difficulty + 1)
       return priority_score
   ```

2. **Categorization and Grouping**:
   - Primary keywords (high volume, brand relevant)
   - Secondary keywords (supporting content)
   - Long-tail keywords (specific, low competition)
   - Seasonal keywords (time-sensitive opportunities)

### Phase 6: Content Strategy Development
1. **Content Gap Identification**:
   - Keywords missing supporting content
   - Content types needed for keyword groups
   - User journey mapping for keywords
   - Content cluster opportunities

2. **Editorial Calendar Integration**:
   - Priority-based content scheduling
   - Seasonal keyword timing
   - Competitor content monitoring
   - Content update recommendations

## Keyword Research Deliverables

### Executive Summary
- Total keywords discovered
- High-priority opportunity count
- Estimated traffic potential
- Quick win recommendations

### Keyword Database
- Complete keyword list with metrics
- Search volume and difficulty scores
- Intent classification
- Priority rankings
- Competitive analysis

### Strategic Recommendations
1. **Immediate Opportunities (0-30 days)**:
   - Low-hanging fruit keywords
   - Content optimization targets
   - Technical SEO fixes

2. **Short-term Strategy (1-3 months)**:
   - Content creation priorities
   - Keyword clustering for topics
   - Competitor gap exploitation

3. **Long-term Strategy (3-12 months)**:
   - High-competition keyword targets
   - Authority building requirements
   - Seasonal content planning

### Visual Analysis
- Keyword difficulty vs search volume scatter plot
- Seasonal trend analysis charts
- Competitor keyword overlap heatmap
- Intent distribution pie charts
- Opportunity matrix visualization

## Advanced Analysis Features

### Semantic Keyword Clustering
- Group related keywords by topic
- Identify content hub opportunities
- Map keyword relationships
- Optimize for topic authority

### Trend and Seasonality Analysis
- Historical search volume patterns
- Seasonal opportunity identification
- Trend correlation analysis
- Future demand forecasting

### Local SEO Integration
- Location-based keyword variations
- Local search volume analysis
- "Near me" keyword opportunities
- Geographic competition assessment

## Error Handling

- Handle API rate limits gracefully
- Provide alternative data sources when primary fails
- Include confidence levels for search volume estimates
- Validate keyword data quality and freshness

## Notes

- Research includes both head terms and long-tail keywords
- Analysis considers search intent and user journey stages
- Results include actionable content creation guidance
- Data is exportable in multiple formats (CSV, Excel, JSON)
- Includes historical data for trend analysis
- Supports multiple languages and geographic targets
- Integrates with content management workflows