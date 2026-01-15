# Hello World Counter

## Goal

Create a simple "Hello World" example that demonstrates the basics of deephaven.ui components and state management.

## Features

- A greeting text display
- A counter with increment/decrement buttons
- Demonstrates `use_state` hook for state management
- Shows basic component composition

## Implementation Details

- Use `@ui.component` decorator to define the main component
- Use `ui.use_state` for counter state management
- Use `ui.flex` for layout
- Use `ui.button` for interactive elements
- Use `ui.text` for display

## UI Layout

```
┌─────────────────────────────────┐
│      Hello, Deephaven UI!       │
│                                 │
│    Counter: 0                   │
│    [−]  [+]  [Reset]            │
│                                 │
└─────────────────────────────────┘
```

## Dependencies

- deephaven-plugin-ui
