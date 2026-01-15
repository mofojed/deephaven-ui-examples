"""Chart creation function - the testable core of chart-builder."""

from __future__ import annotations

from typing import TYPE_CHECKING

import deephaven.plot.express as dx

from chart_config import ChartConfig, validate_config

if TYPE_CHECKING:
    from deephaven.table import Table


def make_chart(table: Table, config: ChartConfig):
    """Create a chart from the given table and configuration.
    
    This is the core chart creation function that can be unit tested
    independently of the UI component.
    
    Args:
        table: The source data table.
        config: Chart configuration options.
        
    Returns:
        A DeephavenFigure containing the chart.
        
    Raises:
        ValueError: If required options are missing for the chart type.
    """
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


def _make_scatter(table: Table, config: ChartConfig):
    """Create a scatter plot.
    
    Args:
        table: The source data table.
        config: Chart configuration options.
        
    Returns:
        A DeephavenFigure containing the scatter plot.
    """
    kwargs = {
        "x": config["x"],
        "y": config["y"],
    }
    
    # Basic optional parameters
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
    if config.get("opacity") is not None:
        kwargs["opacity"] = config["opacity"]
    if config.get("text"):
        kwargs["text"] = config["text"]
    if config.get("hover_name"):
        kwargs["hover_name"] = config["hover_name"]
    
    # Axis options
    if config.get("log_x"):
        kwargs["log_x"] = config["log_x"]
    if config.get("log_y"):
        kwargs["log_y"] = config["log_y"]
    
    # Error bars
    if config.get("error_x"):
        kwargs["error_x"] = config["error_x"]
    if config.get("error_x_minus"):
        kwargs["error_x_minus"] = config["error_x_minus"]
    if config.get("error_y"):
        kwargs["error_y"] = config["error_y"]
    if config.get("error_y_minus"):
        kwargs["error_y_minus"] = config["error_y_minus"]
    
    # Marginal plots
    if config.get("marginal_x"):
        kwargs["marginal_x"] = config["marginal_x"]
    if config.get("marginal_y"):
        kwargs["marginal_y"] = config["marginal_y"]
    
    # Axis configuration
    if config.get("range_x"):
        kwargs["range_x"] = config["range_x"]
    if config.get("range_y"):
        kwargs["range_y"] = config["range_y"]
    if config.get("xaxis_titles"):
        # Convert to list if string (dx.scatter expects list)
        val = config["xaxis_titles"]
        kwargs["xaxis_titles"] = [val] if isinstance(val, str) else val
    if config.get("yaxis_titles"):
        val = config["yaxis_titles"]
        kwargs["yaxis_titles"] = [val] if isinstance(val, str) else val
    
    # Labels
    if config.get("labels"):
        kwargs["labels"] = config["labels"]
    
    # Rendering options
    if config.get("render_mode"):
        kwargs["render_mode"] = config["render_mode"]
    if config.get("template"):
        kwargs["template"] = config["template"]
    
    # Debug: print kwargs to server log
    if config.get("xaxis_titles") or config.get("yaxis_titles"):
        print(f"[make_chart DEBUG] _make_scatter kwargs: {kwargs}", flush=True)
    
    return dx.scatter(table, **kwargs)


def _make_line(table: Table, config: ChartConfig):
    """Create a line plot.
    
    Args:
        table: The source data table.
        config: Chart configuration options.
        
    Returns:
        A DeephavenFigure containing the line plot.
    """
    kwargs = {
        "x": config["x"],
        "y": config["y"],
    }
    
    # Basic optional parameters
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    if config.get("markers") is not None:
        kwargs["markers"] = config["markers"]
    if config.get("line_shape"):
        kwargs["line_shape"] = config["line_shape"]
    if config.get("size"):
        kwargs["size"] = config["size"]
    if config.get("line_dash"):
        kwargs["line_dash"] = config["line_dash"]
    if config.get("width"):
        kwargs["width"] = config["width"]
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("symbol"):
        kwargs["symbol"] = config["symbol"]
    if config.get("text"):
        kwargs["text"] = config["text"]
    if config.get("hover_name"):
        kwargs["hover_name"] = config["hover_name"]
    
    # Axis options
    if config.get("log_x"):
        kwargs["log_x"] = config["log_x"]
    if config.get("log_y"):
        kwargs["log_y"] = config["log_y"]
    
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
    if config.get("range_x"):
        kwargs["range_x"] = config["range_x"]
    if config.get("range_y"):
        kwargs["range_y"] = config["range_y"]
    if config.get("xaxis_titles"):
        # Convert to list if string (dx.line expects list)
        val = config["xaxis_titles"]
        kwargs["xaxis_titles"] = [val] if isinstance(val, str) else val
    if config.get("yaxis_titles"):
        val = config["yaxis_titles"]
        kwargs["yaxis_titles"] = [val] if isinstance(val, str) else val
    
    # Labels
    if config.get("labels"):
        kwargs["labels"] = config["labels"]
    
    # Rendering options
    if config.get("render_mode"):
        kwargs["render_mode"] = config["render_mode"]
    if config.get("template"):
        kwargs["template"] = config["template"]
    
    return dx.line(table, **kwargs)


