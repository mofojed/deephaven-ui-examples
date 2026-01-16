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
# Pre-defined Map Centers
# =============================================================================

# Center coordinates for the outages dataset (Minneapolis-St. Paul metro area)
OUTAGE_CENTER = {"lat": 44.97, "lon": -93.17}

# Center coordinates for the flights dataset (Central Canada)
FLIGHT_CENTER = {"lat": 50.0, "lon": -100.0}

# Pre-defined center options for the UI picker
MAP_CENTER_PRESETS = [
    {"key": "none", "label": "(None - Auto)"},
    {"key": "outages", "label": "Outages Center (Minneapolis)"},
    {"key": "flights", "label": "Flights Center (Canada)"},
    {"key": "custom", "label": "Custom..."},
]

# Map style options for tile-based maps
MAP_STYLE_OPTIONS = [
    {"key": "", "label": "(Default)"},
    {"key": "open-street-map", "label": "Open Street Map"},
    {"key": "carto-positron", "label": "Carto Positron (Light)"},
    {"key": "carto-darkmatter", "label": "Carto Dark Matter"},
    {"key": "carto-voyager", "label": "Carto Voyager"},
    {"key": "streets", "label": "Streets"},
    {"key": "outdoors", "label": "Outdoors"},
    {"key": "light", "label": "Light"},
    {"key": "dark", "label": "Dark"},
    {"key": "satellite", "label": "Satellite"},
    {"key": "satellite-streets", "label": "Satellite Streets"},
]


# =============================================================================
# Type Definitions
# =============================================================================

ChartType = Literal[
    "scatter",
    "line",
    "bar",
    "area",
    "pie",
    "histogram",
    "box",
    "violin",
    "strip",
    "density_heatmap",
    "candlestick",
    "ohlc",
    "treemap",
    "sunburst",
    "icicle",
    "funnel",
    "funnel_area",
    "scatter_3d",
    "line_3d",
    "scatter_polar",
    "line_polar",
    "scatter_ternary",
    "line_ternary",
    "timeline",
    "scatter_geo",
    "line_geo",
    "scatter_map",
    "line_map",
    "density_map",
]
LineShape = Literal["linear", "vhv", "hvh", "vh", "hv"]
Orientation = Literal["v", "h"]
# Distribution chart modes
BoxMode = Literal["group", "overlay"]
ViolinMode = Literal["group", "overlay"]
StripMode = Literal["group", "overlay"]
HistBarMode = Literal["group", "overlay", "relative"]
BarNorm = Literal["fraction", "percent"]
HistNorm = Literal["probability", "percent", "density", "probability density"]
HistFunc = Literal[
    "count",
    "sum",
    "avg",
    "min",
    "max",
    "count_distinct",
    "median",
    "std",
    "var",
    "abs_sum",
]
PointsOption = Literal["outliers", "suspectedoutliers", "all"]
MarginalType = Literal["histogram", "box", "violin", "rug"]


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
    histfunc: NotRequired[str]  # Aggregation function for histogram
    histnorm: NotRequired[str]  # Normalization for histogram
    barnorm: NotRequired[str]  # Bar normalization
    hist_barmode: NotRequired[str]  # Bar mode for histogram (group, overlay, relative)
    cumulative: NotRequired[bool]  # Cumulative histogram
    range_bins: NotRequired[list[int]]  # Range for bins
    # Box/Violin/Strip options
    boxmode: NotRequired[str]  # group or overlay
    violinmode: NotRequired[str]  # group or overlay
    stripmode: NotRequired[str]  # group or overlay
    points: NotRequired[str | bool]  # outliers, suspectedoutliers, all, or False
    notched: NotRequired[bool]  # Show notches on box plot
    violin_box: NotRequired[bool]  # Show box inside violin
    # Distribution chart marginal
    marginal: NotRequired[str]  # Marginal plot type for histogram
    # OHLC/Candlestick options
    open: NotRequired[str]
    high: NotRequired[str]
    low: NotRequired[str]
    close: NotRequired[str]
    increasing_color_sequence: NotRequired[list[str]]  # Colors for up candles/bars
    decreasing_color_sequence: NotRequired[list[str]]  # Colors for down candles/bars
    xaxis_titles: NotRequired[str | list[str]]  # X axis title(s)
    yaxis_titles: NotRequired[str | list[str]]  # Y axis title(s)
    # Hierarchical chart options (treemap, sunburst, icicle)
    parents: NotRequired[str]
    # 3D chart options
    z: NotRequired[str]
    # Polar chart options
    r: NotRequired[str]
    theta: NotRequired[str]
    # Ternary chart options
    a: NotRequired[str]
    b: NotRequired[str]
    c: NotRequired[str]
    # Timeline chart options
    x_start: NotRequired[str]
    x_end: NotRequired[str]
    # Map/Geo chart options
    lat: NotRequired[str]
    lon: NotRequired[str]
    locations: NotRequired[str]
    locationmode: NotRequired[Literal["ISO-3", "USA-states", "country names"]]
    radius: NotRequired[int]
    zoom: NotRequired[int]
    center: NotRequired[dict[str, float]]  # {"lat": float, "lon": float}
    map_style: NotRequired[str]


# =============================================================================
# Chart Configuration Validation
# =============================================================================


def get_required_fields(chart_type: ChartType) -> list[str]:
    """Get the required fields for a given chart type.

    Args:
        chart_type: The type of chart.

    Returns:
        List of required field names.
    """
    if chart_type in ("scatter", "line", "bar", "area"):
        return ["x", "y"]
    elif chart_type == "pie":
        return ["names", "values"]
    elif chart_type == "histogram":
        return []  # x OR y, validated separately
    elif chart_type in ("box", "violin", "strip", "density_heatmap"):
        return ["x", "y"]
    elif chart_type in ("candlestick", "ohlc"):
        return ["x", "open", "high", "low", "close"]
    elif chart_type in ("treemap", "sunburst", "icicle"):
        return ["names", "values", "parents"]
    elif chart_type in ("funnel", "funnel_area"):
        return ["x", "y"]
    elif chart_type in ("scatter_3d", "line_3d"):
        return ["x", "y", "z"]
    elif chart_type in ("scatter_polar", "line_polar"):
        return ["r", "theta"]
    elif chart_type in ("scatter_ternary", "line_ternary"):
        return ["a", "b", "c"]
    elif chart_type == "timeline":
        return ["x_start", "x_end", "y"]
    elif chart_type in ("scatter_geo", "line_geo"):
        return []  # lat+lon OR locations, validated separately
    elif chart_type in ("scatter_map", "line_map", "density_map"):
        return ["lat", "lon"]
    return []


# =============================================================================
# Chart Creation Functions
# =============================================================================


def validate_config(config: ChartConfig) -> list[str]:
    """Validate a chart configuration.

    Args:
        config: The configuration to validate.

    Returns:
        List of validation error messages. Empty if valid.
    """
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
    elif chart_type in ("treemap", "sunburst", "icicle"):
        if not config.get("names"):
            errors.append(f"names is required for {chart_type} charts")
        if not config.get("values"):
            errors.append(f"values is required for {chart_type} charts")
        if not config.get("parents"):
            errors.append(f"parents is required for {chart_type} charts")
    elif chart_type == "funnel":
        if not config.get("x"):
            errors.append("x is required for funnel charts")
        if not config.get("y"):
            errors.append("y is required for funnel charts")
    elif chart_type == "funnel_area":
        if not config.get("names"):
            errors.append("names is required for funnel_area charts")
        if not config.get("values"):
            errors.append("values is required for funnel_area charts")
    elif chart_type in ("scatter_3d", "line_3d"):
        if not config.get("x"):
            errors.append(f"x is required for {chart_type} charts")
        if not config.get("y"):
            errors.append(f"y is required for {chart_type} charts")
        if not config.get("z"):
            errors.append(f"z is required for {chart_type} charts")
    elif chart_type in ("scatter_polar", "line_polar"):
        if not config.get("r"):
            errors.append(f"r is required for {chart_type} charts")
        if not config.get("theta"):
            errors.append(f"theta is required for {chart_type} charts")
    elif chart_type in ("scatter_ternary", "line_ternary"):
        if not config.get("a"):
            errors.append(f"a is required for {chart_type} charts")
        if not config.get("b"):
            errors.append(f"b is required for {chart_type} charts")
        if not config.get("c"):
            errors.append(f"c is required for {chart_type} charts")
    elif chart_type == "timeline":
        if not config.get("x_start"):
            errors.append("x_start is required for timeline charts")
        if not config.get("x_end"):
            errors.append("x_end is required for timeline charts")
        if not config.get("y"):
            errors.append("y is required for timeline charts")
    elif chart_type in ("scatter_geo", "line_geo"):
        # Geo charts need lat+lon OR locations
        has_latlon = config.get("lat") and config.get("lon")
        has_locations = config.get("locations")
        if not has_latlon and not has_locations:
            errors.append(f"lat+lon or locations is required for {chart_type} charts")
    elif chart_type in ("scatter_map", "line_map", "density_map"):
        # Map charts require lat and lon
        if not config.get("lat"):
            errors.append(f"lat is required for {chart_type} charts")
        if not config.get("lon"):
            errors.append(f"lon is required for {chart_type} charts")
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
    # Text and hover options
    if config.get("text"):
        kwargs["text"] = config["text"]
    if config.get("hover_name"):
        kwargs["hover_name"] = config["hover_name"]
    # Scatter-specific options
    if config.get("opacity") is not None:
        kwargs["opacity"] = config["opacity"]
    if config.get("marginal_x"):
        kwargs["marginal_x"] = config["marginal_x"]
    if config.get("marginal_y"):
        kwargs["marginal_y"] = config["marginal_y"]
    # Error bars
    if config.get("error_x"):
        kwargs["error_x"] = config["error_x"]
    if config.get("error_x_minus"):
        kwargs["error_x_minus"] = config["error_x_minus"]
    if config.get("error_y"):
        kwargs["error_y"] = config["error_y"]
    if config.get("error_y_minus"):
        kwargs["error_y_minus"] = config["error_y_minus"]
    # Axis configuration
    if config.get("log_x"):
        kwargs["log_x"] = config["log_x"]
    if config.get("log_y"):
        kwargs["log_y"] = config["log_y"]
    if config.get("range_x"):
        kwargs["range_x"] = config["range_x"]
    if config.get("range_y"):
        kwargs["range_y"] = config["range_y"]
    if config.get("xaxis_titles"):
        # dx.scatter expects list[str] for xaxis_titles
        val = config["xaxis_titles"]
        kwargs["xaxis_titles"] = [val] if isinstance(val, str) else val
    if config.get("yaxis_titles"):
        # dx.scatter expects list[str] for yaxis_titles
        val = config["yaxis_titles"]
        kwargs["yaxis_titles"] = [val] if isinstance(val, str) else val
    # Labels dict
    if config.get("labels"):
        kwargs["labels"] = config["labels"]
    # Rendering options
    if config.get("render_mode"):
        kwargs["render_mode"] = config["render_mode"]
    if config.get("template"):
        kwargs["template"] = config["template"]
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
    # Text and hover options
    if config.get("text"):
        kwargs["text"] = config["text"]
    if config.get("hover_name"):
        kwargs["hover_name"] = config["hover_name"]
    # Line-specific options
    if config.get("line_dash"):
        kwargs["line_dash"] = config["line_dash"]
    if config.get("width"):
        kwargs["width"] = config["width"]
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("symbol"):
        kwargs["symbol"] = config["symbol"]
    # Error bars
    if config.get("error_x"):
        kwargs["error_x"] = config["error_x"]
    if config.get("error_x_minus"):
        kwargs["error_x_minus"] = config["error_x_minus"]
    if config.get("error_y"):
        kwargs["error_y"] = config["error_y"]
    if config.get("error_y_minus"):
        kwargs["error_y_minus"] = config["error_y_minus"]
    # Axis configuration
    if config.get("log_x"):
        kwargs["log_x"] = config["log_x"]
    if config.get("log_y"):
        kwargs["log_y"] = config["log_y"]
    if config.get("range_x"):
        kwargs["range_x"] = config["range_x"]
    if config.get("range_y"):
        kwargs["range_y"] = config["range_y"]
    if config.get("xaxis_titles"):
        # dx.line expects list[str] for xaxis_titles
        val = config["xaxis_titles"]
        kwargs["xaxis_titles"] = [val] if isinstance(val, str) else val
    if config.get("yaxis_titles"):
        # dx.line expects list[str] for yaxis_titles
        val = config["yaxis_titles"]
        kwargs["yaxis_titles"] = [val] if isinstance(val, str) else val
    # Labels dict
    if config.get("labels"):
        kwargs["labels"] = config["labels"]
    # Rendering options
    if config.get("render_mode"):
        kwargs["render_mode"] = config["render_mode"]
    if config.get("template"):
        kwargs["template"] = config["template"]
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
    # Advanced bar options (Phase 10)
    if config.get("text"):
        kwargs["text"] = config["text"]
    if config.get("hover_name"):
        kwargs["hover_name"] = config["hover_name"]
    if config.get("opacity") is not None:
        kwargs["opacity"] = config["opacity"]
    if config.get("barmode"):
        kwargs["barmode"] = config["barmode"]
    if config.get("text_auto"):
        kwargs["text_auto"] = config["text_auto"]
    # Error bars
    if config.get("error_x"):
        kwargs["error_x"] = config["error_x"]
    if config.get("error_x_minus"):
        kwargs["error_x_minus"] = config["error_x_minus"]
    if config.get("error_y"):
        kwargs["error_y"] = config["error_y"]
    if config.get("error_y_minus"):
        kwargs["error_y_minus"] = config["error_y_minus"]
    # Axis configuration (bar only supports log axes, not axis titles)
    if config.get("log_x"):
        kwargs["log_x"] = config["log_x"]
    if config.get("log_y"):
        kwargs["log_y"] = config["log_y"]
    # Rendering
    if config.get("template"):
        kwargs["template"] = config["template"]
    return dx.bar(table, **kwargs)


