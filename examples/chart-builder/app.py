"""Chart Builder example application.

This example demonstrates a chart_builder component which allows users
to interactively create charts from a Deephaven table.

All code is in a single file to work with Deephaven's exec() pattern.
"""

from __future__ import annotations

from typing import Literal, TypedDict, NotRequired, TYPE_CHECKING

import deephaven.plot.express as dx
from deephaven import ui

if TYPE_CHECKING:
    from deephaven.table import Table


# =============================================================================
# Type Definitions
# =============================================================================

ChartType = Literal["scatter", "line"]
LineShape = Literal["linear", "vhv", "hvh", "vh", "hv"]


class ChartConfig(TypedDict):
    """Configuration for chart creation."""
    chart_type: ChartType
    x: NotRequired[str]
    y: NotRequired[str]
    by: NotRequired[str]
    title: NotRequired[str]
    # Scatter options
    size: NotRequired[str]
    symbol: NotRequired[str]
    color: NotRequired[str]
    # Line options
    markers: NotRequired[bool]
    line_shape: NotRequired[LineShape]


# =============================================================================
# Chart Creation Functions
# =============================================================================

def _validate_config(config: ChartConfig) -> list[str]:
    """Validate a chart configuration."""
    errors = []
    chart_type = config.get("chart_type")
    if not chart_type:
        errors.append("chart_type is required")
        return errors
    if chart_type in ("scatter", "line"):
        if not config.get("x"):
            errors.append(f"x is required for {chart_type} charts")
        if not config.get("y"):
            errors.append(f"y is required for {chart_type} charts")
    return errors