def _make_bar(table: Table, config: ChartConfig):
    """Create a bar chart.
    
    Args:
        table: The source data table.
        config: Chart configuration options.
        
    Returns:
        A DeephavenFigure containing the bar chart.
    """
    kwargs = {
        "x": config["x"],
        "y": config["y"],
    }
    
    # Optional parameters
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    if config.get("orientation"):
        kwargs["orientation"] = config["orientation"]
    
    return dx.bar(table, **kwargs)


def _make_area(table: Table, config: ChartConfig):
    """Create an area chart.
    
    Args:
        table: The source data table.
        config: Chart configuration options.
        
    Returns:
        A DeephavenFigure containing the area chart.
    """
    kwargs = {
        "x": config["x"],
        "y": config["y"],
    }
    
    # Optional parameters
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    
    return dx.area(table, **kwargs)


def _make_pie(table: Table, config: ChartConfig):
    """Create a pie chart.
    
    Args:
        table: The source data table.
        config: Chart configuration options.
        
    Returns:
        A DeephavenFigure containing the pie chart.
    """
    kwargs = {
        "names": config["names"],
        "values": config["values"],
    }
    
    # Optional parameters
    if config.get("title"):
        kwargs["title"] = config["title"]
    
    return dx.pie(table, **kwargs)


def _make_histogram(table: Table, config: ChartConfig):
    """Create a histogram.
    
    Args:
        table: The source data table.
        config: Chart configuration options.
        
    Returns:
        A DeephavenFigure containing the histogram.
    """
    kwargs = {}
    
    # x or y (at least one required)
    if config.get("x"):
        kwargs["x"] = config["x"]
    if config.get("y"):
        kwargs["y"] = config["y"]
    
    # Optional parameters
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    if config.get("nbins"):
        kwargs["nbins"] = config["nbins"]
    
    return dx.histogram(table, **kwargs)


def _make_box(table: Table, config: ChartConfig):
    """Create a box plot.
    
    Args:
        table: The source data table.
        config: Chart configuration options.
        
    Returns:
        A DeephavenFigure containing the box plot.
    """
    kwargs = {
        "x": config["x"],
        "y": config["y"],
    }
    
    # Optional parameters
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    
    return dx.box(table, **kwargs)


def _make_violin(table: Table, config: ChartConfig):
    """Create a violin plot.
    
    Args:
        table: The source data table.
        config: Chart configuration options.
        
    Returns:
        A DeephavenFigure containing the violin plot.
    """
    kwargs = {
        "x": config["x"],
        "y": config["y"],
    }
    
    # Optional parameters
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    
    return dx.violin(table, **kwargs)


def _make_strip(table: Table, config: ChartConfig):
    """Create a strip plot.
    
    Args:
        table: The source data table.
        config: Chart configuration options.
        
    Returns:
        A DeephavenFigure containing the strip plot.
    """
    kwargs = {
        "x": config["x"],
        "y": config["y"],
    }
    
    # Optional parameters
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    
    return dx.strip(table, **kwargs)


def _make_density_heatmap(table: Table, config: ChartConfig):
    """Create a density heatmap.
    
    Args:
        table: The source data table.
        config: Chart configuration options.
        
    Returns:
        A DeephavenFigure containing the density heatmap.
    """
    kwargs = {
        "x": config["x"],
        "y": config["y"],
    }
    
    # Optional parameters
    if config.get("title"):
        kwargs["title"] = config["title"]
    
    return dx.density_heatmap(table, **kwargs)


def _make_candlestick(table: Table, config: ChartConfig):
    """Create a candlestick chart.
    
    Args:
        table: The source data table.
        config: Chart configuration options.
        
    Returns:
        A DeephavenFigure containing the candlestick chart.
    """
    kwargs = {
        "x": config["x"],
        "open": config["open"],
        "high": config["high"],
        "low": config["low"],
        "close": config["close"],
    }
    
    return dx.candlestick(table, **kwargs)


def _make_ohlc(table: Table, config: ChartConfig):
    """Create an OHLC chart.
    
    Args:
        table: The source data table.
        config: Chart configuration options.
        
    Returns:
        A DeephavenFigure containing the OHLC chart.
    """
    kwargs = {
        "x": config["x"],
        "open": config["open"],
        "high": config["high"],
        "low": config["low"],
        "close": config["close"],
    }
    
    return dx.ohlc(table, **kwargs)


