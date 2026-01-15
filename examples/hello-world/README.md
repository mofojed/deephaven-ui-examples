# Hello World Counter

A simple example demonstrating the basics of deephaven.ui components and state management.

## Features

- Greeting text display
- Interactive counter with increment/decrement buttons
- State management with `use_state` hook
- Basic component composition with `@ui.component`

## Usage

```python
exec(open('/data/examples/hello-world/app.py').read())
```

Or run from the project root:

```bash
python scripts/run_example.py hello-world
```

## How It Works

This example demonstrates:

1. **Component Definition**: Using `@ui.component` decorator to create reusable components
2. **State Management**: Using `ui.use_state()` to manage reactive state
3. **Event Handling**: Button click handlers that update state
4. **Layout**: Using `ui.flex` for organizing components

### Key Code Patterns

```python
@ui.component
def counter():
    count, set_count = ui.use_state(0)

    return ui.flex(
        ui.text(f"Count: {count}"),
        ui.button("Increment", on_press=lambda: set_count(count + 1)),
        direction="column"
    )
```
