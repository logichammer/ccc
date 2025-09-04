# Claude Code Templates (CCC) - Simplified KISS System

A streamlined, elegant template system for Python, SEO, and WordPress projects following KISS (Keep It Simple, Stupid) principles.

## 🚀 Quick Start

```bash
# Install the system
./install.sh

# Create new projects
claude-init my-python-app python
claude-init client-seo seo  
claude-init my-theme wordpress
claude-init mixed-project python,seo

# Work on existing projects
claude-work /path/to/existing/project
claude-work . --cleanup  # Remove .claude/ when done
```

## 📋 System Overview

CCC is a radical simplification of complex template systems, reducing 203+ commands to 70 unique tools while maintaining all essential functionality. The system provides:

- **Universal Agent Distribution**: 23 specialized AI agents for every project type
- **Type-Specific Workflows**: Tailored CLAUDE.md files for Python, SEO, and WordPress
- **External Project Support**: Work on any existing project without modifying it
- **KISS Architecture**: Simple, maintainable, easy to update

## 🏗️ Architecture

```
/home/loki/code/ccc/           # CCC system (this directory)
├── agents/                    # 23 universal agents
├── commands/                  # 70 curated commands by type
├── templates/                 # Project templates
│   ├── base/                  # Shared foundation
│   ├── python/               # Python-focused CLAUDE.md
│   ├── seo/                  # SEO research-focused CLAUDE.md
│   └── wordpress/            # WordPress dev-focused CLAUDE.md
├── docs/                     # Complete HTML documentation
├── bin/                      # Command-line tools
└── config.toml              # System configuration

/home/loki/python-projects/   # Python projects live here
/home/loki/seo-projects/      # SEO projects live here
```

## 🤖 Agent System

The Universal Agent Distribution System provides 23 specialized agents:

### Core Development Agents
- **SystemArchitectAgent**: Architecture design and validation
- **FeatureDeveloperAgent**: Feature implementation with atomic changes
- **PerformanceOptimizerAgent**: Code optimization and profiling
- **SecurityAuditorAgent**: Security analysis and hardening
- **TestSuiteGeneratorAgent**: Comprehensive test creation

### Specialized Workflow Agents  
- **SEOResearchAgent**: Keyword research and SERP analysis
- **WordPressExpertAgent**: Theme and plugin development
- **DatabaseArchitectAgent**: Schema design and optimization
- **APIDesignAgent**: RESTful API development
- **DevOpsAutomationAgent**: CI/CD and deployment

*[Full agent list in docs/agents-guide.html]*

## 📂 Project Types

### Python Projects
- **Focus**: Beast-mode development with TDD, performance, security
- **Tools**: pytest, black, mypy, profiling, security scanning
- **Workflows**: Feature development, testing, optimization, deployment
- **Agent Integration**: Seamless agent handoffs for complex tasks

### SEO Projects  
- **Focus**: Research, analysis, multi-client management
- **Tools**: Keyword research, SERP analysis, competitor tracking
- **Data Management**: Client-specific data isolation
- **MCP Integration**: DataForSEO, GSC, Firecrawl, Perplexity

### WordPress Projects
- **Focus**: Theme/plugin development, Elementor, performance
- **Tools**: WP-CLI, theme development, Elementor widgets
- **Security**: WordPress-specific security patterns
- **Integration**: SEO optimization, performance tuning

## 🔧 External Project Workflow

The killer feature: work on ANY existing project without modifying it.

```bash
# Work on existing project
claude-work /path/to/legacy/project
# Creates temporary .claude/ directory with full toolkit
# Original project remains untouched

# When done, clean up completely
claude-work /path/to/legacy/project --cleanup
# Removes all traces, original project preserved
```

### How It Works

1. **Auto-Detection**: Analyzes project files to determine type (Python, WordPress, etc.)
2. **Portable Setup**: Creates `.claude/` directory with agents, commands, and workflows
3. **Type-Specific CLAUDE.md**: Copies appropriate workflow documentation
4. **Complete Toolkit**: Full access to 23 agents and relevant commands
5. **Clean Removal**: Delete `.claude/` to remove all traces

## 📚 Documentation

Comprehensive HTML documentation with high-contrast styling:

- **[Getting Started](docs/getting-started.html)**: Installation and first projects
- **[Workflows](docs/workflows.html)**: Complete workflow documentation
- **[Chat Interface](docs/chat-interface.html)**: Agent orchestration patterns  
- **[Agents Guide](docs/agents-guide.html)**: All 23 agents explained
- **[Command Reference](docs/commands.html)**: 70+ commands organized by type

## 🎯 Command Examples

### Python Development
```bash
/test-suite-gen component=UserAuth coverage_target=95
/performance-heatmap target_file=main.py optimization_type=memory
/security-audit scan_type=comprehensive include_dependencies=true
```

