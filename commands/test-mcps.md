---
name: test-mcps
description: Test MCP server connections and functionality with comprehensive status reporting
category: shared
tags: ["testing", "mcp", "diagnostics"]
version: 1.0
---

# Test MCP Servers

## Purpose
Test MCP server connections and functionality with comprehensive status reporting.

## Usage
```bash
/shared:test-mcps
```

## Options
- No arguments required - automatically tests all configured MCPs

## Examples

### Basic MCP Test
```bash
/shared:test-mcps
```

## What It Does

Tests connectivity to all configured MCP servers and displays results in a Rich CLI formatted table showing:
- Working MCPs (green status indicators)
- Broken/unavailable MCPs (red status indicators)  
- Overall success rate and statistics
- Specific error messages for failed connections
- Troubleshooting recommendations
- Determines the most basic function each MCP can perform and tests for success

## Output

- Color-coded summary panel with success statistics
- Side-by-side tables for working vs broken MCPs
- Detailed error messages for troubleshooting
- Actionable next steps for fixing issues

Perfect for system diagnostics before running critical workflows or when troubleshooting MCP connectivity issues.

## Agent Integration
This command works optimally with:
- **SystemArchitectAgent**: For system diagnostics
- **QualityTesterAgent**: For testing validation