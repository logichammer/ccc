---
name: performance-heatmap
description: Generate performance heatmap analysis for Python applications
category: python
tags: ["python", "performance", "profiling", "optimization", "visualization", "analysis"]
version: 1.0
---

# /performance-heatmap

**Purpose**  
Generate performance heatmap analysis for Python applications, identifying bottlenecks and optimization opportunities.

**Tags**: python, performance, profiling, optimization, visualization, analysis

**Arguments**
- `target_module` (optional): Specific module/function to profile (default: entire application)
- `duration` (optional): Profiling duration in seconds (default: 60)
- `profile_type` (optional): Type of profiling - cpu, memory, io (default: cpu)
- `output_detail` (optional): Detail level - summary, detailed, comprehensive (default: detailed)

**Usage Example**
```
/performance-heatmap target_module=app.main duration=120 profile_type=cpu,memory
```

**MCPs Used**
- chart-mcp: Heatmap and performance visualization
- sequential-thinking: Analysis strategy planning

**Output**
Interactive performance heatmap with bottleneck identification and optimization recommendations.

---

## Arguments

- Provide arguments inline as `key=value` pairs.
- Booleans: `true`/`false`. Lists: comma‑separated (no spaces) unless noted.

target_module (optional): Module or function to profile (default: detect main entry point)
duration (number, default: 60): Profiling duration in seconds
profile_type (optional): Profiling types - cpu,memory,io (default: cpu)
output_detail (optional): Analysis detail - summary,detailed,comprehensive (default: detailed)
include_callgraph (boolean, default: true): Generate call graph visualization
benchmark_mode (boolean, default: false): Run with synthetic load for consistent results
export_raw_data (boolean, default: false): Export raw profiling data for external analysis

---

## Runbook

### Phase 1: Profiling Setup
1. **Environment Preparation**:
   - Install required profiling tools (cProfile, memory_profiler, py-spy)
   - Identify target application entry points
   - Configure profiling parameters based on application type
   - Set up monitoring for resource usage

2. **Profiler Selection**:
   - CPU Profiling: cProfile + py-spy for production-safe profiling
   - Memory Profiling: memory_profiler + tracemalloc for heap analysis
   - I/O Profiling: Custom instrumentation for file/network operations
   - Line-by-line profiling for hot spots

### Phase 2: Data Collection
1. **CPU Profiling**:
   ```python
   import cProfile
   import pstats
   from pstats import SortKey
   
   def profile_cpu(func, duration=60):
       profiler = cProfile.Profile()
       profiler.enable()
       
       # Run target function/application
       result = func()
       
       profiler.disable()
       stats = pstats.Stats(profiler)
       return stats, result
   ```

2. **Memory Profiling**:
   ```python
   import tracemalloc
   from memory_profiler import profile
   
   def profile_memory(func):
       tracemalloc.start()
       
       # Run target function
       result = func()
       
       snapshot = tracemalloc.take_snapshot()
       top_stats = snapshot.statistics('lineno')
       return top_stats, result
   ```

3. **I/O Profiling**:
   - Monitor file operations and network calls
   - Track blocking I/O operations
   - Measure database query performance
   - Analyze async operation efficiency

### Phase 3: Performance Analysis
1. **Bottleneck Identification**:
   - Identify functions consuming most CPU time
   - Find memory leaks and high allocation points
   - Locate I/O bound operations
   - Detect recursive or inefficient algorithms

2. **Call Graph Analysis**:
   - Build function call hierarchy
   - Calculate cumulative vs self time
   - Identify deep call stacks
   - Find unexpected call patterns

3. **Hotspot Detection**:
   - Line-level performance analysis
   - Identify expensive operations
   - Find optimization opportunities
   - Prioritize improvements by impact

### Phase 4: Heatmap Generation
1. **Visual Heatmap Creation**:
   ```python
   def create_performance_heatmap(profile_data):
       # Create heatmap showing:
       # - File/function performance intensity
       # - Call frequency vs execution time
       # - Memory usage patterns
       # - I/O operation hotspots
       
       heatmap_data = process_profile_data(profile_data)
       return generate_heatmap_visualization(heatmap_data)
   ```

2. **Interactive Visualization**:
   - Zoomable heatmap with drill-down capability
   - Hover tooltips with detailed metrics
   - Filterable by function, module, or time range
   - Clickable elements linking to code

### Phase 5: Optimization Recommendations
1. **Algorithmic Improvements**:
   - Identify O(n²) algorithms that could be O(n log n)
   - Suggest caching opportunities
   - Recommend data structure optimizations
   - Find unnecessary computations

2. **Code-Level Optimizations**:
   - List comprehensions vs loops
   - Generator usage for memory efficiency
   - Function call overhead reduction
   - String concatenation improvements

3. **Architecture Optimizations**:
   - Database query optimization
   - Caching layer recommendations
   - Async operation improvements
   - Microservice communication efficiency

### Phase 6: Benchmarking and Validation
1. **Before/After Analysis**:
   - Baseline performance metrics
   - Post-optimization measurements
   - Performance improvement quantification
   - Regression testing

2. **Load Testing Integration**:
   - Profile under realistic load
   - Identify scaling bottlenecks
   - Memory usage under stress
   - Response time degradation analysis

## Visualization Examples

### CPU Heatmap
- X-axis: Time progression
- Y-axis: Function/module hierarchy
- Color intensity: CPU usage percentage
- Size: Relative execution time

### Memory Heatmap  
- X-axis: Application lifecycle
- Y-axis: Object types/modules
- Color: Memory allocation rate
- Annotations: Leak detection points

### I/O Operations Heatmap
- X-axis: Operation timeline
- Y-axis: I/O operation types
- Color: Blocking time
- Patterns: Concurrent vs sequential operations

## Output Reports

### Summary Report
- Overall performance score
- Top 5 bottlenecks identified
- Quick win optimization opportunities
- Estimated improvement potential

### Detailed Analysis
- Function-by-function breakdown
- Call graph with timing information
- Memory allocation patterns
- I/O operation analysis
- Line-level profiling for hot functions

### Comprehensive Report
- Complete profiling data analysis
- Cross-reference with code quality metrics
- Historical performance comparison
- Detailed optimization roadmap
- Implementation examples for improvements

## Error Handling

- Handle profiling overhead gracefully
- Provide meaningful results even with partial data
- Include confidence intervals for measurements
- Offer alternative profiling methods if primary tools fail

## Notes

- Profiling overhead is minimized for production use
- Results include both absolute and relative performance metrics
- Heatmaps are interactive and exportable in multiple formats
- Includes integration with CI/CD for continuous performance monitoring
- Supports comparison between different code versions
- Provides actionable optimization recommendations with code examples
- Can profile both synchronous and asynchronous code patterns