# =============================================================================
# Phase 5: Hierarchical Charts
# =============================================================================

def _make_treemap(table: Table, config: ChartConfig):
    """Create a treemap chart."""
    kwargs = {
        "names": config["names"],
        "values": config["values"],
        "parents": config["parents"],
    }
    if config.get("title"):
        kwargs["title"] = config["title"]
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
    return dx.icicle(table, **kwargs)


def _make_funnel(table: Table, config: ChartConfig):
    """Create a funnel chart."""
    kwargs = {
        "x": config["x"],
        "y": config["y"],
    }
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.funnel(table, **kwargs)


def _make_funnel_area(table: Table, config: ChartConfig):
    """Create a funnel area chart."""
    kwargs = {
        "names": config["names"],
        "values": config["values"],
    }
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.funnel_area(table, **kwargs)


# =============================================================================
# Phase 6: 3D, Polar, Ternary, Timeline Charts
# =============================================================================

def _make_scatter_3d(table: Table, config: ChartConfig):
    """Create a 3D scatter chart."""
    kwargs = {
        "x": config["x"],
        "y": config["y"],
        "z": config["z"],
    }
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
    """Create a 3D line chart."""
    kwargs = {
        "x": config["x"],
        "y": config["y"],
        "z": config["z"],
    }
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.line_3d(table, **kwargs)


def _make_scatter_polar(table: Table, config: ChartConfig):
    """Create a polar scatter chart."""
    kwargs = {
        "r": config["r"],
        "theta": config["theta"],
    }
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
    """Create a polar line chart."""
    kwargs = {
        "r": config["r"],
        "theta": config["theta"],
    }
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.line_polar(table, **kwargs)


def _make_scatter_ternary(table: Table, config: ChartConfig):
    """Create a ternary scatter chart."""
    kwargs = {
        "a": config["a"],
        "b": config["b"],
        "c": config["c"],
    }
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
    """Create a ternary line chart."""
    kwargs = {
        "a": config["a"],
        "b": config["b"],
        "c": config["c"],
    }
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.line_ternary(table, **kwargs)


def _make_timeline(table: Table, config: ChartConfig):
    """Create a timeline (Gantt) chart."""
    kwargs = {
        "x_start": config["x_start"],
        "x_end": config["x_end"],
        "y": config["y"],
    }
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    return dx.timeline(table, **kwargs)


# =============================================================================
# Phase 7: Geo/Map Charts
# =============================================================================

def _make_scatter_geo(table: Table, config: ChartConfig):
    """Create a scatter geo chart."""
    kwargs = {}
    
    # Either lat/lon OR locations
    if config.get("lat") and config.get("lon"):
        kwargs["lat"] = config["lat"]
        kwargs["lon"] = config["lon"]
    if config.get("locations"):
        kwargs["locations"] = config["locations"]
    if config.get("locationmode"):
        kwargs["locationmode"] = config["locationmode"]
    
    # Optional
    if config.get("size"):
        kwargs["size"] = config["size"]
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    
    return dx.scatter_geo(table, **kwargs)


def _make_line_geo(table: Table, config: ChartConfig):
    """Create a line geo chart."""
    kwargs = {}
    
    # Either lat/lon OR locations
    if config.get("lat") and config.get("lon"):
        kwargs["lat"] = config["lat"]
        kwargs["lon"] = config["lon"]
    if config.get("locations"):
        kwargs["locations"] = config["locations"]
    if config.get("locationmode"):
        kwargs["locationmode"] = config["locationmode"]
    
    # Optional
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    
    return dx.line_geo(table, **kwargs)


def _make_scatter_map(table: Table, config: ChartConfig):
    """Create a scatter tile map chart."""
    kwargs = {
        "lat": config["lat"],
        "lon": config["lon"],
    }
    
    # Optional
    if config.get("size"):
        kwargs["size"] = config["size"]
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("zoom"):
        kwargs["zoom"] = config["zoom"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    
    return dx.scatter_map(table, **kwargs)


def _make_line_map(table: Table, config: ChartConfig):
    """Create a line tile map chart."""
    kwargs = {
        "lat": config["lat"],
        "lon": config["lon"],
    }
    
    # Optional
    if config.get("color"):
        kwargs["color"] = config["color"]
    if config.get("zoom"):
        kwargs["zoom"] = config["zoom"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    
    return dx.line_map(table, **kwargs)


def _make_density_map(table: Table, config: ChartConfig):
    """Create a density tile map chart."""
    kwargs = {
        "lat": config["lat"],
        "lon": config["lon"],
    }
    
    # Optional
    if config.get("z"):
        kwargs["z"] = config["z"]
    if config.get("radius"):
        kwargs["radius"] = config["radius"]
    if config.get("zoom"):
        kwargs["zoom"] = config["zoom"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    
    return dx.density_map(table, **kwargs)
