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

ChartType = Literal[
    "scatter", "line", "bar", "area", "pie",
    "histogram", "box", "violin", "strip", "density_heatmap",
    "candlestick", "ohlc"
]
LineShape = Literal["linear", "vhv", "hvh", "vh", "hv"]
Orientation = Literal["v", "h"]


class ChartConfig(TypedDict):
    """Configuration for chart creation."""
    chart_type: ChartType
    x: NotRequired[str]
    y: NotRequired[str]
    by: NotRequired[str | list[str]]  # Single column or list of columns
    title: NotRequired[str]
    # Scatter options
    size: NotRequired[str]
    symbol: NotRequired[str]
    color: NotRequired[str]
    # Line options
    markers: NotRequired[bool]
    line_shape: NotRequired[LineShape]
    # Bar options
    orientation: NotRequired[Orientation]
    # Pie options
    names: NotRequired[str]
    values: NotRequired[str]
    # Histogram options
    nbins: NotRequired[int]
    # OHLC/Candlestick options
    open: NotRequired[str]
    high: NotRequired[str]
    low: NotRequired[str]
    close: NotRequired[str]


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
    if chart_type in ("scatter", "line", "bar", "area"):
        if not config.get("x"):
            errors.append(f"x is required for {chart_type} charts")
        if not config.get("y"):
            errors.append(f"y is required for {chart_type} charts")
    elif chart_type == "pie":
        if not config.get("names"):
            errors.append("names is required for pie charts")
        if not config.get("values"):
            errors.append("values is required for pie charts")
    elif chart_type == "histogram":
        placeholder_msg = "Select X or Y column to preview chart"
    elif chart_type in ("candlestick", "ohlc"):
        # Histogram needs at least x OR y
        if not config.get("x") and not config.get("y"):
            errors.append("x or y is required for histogram charts")
    elif chart_type in ("box", "violin", "strip"):
        # These need x and y
        if not config.get("x"):
            errors.append(f"x is required for {chart_type} charts")
        if not config.get("y"):
            errors.append(f"y is required for {chart_type} charts")
    elif chart_type == "density_heatmap":
        if not config.get("x"):
            errors.append("x is required for density_heatmap charts")
        if not config.get("y"):
            errors.append("y is required for density_heatmap charts")
    elif chart_type in ("candlestick", "ohlc"):
        if not config.get("x"):
            errors.append(f"x is required for {chart_type} charts")
        if not config.get("open"):
            errors.append(f"open is required for {chart_type} charts")
        if not config.get("high"):
            errors.append(f"high is required for {chart_type} charts")
        if not config.get("low"):
            errors.append(f"low is required for {chart_type} charts")
        if not config.get("close"):
            errors.append(f"close is required for {chart_type} charts")
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


