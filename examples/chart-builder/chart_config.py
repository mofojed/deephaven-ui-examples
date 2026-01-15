"""Chart configuration type definitions."""

from typing import Literal, TypedDict, NotRequired


# Chart types supported
ChartType = Literal["scatter", "line", "bar", "area", "pie"]

# Line shape options (spline is NOT supported by dx.line)
LineShape = Literal["linear", "vhv", "hvh", "vh", "hv"]

# Bar chart orientation
Orientation = Literal["v", "h"]


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
    
    # Grouping
    by: NotRequired[str]
    
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
    
    required = get_required_fields(chart_type)
    for field in required:
        if not config.get(field):
            errors.append(f"{field} is required for {chart_type} charts")
    
    return errors
