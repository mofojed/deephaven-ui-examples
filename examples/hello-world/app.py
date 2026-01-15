"""Hello World example demonstrating basic deephaven.ui usage.

This example shows:
- Component definition with @ui.component
- State management with use_state
- Event handling with buttons
- Basic layout with flex
"""

from deephaven import ui


@ui.component
def greeting(name: str = "Deephaven UI") -> ui.Element:
    """A simple greeting component.

    Args:
        name: The name to display in the greeting.

    Returns:
        A UI element displaying the greeting.
    """
    return ui.heading(f"Hello, {name}!", level=2)


@ui.component
def counter() -> ui.Element:
    """A counter component with increment, decrement, and reset buttons.

    Returns:
        A UI element with a counter and control buttons.
    """
    count, set_count = ui.use_state(0)

    def increment():
        set_count(count + 1)

    def decrement():
        set_count(count - 1)

    def reset():
        set_count(0)

    return ui.flex(
        ui.text(f"Counter: {count}"),
        ui.flex(
            ui.button("−", on_press=decrement, variant="secondary"),
            ui.button("+", on_press=increment, variant="primary"),
            ui.button("Reset", on_press=reset, variant="negative"),
            gap="size-100",
        ),
        direction="column",
        align_items="center",
        gap="size-200",
    )


@ui.component
def hello_world_app() -> ui.Element:
    """Main application component combining greeting and counter.

    Returns:
        The complete Hello World application UI.
    """
    return ui.flex(
        greeting(),
        counter(),
        direction="column",
        align_items="center",
        gap="size-400",
        UNSAFE_style={"padding": "var(--dh-size-space-400)"},
    )


# Create the panel when this file is executed
hello_world = hello_world_app()
