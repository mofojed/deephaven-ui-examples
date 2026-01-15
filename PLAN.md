# Project Scaffolding Plan

## Goal

Set up a complete development environment for the deephaven-ui-examples repository, including:
- Python virtual environment with all required dependencies
- Utility scripts for running examples
- Unit testing framework
- End-to-end testing with Playwright

## Features

- One-command setup for development environment
- Easy example execution with utility scripts
- Unit tests for individual examples
- E2E tests that launch Deephaven and verify UI behavior
- CI/CD ready testing infrastructure

## Project Structure (Target)

```
deephaven-ui-examples/
├── README.md                    # Project documentation
├── AGENTS.md                    # Agent instructions
├── PLAN.md                      # This file
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── requirements-dev.txt         # Development/testing dependencies
├── setup.sh                     # One-command setup script
├── scripts/
│   ├── run_example.py           # Utility to run a specific example
│   └── start_server.py          # Start Deephaven server
├── tests/
│   ├── conftest.py              # Pytest configuration and fixtures
│   ├── unit/                    # Unit tests
│   │   └── test_<example>.py    # Unit tests for each example
│   └── e2e/                     # End-to-end tests
│       ├── conftest.py          # Playwright fixtures
│       ├── playwright.config.py # Playwright configuration
│       └── test_<example>.py    # E2E tests for each example
├── examples/
│   └── example-name/
│       ├── PLAN.md
│       ├── README.md
│       ├── example_name.py
│       └── test_example_name.py # Optional: example-specific unit tests
└── playwright/                  # Playwright browser data (gitignored)
```

## Implementation Details

### 1. Python Environment Setup

**requirements.txt:**
```
deephaven-core
deephaven-server
deephaven-plugin-ui
deephaven-plugin-plotly-express
```

**requirements-dev.txt:**
```
-r requirements.txt
pytest
pytest-asyncio
playwright
pytest-playwright
```

**setup.sh script will:**
1. Create a Python venv in `.venv/`
2. Install requirements.txt
3. Install requirements-dev.txt (optional with --dev flag)
4. Install Playwright browsers (optional with --dev flag)

### 2. Utility Scripts

**scripts/start_server.py:**
- Start Deephaven server programmatically using `deephaven-server`
- Configure to load examples directory
- Accept port configuration
- Support for running in background or foreground

**scripts/run_example.py:**
- Accept example name as argument
- Start Deephaven server if not running
- Execute the example's main Python file
- Print URL to access the UI

### 3. Unit Testing Framework

**Structure:**
- Use pytest as the test runner
- Tests in `tests/unit/` directory
- Test files named `test_<example_name>.py`
- Each example can also have local tests in its folder

**What to test:**
- Component function returns valid UI elements
- State management works correctly
- Data transformations produce expected results
- Edge cases and error handling

**Running tests:**
```bash
# Run all unit tests
pytest tests/unit/

# Run tests for a specific example
pytest tests/unit/test_example_name.py

# Run tests with coverage
pytest tests/unit/ --cov=examples
```

### 4. End-to-End Testing with Playwright

**Setup:**
- Use pytest-playwright for Python integration
- Configure base URL to local Deephaven server
- Fixtures to start/stop server automatically

**tests/e2e/conftest.py will provide:**
- `deephaven_server` fixture - starts server before tests, stops after
- `deephaven_page` fixture - navigates to Deephaven UI
- Helper functions for common UI interactions

**Test structure:**
```python
def test_example_renders(deephaven_page):
    """Test that the example UI renders correctly."""
    # Load the example
    # Wait for UI to render
    # Assert expected elements are visible
    # Take screenshot for visual regression (optional)
```

**Running E2E tests:**
```bash
# Run all E2E tests
pytest tests/e2e/

# Run E2E tests for a specific example
pytest tests/e2e/test_example_name.py

# Run with headed browser (for debugging)
pytest tests/e2e/ --headed

# Run with specific browser
pytest tests/e2e/ --browser chromium
```

### 5. CI/CD Integration

**GitHub Actions workflow will:**
1. Set up Python environment
2. Install dependencies
3. Run unit tests
4. Start Deephaven server
5. Run E2E tests
6. Upload test artifacts (screenshots, logs)

## Dependencies

**Python packages:**
- deephaven-core
- deephaven-server  
- deephaven-plugin-ui
- deephaven-plugin-plotly-express
- pytest
- pytest-asyncio
- playwright
- pytest-playwright

**System requirements:**
- Python 3.9+
- Node.js (for Playwright browsers)

## Implementation Order

1. [ ] Create requirements.txt and requirements-dev.txt
2. [ ] Create setup.sh script
3. [ ] Create scripts/start_server.py
4. [ ] Create scripts/run_example.py
5. [ ] Set up pytest configuration (tests/conftest.py)
6. [ ] Set up Playwright configuration (tests/e2e/conftest.py)
7. [ ] Update .gitignore for new directories
8. [ ] Update README.md with setup and testing instructions
9. [ ] Update AGENTS.md with testing conventions
10. [ ] Create GitHub Actions workflow (optional)

## Usage Summary

```bash
# Initial setup
./setup.sh --dev

# Activate environment
source .venv/bin/activate

# Run an example
python scripts/run_example.py example-name

# Run all unit tests
pytest tests/unit/

# Run all E2E tests
pytest tests/e2e/

# Run tests for specific example
pytest -k "example_name"
```
