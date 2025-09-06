---
name: seo-audit
description: Perform a comprehensive technical SEO audit of a website
category: seo
tags: ["seo", "audit", "technical", "performance", "analysis"]
version: 1.0
---

# /seo-audit

**Purpose**  
Perform a comprehensive technical SEO audit of a website, analyzing technical and on-page factors.

**Tags**: seo, audit, technical, performance, analysis

**Arguments**
- `website_url` (required): The website URL to audit
- `pages` (optional): Comma-separated list of specific pages to audit
- `mobile_check` (optional): Enable mobile-specific analysis (default: true)

**Usage Example**
```
/seo-audit website_url=https://example.com pages=about,contact mobile_check=true
```

**MCPs Used**
- screenshot-website-fast: Visual verification and mobile testing
- firecrawl: Page crawling and content analysis
- chart-mcp: Performance visualization

**Output**
Comprehensive SEO audit report with actionable recommendations.

---

## Arguments

- Provide arguments inline as `key=value` pairs.
- Booleans: `true`/`false`. Lists: comma‑separated (no spaces) unless noted.

website_url (required): Target website for SEO audit
pages (optional): Specific pages to analyze beyond homepage
mobile_check (boolean, default: true): Include mobile optimization analysis
performance_check (boolean, default: true): Include Core Web Vitals analysis

---

## Runbook

### Phase 1: Initial Analysis
1. **Homepage Loading**: Take screenshot to verify visual loading using screenshot-website-fast MCP
2. **Page Discovery**: Use firecrawl to identify key pages and site structure
3. **Mobile Check**: Capture mobile screenshots if mobile_check enabled

### Phase 2: Technical Analysis
1. **HTML Metadata Audit**:
   - Title tags (length, uniqueness, keyword optimization)
   - Meta descriptions (length, click-through appeal)
   - Canonical links (proper implementation)
   - Meta robots tags (indexation directives)

2. **Content Structure Analysis**:
   - H1-H6 heading hierarchy
   - Content optimization and keyword usage
   - Internal linking structure
   - Image optimization (alt tags, file sizes)

### Phase 3: Technical Health Check
1. **Performance Metrics**:
   - Page loading times
   - Core Web Vitals (LCP, FID, CLS)
   - Mobile responsiveness
   - Resource optimization

2. **Crawlability Analysis**:
   - robots.txt configuration
   - XML sitemap presence and structure
   - URL structure and hierarchy
   - Internal linking quality

### Phase 4: Issue Identification
1. **Critical Issues Detection**:
   - Pages with noindex/nofollow
   - Broken internal/external links
   - Duplicate or missing H1 tags
   - Missing or poor meta descriptions
   - Performance bottlenecks

2. **Opportunity Identification**:
   - Schema markup opportunities
   - Content gap analysis
   - Technical optimization potential
   - Mobile experience improvements

### Phase 5: Report Generation
Generate comprehensive markdown report with:

**Executive Summary**
- Overall SEO health score
- Critical issues count
- Top 3 priority fixes

**Critical Issues**
- Indexation blockers
- Performance problems
- Mobile usability issues
- Technical errors

**Positive Findings**
- Well-optimized elements
- Strong technical foundations
- Good performance metrics

**Recommendations**
- Priority 1: Critical fixes (with code examples)
- Priority 2: Performance improvements
- Priority 3: Enhancement opportunities
- Implementation timeline

**Technical Details**
- Page-by-page analysis
- Performance metrics table
- Before/after screenshots
- Code snippets for fixes

## Error Handling

- Handle connection timeouts gracefully
- Validate URL accessibility before analysis
- Provide alternative analysis methods for restricted pages
- Clear error messages with troubleshooting steps

## Notes

- Audit is comprehensive but respectful of server resources
- Results include both technical and strategic recommendations
- Screenshots and metrics provide visual proof of issues
- All recommendations include implementation guidance
- Report format suitable for both technical teams and stakeholders