def _make_bar(table: Table, config: ChartConfig):
    """Create a bar chart."""
    kwargs = {"x": config["x"], "y": config["y"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    if config.get("orientation"):
        kwargs["orientation"] = config["orientation"]
    return dx.bar(table, **kwargs)


def _make_area(table: Table, config: ChartConfig):
    """Create an area chart."""
    kwargs = {"x": config["x"], "y": config["y"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.area(table, **kwargs)


def _make_pie(table: Table, config: ChartConfig):
    """Create a pie chart."""
    kwargs = {"names": config["names"], "values": config["values"]}
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.pie(table, **kwargs)


def _make_histogram(table: Table, config: ChartConfig):
    """Create a histogram."""
    kwargs = {}
    if config.get("x"):
        kwargs["x"] = config["x"]
    if config.get("y"):
        kwargs["y"] = config["y"]
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    if config.get("nbins"):
        kwargs["nbins"] = config["nbins"]
    return dx.histogram(table, **kwargs)


def _make_box(table: Table, config: ChartConfig):
    """Create a box plot."""
    kwargs = {"x": config["x"], "y": config["y"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.box(table, **kwargs)


def _make_violin(table: Table, config: ChartConfig):
    """Create a violin plot."""
    kwargs = {"x": config["x"], "y": config["y"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.violin(table, **kwargs)


def _make_strip(table: Table, config: ChartConfig):
    """Create a strip plot."""
    kwargs = {"x": config["x"], "y": config["y"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.strip(table, **kwargs)


def _make_density_heatmap(table: Table, config: ChartConfig):
    """Create a density heatmap."""
    kwargs = {"x": config["x"], "y": config["y"]}
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.density_heatmap(table, **kwargs)


def _make_candlestick(table: Table, config: ChartConfig):
    """Create a candlestick chart."""
    kwargs = {
        "x": config["x"],
        "open": config["open"],
        "high": config["high"],
        "low": config["low"],
        "close": config["close"],
    }
    return dx.candlestick(table, **kwargs)


def _make_ohlc(table: Table, config: ChartConfig):
    """Create an OHLC chart."""
    kwargs = {
        "x": config["x"],
        "open": config["open"],
        "high": config["high"],
        "low": config["low"],
        "close": config["close"],
    }
    return dx.ohlc(table, **kwargs)


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
    elif chart_type == "bar":
        return _make_bar(table, config)
    elif chart_type == "area":
        return _make_area(table, config)
    elif chart_type == "pie":
        return _make_pie(table, config)
    elif chart_type == "histogram":
        placeholder_msg = "Select X or Y column to preview chart"
    elif chart_type in ("candlestick", "ohlc"):
        return _make_histogram(table, config)
    elif chart_type == "box":
        return _make_box(table, config)
    elif chart_type == "violin":
        return _make_violin(table, config)
    elif chart_type == "strip":
        return _make_strip(table, config)
    elif chart_type == "density_heatmap":
        return _make_density_heatmap(table, config)
    elif chart_type == "candlestick":
        return _make_candlestick(table, config)
    elif chart_type == "ohlc":
        return _make_ohlc(table, config)
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")


# =============================================================================
# UI Component
# =============================================================================

CHART_TYPES = [
    {"key": "scatter", "label": "Scatter", "icon": "vsCircleFilled"},
    {"key": "line", "label": "Line", "icon": "vsGraphLine"},
    {"key": "bar", "label": "Bar", "icon": "vsGraphLeft"},
    {"key": "area", "label": "Area", "icon": "vsGraph"},
    {"key": "pie", "label": "Pie", "icon": "vsPieChart"},
    {"key": "histogram", "label": "Histogram", "icon": "vsGraphLeft"},
    {"key": "box", "label": "Box", "icon": "vsSymbolClass"},
    {"key": "violin", "label": "Violin", "icon": "vsSymbolClass"},
    {"key": "strip", "label": "Strip", "icon": "vsEllipsis"},
    {"key": "density_heatmap", "label": "Density Heatmap", "icon": "vsSymbolColor"},
    {"key": "candlestick", "label": "Candlestick", "icon": "vsGraphLine"},
    {"key": "ohlc", "label": "OHLC", "icon": "vsGraphLine"},
]

ORIENTATIONS = [
    {"key": "v", "label": "Vertical"},
    {"key": "h", "label": "Horizontal"},
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
    {"key": "ohlc_sample", "label": "OHLC Sample", "description": "Sample OHLC data for candlestick charts"},
]


def _create_ohlc_sample() -> Table:
    """Create a sample OHLC dataset for candlestick/ohlc charts."""
    from deephaven import new_table
    from deephaven.column import int_col, double_col, string_col

    # Sample OHLC data for multiple symbols over several days
    dates = list(range(1, 31)) * 3  # 30 days for 3 symbols
    symbols = ["AAPL"] * 30 + ["GOOGL"] * 30 + ["MSFT"] * 30

    # Generate realistic-looking OHLC data
    import random
    random.seed(42)

    opens, highs, lows, closes, volumes = [], [], [], [], []
    base_prices = {"AAPL": 150.0, "GOOGL": 140.0, "MSFT": 380.0}

    for i, sym in enumerate(symbols):
        day = dates[i]
        base = base_prices[sym] + (day - 15) * 0.5  # Slight upward trend
        open_price = base + random.uniform(-2, 2)
        close_price = open_price + random.uniform(-3, 3)
        high_price = max(open_price, close_price) + random.uniform(0, 2)
        low_price = min(open_price, close_price) - random.uniform(0, 2)
        volume = random.randint(1000000, 5000000)

        opens.append(round(open_price, 2))
        highs.append(round(high_price, 2))
        lows.append(round(low_price, 2))
        closes.append(round(close_price, 2))
        volumes.append(volume)

    return new_table([
        int_col("Day", dates),
        string_col("Symbol", symbols),
        double_col("Open", opens),
        double_col("High", highs),
        double_col("Low", lows),
        double_col("Close", closes),
        int_col("Volume", volumes),
    ])


def _load_dataset(name: str) -> Table:
    """Load a dataset by name."""
    if name == "ohlc_sample":
        return _create_ohlc_sample()

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
    by_cols, set_by_cols = ui.use_state([])  # List of group by columns
    title, set_title = ui.use_state("")
    
    # Scatter-specific state
    size_col, set_size_col = ui.use_state("")
    symbol_col, set_symbol_col = ui.use_state("")
    color_col, set_color_col = ui.use_state("")
    
    # Line-specific state
    markers, set_markers = ui.use_state(False)
    line_shape, set_line_shape = ui.use_state("linear")
    
    # Bar-specific state
    orientation, set_orientation = ui.use_state("v")
    
    # Pie-specific state
    names_col, set_names_col = ui.use_state("")
    values_col, set_values_col = ui.use_state("")
    
    # Histogram-specific state
    nbins, set_nbins = ui.use_state(10)
    
    # OHLC/Candlestick-specific state
    open_col, set_open_col = ui.use_state("")
    high_col, set_high_col = ui.use_state("")
    low_col, set_low_col = ui.use_state("")
    close_col, set_close_col = ui.use_state("")
    
    # Handlers for multi-select group by
    def update_by_col(index: int, col: str):
        """Update a group by column at a specific index."""
        if col == "":
            # Selected (None) - remove this and all subsequent columns
            set_by_cols(by_cols[:index])
        elif index < len(by_cols):
            # Update existing column
            new_cols = by_cols.copy()
            new_cols[index] = col
            set_by_cols(new_cols)
        else:
            # Add new column
            set_by_cols([*by_cols, col])
    
    def remove_by_col(index: int):
        """Remove a group by column at a specific index."""
        set_by_cols(by_cols[:index] + by_cols[index + 1:])
    
    # Get column names from table
    columns = _get_column_names(table)
    column_items = _column_picker_items(columns, include_none=False)
    optional_column_items = _column_picker_items(columns, include_none=True)
    
    # Available columns for group by at each position (exclude already selected except current)
    def get_by_picker_items(index: int) -> list[dict]:
        """Get picker items for a group by dropdown, excluding already selected columns."""
        selected_at_other_indices = [c for i, c in enumerate(by_cols) if i != index]
        available = [c for c in columns if c not in selected_at_other_indices]
        return _column_picker_items(available, include_none=True)
    
    # Build configuration from state
    config: ChartConfig = {"chart_type": chart_type}
    
    # X/Y charts (scatter, line, bar, area)
    if chart_type in ("scatter", "line", "bar", "area"):
        if x_col:
            config["x"] = x_col
        if y_col:
            config["y"] = y_col
        if by_cols:
            # Pass single string if one column, list if multiple
            config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols
    
    # Pie chart uses names/values
    if chart_type == "pie":
        if names_col:
            config["names"] = names_col
        if values_col:
            config["values"] = values_col
    
    # Histogram config
    if chart_type == "histogram":
        if x_col:
            config["x"] = x_col
        if y_col:
            config["y"] = y_col
        if by_cols:
            config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols
        if nbins:
            config["nbins"] = nbins
    
    # Box, violin, strip, density_heatmap config
    if chart_type in ("box", "violin", "strip", "density_heatmap"):
        if x_col:
            config["x"] = x_col
        if y_col:
            config["y"] = y_col
        # Group by for box, violin, strip (not density_heatmap)
        if chart_type in ("box", "violin", "strip") and by_cols:
            config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols
    
    # Candlestick/OHLC config
    if chart_type in ("candlestick", "ohlc"):
        if x_col:
            config["x"] = x_col
        if open_col:
            config["open"] = open_col
        if high_col:
            config["high"] = high_col
        if low_col:
            config["low"] = low_col
        if close_col:
            config["close"] = close_col
    
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
    elif chart_type == "bar":
        if orientation:
            config["orientation"] = orientation
    
    # Candlestick/OHLC config
    if chart_type in ("candlestick", "ohlc"):
        if x_col:
            config["x"] = x_col
        if open_col:
            config["open"] = open_col
        if high_col:
            config["high"] = high_col
        if low_col:
            config["low"] = low_col
        if close_col:
            config["close"] = close_col
    
    # Determine if chart can be created
    can_create_chart = False
    if chart_type in ("scatter", "line", "bar", "area"):
        can_create_chart = bool(x_col and y_col)
    elif chart_type == "pie":
        can_create_chart = bool(names_col and values_col)
    elif chart_type == "histogram":
        placeholder_msg = "Select X or Y column to preview chart"
    elif chart_type in ("candlestick", "ohlc"):
        can_create_chart = bool(x_col or y_col)  # Only need one
    elif chart_type in ("box", "violin", "strip", "density_heatmap"):
        can_create_chart = bool(x_col and y_col)
    elif chart_type in ("candlestick", "ohlc"):
        can_create_chart = bool(x_col and open_col and high_col and low_col and close_col)
    
    # Create chart if we have valid configuration
    chart = None
    error_message = None
    
    if can_create_chart:
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
            
            # X and Y columns side by side (for scatter, line, bar, area, box, violin, strip, density_heatmap)
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
            ) if chart_type in ("scatter", "line", "bar", "area", "box", "violin", "strip", "density_heatmap") else None,
            
            # X and/or Y for histogram (only one required)
            ui.flex(
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in optional_column_items],
                    label="X",
                    selected_key=x_col,
                    on_selection_change=set_x_col,
                    flex_grow=1,
                ),
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in optional_column_items],
                    label="Y",
                    selected_key=y_col,
                    on_selection_change=set_y_col,
                    flex_grow=1,
                ),
                direction="row",
                gap="size-100",
                width="100%",
            ) if chart_type == "histogram" else None,
            
            # X column for candlestick/ohlc (usually timestamp/date)
            ui.picker(
                *[ui.item(item["label"], key=item["key"]) for item in column_items],
                label="X (Date/Time)",
                selected_key=x_col,
                on_selection_change=set_x_col,
                width="100%",
            ) if chart_type in ("candlestick", "ohlc") else None,
            
            # OHLC columns for candlestick/ohlc
            ui.flex(
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in column_items],
                    label="Open",
                    selected_key=open_col,
                    on_selection_change=set_open_col,
                    flex_grow=1,
                ),
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in column_items],
                    label="High",
                    selected_key=high_col,
                    on_selection_change=set_high_col,
                    flex_grow=1,
                ),
                direction="row",
                gap="size-100",
                width="100%",
            ) if chart_type in ("candlestick", "ohlc") else None,
            ui.flex(
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in column_items],
                    label="Low",
                    selected_key=low_col,
                    on_selection_change=set_low_col,
                    flex_grow=1,
                ),
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in column_items],
                    label="Close",
                    selected_key=close_col,
                    on_selection_change=set_close_col,
                    flex_grow=1,
                ),
                direction="row",
                gap="size-100",
                width="100%",
            ) if chart_type in ("candlestick", "ohlc") else None,
            
            # Names and Values columns (for pie)
            ui.flex(
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in column_items],
                    label="Names",
                    selected_key=names_col,
                    on_selection_change=set_names_col,
                    flex_grow=1,
                ),
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in column_items],
                    label="Values",
                    selected_key=values_col,
                    on_selection_change=set_values_col,
                    flex_grow=1,
                ),
                direction="row",
                gap="size-100",
                width="100%",
            ) if chart_type == "pie" else None,
            
            # Group by (for charts that support it - not pie, density_heatmap, or financial)
            ui.flex(
                # Show dropdowns for each selected column plus one empty one
                *[ui.flex(
                    ui.picker(
                        *[ui.item(item["label"], key=item["key"]) for item in get_by_picker_items(i)],
                        label="Group By" if i == 0 else f"Group {i + 1}",
                        selected_key=by_cols[i] if i < len(by_cols) else "",
                        on_selection_change=lambda col, idx=i: update_by_col(idx, col),
                        flex_grow=1,
                    ),
                    # Trash button to remove (only show for selected columns, not the empty "add" picker)
                    ui.action_button(
                        ui.icon("vsTrash"),
                        on_press=(lambda idx: lambda: remove_by_col(idx))(i),
                        is_quiet=True,
                        aria_label=f"Remove group {i + 1}",
                    ) if i < len(by_cols) else None,
                    direction="row",
                    gap="size-100",
                    align_items="end",
                    width="100%",
                ) for i in range(len(by_cols) + 1)],  # +1 for the "add new" picker
                direction="column",
                gap="size-100",
                width="100%",
            ) if chart_type not in ("pie", "density_heatmap", "candlestick", "ohlc") else None,
            
            # Histogram-specific options
            ui.number_field(
                label="Number of Bins",
                value=nbins,
                on_change=set_nbins,
                min_value=1,
                max_value=1000,
                width="100%",
            ) if chart_type == "histogram" else None,
            
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
            
            # Bar-specific options
            ui.picker(
                *[ui.item(o["label"], key=o["key"]) for o in ORIENTATIONS],
                label="Orientation",
                selected_key=orientation,
                on_selection_change=set_orientation,
                width="100%",
            ) if chart_type == "bar" else None,
            
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
    
    # Chart area - update placeholder message based on chart type
    if chart_type == "pie":
        placeholder_msg = "Select Names and Values columns to preview chart"
    elif chart_type == "histogram":
        placeholder_msg = "Select X or Y column to preview chart"
    elif chart_type in ("candlestick", "ohlc"):
        placeholder_msg = "Select X and OHLC columns to preview chart"
    else:
        placeholder_msg = "Select X and Y columns to preview chart"
    
    chart_area = ui.view(
        ui.text(error_message, UNSAFE_style={"color": "var(--spectrum-negative-color-900)"}) if error_message 
        else chart if chart 
        else ui.flex(
            ui.text(placeholder_msg, UNSAFE_style={"color": "var(--spectrum-gray-600)"}),
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
    by_cols, set_by_cols = ui.use_state([])  # List of group by columns
    title, set_title = ui.use_state("")
    
    # Scatter-specific state
    size_col, set_size_col = ui.use_state("")
    symbol_col, set_symbol_col = ui.use_state("")
    color_col, set_color_col = ui.use_state("")
    
    # Line-specific state
    markers, set_markers = ui.use_state(False)
    line_shape, set_line_shape = ui.use_state("linear")
    
    # Bar-specific state
    orientation, set_orientation = ui.use_state("v")
    
    # Pie-specific state
    names_col, set_names_col = ui.use_state("")
    values_col, set_values_col = ui.use_state("")
    
    # Histogram-specific state
    nbins, set_nbins = ui.use_state(10)
    
    # OHLC/Candlestick-specific state
    open_col, set_open_col = ui.use_state("")
    high_col, set_high_col = ui.use_state("")
    low_col, set_low_col = ui.use_state("")
    close_col, set_close_col = ui.use_state("")
    
    # Handlers for multi-select group by
    def update_by_col(index: int, col: str):
        """Update a group by column at a specific index."""
        if col == "":
            # Selected (None) - remove this and all subsequent columns
            set_by_cols(by_cols[:index])
        elif index < len(by_cols):
            # Update existing column
            new_cols = by_cols.copy()
            new_cols[index] = col
            set_by_cols(new_cols)
        else:
            # Add new column
            set_by_cols([*by_cols, col])
    
    def remove_by_col(index: int):
        """Remove a group by column at a specific index."""
        set_by_cols(by_cols[:index] + by_cols[index + 1:])
    
    # Handler to change dataset and reset column selections
    def handle_dataset_change(new_dataset: str):
        set_dataset_name(new_dataset)
        # Reset all column selections when dataset changes
        set_x_col("")
        set_y_col("")
        set_by_cols([])
        set_size_col("")
        set_symbol_col("")
        set_color_col("")
        set_names_col("")
        set_values_col("")
        set_open_col("")
        set_high_col("")
        set_low_col("")
        set_close_col("")
    
    # Get column names from table
    columns = _get_column_names(table)
    column_items = _column_picker_items(columns, include_none=False)
    optional_column_items = _column_picker_items(columns, include_none=True)
    
    # Available columns for group by at each position (exclude already selected except current)
    def get_by_picker_items(index: int) -> list[dict]:
        """Get picker items for a group by dropdown, excluding already selected columns."""
        selected_at_other_indices = [c for i, c in enumerate(by_cols) if i != index]
        available = [c for c in columns if c not in selected_at_other_indices]
        return _column_picker_items(available, include_none=True)
    
    # Build configuration from state
    config: ChartConfig = {"chart_type": chart_type}
    
    if x_col:
        config["x"] = x_col
    if y_col:
        config["y"] = y_col
    if by_cols:
        # Pass single string if one column, list if multiple
        config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols
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
    elif chart_type == "bar":
        config["orientation"] = orientation
    elif chart_type == "pie":
        if names_col:
            config["names"] = names_col
        if values_col:
            config["values"] = values_col
    elif chart_type == "histogram":
        if nbins:
            config["nbins"] = nbins
    
    # Candlestick/OHLC config
    if chart_type in ("candlestick", "ohlc"):
        if x_col:
            config["x"] = x_col
        if open_col:
            config["open"] = open_col
        if high_col:
            config["high"] = high_col
        if low_col:
            config["low"] = low_col
        if close_col:
            config["close"] = close_col
    
    # Determine if chart can be created
    can_create_chart = False
    if chart_type in ("scatter", "line", "bar", "area"):
        can_create_chart = bool(x_col and y_col)
    elif chart_type == "pie":
        can_create_chart = bool(names_col and values_col)
    elif chart_type == "histogram":
        can_create_chart = bool(x_col or y_col)  # Only need one
    elif chart_type in ("box", "violin", "strip", "density_heatmap"):
        can_create_chart = bool(x_col and y_col)
    elif chart_type in ("candlestick", "ohlc"):
        can_create_chart = bool(x_col and open_col and high_col and low_col and close_col)
    
    chart = None
    error_message = None
    
    if can_create_chart:
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
            
            # X and Y columns side by side (for non-pie charts)
            # X and Y columns side by side (for scatter, line, bar, area, box, violin, strip, density_heatmap)
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
            ) if chart_type in ("scatter", "line", "bar", "area", "box", "violin", "strip", "density_heatmap") else None,
            
            # X and/or Y for histogram (only one required)
            ui.flex(
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in optional_column_items],
                    label="X",
                    selected_key=x_col,
                    on_selection_change=set_x_col,
                    flex_grow=1,
                ),
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in optional_column_items],
                    label="Y",
                    selected_key=y_col,
                    on_selection_change=set_y_col,
                    flex_grow=1,
                ),
                direction="row",
                gap="size-100",
                width="100%",
            ) if chart_type == "histogram" else None,
            
            # X column for candlestick/ohlc (usually timestamp/date)
            ui.picker(
                *[ui.item(item["label"], key=item["key"]) for item in column_items],
                label="X (Date/Time)",
                selected_key=x_col,
                on_selection_change=set_x_col,
                width="100%",
            ) if chart_type in ("candlestick", "ohlc") else None,
            
            # OHLC columns for candlestick/ohlc
            ui.flex(
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in column_items],
                    label="Open",
                    selected_key=open_col,
                    on_selection_change=set_open_col,
                    flex_grow=1,
                ),
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in column_items],
                    label="High",
                    selected_key=high_col,
                    on_selection_change=set_high_col,
                    flex_grow=1,
                ),
                direction="row",
                gap="size-100",
                width="100%",
            ) if chart_type in ("candlestick", "ohlc") else None,
            ui.flex(
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in column_items],
                    label="Low",
                    selected_key=low_col,
                    on_selection_change=set_low_col,
                    flex_grow=1,
                ),
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in column_items],
                    label="Close",
                    selected_key=close_col,
                    on_selection_change=set_close_col,
                    flex_grow=1,
                ),
                direction="row",
                gap="size-100",
                width="100%",
            ) if chart_type in ("candlestick", "ohlc") else None,
            
            # Names and Values columns (for pie charts)
            ui.flex(
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in column_items],
                    label="Names",
                    selected_key=names_col,
                    on_selection_change=set_names_col,
                    flex_grow=1,
                ),
                ui.picker(
                    *[ui.item(item["label"], key=item["key"]) for item in column_items],
                    label="Values",
                    selected_key=values_col,
                    on_selection_change=set_values_col,
                    flex_grow=1,
                ),
                direction="row",
                gap="size-100",
                width="100%",
            ) if chart_type == "pie" else None,
            
            # Group by (for charts that support it - not pie, density_heatmap, or OHLC charts)
            ui.flex(
                # Show dropdowns for each selected column plus one empty one
                *[ui.flex(
                    ui.picker(
                        *[ui.item(item["label"], key=item["key"]) for item in get_by_picker_items(i)],
                        label="Group By" if i == 0 else f"Group {i + 1}",
                        selected_key=by_cols[i] if i < len(by_cols) else "",
                        on_selection_change=lambda col, idx=i: update_by_col(idx, col),
                        flex_grow=1,
                    ),
                    # Trash button to remove (only show for selected columns, not the empty "add" picker)
                    ui.action_button(
                        ui.icon("vsTrash"),
                        on_press=(lambda idx: lambda: remove_by_col(idx))(i),
                        is_quiet=True,
                        aria_label=f"Remove group {i + 1}",
                    ) if i < len(by_cols) else None,
                    direction="row",
                    gap="size-100",
                    align_items="end",
                    width="100%",
                ) for i in range(len(by_cols) + 1)],  # +1 for the "add new" picker
                direction="column",
                gap="size-100",
                width="100%",
            ) if chart_type not in ("pie", "density_heatmap", "candlestick", "ohlc") else None,
            
            # Histogram-specific options
            ui.number_field(
                label="Number of Bins",
                value=nbins,
                on_change=set_nbins,
                min_value=1,
                max_value=1000,
                width="100%",
            ) if chart_type == "histogram" else None,
            
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
            
            # Bar-specific options
            ui.picker(
                *[ui.item(o["label"], key=o["key"]) for o in ORIENTATIONS],
                label="Orientation",
                selected_key=orientation,
                on_selection_change=set_orientation,
                width="100%",
            ) if chart_type == "bar" else None,
            
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
    
    # Chart area - update placeholder message based on chart type
    if chart_type == "pie":
        placeholder_msg = "Select Names and Values columns to preview chart"
    elif chart_type == "histogram":
        placeholder_msg = "Select X or Y column to preview chart"
    elif chart_type in ("candlestick", "ohlc"):
        placeholder_msg = "Select X and OHLC columns to preview chart"
    else:
        placeholder_msg = "Select X and Y columns to preview chart"
    
    chart_area = ui.view(
        ui.text(error_message, UNSAFE_style={"color": "var(--spectrum-negative-color-900)"}) if error_message 
        else chart if chart 
        else ui.flex(
            ui.text(placeholder_msg, UNSAFE_style={"color": "var(--spectrum-gray-600)"}),
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
