# Agent Instructions

This file provides guidance for AI coding agents working on this repository.

## Repository Overview

This repository contains example applications and custom components built with [deephaven.ui](https://github.com/deephaven/deephaven-plugins/tree/main/plugins/ui), a Python framework for building reactive user interfaces in Deephaven.

## Project Structure

```
deephaven-ui-examples/
├── README.md          # Project documentation
├── AGENTS.md          # This file - agent instructions
```

## Key Conventions

### Custom Components

- Custom components are defined using the `@ui.component` decorator
- Component functions should have clear type hints for parameters
- Follow the pattern:

```python
from deephaven import ui

@ui.component
def component_name(param: type) -> ui.Element:
    # Component logic here
    return ui.element(...)
```

### Code Style

- Use Python type hints
- Include docstrings for components explaining their purpose and parameters
- Follow PEP 8 style guidelines

## Maintenance Tasks

When making changes to this repository:

1. **Update README.md** - Keep the contents section and examples current
2. **Update AGENTS.md** - Add new directories/files to the project structure
3. **Document new components** - Add docstrings and update relevant documentation

## Resources

- [deephaven.ui Documentation](https://deephaven.io/core/docs/how-to-guides/user-interface/overview/)
- [deephaven.ui GitHub](https://github.com/deephaven/deephaven-plugins/tree/main/plugins/ui)
