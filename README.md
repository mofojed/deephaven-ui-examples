# Deephaven UI Examples

This repository contains example usages of [deephaven.ui](https://github.com/deephaven/deephaven-plugins/tree/main/plugins/ui), a Python framework for building reactive user interfaces in Deephaven.

## Contents

- **Example Applications** - Demonstrations of deephaven.ui capabilities and patterns
- **Custom Components** - Reusable components built with the `@ui.component` decorator

## Getting Started

### Prerequisites

- [Deephaven](https://deephaven.io/) server running
- `deephaven-plugin-ui` installed

### Usage

Import and run the examples in a Deephaven console or notebook.

## Custom Components

Custom components in this repository are defined using the `@ui.component` decorator:

```python
from deephaven import ui

@ui.component
def my_custom_component(name: str):
    return ui.text(f"Hello, {name}!")
```

## Resources

- [deephaven.ui Documentation](https://deephaven.io/core/docs/how-to-guides/user-interface/overview/)
- [Deephaven Community](https://deephaven.io/community/)

## License

Apache License 2.0
