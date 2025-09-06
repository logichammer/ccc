# /test-suite-gen

**Purpose**  
Generate comprehensive test suite including unit tests, UI tests, and accessibility tests from PRD acceptance criteria.

**Tags**: python, testing, pytest, playwright, accessibility, tdd

**Arguments**
- `test_types` (optional): Types of tests to generate (unit,ui,a11y) - default: all
- `prd_file` (optional): Path to PRD file - default: PRD.txt or auto-detect
- `coverage_target` (optional): Target code coverage percentage - default: 80

**Usage Example**
```
/test-suite-gen test_types=unit,ui coverage_target=85
```

**MCPs Used**
- sequential-thinking: Test strategy planning
- chart-mcp: Coverage visualization

**Output**
Complete test suite with unit tests, UI tests, accessibility tests, and coverage reporting.

---

## Arguments

- Provide arguments inline as `key=value` pairs.
- Booleans: `true`/`false`. Lists: comma‑separated (no spaces) unless noted.

test_types (optional): Types of tests to generate - unit,ui,a11y (default: all)
prd_file (optional): Path to PRD file for acceptance criteria extraction
coverage_target (number, default: 80): Target code coverage percentage
framework (optional): Testing framework preference - pytest,unittest (default: pytest)
ui_framework (optional): UI testing framework - playwright,selenium (default: playwright)

---

## Runbook

### Phase 1: Requirements Analysis
1. **PRD Analysis**: Read PRD.txt and tasks/*.md files to extract acceptance criteria
2. **Codebase Scan**: Identify pure functions, service endpoints, and UI components
3. **Test Strategy**: Plan test coverage for critical functionality
4. **Framework Setup**: Configure pytest, playwright, and axe-core for accessibility

### Phase 2: Unit Test Generation
1. **Pure Function Tests**:
   - Identify testable functions in app/lib/
   - Generate parameterized tests for edge cases
   - Mock external dependencies
   - Test error handling and validation

2. **Service Endpoint Tests**:
   - API endpoint testing with different inputs
   - Database interaction mocking
   - Authentication and authorization tests
   - Response format validation

3. **Business Logic Tests**:
   - Core business rule validation
   - Data transformation tests
   - Integration between components
   - Error case handling

### Phase 3: UI Test Generation
1. **Primary User Journeys**:
   - Extract user flows from PRD acceptance criteria
   - Create Playwright test scenarios
   - Cover happy path and error scenarios
   - Test responsive behavior

2. **Component Testing**:
   - Individual UI component tests
   - Form validation and submission
   - Interactive element testing
   - State management validation

### Phase 4: Accessibility Testing
1. **Automated A11y Tests**:
   - Inject axe-core into Playwright tests
   - Test for WCAG compliance
   - Keyboard navigation testing
   - Screen reader compatibility

2. **Manual A11y Guidelines**:
   - Color contrast verification
   - Focus management testing
   - Alternative text validation
   - Semantic HTML structure

### Phase 5: Test Organization
1. **Directory Structure**:
   ```
   tests/
   ├── unit/
   │   ├── test_models.py
   │   ├── test_services.py
   │   └── test_utils.py
   ├── ui/
   │   ├── test_auth_flow.py
   │   ├── test_main_features.py
   │   └── test_responsive.py
   ├── a11y/
   │   └── test_accessibility.py
   ├── fixtures/
   ├── conftest.py
   └── pytest.ini
   ```

2. **Test Markers**:
   - `@pytest.mark.unit` for unit tests
   - `@pytest.mark.ui` for UI tests
   - `@pytest.mark.a11y` for accessibility tests
   - `@pytest.mark.slow` for time-intensive tests

### Phase 6: Execution and Reporting
1. **Test Execution**:
   - Run unit tests first (fast feedback)
   - Execute UI tests with appropriate timeouts
   - Generate accessibility reports
   - Measure code coverage

2. **Report Generation**:
   - HTML coverage reports
   - UI test screenshots on failure
   - Accessibility audit reports
   - Performance metrics

3. **CI/CD Integration**:
   - Configure GitHub Actions workflow
   - Set up test result notifications
   - Implement coverage gates
   - Parallel test execution

## Configuration Templates

### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    unit: Unit tests
    ui: UI tests
    a11y: Accessibility tests
    slow: Slow running tests
addopts = 
    --verbose
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

### Playwright Configuration
```python
# conftest.py
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()
```

## Error Handling

- Handle missing PRD files gracefully
- Validate test framework installations
- Provide clear error messages for test failures
- Automatic retry for flaky UI tests
- Fallback options for accessibility testing tools

## Notes

- Tests are generated based on actual PRD requirements
- Includes both positive and negative test cases
- UI tests include visual regression testing capabilities
- Accessibility tests follow WCAG 2.1 AA guidelines
- All tests include proper setup and teardown
- Generated tests are immediately runnable
- Includes performance benchmarking for critical functions