def _make_scatter(table: Table, config: ChartConfig):
    """Create a scatter plot."""
    kwargs = {"x": config["x"], "y": config["y"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("size"):
        kwargs["size"] = config["size"]
    if config.get("symbol"):
        kwargs["symbol"] = config["symbol"]
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.scatter(table, **kwargs)


def _make_line(table: Table, config: ChartConfig):
    """Create a line plot."""
    kwargs = {"x": config["x"], "y": config["y"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    if config.get("markers") is not None:
        kwargs["markers"] = config["markers"]
    if config.get("line_shape"):
        kwargs["line_shape"] = config["line_shape"]
    return dx.line(table, **kwargs)


def make_chart(table: Table, config: ChartConfig):
    """Create a chart from the given table and configuration."""
    errors = _validate_config(config)
    if errors:
        raise ValueError(f"Invalid configuration: {'; '.join(errors)}")
    
    chart_type = config["chart_type"]
    if chart_type == "scatter":
        return _make_scatter(table, config)
    elif chart_type == "line":
        return _make_line(table, config)
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")


# =============================================================================
# UI Component
# =============================================================================

CHART_TYPES = [
    {"key": "scatter", "label": "Scatter", "icon": "vsCircleFilled"},
    {"key": "line", "label": "Line", "icon": "vsGraphLine"},
]

LINE_SHAPES = [
    {"key": "linear", "label": "Linear"},
    {"key": "vhv", "label": "Vertical-Horizontal-Vertical"},
    {"key": "hvh", "label": "Horizontal-Vertical-Horizontal"},
    {"key": "vh", "label": "Vertical-Horizontal"},
    {"key": "hv", "label": "Horizontal-Vertical"},
]

# Available datasets from dx.data
DATASETS = [
    {"key": "iris", "label": "Iris", "description": "Iris flower measurements"},
    {"key": "stocks", "label": "Stocks", "description": "Stock price data"},
    {"key": "tips", "label": "Tips", "description": "Restaurant tips data"},
    {"key": "gapminder", "label": "Gapminder", "description": "World development indicators"},
    {"key": "wind", "label": "Wind", "description": "Wind speed and direction"},
    {"key": "election", "label": "Election", "description": "Election results"},
    {"key": "fish_market", "label": "Fish Market", "description": "Fish market sales"},
    {"key": "jobs", "label": "Jobs", "description": "Employment data"},
    {"key": "marketing", "label": "Marketing", "description": "Marketing campaign data"},
]


def _load_dataset(name: str) -> Table:
    """Load a dataset by name."""
    loaders = {
        "iris": dx.data.iris,
        "stocks": dx.data.stocks,
        "tips": dx.data.tips,
        "gapminder": dx.data.gapminder,
        "wind": dx.data.wind,
        "election": dx.data.election,
        "fish_market": dx.data.fish_market,
        "jobs": dx.data.jobs,
        "marketing": dx.data.marketing,
    }
    return loaders[name]()


def _get_column_names(table: Table) -> list[str]:
    """Get column names from a table."""
    return [col.name for col in table.columns]


def _column_picker_items(columns: list[str], include_none: bool = True) -> list[dict]:
    """Create picker items from column names."""
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
    config: ChartConfig = {"chart_type": chart_type}
    
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
    
    # Controls panel - compact sidebar
    controls = ui.view(
        ui.flex(
            # Chart type with icons
            ui.picker(
                *[ui.item(
                    ui.icon(ct["icon"]),
                    ct["label"],
                    key=ct["key"],
                    text_value=ct["label"],
                ) for ct in CHART_TYPES],
                label="Chart Type",
                selected_key=chart_type,
                on_selection_change=set_chart_type,
                width="100%",
            ),
            
            # X and Y columns side by side
            ui.flex(
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in column_items],
                    label="X",
                    selected_key=x_col,
                    on_selection_change=set_x_col,
                    flex_grow=1,
                ),
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in column_items],
                    label="Y",
                    selected_key=y_col,
                    on_selection_change=set_y_col,
                    flex_grow=1,
                ),
                direction="row",
                gap="size-100",
                width="100%",
            ),
            
            # Group by
            ui.picker(
                *[ui.item(item["label"], key=item["key"]) for item in optional_column_items],
                label="Group By",
                selected_key=by_col,
                on_selection_change=set_by_col,
                width="100%",
            ),
            
            # Scatter-specific options
            ui.flex(
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in optional_column_items],
                    label="Size",
                    selected_key=size_col,
                    on_selection_change=set_size_col,
                    flex_grow=1,
                ),
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in optional_column_items],
                    label="Color",
                    selected_key=color_col,
                    on_selection_change=set_color_col,
                    flex_grow=1,
                ),
                direction="row",
                gap="size-100",
                width="100%",
            ) if chart_type == "scatter" else None,
            
            # Line-specific options
            ui.flex(
                ui.checkbox(
                    "Markers",
                    is_selected=markers,
                    on_change=set_markers,
                ),
                ui.picker(
                    *[ui.item(ls["label"], key=ls["key"]) for ls in LINE_SHAPES],
                    label="Line Shape",
                    selected_key=line_shape,
                    on_selection_change=set_line_shape,
                    flex_grow=1,
                ),
                direction="row",
                gap="size-100",
                align_items="end",
                width="100%",
            ) if chart_type == "line" else None,
            
            # Title
            ui.text_field(
                label="Title",
                value=title,
                on_change=set_title,
                width="100%",
            ),
            
            direction="column",
            gap="size-100",
        ),
        padding="size-200",
        background_color="gray-100",
        border_radius="medium",
        min_width="size-3000",
    )
    
    # Chart area
    chart_area = ui.view(
        ui.text(error_message, UNSAFE_style={"color": "var(--spectrum-negative-color-900)"}) if error_message 
        else chart if chart 
        else ui.flex(
            ui.text("Select X and Y columns to preview chart", UNSAFE_style={"color": "var(--spectrum-gray-600)"}),
            align_items="center",
            justify_content="center",
            height="100%",
        ),
        flex_grow=1,
        min_height="size-3000",
    )
    
    # Main layout - controls on left, chart on right
    return ui.flex(
        controls,
        chart_area,
        direction="row",
        gap="size-200",
        height="100%",
    )


