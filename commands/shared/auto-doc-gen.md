# Auto Documentation Generator

## Purpose
Automatically generates comprehensive documentation for projects, analyzing code structure, dependencies, and functionality to create professional README.md and technical documentation.

## Usage
```bash
/auto-doc-gen [options]
```

## Options
- `output=readme` - Generate README.md (default)
- `output=api` - Generate API documentation 
- `output=full` - Generate complete documentation set
- `format=markdown` - Markdown format (default)
- `format=html` - HTML format
- `include_examples=true` - Include code examples (default: true)

## Examples

### Basic README Generation
```bash
/auto-doc-gen
```

### Complete Documentation Set
```bash
/auto-doc-gen output=full format=markdown include_examples=true
```

### API Documentation Only
```bash
/auto-doc-gen output=api format=html
```

## What It Generates

### For Python Projects
- **Project Overview**: Description, features, requirements
- **Installation Instructions**: pip install, virtual environment setup
- **Usage Examples**: Code samples and common patterns
- **API Reference**: Function/class documentation from docstrings
- **Development Setup**: How to contribute, testing, linting
- **Dependencies Analysis**: Requirements breakdown and security notes

### For SEO Projects  
- **Research Methodology**: Data sources and analysis approach
- **Keyword Strategy**: Target keywords and competitive analysis
- **Content Calendar**: Planned content and optimization schedule
- **Technical SEO Checklist**: Site optimization requirements
- **Reporting Dashboard**: Metrics and KPI tracking

### For WordPress Projects
- **Theme/Plugin Overview**: Features and compatibility
- **Installation Guide**: WordPress setup and configuration
- **Customization Options**: Available hooks, filters, and settings
- **Template Hierarchy**: Theme structure and file organization
- **Security Considerations**: Best practices and vulnerability prevention

## Intelligence Features
- **Dependency Analysis**: Automatically scans package.json, requirements.txt, composer.json
- **Code Pattern Detection**: Identifies frameworks, architectures, and design patterns
- **Example Extraction**: Pulls real examples from test files and usage patterns
- **Link Generation**: Creates proper links to documentation, repositories, and resources
- **Badge Generation**: Adds appropriate shields.io badges for CI, coverage, version, etc.

## Output Locations
- `README.md` - Root directory
- `docs/` - Complete documentation set
- `api/` - API reference documentation
- `.claude/docs/` - Internal documentation (preserves on cleanup)

## Agent Integration
This command works optimally with:
- **CodebaseAnalyzerAgent**: For deep code analysis
- **DocumentationGeneratorAgent**: For writing and formatting
- **QualityTesterAgent**: For ensuring documentation accuracy
- **TechnicalSEOAgent**: For SEO project documentation