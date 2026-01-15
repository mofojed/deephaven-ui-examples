"""Chart Builder UI component."""

from __future__ import annotations

from typing import TYPE_CHECKING

from deephaven import ui

from chart_config import ChartConfig, ChartType, LineShape
from make_chart import make_chart

if TYPE_CHECKING:
    from deephaven.table import Table


# Chart type options for the picker
CHART_TYPES: list[dict] = [
    {"key": "scatter", "label": "Scatter"},
    {"key": "line", "label": "Line"},
]

# Line shape options (spline is not supported by dx.line)
LINE_SHAPES: list[dict] = [
    {"key": "linear", "label": "Linear"},
    {"key": "vhv", "label": "Vertical-Horizontal-Vertical"},
    {"key": "hvh", "label": "Horizontal-Vertical-Horizontal"},
    {"key": "vh", "label": "Vertical-Horizontal"},
    {"key": "hv", "label": "Horizontal-Vertical"},
]


def _get_column_names(table: Table) -> list[str]:
    """Get column names from a table.
    
    Args:
        table: The table to get column names from.
        
    Returns:
        List of column names.
    """
    return [col.name for col in table.columns]


def _column_picker_items(columns: list[str], include_none: bool = True) -> list[dict]:
    """Create picker items from column names.
    
    Args:
        columns: List of column names.
        include_none: Whether to include a "None" option.
        
    Returns:
        List of picker item dicts.
    """
    items = []
    if include_none:
        items.append({"key": "", "label": "(None)"})
    items.extend({"key": col, "label": col} for col in columns)
    return items


@ui.component
def chart_builder(table: Table) -> ui.Element:
    """A component for interactively building charts from a table.
    
    Args:
        table: The source data table to create charts from.
        
    Returns:
        A UI element containing the chart builder interface.
    """
    # State for chart configuration
    chart_type, set_chart_type = ui.use_state("scatter")
    x_col, set_x_col = ui.use_state("")
    y_col, set_y_col = ui.use_state("")
    by_col, set_by_col = ui.use_state("")
    title, set_title = ui.use_state("")
    
    # Scatter-specific state
    size_col, set_size_col = ui.use_state("")
    symbol_col, set_symbol_col = ui.use_state("")
    color_col, set_color_col = ui.use_state("")
    
    # Line-specific state
    markers, set_markers = ui.use_state(False)
    line_shape, set_line_shape = ui.use_state("linear")
    
    # Get column names from table
    columns = _get_column_names(table)
    column_items = _column_picker_items(columns, include_none=False)
    optional_column_items = _column_picker_items(columns, include_none=True)
    
    # Build configuration from state
    config: ChartConfig = {
        "chart_type": chart_type,
    }
    
    if x_col:
        config["x"] = x_col
    if y_col:
        config["y"] = y_col
    if by_col:
        config["by"] = by_col
    if title:
        config["title"] = title
    
    # Add chart-type-specific options
    if chart_type == "scatter":
        if size_col:
            config["size"] = size_col
        if symbol_col:
            config["symbol"] = symbol_col
        if color_col:
            config["color"] = color_col
    elif chart_type == "line":
        config["markers"] = markers
        if line_shape:
            config["line_shape"] = line_shape
    
    # Create chart if we have valid x and y
    chart = None
    error_message = None
    
    if x_col and y_col:
        try:
            chart = make_chart(table, config)
        except Exception as e:
            error_message = str(e)
    
    # Build the UI
    return ui.flex(
        # Chart type selector
        ui.picker(
            *[ui.item(ct["label"], key=ct["key"]) for ct in CHART_TYPES],
            label="Chart Type",
            selected_key=chart_type,
            on_selection_change=set_chart_type,
        ),
        
        # Data mapping section
        ui.flex(
            ui.picker(
                *[ui.item(item["label"], key=item["key"]) for item in column_items],
                label="X Column",
                selected_key=x_col,
                on_selection_change=set_x_col,
            ),
            ui.picker(
                *[ui.item(item["label"], key=item["key"]) for item in column_items],
                label="Y Column",
                selected_key=y_col,
                on_selection_change=set_y_col,
            ),
            direction="row",
            gap="size-200",
        ),
        
        # Grouping section
        ui.picker(
            *[ui.item(item["label"], key=item["key"]) for item in optional_column_items],
            label="Group By",
            selected_key=by_col,
            on_selection_change=set_by_col,
        ),
        
        # Scatter-specific options
        ui.flex(
            ui.picker(
                *[ui.item(item["label"], key=item["key"]) for item in optional_column_items],
                label="Size Column",
                selected_key=size_col,
                on_selection_change=set_size_col,
            ),
            ui.picker(
                *[ui.item(item["label"], key=item["key"]) for item in optional_column_items],
                label="Symbol Column",
                selected_key=symbol_col,
                on_selection_change=set_symbol_col,
            ),
            ui.picker(
                *[ui.item(item["label"], key=item["key"]) for item in optional_column_items],
                label="Color Column",
                selected_key=color_col,
                on_selection_change=set_color_col,
            ),
            direction="row",
            gap="size-200",
        ) if chart_type == "scatter" else None,
        
        # Line-specific options
        ui.flex(
            ui.checkbox(
                "Show Markers",
                is_selected=markers,
                on_change=set_markers,
            ),
            ui.picker(
                *[ui.item(ls["label"], key=ls["key"]) for ls in LINE_SHAPES],
                label="Line Shape",
                selected_key=line_shape,
                on_selection_change=set_line_shape,
            ),
            direction="row",
            gap="size-200",
            align_items="end",
        ) if chart_type == "line" else None,
        
        # Title input
        ui.text_field(
            label="Chart Title",
            value=title,
            on_change=set_title,
        ),
        
        # Error message
        ui.text(error_message, UNSAFE_style={"color": "red"}) if error_message else None,
        
        # Chart preview
        chart if chart else ui.text("Select X and Y columns to preview chart"),
        
        direction="column",
        gap="size-200",
    )
