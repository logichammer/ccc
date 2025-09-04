# Claude Code Templates (CCC) - Universal Development Toolkit

> **Beast Mode**: Advanced AI-assisted development with 23 specialized agents, type-specific workflows, and universal project support.

---

## 🚨 **CRITICAL SYSTEM RULE: LINE ENDINGS**

### **MANDATORY LINE ENDING POLICY**
**ALL files in the CCC system MUST use Unix line endings (`\n` only, NO `\r\n`)**

**Why this matters:**
- Scripts fail with `/bin/bash^M: bad interpreter` error when using Windows line endings
- Python execution issues and import failures
- Git conflicts and inconsistent behavior across systems

### **PREVENTION PROTOCOL**
**Before creating/editing ANY file:**

1. **Auto-fix line endings immediately:**
   ```bash
   # Fix all files in CCC system
   find /home/loki/code/ccc -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "*.txt" -o -name "*.toml" \) -exec sed -i 's/\r$//' {} \;
   ```

2. **Configure Git properly:**
   ```bash
   git config --global core.autocrlf false
   git config --global core.eol lf
   ```

3. **Verify before committing:**
   ```bash
   # Check for Windows line endings
   grep -r $'\r' /home/loki/code/ccc/ || echo "✅ All line endings correct"
   ```

### **ENFORCEMENT RULES**
- **BEFORE any script creation**: Run line ending fix
- **BEFORE any file editing**: Check and fix line endings
- **BEFORE any git commit**: Verify no `\r` characters exist
- **DURING installation**: Auto-fix line endings (already implemented)

### **IMMEDIATE ACTION REQUIRED**
If you encounter line ending errors:
```bash
# Emergency fix - run immediately
find /home/loki/code/ccc -type f -exec sed -i 's/\r$//' {} \;
chmod +x /home/loki/code/ccc/bin/* /home/loki/code/ccc/*.sh
```

**This rule applies to ALL CCC system files: scripts, configs, docs, everything.**

---

## 🤖 **AGENT ORCHESTRATION SYSTEM**

### **Current Session Context**
This is the **CCC System Root** - a simplified, elegant template system following KISS principles. You have access to:

- **23 Universal Agents**: Specialized for every development task
- **Type-Specific Workflows**: Python, SEO, WordPress optimized patterns
- **External Project Support**: Work on ANY existing project
- **70+ Curated Commands**: Organized by project type
- **Complete Documentation**: HTML guides for all workflows

### **Agent Switching Protocol**

Use this pattern for seamless agent handoffs:

```
I need to [TASK DESCRIPTION]. Please hand this off to [AGENT_NAME] with the following context:
- Current task: [BRIEF DESCRIPTION]
- Files involved: [LIST KEY FILES]
- Specific requirements: [KEY REQUIREMENTS]
- Expected deliverable: [WHAT TO RETURN]
```

### **Available Agents**

#### **🏗️ Core Development Agents**
- **SystemArchitectAgent**: System design, architecture validation, technical debt analysis
- **FeatureDeveloperAgent**: Feature implementation with atomic changes, hook compliance
- **CodebaseAnalyzerAgent**: Deep code analysis, pattern detection, refactoring opportunities
- **QualityTesterAgent**: Test strategy, coverage analysis, quality assurance
- **PerformanceProfilerAgent**: Performance optimization, bottleneck identification, profiling

#### **🔧 Specialized Development Agents**
- **DatabaseOptimizerAgent**: Schema design, query optimization, performance tuning
- **SecurityAuditorAgent**: Security analysis, vulnerability assessment, hardening
- **DataPipelineAgent**: Data processing workflows, ETL optimization
- **DeliveryVerifierAgent**: Deployment validation, rollback strategies, production readiness

#### **🎨 Frontend & UX Agents**
- **FrontendBuilderAgent**: Modern frontend development, component architecture
- **FrontendImplementerAgent**: UI implementation, responsive design
- **InterfaceDesignerAgent**: User interface design, UX optimization
- **ResponsiveAdapterAgent**: Mobile optimization, cross-platform compatibility
- **InteractionEnhancerAgent**: User experience optimization, interaction design

#### **📈 SEO & Marketing Agents**
- **TechnicalSEOAgent**: Technical SEO audits, Core Web Vitals, schema markup
- **KeywordStrategyAgent**: Keyword research, content strategy, SERP analysis
- **ConversionOptimizerAgent**: CRO analysis, funnel optimization, A/B testing
- **MetricsReporterAgent**: Analytics setup, KPI tracking, performance reporting

