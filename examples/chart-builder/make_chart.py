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
    
    # Optional parameters
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
    if config.get("log_x"):
        kwargs["log_x"] = config["log_x"]
    if config.get("log_y"):
        kwargs["log_y"] = config["log_y"]
    
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
    
    # Optional parameters
    if config.get("by"):
        kwargs["by"] = config["by"]
    if config.get("title"):
        kwargs["title"] = config["title"]
    if config.get("markers") is not None:
        kwargs["markers"] = config["markers"]
    if config.get("line_shape"):
        kwargs["line_shape"] = config["line_shape"]
    if config.get("log_x"):
        kwargs["log_x"] = config["log_x"]
    if config.get("log_y"):
        kwargs["log_y"] = config["log_y"]
    
    return dx.line(table, **kwargs)
