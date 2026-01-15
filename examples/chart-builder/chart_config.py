"""Chart configuration type definitions."""

from typing import Literal, TypedDict, NotRequired


# Chart types supported
ChartType = Literal[
    "scatter", "line", "bar", "area", "pie", "histogram", "box", "violin", "strip",
    "density_heatmap", "candlestick", "ohlc", "treemap", "sunburst", "icicle", "funnel", "funnel_area",
    "scatter_3d", "line_3d", "scatter_polar", "line_polar", "scatter_ternary", "line_ternary", "timeline",
    "scatter_geo", "line_geo", "scatter_map", "line_map", "density_map"
]

# Line shape options (spline is NOT supported by dx.line)
LineShape = Literal["linear", "vhv", "hvh", "vh", "hv"]

# Bar chart orientation
Orientation = Literal["v", "h"]

# Location mode for geo charts
LocationMode = Literal["ISO-3", "USA-states", "country names"]


class ChartConfig(TypedDict):
    """Configuration for chart creation.
    
    This TypedDict defines all options that can be passed to make_chart.
    Required and optional fields vary by chart_type.
    """
    
    # Required for all chart types
    chart_type: ChartType
    
    # Common axis options (required for scatter/line)
    x: NotRequired[str]
    y: NotRequired[str]
    
    # Grouping - single column or list of columns
    by: NotRequired[str | list[str]]
    
    # Title
    title: NotRequired[str]
    
    # Scatter-specific options
    size: NotRequired[str]
    symbol: NotRequired[str]
    color: NotRequired[str]
    opacity: NotRequired[float]
    
    # Line-specific options
    markers: NotRequired[bool]
    line_shape: NotRequired[LineShape]
    
    # Bar-specific options
    orientation: NotRequired[Orientation]
    
    # Pie-specific options
    names: NotRequired[str]
    values: NotRequired[str]
    
    # Histogram-specific options
    nbins: NotRequired[int]
    
    # OHLC/Candlestick-specific options
    open: NotRequired[str]
    high: NotRequired[str]
    low: NotRequired[str]
    close: NotRequired[str]
    
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
    
    # Geo/Map chart options
    lat: NotRequired[str]
    lon: NotRequired[str]
    locations: NotRequired[str]
    locationmode: NotRequired[LocationMode]
    radius: NotRequired[int]
    zoom: NotRequired[int]
    
    # Axis options
    log_x: NotRequired[bool]
    log_y: NotRequired[bool]


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
    
    # Special validation for histogram (needs x OR y)
    if chart_type == "histogram":
        if not config.get("x") and not config.get("y"):
            errors.append("x or y is required for histogram charts")
        return errors
    
    # Special validation for geo charts (needs lat+lon OR locations)
    if chart_type in ("scatter_geo", "line_geo"):
        has_lat_lon = config.get("lat") and config.get("lon")
        has_locations = config.get("locations")
        if not has_lat_lon and not has_locations:
            errors.append(f"lat and lon, OR locations is required for {chart_type} charts")
        return errors
    
    # Special validation for tile map charts (needs lat+lon)
    if chart_type in ("scatter_map", "line_map", "density_map"):
        if not config.get("lat"):
            errors.append(f"lat is required for {chart_type} charts")
        if not config.get("lon"):
            errors.append(f"lon is required for {chart_type} charts")
        return errors
    
    required = get_required_fields(chart_type)
    for field in required:
        if not config.get(field):
            errors.append(f"{field} is required for {chart_type} charts")
    
    return errors