@ui.component
def chart_builder_app() -> ui.Element:
    """A complete chart builder app with dataset selection.
    
    Returns:
        A UI element containing the chart builder with dataset selector.
    """
    dataset_name, set_dataset_name = ui.use_state("iris")
    
    # Load the selected dataset
    table = ui.use_memo(lambda: _load_dataset(dataset_name), [dataset_name])
    
    # Chart configuration state
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
    
    # Handler to change dataset and reset column selections
    def handle_dataset_change(new_dataset: str):
        set_dataset_name(new_dataset)
        # Reset all column selections when dataset changes
        set_x_col("")
        set_y_col("")
        set_by_col("")
        set_size_col("")
        set_symbol_col("")
        set_color_col("")
    
    # Get column names from table
    columns = _get_column_names(table)
    column_items = _column_picker_items(columns, include_none=False)
    optional_column_items = _column_picker_items(columns, include_none=True)
    
    # Build configuration from state
    config: ChartConfig = {"chart_type": chart_type}
    
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
    
    # Controls panel - compact sidebar
    controls = ui.view(
        ui.flex(
            # Dataset selector
            ui.picker(
                *[ui.item(ds["label"], key=ds["key"], text_value=ds["label"]) for ds in DATASETS],
                label="Dataset",
                selected_key=dataset_name,
                on_selection_change=handle_dataset_change,
                width="100%",
            ),
            
            # Divider
            ui.divider(),
            
            # Chart type with icons
            ui.picker(
                *[ui.item(
                    ui.icon(ct["icon"]),
                    ct["label"],
                    key=ct["key"],
                    text_value=ct["label"],
                ) for ct in CHART_TYPES],
                label="Chart Type",
                selected_key=chart_type,
                on_selection_change=set_chart_type,
                width="100%",
            ),
            
            # X and Y columns side by side
            ui.flex(
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in column_items],
                    label="X",
                    selected_key=x_col,
                    on_selection_change=set_x_col,
                    flex_grow=1,
                ),
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in column_items],
                    label="Y",
                    selected_key=y_col,
                    on_selection_change=set_y_col,
                    flex_grow=1,
                ),
                direction="row",
                gap="size-100",
                width="100%",
            ),
            
            # Group by
            ui.picker(
                *[ui.item(item["label"], key=item["key"]) for item in optional_column_items],
                label="Group By",
                selected_key=by_col,
                on_selection_change=set_by_col,
                width="100%",
            ),
            
            # Scatter-specific options
            ui.flex(
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in optional_column_items],
                    label="Size",
                    selected_key=size_col,
                    on_selection_change=set_size_col,
                    flex_grow=1,
                ),
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in optional_column_items],
                    label="Color",
                    selected_key=color_col,
                    on_selection_change=set_color_col,
                    flex_grow=1,
                ),
                direction="row",
                gap="size-100",
                width="100%",
            ) if chart_type == "scatter" else None,
            
            # Line-specific options
            ui.flex(
                ui.checkbox(
                    "Markers",
                    is_selected=markers,
                    on_change=set_markers,
                ),
                ui.picker(
                    *[ui.item(ls["label"], key=ls["key"]) for ls in LINE_SHAPES],
                    label="Line Shape",
                    selected_key=line_shape,
                    on_selection_change=set_line_shape,
                    flex_grow=1,
                ),
                direction="row",
                gap="size-100",
                align_items="end",
                width="100%",
            ) if chart_type == "line" else None,
            
            # Title
            ui.text_field(
                label="Title",
                value=title,
                on_change=set_title,
                width="100%",
            ),
            
            direction="column",
            gap="size-100",
        ),
        padding="size-200",
        background_color="gray-100",
        border_radius="medium",
        min_width="size-3000",
    )
    
    # Chart area
    chart_area = ui.view(
        ui.text(error_message, UNSAFE_style={"color": "var(--spectrum-negative-color-900)"}) if error_message 
        else chart if chart 
        else ui.flex(
            ui.text("Select X and Y columns to preview chart", UNSAFE_style={"color": "var(--spectrum-gray-600)"}),
            align_items="center",
            justify_content="center",
            height="100%",
        ),
        flex_grow=1,
        min_height="size-3000",
    )
    
    # Main layout - controls on left, chart on right
    return ui.flex(
        controls,
        chart_area,
        direction="row",
        gap="size-200",
        height="100%",
    )


# =============================================================================
# Example Usage
# =============================================================================

# Main app with dataset selector
chart_builder_demo = chart_builder_app()

# Also export individual chart builders for specific datasets
iris_chart_builder = chart_builder(dx.data.iris())
stocks_chart_builder = chart_builder(dx.data.stocks())
