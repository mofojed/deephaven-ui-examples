# Deephaven UI Examples

This repository contains example usages of [deephaven.ui](https://github.com/deephaven/deephaven-plugins/tree/main/plugins/ui), a Python framework for building reactive user interfaces in Deephaven.

## Contents

- **Example Applications** - Demonstrations of deephaven.ui capabilities and patterns
- **Custom Components** - Reusable components built with the `@ui.component` decorator

## Project Structure

```
deephaven-ui-examples/
├── README.md                 # This file
├── AGENTS.md                 # AI agent instructions
├── requirements.txt          # Python dependencies
├── requirements-dev.txt      # Development dependencies
├── setup.sh                  # Setup script
├── pytest.ini                # Pytest configuration
├── scripts/
│   ├── start_server.py       # Start Deephaven server
│   └── run_example.py        # Run a specific example
├── tests/
│   ├── conftest.py           # Shared pytest fixtures
│   └── e2e/
│       └── conftest.py       # Playwright fixtures
└── examples/
    └── example-name/
        ├── PLAN.md           # Design plan
        ├── README.md         # Usage instructions
        ├── app.py            # Main example code
        ├── unit/             # Unit tests
        │   └── test_*.py
        └── e2e/              # E2E tests
            └── test_*.py
```

## Getting Started

### Prerequisites

- Python 3.9+
- [Deephaven](https://deephaven.io/) (installed via pip)

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/deephaven/deephaven-ui-examples.git
   cd deephaven-ui-examples
   ```

2. Run the setup script:

   ```bash
   # Basic setup
   ./setup.sh

   # With development dependencies (pytest, playwright)
   ./setup.sh --dev
   ```

3. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

### Running Examples

**Option 1: Using the run script**

```bash
# List available examples
python scripts/run_example.py --list

# Run a specific example
python scripts/run_example.py hello-world
```

**Option 2: Start server and run manually**

```bash
# Start the server
python scripts/start_server.py

# Then in the Deephaven console, run:
exec(open('/path/to/examples/hello-world/app.py').read())
```

**Option 3: Using Docker**

```bash
docker run -it --rm -p 10000:10000 \
  -v $(pwd):/data/examples \
  ghcr.io/deephaven/server:latest
```

## Testing

### Unit Tests

Run all unit tests:

```bash
pytest examples/*/unit/
```

Run tests for a specific example:

```bash
pytest examples/hello-world/unit/
```

### E2E Tests

Run all E2E tests (requires Playwright browsers):

```bash
pytest examples/*/e2e/
```

Run with headed browser for debugging:

```bash
pytest examples/*/e2e/ --headed
```

Run all tests for a specific example:

```bash
pytest examples/hello-world/
```

## Custom Components

Custom components in this repository are defined using the `@ui.component` decorator:

```python
from deephaven import ui

@ui.component
def my_custom_component(name: str):
    """A simple greeting component.

    Args:
        name: The name to display in the greeting.
    """
    return ui.text(f"Hello, {name}!")
```

## Examples

| Example | Description |
| ------- | ----------- |
| [hello-world](examples/hello-world/) | Basic component and state management demo |

## Resources

- [deephaven.ui Documentation](https://deephaven.io/core/docs/how-to-guides/user-interface/overview/)
- [Deephaven Community](https://deephaven.io/community/)

## License

Apache License 2.0
