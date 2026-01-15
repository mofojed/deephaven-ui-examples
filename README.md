# Deephaven UI Examples

This repository contains example usages of [deephaven.ui](https://github.com/deephaven/deephaven-plugins/tree/main/plugins/ui), a Python framework for building reactive user interfaces in Deephaven.

## Contents

- **Example Applications** - Demonstrations of deephaven.ui capabilities and patterns
- **Custom Components** - Reusable components built with the `@ui.component` decorator

## Project Structure

Each example lives in its own subfolder with the following structure:

```
examples/
├── example-name/
│   ├── PLAN.md           # Design plan and implementation details
│   ├── README.md         # Usage instructions and screenshots
│   ├── example_name.py   # Main example code
│   └── ...               # Additional files as needed
```

## Getting Started

### Prerequisites

- [Deephaven](https://deephaven.io/) server running (v0.36.0+)
- `deephaven-plugin-ui` installed

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/deephaven/deephaven-ui-examples.git
   cd deephaven-ui-examples
   ```

2. Start your Deephaven server with the examples directory mounted:
   ```bash
   # Using Docker
   docker run -it --rm -p 10000:10000 \
     -v $(pwd):/data/examples \
     ghcr.io/deephaven/server:latest
   ```

3. Navigate to an example folder and follow its README for specific usage instructions.

### Running Examples

Each example can be run by importing it in the Deephaven console:

```python
# Example: Running a specific example
exec(open('/data/examples/example-name/example_name.py').read())
```

Or by copying the code directly into a Deephaven notebook.

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
|---------|-------------|
| *Coming soon* | *Examples will be listed here as they are added* |

## Resources

- [deephaven.ui Documentation](https://deephaven.io/core/docs/how-to-guides/user-interface/overview/)
- [Deephaven Community](https://deephaven.io/community/)

## License

Apache License 2.0