#### **🔧 WordPress Specialists**
- **WordPressBuilderAgent**: Theme development, plugin creation, WP optimization
- **ElementorSpecialistAgent**: Elementor widgets, custom templates, advanced layouts

#### **⚡ Performance & Automation**
- **BenchmarkResearchAgent**: Performance benchmarking, competitive analysis
- **WorkflowOrchestratorAgent**: Development workflow optimization, automation

#### **🎯 Meta-Agent**
- **DeliveryVerifierAgent**: Final verification, quality gates, release preparation

## 🚀 **DEVELOPMENT WORKFLOWS**

### **Python Beast Mode Development**
1. **Architecture Phase**: Use SystemArchitectAgent for design validation
2. **Feature Development**: FeatureDeveloperAgent for implementation
3. **Testing**: QualityTesterAgent for comprehensive test coverage
4. **Performance**: PerformanceProfilerAgent for optimization
5. **Security**: SecurityAuditorAgent for vulnerability assessment
6. **Delivery**: DeliveryVerifierAgent for production readiness

### **SEO Research & Analysis**
1. **Strategy**: KeywordStrategyAgent for keyword research and planning
2. **Technical**: TechnicalSEOAgent for technical audits and optimization
3. **Content**: ConversionOptimizerAgent for content strategy and CRO
4. **Metrics**: MetricsReporterAgent for performance tracking

### **WordPress Development**
1. **Planning**: SystemArchitectAgent for WordPress architecture
2. **Development**: WordPressBuilderAgent for theme/plugin development
3. **Elementor**: ElementorSpecialistAgent for custom widgets and layouts
4. **Performance**: PerformanceProfilerAgent for WP optimization
5. **Security**: SecurityAuditorAgent for WordPress-specific security

## 📋 **COMMAND SYSTEM**

### **Command Usage Pattern**
```
/command-name arg1=value1 arg2=value2 flag=true
```

### **Available Command Categories**

#### **Shared Commands** (Universal)
- `/project-summary` - Complete project analysis and documentation
- `/code-review` - Comprehensive code review with recommendations
- `/dependency-audit` - Security and update analysis of dependencies
- `/performance-baseline` - Establish performance benchmarks
- `/documentation-gen` - Auto-generate project documentation

#### **Python Commands** 
- `/test-suite-gen` - Generate comprehensive test suites
- `/performance-heatmap` - Identify performance bottlenecks
- `/security-audit` - Python-specific security analysis
- `/refactor-analysis` - Code refactoring opportunities

#### **SEO Commands**
- `/keyword-research` - Comprehensive keyword research and analysis
- `/seo-audit` - Technical SEO audit with recommendations
- `/serp-analysis` - Search result analysis and opportunities
- `/competitor-analysis` - Competitive landscape analysis
- `/content-strategy` - Data-driven content planning
- And 7 more specialized SEO tools...

#### **WordPress Commands**
- `/wp-security-audit` - WordPress security analysis
- `/elementor-widget` - Custom Elementor widget development
- `/theme-performance` - WordPress theme optimization
- `/wp-seo-integration` - SEO optimization for WordPress
- And 4 more WordPress-specific tools...

## 🔄 **PROJECT WORKFLOWS**

### **New Project Creation**
```bash
claude-init project-name python     # Python project
claude-init project-name seo        # SEO project  
claude-init project-name wordpress  # WordPress project
claude-init project-name python,seo # Mixed project
```

### **External Project Analysis**
```bash
claude-work /path/to/existing/project  # Auto-detect and setup
claude-work . --type python           # Force specific type
claude-work . --cleanup               # Remove .claude/ when done
```

### **Agent Handoff Examples**

#### **Complex Feature Development**
```
I need to implement user authentication with OAuth2. Please hand this off to SystemArchitectAgent with:
- Current task: Design secure OAuth2 authentication system
- Files involved: auth/, models/user.py, requirements.txt
- Requirements: Google/GitHub OAuth, JWT tokens, role-based access
- Deliverable: Complete architecture plan and implementation roadmap
```

#### **Performance Optimization**
```
I have performance issues in my Python app. Hand to PerformanceProfilerAgent:
- Current task: Identify and resolve performance bottlenecks
- Files involved: main.py, data_processing/, requirements.txt
- Requirements: Sub-200ms response times, memory optimization
- Deliverable: Performance analysis report and optimization plan
```

#### **SEO Analysis**
```
Need comprehensive SEO audit for client website. Hand to TechnicalSEOAgent:
- Current task: Complete technical SEO audit
- Target: https://client-website.com
- Requirements: Core Web Vitals, mobile optimization, schema markup
- Deliverable: Prioritized action plan with implementation guidance
```