### SEO Research
```bash
/keyword-research seed_keywords="digital marketing,seo" target_location=US
/seo-audit target_url=https://example.com audit_type=comprehensive
/serp-analysis keywords="seo tools" location=US analyze_features=true
```

### WordPress Development
```bash
/elementor-widget widget_name=TestimonialSlider widget_type=dynamic
/wp-theme-security theme_path=./my-theme scan_type=comprehensive
/wp-performance target_url=https://mysite.com optimization_type=full
```

## 🔄 KISS Principles Applied

### Before (Complex)
- 203+ command files with duplicates
- 3 separate template systems
- Complex agent management
- Inconsistent documentation
- Hard to maintain/update

### After (KISS)
- 70 unique commands, organized by type
- Single flexible template system
- Universal agent distribution
- Comprehensive documentation
- Easy maintenance and updates

## 🛠️ Installation

### Prerequisites
- Python 3.x
- pip/pip3
- git

### Install
```bash
git clone <your-repo> /home/loki/code/ccc
cd /home/loki/code/ccc
./install.sh
```

### What Installation Does
1. Checks dependencies (Python, pip, git)
2. Installs required Python packages (toml)
3. Creates external project directories
4. Installs `claude-init` and `claude-work` to `/usr/local/bin`
5. Sets up shell aliases
6. Verifies everything works

## 🔧 Configuration

Edit `config.toml` to customize:

```toml
[directories]
toolkit_path = "/home/loki/code/ccc"
python_projects = "/home/loki/python-projects"
seo_projects = "/home/loki/seo-projects"

[templates]
available = ["python", "seo", "wordpress"]

[agents]
count = 23
universal_distribution = true

[agents.default_agents]
python = "SystemArchitectAgent"
seo = "SEOResearchAgent"
wordpress = "WordPressExpertAgent"
```

## 🏆 Key Benefits

### For Developers
- **Beast-Mode Python**: TDD, performance optimization, security hardening
- **Agent Orchestration**: Seamless handoffs between specialized agents
- **External Project Support**: Work on legacy projects without modification
- **Type-Specific Workflows**: Optimized for each project type

### For SEO Professionals  
- **Multi-Client Management**: Isolated data per client
- **Research Workflows**: Keyword research, competitor analysis, SERP tracking
- **MCP Integration**: Direct access to SEO tools and APIs
- **Comprehensive Auditing**: Technical and content SEO analysis

### For WordPress Developers
- **Theme Development**: Complete WordPress development toolkit
- **Elementor Integration**: Custom widget development workflows
- **Performance Focus**: WP-specific optimization patterns
- **Security Patterns**: WordPress security best practices

### For System Maintainers
- **KISS Architecture**: Simple, understandable, maintainable
- **Single Source of Truth**: No duplication, easy updates
- **Comprehensive Docs**: Everything documented in HTML
- **Easy Extension**: Add new project types easily

## 🚦 Usage Patterns

### Daily Development Workflow
1. `claude-init my-feature python` - Create new Python project
2. Use agents in CLAUDE.md for development tasks
3. Run commands for testing, optimization, security
4. Agent handoffs for complex multi-step tasks

### External Project Analysis
1. `claude-work /path/to/legacy/project` - Setup toolkit
2. Auto-detection determines project type
3. Full agent system available for analysis
4. `claude-work . --cleanup` when done

### SEO Client Management
1. `claude-init client-name seo` - New client project
2. Research workflows with keyword analysis
3. Competitor tracking and SERP monitoring
4. Data isolation per client

## 📈 Migration from Complex Systems

If migrating from the original 203-command system:

1. **Command Mapping**: Most functionality preserved in simplified commands
2. **Agent Compatibility**: All agents preserved and enhanced
3. **Workflow Continuity**: Improved workflows in type-specific CLAUDE.md files
4. **Data Preservation**: External projects maintain all data

## 🤝 Contributing

The system is designed for easy extension:

1. **New Project Types**: Add template in `templates/new-type/`
2. **New Commands**: Add to appropriate `commands/type/` directory  
3. **New Agents**: Add agent JSON to `agents/` directory
4. **Documentation**: Update relevant HTML docs

## 📄 License

MIT License - Use freely for personal and commercial projects.

## 🎯 Next Steps

After installation:

1. **Read the docs**: `open docs/index.html` (or use `ccc-docs` alias)
2. **Create first project**: `claude-init test-project python`
3. **Try external workflow**: `claude-work /path/to/existing/project`
4. **Explore agents**: Check out the 23 specialized agents
5. **Master workflows**: Study the type-specific CLAUDE.md files

---

*Claude Code Templates (CCC) v2.0 - Simplified, Elegant, Powerful*