def _make_area(table: Table, config: ChartConfig):
    """Create an area chart."""
    kwargs = {"x": config["x"], "y": config["y"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    # Advanced area options (Phase 10)
    if config.get("markers") is not None:
        kwargs["markers"] = config["markers"]
    if config.get("line_shape"):
        kwargs["line_shape"] = config["line_shape"]
    if config.get("text"):
        kwargs["text"] = config["text"]
    if config.get("hover_name"):
        kwargs["hover_name"] = config["hover_name"]
    if config.get("opacity") is not None:
        kwargs["opacity"] = config["opacity"]
    # Axis configuration
    if config.get("log_x"):
        kwargs["log_x"] = config["log_x"]
    if config.get("log_y"):
        kwargs["log_y"] = config["log_y"]
    if config.get("xaxis_titles"):
        kwargs["xaxis_titles"] = config["xaxis_titles"]
    if config.get("yaxis_titles"):
        kwargs["yaxis_titles"] = config["yaxis_titles"]
    # Rendering
    if config.get("template"):
        kwargs["template"] = config["template"]
    return dx.area(table, **kwargs)


def _make_pie(table: Table, config: ChartConfig):
    """Create a pie chart."""
    kwargs = {"names": config["names"], "values": config["values"]}
    if config.get("title"):
        kwargs["title"] = config["title"]
    # Advanced pie options (Phase 10)
    if config.get("hover_name"):
        kwargs["hover_name"] = config["hover_name"]
    if config.get("opacity") is not None:
        kwargs["opacity"] = config["opacity"]
    if config.get("hole"):
        kwargs["hole"] = config["hole"]
    # Rendering
    if config.get("template"):
        kwargs["template"] = config["template"]
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
    # Advanced histogram options (Phase 11)
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("opacity") is not None:
        kwargs["opacity"] = config["opacity"]
    if config.get("histfunc"):
        kwargs["histfunc"] = config["histfunc"]
    if config.get("histnorm"):
        kwargs["histnorm"] = config["histnorm"]
    if config.get("barnorm"):
        kwargs["barnorm"] = config["barnorm"]
    if config.get("hist_barmode"):
        kwargs["barmode"] = config["hist_barmode"]
    if config.get("cumulative"):
        kwargs["cumulative"] = config["cumulative"]
    if config.get("range_bins"):
        kwargs["range_bins"] = config["range_bins"]
    if config.get("marginal"):
        kwargs["marginal"] = config["marginal"]
    if config.get("text_auto"):
        kwargs["text_auto"] = config["text_auto"]
    if config.get("log_x"):
        kwargs["log_x"] = config["log_x"]
    if config.get("log_y"):
        kwargs["log_y"] = config["log_y"]
    if config.get("template"):
        kwargs["template"] = config["template"]
    return dx.histogram(table, **kwargs)


def _make_box(table: Table, config: ChartConfig):
    """Create a box plot."""
    kwargs = {"x": config["x"], "y": config["y"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    # Advanced box options (Phase 11)
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("hover_name"):
        kwargs["hover_name"] = config["hover_name"]
    if config.get("boxmode"):
        kwargs["boxmode"] = config["boxmode"]
    if config.get("points"):
        kwargs["points"] = config["points"]
    if config.get("notched"):
        kwargs["notched"] = config["notched"]
    if config.get("log_x"):
        kwargs["log_x"] = config["log_x"]
    if config.get("log_y"):
        kwargs["log_y"] = config["log_y"]
    if config.get("template"):
        kwargs["template"] = config["template"]
    return dx.box(table, **kwargs)


def _make_violin(table: Table, config: ChartConfig):
    """Create a violin plot."""
    kwargs = {"x": config["x"], "y": config["y"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    # Advanced violin options (Phase 11)
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("hover_name"):
        kwargs["hover_name"] = config["hover_name"]
    if config.get("violinmode"):
        kwargs["violinmode"] = config["violinmode"]
    if config.get("points"):
        kwargs["points"] = config["points"]
    if config.get("violin_box"):
        kwargs["box"] = config["violin_box"]
    if config.get("log_x"):
        kwargs["log_x"] = config["log_x"]
    if config.get("log_y"):
        kwargs["log_y"] = config["log_y"]
    if config.get("template"):
        kwargs["template"] = config["template"]
    return dx.violin(table, **kwargs)


def _make_strip(table: Table, config: ChartConfig):
    """Create a strip plot."""
    kwargs = {"x": config["x"], "y": config["y"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    # Advanced strip options (Phase 11)
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("hover_name"):
        kwargs["hover_name"] = config["hover_name"]
    if config.get("stripmode"):
        kwargs["stripmode"] = config["stripmode"]
    if config.get("log_x"):
        kwargs["log_x"] = config["log_x"]
    if config.get("log_y"):
        kwargs["log_y"] = config["log_y"]
    if config.get("template"):
        kwargs["template"] = config["template"]
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
    # Advanced options
    if config.get("increasing_color_sequence"):
        kwargs["increasing_color_sequence"] = config["increasing_color_sequence"]
    if config.get("decreasing_color_sequence"):
        kwargs["decreasing_color_sequence"] = config["decreasing_color_sequence"]
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
    # Advanced options
    if config.get("increasing_color_sequence"):
        kwargs["increasing_color_sequence"] = config["increasing_color_sequence"]
    if config.get("decreasing_color_sequence"):
        kwargs["decreasing_color_sequence"] = config["decreasing_color_sequence"]
    return dx.ohlc(table, **kwargs)


def _make_treemap(table: Table, config: ChartConfig):
    """Create a treemap chart."""
    kwargs = {
        "names": config["names"],
        "values": config["values"],
        "parents": config["parents"],
    }
    if config.get("title"):
        kwargs["title"] = config["title"]
    # Advanced options (Phase 13)
    if config.get("hier_color"):
        kwargs["color"] = config["hier_color"]
    if config.get("branchvalues"):
        kwargs["branchvalues"] = config["branchvalues"]
    if config.get("maxdepth") is not None and config.get("maxdepth") != -1:
        kwargs["maxdepth"] = config["maxdepth"]
    if config.get("template"):
        kwargs["template"] = config["template"]
    return dx.treemap(table, **kwargs)


def _make_sunburst(table: Table, config: ChartConfig):
    """Create a sunburst chart."""
    kwargs = {
        "names": config["names"],
        "values": config["values"],
        "parents": config["parents"],
    }
    if config.get("title"):
        kwargs["title"] = config["title"]
    # Advanced options (Phase 13)
    if config.get("hier_color"):
        kwargs["color"] = config["hier_color"]
    if config.get("branchvalues"):
        kwargs["branchvalues"] = config["branchvalues"]
    if config.get("maxdepth") is not None and config.get("maxdepth") != -1:
        kwargs["maxdepth"] = config["maxdepth"]
    if config.get("template"):
        kwargs["template"] = config["template"]
    return dx.sunburst(table, **kwargs)


def _make_icicle(table: Table, config: ChartConfig):
    """Create an icicle chart."""
    kwargs = {
        "names": config["names"],
        "values": config["values"],
        "parents": config["parents"],
    }
    if config.get("title"):
        kwargs["title"] = config["title"]
    # Advanced options (Phase 13)
    if config.get("hier_color"):
        kwargs["color"] = config["hier_color"]
    if config.get("branchvalues"):
        kwargs["branchvalues"] = config["branchvalues"]
    if config.get("maxdepth") is not None and config.get("maxdepth") != -1:
        kwargs["maxdepth"] = config["maxdepth"]
    if config.get("template"):
        kwargs["template"] = config["template"]
    return dx.icicle(table, **kwargs)


def _make_funnel(table: Table, config: ChartConfig):
    """Create a funnel chart."""
    kwargs = {"x": config["x"], "y": config["y"]}
    if config.get("title"):
        kwargs["title"] = config["title"]
    # Advanced options (Phase 13)
    if config.get("funnel_text"):
        kwargs["text"] = config["funnel_text"]
    if config.get("funnel_color"):
        kwargs["color"] = config["funnel_color"]
    if config.get("funnel_orientation"):
        kwargs["orientation"] = config["funnel_orientation"]
    if config.get("opacity") is not None:
        kwargs["opacity"] = config["opacity"]
    if config.get("log_x"):
        kwargs["log_x"] = config["log_x"]
    if config.get("log_y"):
        kwargs["log_y"] = config["log_y"]
    if config.get("template"):
        kwargs["template"] = config["template"]
    return dx.funnel(table, **kwargs)


def _make_funnel_area(table: Table, config: ChartConfig):
    """Create a funnel area chart."""
    kwargs = {
        "names": config["names"],
        "values": config["values"],
    }
    if config.get("title"):
        kwargs["title"] = config["title"]
    # Advanced options (Phase 13)
    if config.get("funnel_area_color"):
        kwargs["color"] = config["funnel_area_color"]
    if config.get("opacity") is not None:
        kwargs["opacity"] = config["opacity"]
    if config.get("template"):
        kwargs["template"] = config["template"]
    return dx.funnel_area(table, **kwargs)


def _make_scatter_3d(table: Table, config: ChartConfig):
    """Create a 3D scatter plot."""
    kwargs = {"x": config["x"], "y": config["y"], "z": config["z"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("size"):
        kwargs["size"] = config["size"]
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.scatter_3d(table, **kwargs)


def _make_line_3d(table: Table, config: ChartConfig):
    """Create a 3D line plot."""
    kwargs = {"x": config["x"], "y": config["y"], "z": config["z"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.line_3d(table, **kwargs)


def _make_scatter_polar(table: Table, config: ChartConfig):
    """Create a polar scatter plot."""
    kwargs = {"r": config["r"], "theta": config["theta"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("size"):
        kwargs["size"] = config["size"]
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.scatter_polar(table, **kwargs)


def _make_line_polar(table: Table, config: ChartConfig):
    """Create a polar line plot."""
    kwargs = {"r": config["r"], "theta": config["theta"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.line_polar(table, **kwargs)


def _make_scatter_ternary(table: Table, config: ChartConfig):
    """Create a ternary scatter plot."""
    kwargs = {"a": config["a"], "b": config["b"], "c": config["c"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("size"):
        kwargs["size"] = config["size"]
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.scatter_ternary(table, **kwargs)


def _make_line_ternary(table: Table, config: ChartConfig):
    """Create a ternary line plot."""
    kwargs = {"a": config["a"], "b": config["b"], "c": config["c"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.line_ternary(table, **kwargs)


def _make_timeline(table: Table, config: ChartConfig):
    """Create a timeline/Gantt chart."""
    kwargs = {
        "x_start": config["x_start"],
        "x_end": config["x_end"],
        "y": config["y"],
    }
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.timeline(table, **kwargs)


def _make_scatter_geo(table: Table, config: ChartConfig):
    """Create a geographic scatter plot on a world map."""
    kwargs = {}
    if config.get("lat"):
        kwargs["lat"] = config["lat"]
    if config.get("lon"):
        kwargs["lon"] = config["lon"]
    if config.get("locations"):
        kwargs["locations"] = config["locations"]
    if config.get("locationmode"):
        kwargs["locationmode"] = config["locationmode"]
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("size"):
        kwargs["size"] = config["size"]
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.scatter_geo(table, **kwargs)


def _make_line_geo(table: Table, config: ChartConfig):
    """Create a geographic line plot on a world map."""
    kwargs = {}
    if config.get("lat"):
        kwargs["lat"] = config["lat"]
    if config.get("lon"):
        kwargs["lon"] = config["lon"]
    if config.get("locations"):
        kwargs["locations"] = config["locations"]
    if config.get("locationmode"):
        kwargs["locationmode"] = config["locationmode"]
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.line_geo(table, **kwargs)


def _make_scatter_map(table: Table, config: ChartConfig):
    """Create a scatter plot on a tile-based map."""
    kwargs = {"lat": config["lat"], "lon": config["lon"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("size"):
        kwargs["size"] = config["size"]
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("zoom"):
        kwargs["zoom"] = config["zoom"]
    if config.get("center"):
        kwargs["center"] = config["center"]
    if config.get("map_style"):
        kwargs["map_style"] = config["map_style"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.scatter_map(table, **kwargs)


def _make_line_map(table: Table, config: ChartConfig):
    """Create a line plot on a tile-based map."""
    kwargs = {"lat": config["lat"], "lon": config["lon"]}
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("zoom"):
        kwargs["zoom"] = config["zoom"]
    if config.get("center"):
        kwargs["center"] = config["center"]
    if config.get("map_style"):
        kwargs["map_style"] = config["map_style"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.line_map(table, **kwargs)


def _make_density_map(table: Table, config: ChartConfig):
    """Create a density heatmap on a tile-based map."""
    kwargs = {"lat": config["lat"], "lon": config["lon"]}
    if config.get("z"):
        kwargs["z"] = config["z"]
    if config.get("radius"):
        kwargs["radius"] = config["radius"]
    if config.get("zoom"):
        kwargs["zoom"] = config["zoom"]
    if config.get("center"):
        kwargs["center"] = config["center"]
    if config.get("map_style"):
        kwargs["map_style"] = config["map_style"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.density_map(table, **kwargs)


def make_chart(table: Table, config: ChartConfig):
    """Create a chart from the given table and configuration."""
    errors = validate_config(config)
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
    elif chart_type == "treemap":
        return _make_treemap(table, config)
    elif chart_type == "sunburst":
        return _make_sunburst(table, config)
    elif chart_type == "icicle":
        return _make_icicle(table, config)
    elif chart_type == "funnel":
        return _make_funnel(table, config)
    elif chart_type == "funnel_area":
        return _make_funnel_area(table, config)
    elif chart_type == "scatter_3d":
        return _make_scatter_3d(table, config)
    elif chart_type == "line_3d":
        return _make_line_3d(table, config)
    elif chart_type == "scatter_polar":
        return _make_scatter_polar(table, config)
    elif chart_type == "line_polar":
        return _make_line_polar(table, config)
    elif chart_type == "scatter_ternary":
        return _make_scatter_ternary(table, config)
    elif chart_type == "line_ternary":
        return _make_line_ternary(table, config)
    elif chart_type == "timeline":
        return _make_timeline(table, config)
    elif chart_type == "scatter_geo":
        return _make_scatter_geo(table, config)
    elif chart_type == "line_geo":
        return _make_line_geo(table, config)
    elif chart_type == "scatter_map":
        return _make_scatter_map(table, config)
    elif chart_type == "line_map":
        return _make_line_map(table, config)
    elif chart_type == "density_map":
        return _make_density_map(table, config)
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")


# =============================================================================
# Code Generation
# =============================================================================

# Dataset loader code for each dataset
DATASET_LOADERS = {
    "iris": "dx.data.iris()",
    "stocks": "dx.data.stocks()",
    "tips": "dx.data.tips()",
    "gapminder": "dx.data.gapminder()",
    "wind": "dx.data.wind()",
    "election": "dx.data.election()",
    "fish_market": "dx.data.fish_market()",
    "jobs": "dx.data.jobs()",
    "marketing": "dx.data.marketing()",
    "flights": "dx.data.flights()",
    "outages": "dx.data.outages()",
    # Custom datasets - show placeholder
    "ohlc_sample": "# Custom OHLC dataset - see chart-builder source for creation code\ntable = create_ohlc_sample()",
    "hierarchy_sample": "# Custom hierarchy dataset - see chart-builder source for creation code\ntable = create_hierarchy_sample()",
    "funnel_sample": "# Custom funnel dataset - see chart-builder source for creation code\ntable = create_funnel_sample()",
    "scatter_3d_sample": "# Custom 3D dataset - see chart-builder source for creation code\ntable = create_scatter_3d_sample()",
    "polar_sample": "# Custom polar dataset - see chart-builder source for creation code\ntable = create_polar_sample()",
    "ternary_sample": "# Custom ternary dataset - see chart-builder source for creation code\ntable = create_ternary_sample()",
    "timeline_sample": "# Custom timeline dataset - see chart-builder source for creation code\ntable = create_timeline_sample()",
}


def _format_value(value) -> str:
    """Format a value for Python code generation."""
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return "True" if value else "False"
    elif isinstance(value, dict):
        # Format dict like {"lat": 44.97, "lon": -93.17}
        items = ", ".join(f'"{k}": {v}' for k, v in value.items())
        return "{" + items + "}"
    elif isinstance(value, list):
        # Format list like ["col1", "col2"]
        items = ", ".join(_format_value(v) for v in value)
        return "[" + items + "]"
    else:
        return str(value)


def generate_chart_code(config: ChartConfig, dataset_name: str) -> str:
    """Generate Python code to recreate the current chart configuration.

    Args:
        config: The chart configuration dictionary.
        dataset_name: The name of the dataset being used.

    Returns:
        A string containing Python code that recreates the chart.
    """
    chart_type = config.get("chart_type", "scatter")

    # Build the import statement
    lines = ["from deephaven.plot import express as dx", ""]

    # Build the table loading code
    loader = DATASET_LOADERS.get(
        dataset_name, f"# Load your table here\ntable = your_table"
    )
    if dataset_name in (
        "ohlc_sample",
        "hierarchy_sample",
        "funnel_sample",
        "scatter_3d_sample",
        "polar_sample",
        "ternary_sample",
        "timeline_sample",
    ):
        lines.append(loader)
    else:
        lines.append(f"table = {loader}")
    lines.append("")

    # Build the chart function call
    # Determine which parameters to include based on chart type
    params = []

    # Common parameters for most chart types
    if chart_type in (
        "scatter",
        "line",
        "bar",
        "area",
        "histogram",
        "box",
        "violin",
        "strip",
        "density_heatmap",
        "funnel",
    ):
        if config.get("x"):
            params.append(f'x="{config["x"]}"')
        if config.get("y"):
            params.append(f'y="{config["y"]}"')

    # Pie-style charts (names, values)
    if chart_type in ("pie", "funnel_area"):
        if config.get("names"):
            params.append(f'names="{config["names"]}"')
        if config.get("values"):
            params.append(f'values="{config["values"]}"')
        # Funnel area advanced options (Phase 13)
        if chart_type == "funnel_area":
            if config.get("funnel_area_color"):
                params.append(f'color="{config["funnel_area_color"]}"')

    # Hierarchical charts
    if chart_type in ("treemap", "sunburst", "icicle"):
        if config.get("names"):
            params.append(f'names="{config["names"]}"')
        if config.get("values"):
            params.append(f'values="{config["values"]}"')
        if config.get("parents"):
            params.append(f'parents="{config["parents"]}"')
        # Advanced options (Phase 13)
        if config.get("hier_color"):
            params.append(f'color="{config["hier_color"]}"')
        if config.get("branchvalues"):
            params.append(f'branchvalues="{config["branchvalues"]}"')
        if config.get("maxdepth") is not None and config.get("maxdepth") != -1:
            params.append(f'maxdepth={config["maxdepth"]}')

    # OHLC/Candlestick
    if chart_type in ("candlestick", "ohlc"):
        if config.get("x"):
            params.append(f'x="{config["x"]}"')
        if config.get("open"):
            params.append(f'open="{config["open"]}"')
        if config.get("high"):
            params.append(f'high="{config["high"]}"')
        if config.get("low"):
            params.append(f'low="{config["low"]}"')
        if config.get("close"):
            params.append(f'close="{config["close"]}"')

    # 3D charts
    if chart_type in ("scatter_3d", "line_3d"):
        if config.get("x"):
            params.append(f'x="{config["x"]}"')
        if config.get("y"):
            params.append(f'y="{config["y"]}"')
        if config.get("z"):
            params.append(f'z="{config["z"]}"')

    # Polar charts
    if chart_type in ("scatter_polar", "line_polar"):
        if config.get("r"):
            params.append(f'r="{config["r"]}"')
        if config.get("theta"):
            params.append(f'theta="{config["theta"]}"')

    # Ternary charts
    if chart_type in ("scatter_ternary", "line_ternary"):
        if config.get("a"):
            params.append(f'a="{config["a"]}"')
        if config.get("b"):
            params.append(f'b="{config["b"]}"')
        if config.get("c"):
            params.append(f'c="{config["c"]}"')

    # Timeline
    if chart_type == "timeline":
        if config.get("x_start"):
            params.append(f'x_start="{config["x_start"]}"')
        if config.get("x_end"):
            params.append(f'x_end="{config["x_end"]}"')
        if config.get("y"):
            params.append(f'y="{config["y"]}"')

    # Geo charts
    if chart_type in ("scatter_geo", "line_geo"):
        if config.get("lat"):
            params.append(f'lat="{config["lat"]}"')
        if config.get("lon"):
            params.append(f'lon="{config["lon"]}"')
        if config.get("locations"):
            params.append(f'locations="{config["locations"]}"')
        if config.get("locationmode"):
            params.append(f'locationmode="{config["locationmode"]}"')

    # Map charts (tile-based)
    if chart_type in ("scatter_map", "line_map", "density_map"):
        if config.get("lat"):
            params.append(f'lat="{config["lat"]}"')
        if config.get("lon"):
            params.append(f'lon="{config["lon"]}"')
        if config.get("zoom"):
            params.append(f'zoom={config["zoom"]}')
        if config.get("center"):
            params.append(f'center={_format_value(config["center"])}')
        if config.get("map_style"):
            params.append(f'map_style="{config["map_style"]}"')

    # Density map specific
    if chart_type == "density_map":
        if config.get("z"):
            params.append(f'z="{config["z"]}"')
        if config.get("radius"):
            params.append(f'radius={config["radius"]}')

    # Common optional parameters
    if config.get("by"):
        by_val = config["by"]
        if isinstance(by_val, list):
            params.append(f"by={_format_value(by_val)}")
        else:
            params.append(f'by="{by_val}"')

    if config.get("color"):
        params.append(f'color="{config["color"]}"')

    if config.get("size"):
        params.append(f'size="{config["size"]}"')

    if config.get("symbol"):
        params.append(f'symbol="{config["symbol"]}"')

    # Text and hover options (scatter/line)
    if chart_type in ("scatter", "line"):
        if config.get("text"):
            params.append(f'text="{config["text"]}"')
        if config.get("hover_name"):
            params.append(f'hover_name="{config["hover_name"]}"')

    # Line-specific options
    if chart_type == "line":
        if config.get("markers"):
            params.append("markers=True")
        if config.get("line_shape") and config["line_shape"] != "linear":
            params.append(f'line_shape="{config["line_shape"]}"')
        if config.get("line_dash"):
            params.append(f'line_dash="{config["line_dash"]}"')
        if config.get("width"):
            params.append(f'width="{config["width"]}"')

    # Scatter-specific options
    if chart_type == "scatter":
        if config.get("opacity") is not None and config["opacity"] != 1.0:
            params.append(f'opacity={config["opacity"]}')
        if config.get("marginal_x"):
            params.append(f'marginal_x="{config["marginal_x"]}"')
        if config.get("marginal_y"):
            params.append(f'marginal_y="{config["marginal_y"]}"')

    # Error bars (scatter/line)
    if chart_type in ("scatter", "line"):
        if config.get("error_x"):
            params.append(f'error_x="{config["error_x"]}"')
        if config.get("error_x_minus"):
            params.append(f'error_x_minus="{config["error_x_minus"]}"')
        if config.get("error_y"):
            params.append(f'error_y="{config["error_y"]}"')
        if config.get("error_y_minus"):
            params.append(f'error_y_minus="{config["error_y_minus"]}"')

    # Axis configuration (scatter/line)
    if chart_type in ("scatter", "line"):
        if config.get("log_x"):
            params.append("log_x=True")
        if config.get("log_y"):
            params.append("log_y=True")
        if config.get("range_x"):
            params.append(f'range_x={_format_value(config["range_x"])}')
        if config.get("range_y"):
            params.append(f'range_y={_format_value(config["range_y"])}')
        if config.get("xaxis_titles"):
            params.append(f'xaxis_titles={_format_value(config["xaxis_titles"])}')
        if config.get("yaxis_titles"):
            params.append(f'yaxis_titles={_format_value(config["yaxis_titles"])}')

    # Labels dict (scatter/line)
    if chart_type in ("scatter", "line"):
        if config.get("labels"):
            params.append(f'labels={_format_value(config["labels"])}')

    # Rendering options (scatter/line)
    if chart_type in ("scatter", "line"):
        if config.get("render_mode") and config["render_mode"] != "webgl":
            params.append(f'render_mode="{config["render_mode"]}"')
        if config.get("template"):
            params.append(f'template="{config["template"]}"')

    # Bar-specific options
    if chart_type == "bar":
        if config.get("orientation") and config["orientation"] != "v":
            params.append(f'orientation="{config["orientation"]}"')
        # Advanced bar options (Phase 10)
        if config.get("text"):
            params.append(f'text="{config["text"]}"')
        if config.get("hover_name"):
            params.append(f'hover_name="{config["hover_name"]}"')
        if config.get("opacity") is not None and config["opacity"] != 1.0:
            params.append(f'opacity={config["opacity"]}')
        if config.get("barmode") and config["barmode"] != "relative":
            params.append(f'barmode="{config["barmode"]}"')
        if config.get("text_auto"):
            params.append("text_auto=True")
        # Error bars
        if config.get("error_x"):
            params.append(f'error_x="{config["error_x"]}"')
        if config.get("error_x_minus"):
            params.append(f'error_x_minus="{config["error_x_minus"]}"')
        if config.get("error_y"):
            params.append(f'error_y="{config["error_y"]}"')
        if config.get("error_y_minus"):
            params.append(f'error_y_minus="{config["error_y_minus"]}"')
        # Axis configuration (bar only supports log axes, not axis titles)
        if config.get("log_x"):
            params.append("log_x=True")
        if config.get("log_y"):
            params.append("log_y=True")
        # Rendering
        if config.get("template"):
            params.append(f'template="{config["template"]}"')

    # Area-specific options (Phase 10)
    if chart_type == "area":
        if config.get("markers"):
            params.append("markers=True")
        if config.get("line_shape") and config["line_shape"] != "linear":
            params.append(f'line_shape="{config["line_shape"]}"')
        if config.get("text"):
            params.append(f'text="{config["text"]}"')
        if config.get("hover_name"):
            params.append(f'hover_name="{config["hover_name"]}"')
        if config.get("opacity") is not None and config["opacity"] != 1.0:
            params.append(f'opacity={config["opacity"]}')
        # Axis configuration
        if config.get("log_x"):
            params.append("log_x=True")
        if config.get("log_y"):
            params.append("log_y=True")
        if config.get("xaxis_titles"):
            params.append(f'xaxis_titles={_format_value(config["xaxis_titles"])}')
        if config.get("yaxis_titles"):
            params.append(f'yaxis_titles={_format_value(config["yaxis_titles"])}')
        # Rendering
        if config.get("template"):
            params.append(f'template="{config["template"]}"')

    # Pie-specific options (Phase 10)
    if chart_type == "pie":
        if config.get("hover_name"):
            params.append(f'hover_name="{config["hover_name"]}"')
        if config.get("opacity") is not None and config["opacity"] != 1.0:
            params.append(f'opacity={config["opacity"]}')
        if config.get("hole") and config["hole"] > 0:
            params.append(f'hole={config["hole"]}')
        # Rendering
        if config.get("template"):
            params.append(f'template="{config["template"]}"')

    # Histogram-specific options (Phase 11)
    if chart_type == "histogram":
        if config.get("nbins") and config["nbins"] > 0:
            params.append(f'nbins={config["nbins"]}')
        if config.get("histfunc") and config["histfunc"] != "count":
            params.append(f'histfunc="{config["histfunc"]}"')
        if config.get("histnorm"):
            params.append(f'histnorm="{config["histnorm"]}"')
        if config.get("barnorm"):
            params.append(f'barnorm="{config["barnorm"]}"')
        if config.get("hist_barmode") and config["hist_barmode"] != "relative":
            params.append(f'barmode="{config["hist_barmode"]}"')
        if config.get("cumulative"):
            params.append("cumulative=True")
        if config.get("hover_name"):
            params.append(f'hover_name="{config["hover_name"]}"')
        if config.get("log_x"):
            params.append("log_x=True")
        if config.get("log_y"):
            params.append("log_y=True")
        if config.get("template"):
            params.append(f'template="{config["template"]}"')

    # Box plot options (Phase 11)
    if chart_type == "box":
        if config.get("boxmode") and config["boxmode"] != "group":
            params.append(f'boxmode="{config["boxmode"]}"')
        if config.get("points") is not None:
            if config["points"] is False:
                params.append("points=False")
            elif config["points"] != "outliers":
                params.append(f'points="{config["points"]}"')
        if config.get("notched"):
            params.append("notched=True")
        if config.get("hover_name"):
            params.append(f'hover_name="{config["hover_name"]}"')
        if config.get("log_x"):
            params.append("log_x=True")
        if config.get("log_y"):
            params.append("log_y=True")
        if config.get("template"):
            params.append(f'template="{config["template"]}"')

    # Violin plot options (Phase 11)
    if chart_type == "violin":
        if config.get("violinmode") and config["violinmode"] != "group":
            params.append(f'violinmode="{config["violinmode"]}"')
        if config.get("points"):
            params.append(f'points="{config["points"]}"')
        if config.get("violin_box"):
            params.append("box=True")
        if config.get("hover_name"):
            params.append(f'hover_name="{config["hover_name"]}"')
        if config.get("log_x"):
            params.append("log_x=True")
        if config.get("log_y"):
            params.append("log_y=True")
        if config.get("template"):
            params.append(f'template="{config["template"]}"')

    # Strip plot options (Phase 11)
    if chart_type == "strip":
        if config.get("stripmode") and config["stripmode"] != "group":
            params.append(f'stripmode="{config["stripmode"]}"')
        if config.get("hover_name"):
            params.append(f'hover_name="{config["hover_name"]}"')
        if config.get("log_x"):
            params.append("log_x=True")
        if config.get("log_y"):
            params.append("log_y=True")
        if config.get("template"):
            params.append(f'template="{config["template"]}"')

    # Candlestick/OHLC options (Phase 12)
    if chart_type in ("candlestick", "ohlc"):
        if config.get("increasing_color_sequence"):
            params.append(
                f'increasing_color_sequence={_format_value(config["increasing_color_sequence"])}'
            )
        if config.get("decreasing_color_sequence"):
            params.append(
                f'decreasing_color_sequence={_format_value(config["decreasing_color_sequence"])}'
            )

    # Funnel chart options (Phase 13)
    if chart_type == "funnel":
        if config.get("funnel_text"):
            params.append(f'text="{config["funnel_text"]}"')
        if config.get("funnel_color"):
            params.append(f'color="{config["funnel_color"]}"')
        if config.get("funnel_orientation"):
            params.append(f'orientation="{config["funnel_orientation"]}"')
        if config.get("opacity") is not None:
            params.append(f'opacity={config["opacity"]}')
        if config.get("log_x"):
            params.append("log_x=True")
        if config.get("log_y"):
            params.append("log_y=True")
        if config.get("template"):
            params.append(f'template="{config["template"]}"')

    # Funnel area advanced options (Phase 13) - opacity and template
    if chart_type == "funnel_area":
        if config.get("opacity") is not None:
            params.append(f'opacity={config["opacity"]}')
        if config.get("template"):
            params.append(f'template="{config["template"]}"')

    # Hierarchical chart template (Phase 13)
    if chart_type in ("treemap", "sunburst", "icicle"):
        if config.get("template"):
            params.append(f'template="{config["template"]}"')

    # Title (common to all)
    if config.get("title"):
        params.append(f'title="{config["title"]}"')

    # Format the function call
    if params:
        params_str = ",\n    ".join(params)
        lines.append(f"chart = dx.{chart_type}(")
        lines.append("    table,")
        lines.append(f"    {params_str},")
        lines.append(")")
    else:
        lines.append(f"chart = dx.{chart_type}(table)")

    return "\n".join(lines)


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
    {"key": "treemap", "label": "Treemap", "icon": "vsSymbolClass"},
    {"key": "sunburst", "label": "Sunburst", "icon": "vsPieChart"},
    {"key": "icicle", "label": "Icicle", "icon": "vsGraphLeft"},
    {"key": "funnel", "label": "Funnel", "icon": "vsFilter"},
    {"key": "funnel_area", "label": "Funnel Area", "icon": "vsFilter"},
    {"key": "scatter_3d", "label": "Scatter 3D", "icon": "vsCircleFilled"},
    {"key": "line_3d", "label": "Line 3D", "icon": "vsGraphLine"},
    {"key": "scatter_polar", "label": "Scatter Polar", "icon": "vsCircleFilled"},
    {"key": "line_polar", "label": "Line Polar", "icon": "vsGraphLine"},
    {"key": "scatter_ternary", "label": "Scatter Ternary", "icon": "vsCircleFilled"},
    {"key": "line_ternary", "label": "Line Ternary", "icon": "vsGraphLine"},
    {"key": "timeline", "label": "Timeline", "icon": "vsCalendar"},
    {"key": "scatter_geo", "label": "Scatter Geo", "icon": "vsGlobe"},
    {"key": "line_geo", "label": "Line Geo", "icon": "vsGlobe"},
    {"key": "scatter_map", "label": "Scatter Map", "icon": "vsMap"},
    {"key": "line_map", "label": "Line Map", "icon": "vsMap"},
    {"key": "density_map", "label": "Density Map", "icon": "vsMap"},
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
    {
        "key": "iris",
        "label": "Iris",
        "icon": "vsSymbolColor",
        "description": "Iris flower measurements (sepal/petal dimensions). Good for: scatter, histogram, box, violin, strip, density_heatmap",
    },
    {
        "key": "stocks",
        "label": "Stocks",
        "icon": "vsGraphLine",
        "description": "Real-time stock prices over time. Good for: line, area, scatter, histogram",
    },
    {
        "key": "tips",
        "label": "Tips",
        "icon": "vsCreditCard",
        "description": "Restaurant tips with bill totals. Good for: scatter, bar, histogram, box, violin",
    },
    {
        "key": "gapminder",
        "label": "Gapminder",
        "icon": "vsGlobe",
        "description": "World development indicators by country/year. Good for: scatter, line, bar, scatter_geo",
    },
    {
        "key": "wind",
        "label": "Wind",
        "icon": "vsCompass",
        "description": "Wind speed and direction data. Good for: scatter_polar, line_polar, bar",
    },
    {
        "key": "election",
        "label": "Election",
        "icon": "vsOrganization",
        "description": "Election results by district. Good for: bar, pie, scatter_geo",
    },
    {
        "key": "fish_market",
        "label": "Fish Market",
        "icon": "vsTag",
        "description": "Fish market sales with species/weight. Good for: scatter, bar, histogram, box",
    },
    {
        "key": "jobs",
        "label": "Jobs",
        "icon": "vsBriefcase",
        "description": "Employment data over time by gender. Good for: line, area, bar, pie",
    },
    {
        "key": "marketing",
        "label": "Marketing",
        "icon": "vsMegaphone",
        "description": "Marketing campaign performance. Good for: scatter, bar, pie, funnel",
    },
    {
        "key": "ohlc_sample",
        "label": "Stocks OHLC (1min)",
        "icon": "vsGraphScatter",
        "description": "Stock data binned to 1-minute OHLC. Good for: candlestick, ohlc",
    },
    {
        "key": "hierarchy_sample",
        "label": "Product Hierarchy",
        "icon": "vsTypeHierarchy",
        "description": "Hierarchical product sales (category/product). Good for: treemap, sunburst, icicle",
    },
    {
        "key": "funnel_sample",
        "label": "Sales Funnel",
        "icon": "vsFilter",
        "description": "Sales pipeline stages with conversion. Good for: funnel, funnel_area",
    },
    {
        "key": "scatter_3d_sample",
        "label": "3D Points",
        "icon": "vsSymbolMisc",
        "description": "Random 3D point cloud with categories. Good for: scatter_3d, line_3d",
    },
    {
        "key": "polar_sample",
        "label": "Polar Data",
        "icon": "vsPieChart",
        "description": "Wind-like polar coordinate data. Good for: scatter_polar, line_polar",
    },
    {
        "key": "ternary_sample",
        "label": "Ternary Data",
        "icon": "vsTriangleUp",
        "description": "Composition data (soil types). Good for: scatter_ternary, line_ternary",
    },
    {
        "key": "timeline_sample",
        "label": "Timeline",
        "icon": "vsCalendar",
        "description": "Project timeline with task durations. Good for: timeline",
    },
    {
        "key": "flights",
        "label": "Flights",
        "icon": "vsRocket",
        "description": "Flight tracking with lat/lon positions. Good for: scatter_geo, line_geo, scatter_map, line_map",
    },
    {
        "key": "outages",
        "label": "Outages",
        "icon": "vsWarning",
        "description": "Power outage locations with severity. Good for: scatter_map, density_map, scatter_geo",
    },
]


def _create_ohlc_sample() -> Table:
    """Create an OHLC dataset by binning the stocks data into 1-minute intervals.

    This follows the approach from the Deephaven plotly-express docs:
    https://deephaven.io/core/plotly/docs/candlestick/

    Note: Filtered to DOG symbol since candlestick charts can't aggregate
    multiple symbols with the same timestamp.
    """
    import deephaven.agg as agg

    stocks = dx.data.stocks()

    # Compute OHLC per symbol for each minute
    # Use nanoseconds for the bin size (1 minute = 60 * 1e9 nanos)
    # Filter to single symbol since candlestick can't handle multiple symbols
    return (
        stocks.update_view("BinnedTimestamp = lowerBin(Timestamp, 'PT1m')")
        .agg_by(
            [
                agg.first("Open=Price"),
                agg.max_("High=Price"),
                agg.min_("Low=Price"),
                agg.last("Close=Price"),
            ],
            by=["Sym", "BinnedTimestamp"],
        )
        .where("Sym == `DOG`")
    )


def _create_hierarchy_sample() -> Table:
    """Create a hierarchical dataset for treemap, sunburst, icicle charts.

    Creates a product hierarchy: Total -> Category -> Subcategory
    with sales values for each node.
    """
    from deephaven import new_table
    from deephaven.column import string_col, int_col

    # Hierarchical data: names, parents (empty string for root), values
    # Structure: Total (root) -> Electronics, Clothing, Food -> specific items
    return new_table(
        [
            string_col(
                "Name",
                [
                    "Total",
                    "Electronics",
                    "Clothing",
                    "Food",
                    "Phones",
                    "Laptops",
                    "Tablets",
                    "Shirts",
                    "Pants",
                    "Shoes",
                    "Fruits",
                    "Vegetables",
                    "Dairy",
                ],
            ),
            string_col(
                "Parent",
                [
                    "",  # root has no parent
                    "Total",
                    "Total",
                    "Total",
                    "Electronics",
                    "Electronics",
                    "Electronics",
                    "Clothing",
                    "Clothing",
                    "Clothing",
                    "Food",
                    "Food",
                    "Food",
                ],
            ),
            int_col(
                "Sales",
                [
                    0,  # root value (will be sum of children)
                    0,
                    0,
                    0,  # category values (sum of children)
                    500,
                    400,
                    300,  # Electronics items
                    200,
                    250,
                    150,  # Clothing items
                    100,
                    80,
                    120,  # Food items
                ],
            ),
        ]
    )


def _create_funnel_sample() -> Table:
    """Create a funnel dataset for funnel and funnel_area charts.

    Creates a sales funnel with stages from awareness to purchase.
    """
    from deephaven import new_table
    from deephaven.column import string_col, int_col

    return new_table(
        [
            string_col(
                "Stage",
                ["Website Visits", "Downloads", "Signups", "Free Trials", "Purchases"],
            ),
            int_col("Count", [10000, 5000, 2500, 1000, 500]),
        ]
    )


def _create_scatter_3d_sample() -> Table:
    """Create a 3D scatter dataset.

    Creates random 3D points with categories for demonstrating 3D scatter/line.
    """
    from deephaven import new_table
    from deephaven.column import string_col, double_col
    import random

    # Generate random 3D points with categories
    n_points = 100
    random.seed(42)

    x_vals = [random.gauss(0, 1) for _ in range(n_points)]
    y_vals = [random.gauss(0, 1) for _ in range(n_points)]
    z_vals = [random.gauss(0, 1) for _ in range(n_points)]
    categories = [random.choice(["A", "B", "C"]) for _ in range(n_points)]
    sizes = [random.uniform(5, 20) for _ in range(n_points)]

    return new_table(
        [
            double_col("X", x_vals),
            double_col("Y", y_vals),
            double_col("Z", z_vals),
            string_col("Category", categories),
            double_col("Size", sizes),
        ]
    )


def _create_polar_sample() -> Table:
    """Create a polar coordinate dataset.

    Creates wind-like data with radius (speed) and theta (direction) values.
    """
    from deephaven import new_table
    from deephaven.column import string_col, double_col, int_col
    import random
    import math

    # Generate wind-like polar data
    n_points = 72
    random.seed(42)

    # Directions from 0 to 360 degrees
    theta_vals = [i * 5 for i in range(n_points)]  # 0, 5, 10, ..., 355
    r_vals = [5 + random.gauss(3, 1.5) for _ in range(n_points)]  # Wind speeds
    directions = [
        ["N", "NE", "E", "SE", "S", "SW", "W", "NW"][int((t + 22.5) // 45) % 8]
        for t in theta_vals
    ]

    return new_table(
        [
            double_col("R", r_vals),
            int_col("Theta", theta_vals),
            string_col("Direction", directions),
        ]
    )


def _create_ternary_sample() -> Table:
    """Create a ternary coordinate dataset.

    Creates composition data (e.g., soil types) where a + b + c = 1.
    """
    from deephaven import new_table
    from deephaven.column import string_col, double_col
    import random

    # Generate composition data (proportions that sum to 1)
    n_points = 50
    random.seed(42)

    a_vals = []
    b_vals = []
    c_vals = []
    types = []

    for _ in range(n_points):
        # Generate random proportions that sum to 1
        raw_a = random.random()
        raw_b = random.random()
        raw_c = random.random()
        total = raw_a + raw_b + raw_c

        a = raw_a / total
        b = raw_b / total
        c = raw_c / total

        a_vals.append(a)
        b_vals.append(b)
        c_vals.append(c)

        # Classify based on dominant component
        if a > 0.5:
            types.append("Sand")
        elif b > 0.5:
            types.append("Silt")
        elif c > 0.5:
            types.append("Clay")
        else:
            types.append("Loam")

    return new_table(
        [
            double_col("Sand", a_vals),
            double_col("Silt", b_vals),
            double_col("Clay", c_vals),
            string_col("SoilType", types),
        ]
    )


def _create_timeline_sample() -> Table:
    """Create a timeline/Gantt chart dataset.

    Creates project tasks with start and end dates.
    """
    from deephaven import new_table
    from deephaven.column import string_col, datetime_col
    from deephaven.time import to_j_instant

    # Project timeline data
    tasks = [
        ("Planning", "2024-01-01T00:00:00Z", "2024-01-15T00:00:00Z", "Phase 1"),
        ("Design", "2024-01-10T00:00:00Z", "2024-02-01T00:00:00Z", "Phase 1"),
        ("Development", "2024-01-25T00:00:00Z", "2024-03-15T00:00:00Z", "Phase 2"),
        ("Testing", "2024-03-01T00:00:00Z", "2024-03-31T00:00:00Z", "Phase 2"),
        ("Deployment", "2024-03-25T00:00:00Z", "2024-04-05T00:00:00Z", "Phase 3"),
        ("Documentation", "2024-02-15T00:00:00Z", "2024-04-01T00:00:00Z", "Phase 2"),
        ("Training", "2024-03-20T00:00:00Z", "2024-04-10T00:00:00Z", "Phase 3"),
        ("Launch", "2024-04-01T00:00:00Z", "2024-04-15T00:00:00Z", "Phase 3"),
    ]

    return new_table(
        [
            string_col("Task", [t[0] for t in tasks]),
            datetime_col("Start", [to_j_instant(t[1]) for t in tasks]),
            datetime_col("End", [to_j_instant(t[2]) for t in tasks]),
            string_col("Phase", [t[3] for t in tasks]),
        ]
    )


def _load_dataset(name: str) -> Table:
    """Load a dataset by name."""
    if name == "ohlc_sample":
        return _create_ohlc_sample()
    if name == "hierarchy_sample":
        return _create_hierarchy_sample()
    if name == "funnel_sample":
        return _create_funnel_sample()
    if name == "scatter_3d_sample":
        return _create_scatter_3d_sample()
    if name == "polar_sample":
        return _create_polar_sample()
    if name == "ternary_sample":
        return _create_ternary_sample()
    if name == "timeline_sample":
        return _create_timeline_sample()
    if name == "flights":
        return dx.data.flights()
    if name == "outages":
        return dx.data.outages()

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


# Mapping of data types to icons and friendly names
DATA_TYPE_INFO = {
    # Numeric types - use vsSymbolNumeric or a number-related icon
    "int": {"icon": "vsSymbolNumeric", "label": "Integer"},
    "long": {"icon": "vsSymbolNumeric", "label": "Long"},
    "short": {"icon": "vsSymbolNumeric", "label": "Short"},
    "byte": {"icon": "vsSymbolNumeric", "label": "Byte"},
    "float": {"icon": "vsSymbolNumeric", "label": "Float"},
    "double": {"icon": "vsSymbolNumeric", "label": "Double"},
    "java.lang.Integer": {"icon": "vsSymbolNumeric", "label": "Integer"},
    "java.lang.Long": {"icon": "vsSymbolNumeric", "label": "Long"},
    "java.lang.Short": {"icon": "vsSymbolNumeric", "label": "Short"},
    "java.lang.Byte": {"icon": "vsSymbolNumeric", "label": "Byte"},
    "java.lang.Float": {"icon": "vsSymbolNumeric", "label": "Float"},
    "java.lang.Double": {"icon": "vsSymbolNumeric", "label": "Double"},
    "java.math.BigDecimal": {"icon": "vsSymbolNumeric", "label": "Decimal"},
    "java.math.BigInteger": {"icon": "vsSymbolNumeric", "label": "Big Integer"},
    # String types
    "java.lang.String": {"icon": "vsSymbolString", "label": "String"},
    "char": {"icon": "vsSymbolString", "label": "Char"},
    "java.lang.Character": {"icon": "vsSymbolString", "label": "Character"},
    # Boolean
    "boolean": {"icon": "vsSymbolBoolean", "label": "Boolean"},
    "java.lang.Boolean": {"icon": "vsSymbolBoolean", "label": "Boolean"},
    # Date/Time types
    "java.time.Instant": {"icon": "vsCalendar", "label": "Instant"},
    "java.time.LocalDate": {"icon": "vsCalendar", "label": "Date"},
    "java.time.LocalTime": {"icon": "vsClock", "label": "Time"},
    "java.time.LocalDateTime": {"icon": "vsCalendar", "label": "DateTime"},
    "java.time.ZonedDateTime": {"icon": "vsCalendar", "label": "ZonedDateTime"},
    "io.deephaven.time.DateTime": {"icon": "vsCalendar", "label": "DateTime"},
}


def _get_type_info(type_str: str) -> dict:
    """Get icon and label for a data type."""
    # Check for exact match first
    if type_str in DATA_TYPE_INFO:
        return DATA_TYPE_INFO[type_str]
    # Check for array types
    if type_str.endswith("[]"):
        return {"icon": "vsSymbolArray", "label": "Array"}
    # Default for unknown types
    return {"icon": "vsSymbolField", "label": type_str.split(".")[-1]}


def _get_column_info(table: Table) -> list[dict]:
    """Get column names and types from a table."""
    result = []
    for col in table.columns:
        type_str = str(col.data_type)
        type_info = _get_type_info(type_str)
        result.append(
            {
                "name": col.name,
                "type": type_str,
                "type_label": type_info["label"],
                "icon": type_info["icon"],
            }
        )
    return result


def _get_column_names(table: Table) -> list[str]:
    """Get column names from a table."""
    return [col.name for col in table.columns]


def _column_picker_items(columns: list[dict], include_none: bool = True) -> list[dict]:
    """Create picker items from column info with types and icons."""
    items = []
    if include_none:
        items.append(
            {
                "key": "",
                "label": "(None)",
                "description": "",
                "icon": "vsCircleSlash",
            }
        )
    items.extend(
        {
            "key": col["name"],
            "label": col["name"],
            "description": col["type_label"],
            "icon": col["icon"],
        }
        for col in columns
    )
    return items


def _render_column_picker_items(items: list[dict]) -> list:
    """Render column picker items with icons and descriptions."""
    return [
        ui.item(
            ui.icon(item["icon"]),
            ui.text(item["label"]),
            (
                ui.text(item["description"], slot="description")
                if item["description"]
                else None
            ),
            key=item["key"],
            text_value=item["label"],
        )
        for item in items
    ]


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

    # Hierarchical chart state (treemap, sunburst, icicle)
    parents_col, set_parents_col = ui.use_state("")

    # 3D chart state
    z_col, set_z_col = ui.use_state("")

    # Polar chart state
    r_col, set_r_col = ui.use_state("")
    theta_col, set_theta_col = ui.use_state("")

    # Ternary chart state
    a_col, set_a_col = ui.use_state("")
    b_col, set_b_col = ui.use_state("")
    c_col, set_c_col = ui.use_state("")

    # Timeline chart state
    x_start_col, set_x_start_col = ui.use_state("")
    x_end_col, set_x_end_col = ui.use_state("")

    # Map/Geo chart state
    lat_col, set_lat_col = ui.use_state("")
    lon_col, set_lon_col = ui.use_state("")
    locations_col, set_locations_col = ui.use_state("")
    locationmode, set_locationmode = ui.use_state("")
    radius, set_radius = ui.use_state(15)
    zoom, set_zoom = ui.use_state(3)
    center_preset, set_center_preset = ui.use_state("none")
    center_lat, set_center_lat = ui.use_state(0.0)
    center_lon, set_center_lon = ui.use_state(0.0)
    map_style, set_map_style = ui.use_state("")

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
        set_by_cols(by_cols[:index] + by_cols[index + 1 :])

    # Get column info from table (with types and icons)
    column_info = _get_column_info(table)
    columns = [col["name"] for col in column_info]
    column_items = _column_picker_items(column_info, include_none=False)
    optional_column_items = _column_picker_items(column_info, include_none=True)

    # Available columns for group by at each position (exclude already selected except current)
    def get_by_picker_items(index: int) -> list[dict]:
        """Get picker items for a group by dropdown, excluding already selected columns."""
        selected_at_other_indices = [c for i, c in enumerate(by_cols) if i != index]
        available = [
            col for col in column_info if col["name"] not in selected_at_other_indices
        ]
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

    # Hierarchical chart config (treemap, sunburst, icicle)
    if chart_type in ("treemap", "sunburst", "icicle"):
        if names_col:
            config["names"] = names_col
        if values_col:
            config["values"] = values_col
        if parents_col:
            config["parents"] = parents_col

    # Funnel chart config
    if chart_type == "funnel":
        if x_col:
            config["x"] = x_col
        if y_col:
            config["y"] = y_col

    # Funnel area chart config
    if chart_type == "funnel_area":
        if names_col:
            config["names"] = names_col
        if values_col:
            config["values"] = values_col

    # 3D chart config (scatter_3d, line_3d)
    if chart_type in ("scatter_3d", "line_3d"):
        if x_col:
            config["x"] = x_col
        if y_col:
            config["y"] = y_col
        if z_col:
            config["z"] = z_col
        if by_cols:
            config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols
        if chart_type == "scatter_3d":
            if size_col:
                config["size"] = size_col
            if color_col:
                config["color"] = color_col

    # Polar chart config (scatter_polar, line_polar)
    if chart_type in ("scatter_polar", "line_polar"):
        if r_col:
            config["r"] = r_col
        if theta_col:
            config["theta"] = theta_col
        if by_cols:
            config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols
        if chart_type == "scatter_polar":
            if size_col:
                config["size"] = size_col
            if color_col:
                config["color"] = color_col

    # Ternary chart config (scatter_ternary, line_ternary)
    if chart_type in ("scatter_ternary", "line_ternary"):
        if a_col:
            config["a"] = a_col
        if b_col:
            config["b"] = b_col
        if c_col:
            config["c"] = c_col
        if by_cols:
            config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols
        if chart_type == "scatter_ternary":
            if size_col:
                config["size"] = size_col
            if color_col:
                config["color"] = color_col

    # Timeline chart config
    if chart_type == "timeline":
        if x_start_col:
            config["x_start"] = x_start_col
        if x_end_col:
            config["x_end"] = x_end_col
        if y_col:
            config["y"] = y_col
        if by_cols:
            config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols

    # Map/Geo chart config (scatter_geo, line_geo)
    if chart_type in ("scatter_geo", "line_geo"):
        if lat_col:
            config["lat"] = lat_col
        if lon_col:
            config["lon"] = lon_col
        if locations_col:
            config["locations"] = locations_col
        if locationmode:
            config["locationmode"] = locationmode
        if by_cols:
            config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols
        if chart_type == "scatter_geo":
            if size_col:
                config["size"] = size_col
            if color_col:
                config["color"] = color_col
        elif chart_type == "line_geo":
            if color_col:
                config["color"] = color_col

    # Tile-based map chart config (scatter_map, line_map, density_map)
    if chart_type in ("scatter_map", "line_map", "density_map"):
        if lat_col:
            config["lat"] = lat_col
        if lon_col:
            config["lon"] = lon_col
        if zoom:
            config["zoom"] = zoom
        # Set center based on preset or custom values
        if center_preset == "outages":
            config["center"] = OUTAGE_CENTER
        elif center_preset == "flights":
            config["center"] = FLIGHT_CENTER
        elif center_preset == "custom":
            config["center"] = {"lat": center_lat, "lon": center_lon}
        if map_style:
            config["map_style"] = map_style
        if chart_type == "scatter_map":
            if by_cols:
                config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols
            if size_col:
                config["size"] = size_col
            if color_col:
                config["color"] = color_col
        elif chart_type == "line_map":
            if by_cols:
                config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols
            if color_col:
                config["color"] = color_col
        elif chart_type == "density_map":
            if z_col:
                config["z"] = z_col
            if radius:
                config["radius"] = radius

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
        can_create_chart = bool(
            x_col and open_col and high_col and low_col and close_col
        )
    elif chart_type in ("treemap", "sunburst", "icicle"):
        can_create_chart = bool(names_col and values_col and parents_col)
    elif chart_type == "funnel":
        can_create_chart = bool(x_col and y_col)
    elif chart_type == "funnel_area":
        can_create_chart = bool(names_col and values_col)
    elif chart_type in ("scatter_3d", "line_3d"):
        can_create_chart = bool(x_col and y_col and z_col)
    elif chart_type in ("scatter_polar", "line_polar"):
        can_create_chart = bool(r_col and theta_col)
    elif chart_type in ("scatter_ternary", "line_ternary"):
        can_create_chart = bool(a_col and b_col and c_col)
    elif chart_type == "timeline":
        can_create_chart = bool(x_start_col and x_end_col and y_col)
    elif chart_type in ("scatter_geo", "line_geo"):
        can_create_chart = bool((lat_col and lon_col) or locations_col)
    elif chart_type in ("scatter_map", "line_map", "density_map"):
        can_create_chart = bool(lat_col and lon_col)

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
                *[
                    ui.item(
                        ui.icon(ct["icon"]),
                        ct["label"],
                        key=ct["key"],
                        text_value=ct["label"],
                    )
                    for ct in CHART_TYPES
                ],
                label="Chart Type",
                selected_key=chart_type,
                on_selection_change=set_chart_type,
                width="100%",
            ),
            # X and Y columns side by side (for scatter, line, bar, area, box, violin, strip, density_heatmap)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="X",
                        selected_key=x_col,
                        on_selection_change=set_x_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Y",
                        selected_key=y_col,
                        on_selection_change=set_y_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type
                in (
                    "scatter",
                    "line",
                    "bar",
                    "area",
                    "box",
                    "violin",
                    "strip",
                    "density_heatmap",
                )
                else None
            ),
            # X and/or Y for histogram (only one required)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="X",
                        selected_key=x_col,
                        on_selection_change=set_x_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Y",
                        selected_key=y_col,
                        on_selection_change=set_y_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "histogram"
                else None
            ),
            # X column for candlestick/ohlc (usually timestamp/date)
            (
                ui.picker(
                    *_render_column_picker_items(column_items),
                    label="X (Date/Time)",
                    selected_key=x_col,
                    on_selection_change=set_x_col,
                    width="100%",
                )
                if chart_type in ("candlestick", "ohlc")
                else None
            ),
            # OHLC columns for candlestick/ohlc
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Open",
                        selected_key=open_col,
                        on_selection_change=set_open_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="High",
                        selected_key=high_col,
                        on_selection_change=set_high_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("candlestick", "ohlc")
                else None
            ),
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Low",
                        selected_key=low_col,
                        on_selection_change=set_low_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Close",
                        selected_key=close_col,
                        on_selection_change=set_close_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("candlestick", "ohlc")
                else None
            ),
            # Names and Values columns (for pie)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Names",
                        selected_key=names_col,
                        on_selection_change=set_names_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Values",
                        selected_key=values_col,
                        on_selection_change=set_values_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "pie"
                else None
            ),
            # Names, Values, and Parents columns (for treemap, sunburst, icicle)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Names",
                        selected_key=names_col,
                        on_selection_change=set_names_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Values",
                        selected_key=values_col,
                        on_selection_change=set_values_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("treemap", "sunburst", "icicle")
                else None
            ),
            (
                ui.picker(
                    *_render_column_picker_items(column_items),
                    label="Parents",
                    selected_key=parents_col,
                    on_selection_change=set_parents_col,
                    width="100%",
                )
                if chart_type in ("treemap", "sunburst", "icicle")
                else None
            ),
            # Names and Values columns (for funnel_area)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Names",
                        selected_key=names_col,
                        on_selection_change=set_names_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Values",
                        selected_key=values_col,
                        on_selection_change=set_values_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "funnel_area"
                else None
            ),
            # X and Y columns (for funnel)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="X",
                        selected_key=x_col,
                        on_selection_change=set_x_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Y",
                        selected_key=y_col,
                        on_selection_change=set_y_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "funnel"
                else None
            ),
            # X, Y, Z columns (for 3D charts)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="X",
                        selected_key=x_col,
                        on_selection_change=set_x_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Y",
                        selected_key=y_col,
                        on_selection_change=set_y_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Z",
                        selected_key=z_col,
                        on_selection_change=set_z_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_3d", "line_3d")
                else None
            ),
            # R and Theta columns (for polar charts)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="R (radius)",
                        selected_key=r_col,
                        on_selection_change=set_r_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Theta (angle)",
                        selected_key=theta_col,
                        on_selection_change=set_theta_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_polar", "line_polar")
                else None
            ),
            # A, B, C columns (for ternary charts)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="A",
                        selected_key=a_col,
                        on_selection_change=set_a_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="B",
                        selected_key=b_col,
                        on_selection_change=set_b_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="C",
                        selected_key=c_col,
                        on_selection_change=set_c_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_ternary", "line_ternary")
                else None
            ),
            # X Start, X End, Y columns (for timeline)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Start",
                        selected_key=x_start_col,
                        on_selection_change=set_x_start_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="End",
                        selected_key=x_end_col,
                        on_selection_change=set_x_end_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "timeline"
                else None
            ),
            (
                ui.picker(
                    *_render_column_picker_items(column_items),
                    label="Y (Task/Label)",
                    selected_key=y_col,
                    on_selection_change=set_y_col,
                    width="100%",
                )
                if chart_type == "timeline"
                else None
            ),
            # Geo chart controls (scatter_geo, line_geo)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Lat",
                        selected_key=lat_col,
                        on_selection_change=set_lat_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Lon",
                        selected_key=lon_col,
                        on_selection_change=set_lon_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_geo", "line_geo")
                else None
            ),
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Locations",
                        selected_key=locations_col,
                        on_selection_change=set_locations_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        ui.item("(None)", key=""),
                        ui.item("ISO-3", key="ISO-3"),
                        ui.item("USA-states", key="USA-states"),
                        ui.item("Country names", key="country names"),
                        label="Location Mode",
                        selected_key=locationmode,
                        on_selection_change=set_locationmode,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_geo", "line_geo")
                else None
            ),
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Size",
                        selected_key=size_col,
                        on_selection_change=set_size_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Color",
                        selected_key=color_col,
                        on_selection_change=set_color_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "scatter_geo"
                else None
            ),
            (
                ui.picker(
                    *_render_column_picker_items(optional_column_items),
                    label="Color",
                    selected_key=color_col,
                    on_selection_change=set_color_col,
                    width="100%",
                )
                if chart_type == "line_geo"
                else None
            ),
            # Tile map chart controls (scatter_map, line_map, density_map)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Lat",
                        selected_key=lat_col,
                        on_selection_change=set_lat_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Lon",
                        selected_key=lon_col,
                        on_selection_change=set_lon_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_map", "line_map", "density_map")
                else None
            ),
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Size",
                        selected_key=size_col,
                        on_selection_change=set_size_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Color",
                        selected_key=color_col,
                        on_selection_change=set_color_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "scatter_map"
                else None
            ),
            (
                ui.picker(
                    *_render_column_picker_items(optional_column_items),
                    label="Color",
                    selected_key=color_col,
                    on_selection_change=set_color_col,
                    width="100%",
                )
                if chart_type == "line_map"
                else None
            ),
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Z (Intensity)",
                        selected_key=z_col,
                        on_selection_change=set_z_col,
                        flex_grow=1,
                    ),
                    ui.number_field(
                        label="Radius",
                        value=radius,
                        on_change=set_radius,
                        min_value=1,
                        max_value=50,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "density_map"
                else None
            ),
            (
                ui.number_field(
                    label="Zoom",
                    value=zoom,
                    on_change=set_zoom,
                    min_value=0,
                    max_value=20,
                    width="100%",
                )
                if chart_type in ("scatter_map", "line_map", "density_map")
                else None
            ),
            # Center selection for tile-based maps
            (
                ui.picker(
                    *[
                        ui.item(item["label"], key=item["key"])
                        for item in MAP_CENTER_PRESETS
                    ],
                    label="Map Center",
                    selected_key=center_preset,
                    on_selection_change=set_center_preset,
                    width="100%",
                )
                if chart_type in ("scatter_map", "line_map", "density_map")
                else None
            ),
            # Custom center coordinates (only shown when "custom" is selected)
            (
                ui.flex(
                    ui.number_field(
                        label="Center Latitude",
                        value=center_lat,
                        on_change=set_center_lat,
                        min_value=-90,
                        max_value=90,
                        flex_grow=1,
                    ),
                    ui.number_field(
                        label="Center Longitude",
                        value=center_lon,
                        on_change=set_center_lon,
                        min_value=-180,
                        max_value=180,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_map", "line_map", "density_map")
                and center_preset == "custom"
                else None
            ),
            # Map style selection for tile-based maps
            (
                ui.picker(
                    *[
                        ui.item(item["label"], key=item["key"])
                        for item in MAP_STYLE_OPTIONS
                    ],
                    label="Map Style",
                    selected_key=map_style,
                    on_selection_change=set_map_style,
                    width="100%",
                )
                if chart_type in ("scatter_map", "line_map", "density_map")
                else None
            ),
            # Group by (for charts that support it - not pie, density_heatmap, financial, or hierarchical)
            (
                ui.flex(
                    # Show dropdowns for each selected column plus one empty one
                    *[
                        ui.flex(
                            ui.picker(
                                *_render_column_picker_items(get_by_picker_items(i)),
                                label="Group By" if i == 0 else f"Group {i + 1}",
                                selected_key=by_cols[i] if i < len(by_cols) else "",
                                on_selection_change=lambda col, idx=i: update_by_col(
                                    idx, col
                                ),
                                flex_grow=1,
                            ),
                            # Trash button to remove (only show for selected columns, not the empty "add" picker)
                            (
                                ui.action_button(
                                    ui.icon("vsTrash"),
                                    on_press=(lambda idx: lambda: remove_by_col(idx))(
                                        i
                                    ),
                                    is_quiet=True,
                                    aria_label=f"Remove group {i + 1}",
                                )
                                if i < len(by_cols)
                                else None
                            ),
                            direction="row",
                            gap="size-100",
                            align_items="end",
                            width="100%",
                        )
                        for i in range(len(by_cols) + 1)
                    ],  # +1 for the "add new" picker
                    direction="column",
                    gap="size-100",
                    width="100%",
                )
                if chart_type
                not in (
                    "pie",
                    "density_heatmap",
                    "candlestick",
                    "ohlc",
                    "treemap",
                    "sunburst",
                    "icicle",
                    "funnel",
                    "funnel_area",
                    "scatter_polar",
                    "line_polar",
                    "scatter_ternary",
                    "line_ternary",
                    "timeline",
                    "scatter_geo",
                    "line_geo",
                    "scatter_map",
                    "line_map",
                    "density_map",
                )
                else None
            ),
            # Histogram-specific options
            (
                ui.number_field(
                    label="Number of Bins",
                    value=nbins,
                    on_change=set_nbins,
                    min_value=1,
                    max_value=1000,
                    width="100%",
                )
                if chart_type == "histogram"
                else None
            ),
            # Scatter-specific options
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Size",
                        selected_key=size_col,
                        on_selection_change=set_size_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Color",
                        selected_key=color_col,
                        on_selection_change=set_color_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "scatter"
                else None
            ),
            # Line-specific options
            (
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
                )
                if chart_type == "line"
                else None
            ),
            # Bar-specific options
            (
                ui.picker(
                    *[ui.item(o["label"], key=o["key"]) for o in ORIENTATIONS],
                    label="Orientation",
                    selected_key=orientation,
                    on_selection_change=set_orientation,
                    width="100%",
                )
                if chart_type == "bar"
                else None
            ),
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
    elif chart_type in ("scatter_geo", "line_geo"):
        placeholder_msg = "Select Lat+Lon or Locations to preview chart"
    elif chart_type in ("scatter_map", "line_map", "density_map"):
        placeholder_msg = "Select Lat and Lon columns to preview chart"
    else:
        placeholder_msg = "Select X and Y columns to preview chart"

    chart_area = ui.view(
        (
            ui.text(
                error_message,
                UNSAFE_style={"color": "var(--spectrum-negative-color-900)"},
            )
            if error_message
            else (
                chart
                if chart
                else ui.flex(
                    ui.text(
                        placeholder_msg,
                        UNSAFE_style={"color": "var(--spectrum-gray-600)"},
                    ),
                    align_items="center",
                    justify_content="center",
                    height="100%",
                )
            )
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

    # Hierarchical chart state
    parents_col, set_parents_col = ui.use_state("")

    # 3D chart state
    z_col, set_z_col = ui.use_state("")

    # Polar chart state
    r_col, set_r_col = ui.use_state("")
    theta_col, set_theta_col = ui.use_state("")

    # Ternary chart state
    a_col, set_a_col = ui.use_state("")
    b_col, set_b_col = ui.use_state("")
    c_col, set_c_col = ui.use_state("")

    # Timeline chart state
    x_start_col, set_x_start_col = ui.use_state("")
    x_end_col, set_x_end_col = ui.use_state("")

    # Map/Geo chart state
    lat_col, set_lat_col = ui.use_state("")
    lon_col, set_lon_col = ui.use_state("")
    locations_col, set_locations_col = ui.use_state("")
    locationmode, set_locationmode = ui.use_state("")
    radius, set_radius = ui.use_state(15)
    zoom, set_zoom = ui.use_state(3)
    center_preset, set_center_preset = ui.use_state("none")
    center_lat, set_center_lat = ui.use_state(0.0)
    center_lon, set_center_lon = ui.use_state(0.0)
    map_style, set_map_style = ui.use_state("")

    # Advanced options state (Phase 9)
    # Text and hover options
    text_col, set_text_col = ui.use_state("")
    hover_name_col, set_hover_name_col = ui.use_state("")

    # Error bars
    error_x_col, set_error_x_col = ui.use_state("")
    error_x_minus_col, set_error_x_minus_col = ui.use_state("")
    error_y_col, set_error_y_col = ui.use_state("")
    error_y_minus_col, set_error_y_minus_col = ui.use_state("")

    # Marginal plots (scatter only)
    marginal_x, set_marginal_x = ui.use_state("")
    marginal_y, set_marginal_y = ui.use_state("")

    # Axis configuration
    log_x, set_log_x = ui.use_state(False)
    log_y, set_log_y = ui.use_state(False)
    range_x_min, set_range_x_min = ui.use_state(None)
    range_x_max, set_range_x_max = ui.use_state(None)
    range_y_min, set_range_y_min = ui.use_state(None)
    range_y_max, set_range_y_max = ui.use_state(None)
    xaxis_title, set_xaxis_title = ui.use_state("")
    yaxis_title, set_yaxis_title = ui.use_state("")

    # Opacity (scatter, bar, area, pie)
    opacity, set_opacity = ui.use_state(1.0)

    # Line-specific advanced options
    line_dash_col, set_line_dash_col = ui.use_state("")
    width_col, set_width_col = ui.use_state("")

    # Bar-specific advanced options (Phase 10)
    barmode, set_barmode = ui.use_state("relative")
    text_auto, set_text_auto = ui.use_state(False)

    # Pie-specific advanced options (Phase 10)
    hole, set_hole = ui.use_state(0.0)

    # Distribution chart advanced options (Phase 11)
    # Histogram options
    histfunc, set_histfunc = ui.use_state("count")
    histnorm, set_histnorm = ui.use_state("")
    barnorm, set_barnorm = ui.use_state("")
    hist_barmode, set_hist_barmode = ui.use_state("relative")
    cumulative, set_cumulative = ui.use_state(False)
    nbins, set_nbins = ui.use_state(0)  # 0 = auto

    # Box plot options
    boxmode, set_boxmode = ui.use_state("group")
    notched, set_notched = ui.use_state(False)
    box_points, set_box_points = ui.use_state("outliers")

    # Violin plot options
    violinmode, set_violinmode = ui.use_state("group")
    violin_box, set_violin_box = ui.use_state(False)
    violin_points, set_violin_points = ui.use_state("")

    # Strip plot options
    stripmode, set_stripmode = ui.use_state("group")

    # Financial chart advanced options (Phase 12)
    increasing_color, set_increasing_color = ui.use_state(
        None
    )  # Color for up candles/bars
    decreasing_color, set_decreasing_color = ui.use_state(
        None
    )  # Color for down candles/bars

    # Hierarchical chart advanced options (Phase 13)
    hier_color_col, set_hier_color_col = ui.use_state("")  # Color column for hierarchical
    branchvalues, set_branchvalues = ui.use_state("")  # "total" or "remainder"
    maxdepth, set_maxdepth = ui.use_state(-1)  # Max visible levels, -1 for all

    # Funnel chart advanced options (Phase 13)
    funnel_text_col, set_funnel_text_col = ui.use_state("")  # Text column for funnel
    funnel_color_col, set_funnel_color_col = ui.use_state("")  # Color column for funnel
    funnel_orientation, set_funnel_orientation = ui.use_state("")  # "v" or "h"

    # Funnel area advanced options (Phase 13)
    funnel_area_color_col, set_funnel_area_color_col = ui.use_state(
        ""
    )  # Color column for funnel_area

    # Rendering options
    render_mode, set_render_mode = ui.use_state("webgl")
    template, set_template = ui.use_state("")

    # Advanced section expanded state
    advanced_expanded, set_advanced_expanded = ui.use_state(False)

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
        set_by_cols(by_cols[:index] + by_cols[index + 1 :])

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
        set_parents_col("")
        set_z_col("")
        set_r_col("")
        set_theta_col("")
        set_a_col("")
        set_b_col("")
        set_c_col("")
        set_x_start_col("")
        set_x_end_col("")
        set_lat_col("")
        set_lon_col("")
        set_locations_col("")
        set_locationmode("")
        # Reset map center options
        set_center_preset("none")
        set_center_lat(0.0)
        set_center_lon(0.0)
        set_map_style("")

    # Get column info from table (with types and icons)
    column_info = _get_column_info(table)
    columns = [col["name"] for col in column_info]
    column_items = _column_picker_items(column_info, include_none=False)
    optional_column_items = _column_picker_items(column_info, include_none=True)

    # Available columns for group by at each position (exclude already selected except current)
    def get_by_picker_items(index: int) -> list[dict]:
        """Get picker items for a group by dropdown, excluding already selected columns."""
        selected_at_other_indices = [c for i, c in enumerate(by_cols) if i != index]
        available = [
            col for col in column_info if col["name"] not in selected_at_other_indices
        ]
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
        # Advanced scatter options
        if text_col:
            config["text"] = text_col
        if hover_name_col:
            config["hover_name"] = hover_name_col
        if opacity is not None and opacity != 1.0:
            config["opacity"] = opacity
        if marginal_x:
            config["marginal_x"] = marginal_x
        if marginal_y:
            config["marginal_y"] = marginal_y
        # Error bars
        if error_x_col:
            config["error_x"] = error_x_col
        if error_x_minus_col:
            config["error_x_minus"] = error_x_minus_col
        if error_y_col:
            config["error_y"] = error_y_col
        if error_y_minus_col:
            config["error_y_minus"] = error_y_minus_col
        # Axis configuration
        if log_x:
            config["log_x"] = log_x
        if log_y:
            config["log_y"] = log_y
        if range_x_min is not None and range_x_max is not None:
            config["range_x"] = [range_x_min, range_x_max]
        if range_y_min is not None and range_y_max is not None:
            config["range_y"] = [range_y_min, range_y_max]
        if xaxis_title:
            config["xaxis_titles"] = xaxis_title
        if yaxis_title:
            config["yaxis_titles"] = yaxis_title
        # Rendering
        if render_mode and render_mode != "webgl":
            config["render_mode"] = render_mode
        if template:
            config["template"] = template
    elif chart_type == "line":
        config["markers"] = markers
        if line_shape:
            config["line_shape"] = line_shape
        if color_col:
            config["color"] = color_col
        if size_col:
            config["size"] = size_col
        if symbol_col:
            config["symbol"] = symbol_col
        # Advanced line options
        if text_col:
            config["text"] = text_col
        if hover_name_col:
            config["hover_name"] = hover_name_col
        if line_dash_col:
            config["line_dash"] = line_dash_col
        if width_col:
            config["width"] = width_col
        # Error bars
        if error_x_col:
            config["error_x"] = error_x_col
        if error_x_minus_col:
            config["error_x_minus"] = error_x_minus_col
        if error_y_col:
            config["error_y"] = error_y_col
        if error_y_minus_col:
            config["error_y_minus"] = error_y_minus_col
        # Axis configuration
        if log_x:
            config["log_x"] = log_x
        if log_y:
            config["log_y"] = log_y
        if range_x_min is not None and range_x_max is not None:
            config["range_x"] = [range_x_min, range_x_max]
        if range_y_min is not None and range_y_max is not None:
            config["range_y"] = [range_y_min, range_y_max]
        if xaxis_title:
            config["xaxis_titles"] = xaxis_title
        if yaxis_title:
            config["yaxis_titles"] = yaxis_title
        # Rendering
        if render_mode and render_mode != "webgl":
            config["render_mode"] = render_mode
        if template:
            config["template"] = template
    elif chart_type == "bar":
        config["orientation"] = orientation
        # Advanced bar options (Phase 10)
        if text_col:
            config["text"] = text_col
        if hover_name_col:
            config["hover_name"] = hover_name_col
        if opacity is not None and opacity != 1.0:
            config["opacity"] = opacity
        if barmode and barmode != "relative":
            config["barmode"] = barmode
        if text_auto:
            config["text_auto"] = text_auto
        # Error bars
        if error_x_col:
            config["error_x"] = error_x_col
        if error_x_minus_col:
            config["error_x_minus"] = error_x_minus_col
        if error_y_col:
            config["error_y"] = error_y_col
        if error_y_minus_col:
            config["error_y_minus"] = error_y_minus_col
        # Axis configuration (bar only supports log axes, not axis titles)
        if log_x:
            config["log_x"] = log_x
        if log_y:
            config["log_y"] = log_y
        # Rendering
        if template:
            config["template"] = template
    elif chart_type == "area":
        # Advanced area options (Phase 10)
        config["markers"] = markers
        if line_shape:
            config["line_shape"] = line_shape
        if text_col:
            config["text"] = text_col
        if hover_name_col:
            config["hover_name"] = hover_name_col
        if opacity is not None and opacity != 1.0:
            config["opacity"] = opacity
        # Axis configuration
        if log_x:
            config["log_x"] = log_x
        if log_y:
            config["log_y"] = log_y
        if xaxis_title:
            config["xaxis_titles"] = xaxis_title
        if yaxis_title:
            config["yaxis_titles"] = yaxis_title
        # Rendering
        if template:
            config["template"] = template
    elif chart_type == "pie":
        if names_col:
            config["names"] = names_col
        if values_col:
            config["values"] = values_col
        # Advanced pie options (Phase 10)
        if hover_name_col:
            config["hover_name"] = hover_name_col
        if opacity is not None and opacity != 1.0:
            config["opacity"] = opacity
        if hole > 0.0:
            config["hole"] = hole
        # Rendering
        if template:
            config["template"] = template
    elif chart_type == "histogram":
        # Histogram advanced options (Phase 11)
        if nbins:
            config["nbins"] = nbins
        if histfunc and histfunc != "count":
            config["histfunc"] = histfunc
        if histnorm:
            config["histnorm"] = histnorm
        if barnorm:
            config["barnorm"] = barnorm
        if hist_barmode and hist_barmode != "relative":
            config["hist_barmode"] = hist_barmode
        if cumulative:
            config["cumulative"] = cumulative
        if hover_name_col:
            config["hover_name"] = hover_name_col
        if color_col:
            config["color"] = color_col
        if log_x:
            config["log_x"] = log_x
        if log_y:
            config["log_y"] = log_y
        if template:
            config["template"] = template
    elif chart_type == "box":
        # Box plot advanced options (Phase 11)
        if boxmode and boxmode != "group":
            config["boxmode"] = boxmode
        if box_points and box_points != "outliers":
            config["points"] = box_points if box_points != "false" else False
        if notched:
            config["notched"] = notched
        if hover_name_col:
            config["hover_name"] = hover_name_col
        if color_col:
            config["color"] = color_col
        if log_x:
            config["log_x"] = log_x
        if log_y:
            config["log_y"] = log_y
        if template:
            config["template"] = template
    elif chart_type == "violin":
        # Violin plot advanced options (Phase 11)
        if violinmode and violinmode != "group":
            config["violinmode"] = violinmode
        if violin_points:
            config["points"] = violin_points
        if violin_box:
            config["violin_box"] = violin_box
        if hover_name_col:
            config["hover_name"] = hover_name_col
        if color_col:
            config["color"] = color_col
        if log_x:
            config["log_x"] = log_x
        if log_y:
            config["log_y"] = log_y
        if template:
            config["template"] = template
    elif chart_type == "strip":
        # Strip plot advanced options (Phase 11)
        if stripmode and stripmode != "group":
            config["stripmode"] = stripmode
        if hover_name_col:
            config["hover_name"] = hover_name_col
        if color_col:
            config["color"] = color_col
        if log_x:
            config["log_x"] = log_x
        if log_y:
            config["log_y"] = log_y
        if template:
            config["template"] = template

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
        # Advanced options (Phase 12)
        if increasing_color:
            config["increasing_color_sequence"] = [increasing_color]
        if decreasing_color:
            config["decreasing_color_sequence"] = [decreasing_color]

    # Hierarchical chart config (treemap, sunburst, icicle)
    if chart_type in ("treemap", "sunburst", "icicle"):
        if names_col:
            config["names"] = names_col
        if values_col:
            config["values"] = values_col
        if parents_col:
            config["parents"] = parents_col
        # Advanced options (Phase 13)
        if hier_color_col:
            config["hier_color"] = hier_color_col
        if branchvalues:
            config["branchvalues"] = branchvalues
        if maxdepth != -1:
            config["maxdepth"] = maxdepth
        if template:
            config["template"] = template

    # Funnel chart config
    if chart_type == "funnel":
        if x_col:
            config["x"] = x_col
        if y_col:
            config["y"] = y_col
        # Advanced options (Phase 13)
        if funnel_text_col:
            config["funnel_text"] = funnel_text_col
        if funnel_color_col:
            config["funnel_color"] = funnel_color_col
        if funnel_orientation:
            config["funnel_orientation"] = funnel_orientation
        if opacity is not None and opacity != 1.0:
            config["opacity"] = opacity
        if log_x:
            config["log_x"] = log_x
        if log_y:
            config["log_y"] = log_y
        if template:
            config["template"] = template

    # Funnel area chart config
    if chart_type == "funnel_area":
        if names_col:
            config["names"] = names_col
        if values_col:
            config["values"] = values_col
        # Advanced options (Phase 13)
        if funnel_area_color_col:
            config["funnel_area_color"] = funnel_area_color_col
        if opacity is not None and opacity != 1.0:
            config["opacity"] = opacity
        if template:
            config["template"] = template

    # 3D chart config (scatter_3d, line_3d)
    if chart_type in ("scatter_3d", "line_3d"):
        if x_col:
            config["x"] = x_col
        if y_col:
            config["y"] = y_col
        if z_col:
            config["z"] = z_col
        if by_cols:
            config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols
        if size_col:
            config["size"] = size_col
        if color_col:
            config["color"] = color_col

    # Polar chart config (scatter_polar, line_polar)
    if chart_type in ("scatter_polar", "line_polar"):
        if r_col:
            config["r"] = r_col
        if theta_col:
            config["theta"] = theta_col
        if by_cols:
            config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols
        if size_col:
            config["size"] = size_col
        if color_col:
            config["color"] = color_col

    # Ternary chart config (scatter_ternary, line_ternary)
    if chart_type in ("scatter_ternary", "line_ternary"):
        if a_col:
            config["a"] = a_col
        if b_col:
            config["b"] = b_col
        if c_col:
            config["c"] = c_col
        if by_cols:
            config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols
        if size_col:
            config["size"] = size_col
        if color_col:
            config["color"] = color_col

    # Timeline chart config
    if chart_type == "timeline":
        if x_start_col:
            config["x_start"] = x_start_col
        if x_end_col:
            config["x_end"] = x_end_col
        if y_col:
            config["y"] = y_col
        if by_cols:
            config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols

    # Map/Geo chart config (scatter_geo, line_geo)
    if chart_type in ("scatter_geo", "line_geo"):
        if lat_col:
            config["lat"] = lat_col
        if lon_col:
            config["lon"] = lon_col
        if locations_col:
            config["locations"] = locations_col
        if locationmode:
            config["locationmode"] = locationmode
        if by_cols:
            config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols
        if chart_type == "scatter_geo":
            if size_col:
                config["size"] = size_col
            if color_col:
                config["color"] = color_col
        elif chart_type == "line_geo":
            if color_col:
                config["color"] = color_col

    # Tile-based map chart config (scatter_map, line_map, density_map)
    if chart_type in ("scatter_map", "line_map", "density_map"):
        if lat_col:
            config["lat"] = lat_col
        if lon_col:
            config["lon"] = lon_col
        if zoom:
            config["zoom"] = zoom
        # Set center based on preset or custom values
        if center_preset == "outages":
            config["center"] = OUTAGE_CENTER
        elif center_preset == "flights":
            config["center"] = FLIGHT_CENTER
        elif center_preset == "custom":
            config["center"] = {"lat": center_lat, "lon": center_lon}
        if map_style:
            config["map_style"] = map_style
        if chart_type == "scatter_map":
            if by_cols:
                config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols
            if size_col:
                config["size"] = size_col
            if color_col:
                config["color"] = color_col
        elif chart_type == "line_map":
            if by_cols:
                config["by"] = by_cols[0] if len(by_cols) == 1 else by_cols
            if color_col:
                config["color"] = color_col
        elif chart_type == "density_map":
            if z_col:
                config["z"] = z_col
            if radius:
                config["radius"] = radius

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
        can_create_chart = bool(
            x_col and open_col and high_col and low_col and close_col
        )
    elif chart_type in ("treemap", "sunburst", "icicle"):
        can_create_chart = bool(names_col and values_col and parents_col)
    elif chart_type == "funnel":
        can_create_chart = bool(x_col and y_col)
    elif chart_type == "funnel_area":
        can_create_chart = bool(names_col and values_col)
    elif chart_type in ("scatter_3d", "line_3d"):
        can_create_chart = bool(x_col and y_col and z_col)
    elif chart_type in ("scatter_polar", "line_polar"):
        can_create_chart = bool(r_col and theta_col)
    elif chart_type in ("scatter_ternary", "line_ternary"):
        can_create_chart = bool(a_col and b_col and c_col)
    elif chart_type == "timeline":
        can_create_chart = bool(x_start_col and x_end_col and y_col)
    elif chart_type in ("scatter_geo", "line_geo"):
        can_create_chart = bool((lat_col and lon_col) or locations_col)
    elif chart_type in ("scatter_map", "line_map", "density_map"):
        can_create_chart = bool(lat_col and lon_col)

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
            # Dataset selector with icons and descriptions
            ui.picker(
                *[
                    ui.item(
                        ui.icon(ds["icon"]),
                        ui.text(ds["label"]),
                        ui.text(ds["description"], slot="description"),
                        key=ds["key"],
                        text_value=ds["label"],
                    )
                    for ds in DATASETS
                ],
                label="Dataset",
                selected_key=dataset_name,
                on_selection_change=handle_dataset_change,
                width="100%",
            ),
            # Divider
            ui.divider(),
            # Chart type with icons
            ui.picker(
                *[
                    ui.item(
                        ui.icon(ct["icon"]),
                        ct["label"],
                        key=ct["key"],
                        text_value=ct["label"],
                    )
                    for ct in CHART_TYPES
                ],
                label="Chart Type",
                selected_key=chart_type,
                on_selection_change=set_chart_type,
                width="100%",
            ),
            # X and Y columns side by side (for non-pie charts)
            # X and Y columns side by side (for scatter, line, bar, area, box, violin, strip, density_heatmap)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="X",
                        selected_key=x_col,
                        on_selection_change=set_x_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Y",
                        selected_key=y_col,
                        on_selection_change=set_y_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type
                in (
                    "scatter",
                    "line",
                    "bar",
                    "area",
                    "box",
                    "violin",
                    "strip",
                    "density_heatmap",
                )
                else None
            ),
            # X and/or Y for histogram (only one required)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="X",
                        selected_key=x_col,
                        on_selection_change=set_x_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Y",
                        selected_key=y_col,
                        on_selection_change=set_y_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "histogram"
                else None
            ),
            # X column for candlestick/ohlc (usually timestamp/date)
            (
                ui.picker(
                    *_render_column_picker_items(column_items),
                    label="X (Date/Time)",
                    selected_key=x_col,
                    on_selection_change=set_x_col,
                    width="100%",
                )
                if chart_type in ("candlestick", "ohlc")
                else None
            ),
            # OHLC columns for candlestick/ohlc
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Open",
                        selected_key=open_col,
                        on_selection_change=set_open_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="High",
                        selected_key=high_col,
                        on_selection_change=set_high_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("candlestick", "ohlc")
                else None
            ),
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Low",
                        selected_key=low_col,
                        on_selection_change=set_low_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Close",
                        selected_key=close_col,
                        on_selection_change=set_close_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("candlestick", "ohlc")
                else None
            ),
            # Names and Values columns (for pie charts)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Names",
                        selected_key=names_col,
                        on_selection_change=set_names_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Values",
                        selected_key=values_col,
                        on_selection_change=set_values_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "pie"
                else None
            ),
            # Names, Values, and Parents columns (for treemap, sunburst, icicle)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Names",
                        selected_key=names_col,
                        on_selection_change=set_names_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Values",
                        selected_key=values_col,
                        on_selection_change=set_values_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("treemap", "sunburst", "icicle")
                else None
            ),
            (
                ui.picker(
                    *_render_column_picker_items(column_items),
                    label="Parents",
                    selected_key=parents_col,
                    on_selection_change=set_parents_col,
                    width="100%",
                )
                if chart_type in ("treemap", "sunburst", "icicle")
                else None
            ),
            # Names and Values columns (for funnel_area)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Names",
                        selected_key=names_col,
                        on_selection_change=set_names_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Values",
                        selected_key=values_col,
                        on_selection_change=set_values_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "funnel_area"
                else None
            ),
            # X and Y columns (for funnel)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="X",
                        selected_key=x_col,
                        on_selection_change=set_x_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Y",
                        selected_key=y_col,
                        on_selection_change=set_y_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "funnel"
                else None
            ),
            # 3D chart controls (scatter_3d, line_3d)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="X",
                        selected_key=x_col,
                        on_selection_change=set_x_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Y",
                        selected_key=y_col,
                        on_selection_change=set_y_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Z",
                        selected_key=z_col,
                        on_selection_change=set_z_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_3d", "line_3d")
                else None
            ),
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Size",
                        selected_key=size_col,
                        on_selection_change=set_size_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Color",
                        selected_key=color_col,
                        on_selection_change=set_color_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_3d", "line_3d")
                else None
            ),
            # Polar chart controls (scatter_polar, line_polar)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="R",
                        selected_key=r_col,
                        on_selection_change=set_r_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Theta",
                        selected_key=theta_col,
                        on_selection_change=set_theta_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_polar", "line_polar")
                else None
            ),
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Size",
                        selected_key=size_col,
                        on_selection_change=set_size_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Color",
                        selected_key=color_col,
                        on_selection_change=set_color_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_polar", "line_polar")
                else None
            ),
            # Ternary chart controls (scatter_ternary, line_ternary)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="A",
                        selected_key=a_col,
                        on_selection_change=set_a_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="B",
                        selected_key=b_col,
                        on_selection_change=set_b_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="C",
                        selected_key=c_col,
                        on_selection_change=set_c_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_ternary", "line_ternary")
                else None
            ),
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Size",
                        selected_key=size_col,
                        on_selection_change=set_size_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Color",
                        selected_key=color_col,
                        on_selection_change=set_color_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_ternary", "line_ternary")
                else None
            ),
            # Timeline chart controls
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="X Start",
                        selected_key=x_start_col,
                        on_selection_change=set_x_start_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="X End",
                        selected_key=x_end_col,
                        on_selection_change=set_x_end_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Y",
                        selected_key=y_col,
                        on_selection_change=set_y_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "timeline"
                else None
            ),
            # Geo chart controls (scatter_geo, line_geo)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Lat",
                        selected_key=lat_col,
                        on_selection_change=set_lat_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Lon",
                        selected_key=lon_col,
                        on_selection_change=set_lon_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_geo", "line_geo")
                else None
            ),
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Locations",
                        selected_key=locations_col,
                        on_selection_change=set_locations_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        ui.item("(None)", key=""),
                        ui.item("ISO-3", key="ISO-3"),
                        ui.item("USA-states", key="USA-states"),
                        ui.item("Country names", key="country names"),
                        label="Location Mode",
                        selected_key=locationmode,
                        on_selection_change=set_locationmode,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_geo", "line_geo")
                else None
            ),
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Size",
                        selected_key=size_col,
                        on_selection_change=set_size_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Color",
                        selected_key=color_col,
                        on_selection_change=set_color_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "scatter_geo"
                else None
            ),
            (
                ui.picker(
                    *_render_column_picker_items(optional_column_items),
                    label="Color",
                    selected_key=color_col,
                    on_selection_change=set_color_col,
                    width="100%",
                )
                if chart_type == "line_geo"
                else None
            ),
            # Tile map chart controls (scatter_map, line_map, density_map)
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Lat",
                        selected_key=lat_col,
                        on_selection_change=set_lat_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(column_items),
                        label="Lon",
                        selected_key=lon_col,
                        on_selection_change=set_lon_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_map", "line_map", "density_map")
                else None
            ),
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Size",
                        selected_key=size_col,
                        on_selection_change=set_size_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Color",
                        selected_key=color_col,
                        on_selection_change=set_color_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "scatter_map"
                else None
            ),
            (
                ui.picker(
                    *_render_column_picker_items(optional_column_items),
                    label="Color",
                    selected_key=color_col,
                    on_selection_change=set_color_col,
                    width="100%",
                )
                if chart_type == "line_map"
                else None
            ),
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Z (Intensity)",
                        selected_key=z_col,
                        on_selection_change=set_z_col,
                        flex_grow=1,
                    ),
                    ui.number_field(
                        label="Radius",
                        value=radius,
                        on_change=set_radius,
                        min_value=1,
                        max_value=50,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "density_map"
                else None
            ),
            (
                ui.number_field(
                    label="Zoom",
                    value=zoom,
                    on_change=set_zoom,
                    min_value=0,
                    max_value=20,
                    width="100%",
                )
                if chart_type in ("scatter_map", "line_map", "density_map")
                else None
            ),
            # Center selection for tile-based maps
            (
                ui.picker(
                    *[
                        ui.item(item["label"], key=item["key"])
                        for item in MAP_CENTER_PRESETS
                    ],
                    label="Map Center",
                    selected_key=center_preset,
                    on_selection_change=set_center_preset,
                    width="100%",
                )
                if chart_type in ("scatter_map", "line_map", "density_map")
                else None
            ),
            # Custom center coordinates (only shown when "custom" is selected)
            (
                ui.flex(
                    ui.number_field(
                        label="Center Latitude",
                        value=center_lat,
                        on_change=set_center_lat,
                        min_value=-90,
                        max_value=90,
                        flex_grow=1,
                    ),
                    ui.number_field(
                        label="Center Longitude",
                        value=center_lon,
                        on_change=set_center_lon,
                        min_value=-180,
                        max_value=180,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type in ("scatter_map", "line_map", "density_map")
                and center_preset == "custom"
                else None
            ),
            # Map style selection for tile-based maps
            (
                ui.picker(
                    *[
                        ui.item(item["label"], key=item["key"])
                        for item in MAP_STYLE_OPTIONS
                    ],
                    label="Map Style",
                    selected_key=map_style,
                    on_selection_change=set_map_style,
                    width="100%",
                )
                if chart_type in ("scatter_map", "line_map", "density_map")
                else None
            ),
            # Group by (for charts that support it - not pie, density_heatmap, OHLC, or hierarchical charts)
            (
                ui.flex(
                    # Show dropdowns for each selected column plus one empty one
                    *[
                        ui.flex(
                            ui.picker(
                                *_render_column_picker_items(get_by_picker_items(i)),
                                label="Group By" if i == 0 else f"Group {i + 1}",
                                selected_key=by_cols[i] if i < len(by_cols) else "",
                                on_selection_change=lambda col, idx=i: update_by_col(
                                    idx, col
                                ),
                                flex_grow=1,
                            ),
                            # Trash button to remove (only show for selected columns, not the empty "add" picker)
                            (
                                ui.action_button(
                                    ui.icon("vsTrash"),
                                    on_press=(lambda idx: lambda: remove_by_col(idx))(
                                        i
                                    ),
                                    is_quiet=True,
                                    aria_label=f"Remove group {i + 1}",
                                )
                                if i < len(by_cols)
                                else None
                            ),
                            direction="row",
                            gap="size-100",
                            align_items="end",
                            width="100%",
                        )
                        for i in range(len(by_cols) + 1)
                    ],  # +1 for the "add new" picker
                    direction="column",
                    gap="size-100",
                    width="100%",
                )
                if chart_type
                not in (
                    "pie",
                    "density_heatmap",
                    "candlestick",
                    "ohlc",
                    "treemap",
                    "sunburst",
                    "icicle",
                    "funnel",
                    "funnel_area",
                    "scatter_3d",
                    "line_3d",
                    "scatter_polar",
                    "line_polar",
                    "scatter_ternary",
                    "line_ternary",
                    "timeline",
                    "scatter_geo",
                    "line_geo",
                    "scatter_map",
                    "line_map",
                    "density_map",
                )
                else None
            ),
            # Histogram-specific options
            (
                ui.number_field(
                    label="Number of Bins",
                    value=nbins,
                    on_change=set_nbins,
                    min_value=1,
                    max_value=1000,
                    width="100%",
                )
                if chart_type == "histogram"
                else None
            ),
            # Scatter-specific options
            (
                ui.flex(
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Size",
                        selected_key=size_col,
                        on_selection_change=set_size_col,
                        flex_grow=1,
                    ),
                    ui.picker(
                        *_render_column_picker_items(optional_column_items),
                        label="Color",
                        selected_key=color_col,
                        on_selection_change=set_color_col,
                        flex_grow=1,
                    ),
                    direction="row",
                    gap="size-100",
                    width="100%",
                )
                if chart_type == "scatter"
                else None
            ),
            # Line-specific options
            (
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
                )
                if chart_type == "line"
                else None
            ),
            # Bar-specific options
            (
                ui.picker(
                    *[ui.item(o["label"], key=o["key"]) for o in ORIENTATIONS],
                    label="Orientation",
                    selected_key=orientation,
                    on_selection_change=set_orientation,
                    width="100%",
                )
                if chart_type == "bar"
                else None
            ),
            # Advanced Options (collapsible) - for scatter, line, bar, area, pie
            (
                ui.disclosure(
                    title="Advanced Options",
                    panel=ui.flex(
                        # Text and Hover options (text for scatter/line/bar/area, hover for all)
                        (
                            ui.flex(
                                (
                                    ui.picker(
                                        *_render_column_picker_items(
                                            optional_column_items
                                        ),
                                        label="Text Labels",
                                        selected_key=text_col,
                                        on_selection_change=set_text_col,
                                        flex_grow=1,
                                    )
                                    if chart_type != "pie"
                                    else None
                                ),
                                ui.picker(
                                    *_render_column_picker_items(optional_column_items),
                                    label="Hover Name",
                                    selected_key=hover_name_col,
                                    on_selection_change=set_hover_name_col,
                                    flex_grow=1,
                                ),
                                direction="row",
                                gap="size-100",
                                width="100%",
                            )
                        ),
                        # Opacity (scatter, bar, area, pie)
                        (
                            ui.slider(
                                label="Opacity",
                                value=opacity,
                                on_change=set_opacity,
                                min_value=0.0,
                                max_value=1.0,
                                step=0.1,
                                width="100%",
                            )
                            if chart_type in ("scatter", "bar", "area", "pie")
                            else None
                        ),
                        # Line-specific: line_dash and width columns
                        (
                            ui.flex(
                                ui.picker(
                                    *_render_column_picker_items(optional_column_items),
                                    label="Line Dash",
                                    selected_key=line_dash_col,
                                    on_selection_change=set_line_dash_col,
                                    flex_grow=1,
                                ),
                                ui.picker(
                                    *_render_column_picker_items(optional_column_items),
                                    label="Line Width",
                                    selected_key=width_col,
                                    on_selection_change=set_width_col,
                                    flex_grow=1,
                                ),
                                direction="row",
                                gap="size-100",
                                width="100%",
                            )
                            if chart_type == "line"
                            else None
                        ),
                        # Bar-specific: barmode and text_auto
                        (
                            ui.flex(
                                ui.picker(
                                    ui.item("Relative (stacked)", key="relative"),
                                    ui.item("Group (side by side)", key="group"),
                                    ui.item("Overlay", key="overlay"),
                                    label="Bar Mode",
                                    selected_key=barmode,
                                    on_selection_change=set_barmode,
                                    flex_grow=1,
                                ),
                                ui.checkbox(
                                    "Auto Text Labels",
                                    is_selected=text_auto,
                                    on_change=set_text_auto,
                                ),
                                direction="row",
                                gap="size-100",
                                width="100%",
                                align_items="end",
                            )
                            if chart_type == "bar"
                            else None
                        ),
                        # Area-specific: markers and line_shape
                        (
                            ui.flex(
                                ui.checkbox(
                                    "Show Markers",
                                    is_selected=markers,
                                    on_change=set_markers,
                                ),
                                ui.picker(
                                    *[
                                        ui.item(ls["label"], key=ls["key"])
                                        for ls in LINE_SHAPES
                                    ],
                                    label="Line Shape",
                                    selected_key=line_shape,
                                    on_selection_change=set_line_shape,
                                    flex_grow=1,
                                ),
                                direction="row",
                                gap="size-100",
                                width="100%",
                                align_items="end",
                            )
                            if chart_type == "area"
                            else None
                        ),
                        # Pie-specific: hole (for donut chart)
                        (
                            ui.slider(
                                label="Hole Size (Donut Chart)",
                                value=hole,
                                on_change=set_hole,
                                min_value=0.0,
                                max_value=0.9,
                                step=0.1,
                                width="100%",
                            )
                            if chart_type == "pie"
                            else None
                        ),
                        # Histogram-specific options (Phase 11)
                        (
                            ui.flex(
                                ui.text(
                                    "Histogram Options",
                                    UNSAFE_style={"fontWeight": "bold"},
                                ),
                                ui.flex(
                                    ui.picker(
                                        ui.item("Count", key="count"),
                                        ui.item("Sum", key="sum"),
                                        ui.item("Average", key="avg"),
                                        ui.item("Min", key="min"),
                                        ui.item("Max", key="max"),
                                        label="Aggregation",
                                        selected_key=histfunc,
                                        on_selection_change=set_histfunc,
                                        flex_grow=1,
                                    ),
                                    ui.picker(
                                        ui.item("(None)", key=""),
                                        ui.item("Probability", key="probability"),
                                        ui.item("Percent", key="percent"),
                                        ui.item("Density", key="density"),
                                        ui.item(
                                            "Prob. Density", key="probability density"
                                        ),
                                        label="Normalization",
                                        selected_key=histnorm,
                                        on_selection_change=set_histnorm,
                                        flex_grow=1,
                                    ),
                                    direction="row",
                                    gap="size-100",
                                    width="100%",
                                ),
                                ui.flex(
                                    ui.picker(
                                        ui.item("Stacked", key="relative"),
                                        ui.item("Group (side by side)", key="group"),
                                        ui.item("Overlay", key="overlay"),
                                        label="Bar Mode",
                                        selected_key=hist_barmode,
                                        on_selection_change=set_hist_barmode,
                                        flex_grow=1,
                                    ),
                                    ui.picker(
                                        ui.item("(None)", key=""),
                                        ui.item("Fraction", key="fraction"),
                                        ui.item("Percent", key="percent"),
                                        label="Bar Normalization",
                                        selected_key=barnorm,
                                        on_selection_change=set_barnorm,
                                        flex_grow=1,
                                    ),
                                    direction="row",
                                    gap="size-100",
                                    width="100%",
                                ),
                                ui.flex(
                                    ui.number_field(
                                        label="Number of Bins (0=auto)",
                                        value=nbins,
                                        on_change=set_nbins,
                                        min_value=0,
                                        flex_grow=1,
                                    ),
                                    ui.checkbox(
                                        "Cumulative",
                                        is_selected=cumulative,
                                        on_change=set_cumulative,
                                    ),
                                    direction="row",
                                    gap="size-100",
                                    width="100%",
                                    align_items="end",
                                ),
                                direction="column",
                                gap="size-100",
                            )
                            if chart_type == "histogram"
                            else None
                        ),
                        # Box plot options (Phase 11)
                        (
                            ui.flex(
                                ui.text(
                                    "Box Plot Options",
                                    UNSAFE_style={"fontWeight": "bold"},
                                ),
                                ui.flex(
                                    ui.picker(
                                        ui.item("Group (side by side)", key="group"),
                                        ui.item("Overlay", key="overlay"),
                                        label="Box Mode",
                                        selected_key=boxmode,
                                        on_selection_change=set_boxmode,
                                        flex_grow=1,
                                    ),
                                    ui.picker(
                                        ui.item("Outliers only", key="outliers"),
                                        ui.item(
                                            "Suspected outliers",
                                            key="suspectedoutliers",
                                        ),
                                        ui.item("All points", key="all"),
                                        ui.item("No points", key="false"),
                                        label="Show Points",
                                        selected_key=box_points,
                                        on_selection_change=set_box_points,
                                        flex_grow=1,
                                    ),
                                    direction="row",
                                    gap="size-100",
                                    width="100%",
                                ),
                                ui.checkbox(
                                    "Notched (show confidence interval)",
                                    is_selected=notched,
                                    on_change=set_notched,
                                ),
                                direction="column",
                                gap="size-100",
                            )
                            if chart_type == "box"
                            else None
                        ),
                        # Violin plot options (Phase 11)
                        (
                            ui.flex(
                                ui.text(
                                    "Violin Plot Options",
                                    UNSAFE_style={"fontWeight": "bold"},
                                ),
                                ui.flex(
                                    ui.picker(
                                        ui.item("Group (side by side)", key="group"),
                                        ui.item("Overlay", key="overlay"),
                                        label="Violin Mode",
                                        selected_key=violinmode,
                                        on_selection_change=set_violinmode,
                                        flex_grow=1,
                                    ),
                                    ui.picker(
                                        ui.item("(None)", key=""),
                                        ui.item("Outliers only", key="outliers"),
                                        ui.item(
                                            "Suspected outliers",
                                            key="suspectedoutliers",
                                        ),
                                        ui.item("All points", key="all"),
                                        label="Show Points",
                                        selected_key=violin_points,
                                        on_selection_change=set_violin_points,
                                        flex_grow=1,
                                    ),
                                    direction="row",
                                    gap="size-100",
                                    width="100%",
                                ),
                                ui.checkbox(
                                    "Show inner box plot",
                                    is_selected=violin_box,
                                    on_change=set_violin_box,
                                ),
                                direction="column",
                                gap="size-100",
                            )
                            if chart_type == "violin"
                            else None
                        ),
                        # Strip plot options (Phase 11)
                        (
                            ui.flex(
                                ui.text(
                                    "Strip Plot Options",
                                    UNSAFE_style={"fontWeight": "bold"},
                                ),
                                ui.picker(
                                    ui.item("Group (side by side)", key="group"),
                                    ui.item("Overlay", key="overlay"),
                                    label="Strip Mode",
                                    selected_key=stripmode,
                                    on_selection_change=set_stripmode,
                                    width="100%",
                                ),
                                direction="column",
                                gap="size-100",
                            )
                            if chart_type == "strip"
                            else None
                        ),
                        # Financial chart options (Phase 12: candlestick/ohlc)
                        (
                            ui.flex(
                                ui.text(
                                    "Financial Chart Options",
                                    UNSAFE_style={"fontWeight": "bold"},
                                ),
                                ui.flex(
                                    ui.color_picker(
                                        label="Up Color",
                                        value=(
                                            increasing_color
                                            if increasing_color
                                            else "#3D9970"
                                        ),
                                        on_change=set_increasing_color,
                                    ),
                                    ui.color_picker(
                                        label="Down Color",
                                        value=(
                                            decreasing_color
                                            if decreasing_color
                                            else "#FF4136"
                                        ),
                                        on_change=set_decreasing_color,
                                    ),
                                    direction="row",
                                    gap="size-200",
                                    align_items="end",
                                ),
                                direction="column",
                                gap="size-100",
                            )
                            if chart_type in ("candlestick", "ohlc")
                            else None
                        ),
                        # Hierarchical chart options (Phase 13: treemap/sunburst/icicle)
                        (
                            ui.flex(
                                ui.text(
                                    "Hierarchical Chart Options",
                                    UNSAFE_style={"fontWeight": "bold"},
                                ),
                                ui.picker(
                                    *_render_column_picker_items(optional_column_items),
                                    label="Color",
                                    selected_key=hier_color_col,
                                    on_selection_change=set_hier_color_col,
                                    width="100%",
                                ),
                                ui.picker(
                                    ui.item("(Default)", key=""),
                                    ui.item(
                                        "Total (includes descendants)", key="total"
                                    ),
                                    ui.item(
                                        "Remainder (value after subtracting children)",
                                        key="remainder",
                                    ),
                                    label="Branch Values",
                                    selected_key=branchvalues,
                                    on_selection_change=set_branchvalues,
                                    width="100%",
                                ),
                                ui.number_field(
                                    label="Max Depth (-1 for all)",
                                    value=maxdepth,
                                    on_change=set_maxdepth,
                                    min_value=-1,
                                    step=1,
                                    width="100%",
                                ),
                                direction="column",
                                gap="size-100",
                            )
                            if chart_type in ("treemap", "sunburst", "icicle")
                            else None
                        ),
                        # Funnel chart options (Phase 13)
                        (
                            ui.flex(
                                ui.text(
                                    "Funnel Chart Options",
                                    UNSAFE_style={"fontWeight": "bold"},
                                ),
                                ui.picker(
                                    *_render_column_picker_items(optional_column_items),
                                    label="Text",
                                    selected_key=funnel_text_col,
                                    on_selection_change=set_funnel_text_col,
                                    width="100%",
                                ),
                                ui.picker(
                                    *_render_column_picker_items(optional_column_items),
                                    label="Color",
                                    selected_key=funnel_color_col,
                                    on_selection_change=set_funnel_color_col,
                                    width="100%",
                                ),
                                ui.picker(
                                    ui.item("(Default)", key=""),
                                    ui.item("Vertical", key="v"),
                                    ui.item("Horizontal", key="h"),
                                    label="Orientation",
                                    selected_key=funnel_orientation,
                                    on_selection_change=set_funnel_orientation,
                                    width="100%",
                                ),
                                direction="column",
                                gap="size-100",
                            )
                            if chart_type == "funnel"
                            else None
                        ),
                        # Funnel area chart options (Phase 13)
                        (
                            ui.flex(
                                ui.text(
                                    "Funnel Area Chart Options",
                                    UNSAFE_style={"fontWeight": "bold"},
                                ),
                                ui.picker(
                                    *_render_column_picker_items(optional_column_items),
                                    label="Color",
                                    selected_key=funnel_area_color_col,
                                    on_selection_change=set_funnel_area_color_col,
                                    width="100%",
                                ),
                                direction="column",
                                gap="size-100",
                            )
                            if chart_type == "funnel_area"
                            else None
                        ),
                        # Marginal plots (scatter only)
                        (
                            ui.flex(
                                ui.picker(
                                    ui.item("(None)", key=""),
                                    ui.item("Histogram", key="histogram"),
                                    ui.item("Box", key="box"),
                                    ui.item("Violin", key="violin"),
                                    ui.item("Rug", key="rug"),
                                    label="Marginal X",
                                    selected_key=marginal_x,
                                    on_selection_change=set_marginal_x,
                                    flex_grow=1,
                                ),
                                ui.picker(
                                    ui.item("(None)", key=""),
                                    ui.item("Histogram", key="histogram"),
                                    ui.item("Box", key="box"),
                                    ui.item("Violin", key="violin"),
                                    ui.item("Rug", key="rug"),
                                    label="Marginal Y",
                                    selected_key=marginal_y,
                                    on_selection_change=set_marginal_y,
                                    flex_grow=1,
                                ),
                                direction="row",
                                gap="size-100",
                                width="100%",
                            )
                            if chart_type == "scatter"
                            else None
                        ),
                        # Error bars (scatter, line, bar only)
                        (
                            ui.flex(
                                ui.text(
                                    "Error Bars",
                                    UNSAFE_style={"fontWeight": "bold"},
                                ),
                                ui.flex(
                                    ui.picker(
                                        *_render_column_picker_items(
                                            optional_column_items
                                        ),
                                        label="Error X",
                                        selected_key=error_x_col,
                                        on_selection_change=set_error_x_col,
                                        flex_grow=1,
                                    ),
                                    ui.picker(
                                        *_render_column_picker_items(
                                            optional_column_items
                                        ),
                                        label="Error X-",
                                        selected_key=error_x_minus_col,
                                        on_selection_change=set_error_x_minus_col,
                                        flex_grow=1,
                                    ),
                                    direction="row",
                                    gap="size-100",
                                    width="100%",
                                ),
                                ui.flex(
                                    ui.picker(
                                        *_render_column_picker_items(
                                            optional_column_items
                                        ),
                                        label="Error Y",
                                        selected_key=error_y_col,
                                        on_selection_change=set_error_y_col,
                                        flex_grow=1,
                                    ),
                                    ui.picker(
                                        *_render_column_picker_items(
                                            optional_column_items
                                        ),
                                        label="Error Y-",
                                        selected_key=error_y_minus_col,
                                        on_selection_change=set_error_y_minus_col,
                                        flex_grow=1,
                                    ),
                                    direction="row",
                                    gap="size-100",
                                    width="100%",
                                ),
                                direction="column",
                                gap="size-100",
                                margin_top="size-100",
                            )
                            if chart_type in ("scatter", "line", "bar")
                            else None
                        ),
                        # Axis configuration (scatter, line, bar, area, distribution charts)
                        (
                            ui.flex(
                                ui.text(
                                    "Axis Configuration",
                                    UNSAFE_style={"fontWeight": "bold"},
                                ),
                                ui.flex(
                                    ui.checkbox(
                                        "Log X",
                                        is_selected=log_x,
                                        on_change=set_log_x,
                                    ),
                                    ui.checkbox(
                                        "Log Y",
                                        is_selected=log_y,
                                        on_change=set_log_y,
                                    ),
                                    direction="row",
                                    gap="size-200",
                                ),
                                # Axis titles only for scatter, line, area (not bar or distribution charts)
                                (
                                    ui.flex(
                                        ui.text_field(
                                            label="X Axis Title",
                                            value=xaxis_title,
                                            on_change=set_xaxis_title,
                                            flex_grow=1,
                                        ),
                                        ui.text_field(
                                            label="Y Axis Title",
                                            value=yaxis_title,
                                            on_change=set_yaxis_title,
                                            flex_grow=1,
                                        ),
                                        direction="row",
                                        gap="size-100",
                                        width="100%",
                                    )
                                    if chart_type in ("scatter", "line", "area")
                                    else None
                                ),
                                direction="column",
                                gap="size-100",
                                margin_top="size-100",
                            )
                            if chart_type
                            in (
                                "scatter",
                                "line",
                                "bar",
                                "area",
                                "histogram",
                                "box",
                                "violin",
                                "strip",
                            )
                            else None
                        ),
                        # Rendering options
                        ui.flex(
                            ui.text(
                                "Rendering",
                                UNSAFE_style={"fontWeight": "bold"},
                            ),
                            ui.flex(
                                # Render mode only for scatter/line
                                (
                                    ui.picker(
                                        ui.item("WebGL (faster)", key="webgl"),
                                        ui.item("SVG (more compatible)", key="svg"),
                                        label="Render Mode",
                                        selected_key=render_mode,
                                        on_selection_change=set_render_mode,
                                        flex_grow=1,
                                    )
                                    if chart_type in ("scatter", "line")
                                    else None
                                ),
                                ui.picker(
                                    ui.item("(Default)", key=""),
                                    ui.item("plotly", key="plotly"),
                                    ui.item("plotly_white", key="plotly_white"),
                                    ui.item("plotly_dark", key="plotly_dark"),
                                    ui.item("ggplot2", key="ggplot2"),
                                    ui.item("seaborn", key="seaborn"),
                                    ui.item("simple_white", key="simple_white"),
                                    label="Template",
                                    selected_key=template,
                                    on_selection_change=set_template,
                                    flex_grow=1,
                                ),
                                direction="row",
                                gap="size-100",
                                width="100%",
                            ),
                            direction="column",
                            gap="size-100",
                            margin_top="size-100",
                        ),
                        direction="column",
                        gap="size-100",
                    ),
                    is_expanded=advanced_expanded,
                    on_expanded_change=lambda: set_advanced_expanded(
                        not advanced_expanded
                    ),
                )
                if chart_type
                in (
                    "scatter",
                    "line",
                    "bar",
                    "area",
                    "pie",
                    "histogram",
                    "box",
                    "violin",
                    "strip",
                    "candlestick",
                    "ohlc",
                    "treemap",
                    "sunburst",
                    "icicle",
                    "funnel",
                    "funnel_area",
                )
                else None
            ),
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
        height="100%",
        min_height=0,
        overflow="auto",
    )

    # Chart area - update placeholder message based on chart type
    if chart_type == "pie":
        placeholder_msg = "Select Names and Values columns to preview chart"
    elif chart_type == "histogram":
        placeholder_msg = "Select X or Y column to preview chart"
    elif chart_type in ("candlestick", "ohlc"):
        placeholder_msg = "Select X and OHLC columns to preview chart"
    elif chart_type in ("treemap", "sunburst", "icicle"):
        placeholder_msg = "Select Names, Values, and Parents columns to preview chart"
    elif chart_type == "funnel_area":
        placeholder_msg = "Select Names and Values columns to preview chart"
    elif chart_type in ("scatter_3d", "line_3d"):
        placeholder_msg = "Select X, Y, and Z columns to preview chart"
    elif chart_type in ("scatter_polar", "line_polar"):
        placeholder_msg = "Select R and Theta columns to preview chart"
    elif chart_type in ("scatter_ternary", "line_ternary"):
        placeholder_msg = "Select A, B, and C columns to preview chart"
    elif chart_type == "timeline":
        placeholder_msg = "Select X Start, X End, and Y columns to preview chart"
    elif chart_type in ("scatter_geo", "line_geo"):
        placeholder_msg = "Select Lat/Lon or Locations columns to preview chart"
    elif chart_type in ("scatter_map", "line_map", "density_map"):
        placeholder_msg = "Select Lat and Lon columns to preview chart"
    else:
        placeholder_msg = "Select X and Y columns to preview chart"

    chart_area = ui.view(
        (
            ui.text(
                error_message,
                UNSAFE_style={"color": "var(--spectrum-negative-color-900)"},
            )
            if error_message
            else (
                chart
                if chart
                else ui.flex(
                    ui.text(
                        placeholder_msg,
                        UNSAFE_style={"color": "var(--spectrum-gray-600)"},
                    ),
                    align_items="center",
                    justify_content="center",
                    height="100%",
                )
            )
        ),
        flex_grow=1,
        min_height="size-3000",
    )

    # Generate the code for the current configuration
    generated_code = generate_chart_code(config, dataset_name)

    # Code panel with markdown display
    code_panel = ui.view(
        ui.flex(
            ui.flex(
                ui.icon("vsCode"),
                ui.text("Generated Code", UNSAFE_style={"fontWeight": "bold"}),
                direction="row",
                align_items="center",
                gap="size-100",
            ),
            ui.markdown(f"```python\n{generated_code}\n```"),
            direction="column",
            gap="size-100",
        ),
        padding="size-200",
        background_color="gray-100",
        border_radius="medium",
    )

    # Right side - chart area and code panel stacked vertically
    right_panel = ui.flex(
        chart_area,
        code_panel,
        direction="column",
        gap="size-200",
        flex_grow=1,
        min_height=0,  # Allow flex item to shrink below content size
    )

    # Main layout - controls on left, chart+code on right
    # Wrap in ui.view with position absolute to fill the panel and prevent page scroll
    return ui.view(
        ui.flex(
            controls,
            right_panel,
            direction="row",
            gap="size-200",
            height="100%",
            width="100%",
        ),
        position="absolute",
        top=0,
        bottom=0,
        left=0,
        right=0,
        overflow="hidden",
    )


# =============================================================================
# Example Usage
# =============================================================================

# Main app with dataset selector
chart_builder_demo = chart_builder_app()

# Also export individual chart builders for specific datasets
iris_chart_builder = chart_builder(dx.data.iris())
stocks_chart_builder = chart_builder(dx.data.stocks())