## 🎯 **BEST PRACTICES**

### **Agent Selection Guidelines**
- **SystemArchitectAgent**: When you need system design, architecture validation, or technical strategy
- **FeatureDeveloperAgent**: For implementing specific features with clean, tested code
- **TechnicalSEOAgent**: For SEO audits, Core Web Vitals, and technical optimization
- **WordPressBuilderAgent**: For WordPress-specific development tasks
- **QualityTesterAgent**: When test coverage, quality assurance, or testing strategy is needed

### **Workflow Optimization**
1. **Start with Architecture**: Always begin complex projects with SystemArchitectAgent
2. **Single Responsibility**: Each agent handoff should have one clear objective
3. **Context Preservation**: Always provide sufficient context for smooth handoffs
4. **Quality Gates**: Use QualityTesterAgent and DeliveryVerifierAgent for quality assurance
5. **Performance Focus**: Integrate PerformanceProfilerAgent early in the development cycle

### **External Project Protocol**
1. **Setup**: `claude-work /path/to/project` creates `.claude/` directory
2. **Analysis**: Use appropriate agents to understand existing codebase
3. **Planning**: SystemArchitectAgent for improvement roadmap
4. **Implementation**: Specialized agents for specific improvements
5. **Cleanup**: `claude-work . --cleanup` removes all traces when done

## 📚 **DOCUMENTATION SYSTEM**

### **Complete HTML Documentation**
- **[System Overview](docs/index.html)**: CCC system introduction and navigation
- **[Getting Started](docs/getting-started.html)**: Installation and first projects
- **[Workflows](docs/workflows.html)**: Complete workflow documentation for all project types
- **[Chat Interface](docs/chat-interface.html)**: Agent orchestration patterns and best practices
- **[Agents Guide](docs/agents-guide.html)**: All 23 agents with detailed descriptions
- **[Commands Reference](docs/commands.html)**: Complete command documentation
- **[Installation Guide](docs/installation.html)**: Detailed installation and setup

### **Quick Reference**
```bash
# Open documentation
open docs/index.html
# or use alias after installation
ccc-docs
```

## 🔧 **SYSTEM CONFIGURATION**

### **Project Directories**
- **Python Projects**: `/home/loki/python-projects/`
- **SEO Projects**: `/home/loki/seo-projects/`
- **CCC System**: `/home/loki/code/ccc/`

### **External Project Support**
The CCC system can work on ANY existing project by creating a temporary `.claude/` directory with the full toolkit. This preserves the original project while providing complete development capabilities.

## ⚡ **ADVANCED FEATURES**

### **Multi-Agent Workflows**
Chain multiple agents for complex tasks:
1. **SystemArchitectAgent** → Design and validate architecture
2. **FeatureDeveloperAgent** → Implement features
3. **QualityTesterAgent** → Create comprehensive tests
4. **PerformanceProfilerAgent** → Optimize performance
5. **SecurityAuditorAgent** → Security hardening
6. **DeliveryVerifierAgent** → Final verification and deployment

### **Type-Specific Optimization**
Each project type has optimized workflows:
- **Python**: TDD, performance optimization, security focus
- **SEO**: Research workflows, multi-client data management
- **WordPress**: Theme development, Elementor integration, WP-specific security

### **Command Chaining**
Combine commands for comprehensive analysis:
```bash
/project-summary → /security-audit → /performance-baseline → /test-suite-gen
```

## 🎪 **EMERGENCY PROTOCOLS**

### **Stuck? Use This Hierarchy**
1. **SystemArchitectAgent**: For strategic decisions and architecture questions
2. **CodebaseAnalyzerAgent**: For understanding complex existing code
3. **WorkflowOrchestratorAgent**: For process optimization and workflow questions
4. **DeliveryVerifierAgent**: For final validation and quality assurance

### **Quality Assurance Chain**
Always end significant work with:
1. **QualityTesterAgent**: Verify testing completeness
2. **SecurityAuditorAgent**: Check for security issues
3. **PerformanceProfilerAgent**: Validate performance
4. **DeliveryVerifierAgent**: Final production readiness check

---

## 🚀 **GET STARTED NOW**

1. **Choose Your Agent**: Pick the right agent for your current task
2. **Use Commands**: Leverage the 70+ curated commands for efficiency
3. **Follow Workflows**: Use type-specific patterns for optimal results
4. **Chain Agents**: Create sophisticated multi-step workflows
5. **Document Everything**: Use the comprehensive documentation system

**Welcome to Beast Mode Development with CCC v2.0!**

*The system that transforms complex development tasks into elegant, manageable workflows.*