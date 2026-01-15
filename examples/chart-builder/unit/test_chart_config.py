"""Unit tests for chart_config module."""

import sys
from pathlib import Path

# Add the chart-builder directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from chart_config import (
    ChartConfig,
    get_required_fields,
    validate_config,
)


class TestChartConfig:
    """Tests for chart configuration validation."""

    def test_get_required_fields_scatter(self):
        """Test required fields for scatter chart."""
        required = get_required_fields("scatter")
        assert "x" in required
        assert "y" in required

    def test_get_required_fields_line(self):
        """Test required fields for line chart."""
        required = get_required_fields("line")
        assert "x" in required
        assert "y" in required

    def test_validate_config_missing_chart_type(self):
        """Test validation fails without chart_type."""
        config: ChartConfig = {}  # type: ignore
        errors = validate_config(config)
        assert len(errors) == 1
        assert "chart_type is required" in errors[0]

    def test_validate_config_missing_x(self):
        """Test validation fails without x for scatter."""
        config: ChartConfig = {"chart_type": "scatter", "y": "col1"}
        errors = validate_config(config)
        assert len(errors) == 1
        assert "x is required" in errors[0]

    def test_validate_config_missing_y(self):
        """Test validation fails without y for scatter."""
        config: ChartConfig = {"chart_type": "scatter", "x": "col1"}
        errors = validate_config(config)
        assert len(errors) == 1
        assert "y is required" in errors[0]

    def test_validate_config_valid_scatter(self):
        """Test validation passes for valid scatter config."""
        config: ChartConfig = {"chart_type": "scatter", "x": "col1", "y": "col2"}
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_valid_line(self):
        """Test validation passes for valid line config."""
        config: ChartConfig = {"chart_type": "line", "x": "col1", "y": "col2"}
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_scatter_with_options(self):
        """Test validation passes for scatter with optional params."""
        config: ChartConfig = {
            "chart_type": "scatter",
            "x": "col1",
            "y": "col2",
            "by": "group_col",
            "size": "size_col",
            "symbol": "symbol_col",
            "title": "My Chart",
        }
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_line_with_options(self):
        """Test validation passes for line with optional params."""
        config: ChartConfig = {
            "chart_type": "line",
            "x": "col1",
            "y": "col2",
            "by": "group_col",
            "markers": True,
            "line_shape": "hvh",
            "title": "My Line Chart",
        }
        errors = validate_config(config)
        assert len(errors) == 0

    def test_get_required_fields_bar(self):
        """Test required fields for bar chart."""
        required = get_required_fields("bar")
        assert "x" in required
        assert "y" in required

    def test_get_required_fields_area(self):
        """Test required fields for area chart."""
        required = get_required_fields("area")
        assert "x" in required
        assert "y" in required

    def test_get_required_fields_pie(self):
        """Test required fields for pie chart."""
        required = get_required_fields("pie")
        assert "names" in required
        assert "values" in required
        assert "x" not in required
        assert "y" not in required

    def test_validate_config_valid_bar(self):
        """Test validation passes for valid bar config."""
        config: ChartConfig = {"chart_type": "bar", "x": "col1", "y": "col2"}
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_bar_with_orientation(self):
        """Test validation passes for bar with orientation."""
        config: ChartConfig = {
            "chart_type": "bar",
            "x": "col1",
            "y": "col2",
            "orientation": "h",
        }
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_valid_area(self):
        """Test validation passes for valid area config."""
        config: ChartConfig = {"chart_type": "area", "x": "col1", "y": "col2"}
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_valid_pie(self):
        """Test validation passes for valid pie config."""
        config: ChartConfig = {"chart_type": "pie", "names": "col1", "values": "col2"}
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_pie_missing_names(self):
        """Test validation fails for pie without names."""
        config: ChartConfig = {"chart_type": "pie", "values": "col1"}
        errors = validate_config(config)
        assert len(errors) == 1
        assert "names is required" in errors[0]

    def test_validate_config_pie_missing_values(self):
        """Test validation fails for pie without values."""
        config: ChartConfig = {"chart_type": "pie", "names": "col1"}
        errors = validate_config(config)
        assert len(errors) == 1
        assert "values is required" in errors[0]

    # Phase 3: Distribution Plots
    def test_get_required_fields_histogram(self):
        """Test required fields for histogram - returns empty since x OR y is allowed."""
        required = get_required_fields("histogram")
        assert len(required) == 0  # x OR y validated separately

    def test_validate_config_valid_histogram_with_x(self):
        """Test validation passes for histogram with only x."""
        config: ChartConfig = {"chart_type": "histogram", "x": "col1"}
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_valid_histogram_with_y(self):
        """Test validation passes for histogram with only y."""
        config: ChartConfig = {"chart_type": "histogram", "y": "col1"}
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_valid_histogram_with_both(self):
        """Test validation passes for histogram with both x and y."""
        config: ChartConfig = {"chart_type": "histogram", "x": "col1", "y": "col2"}
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_histogram_missing_both(self):
        """Test validation fails for histogram without x or y."""
        config: ChartConfig = {"chart_type": "histogram"}
        errors = validate_config(config)
        assert len(errors) == 1
        assert "x or y is required" in errors[0]

    def test_validate_config_histogram_with_nbins(self):
        """Test validation passes for histogram with nbins."""
        config: ChartConfig = {"chart_type": "histogram", "x": "col1", "nbins": 20}
        errors = validate_config(config)
        assert len(errors) == 0

    def test_get_required_fields_box(self):
        """Test required fields for box chart."""
        required = get_required_fields("box")
        assert "x" in required
        assert "y" in required

    def test_validate_config_valid_box(self):
        """Test validation passes for valid box config."""
        config: ChartConfig = {"chart_type": "box", "x": "col1", "y": "col2"}
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_box_missing_x(self):
        """Test validation fails for box without x."""
        config: ChartConfig = {"chart_type": "box", "y": "col1"}
        errors = validate_config(config)
        assert len(errors) == 1
        assert "x is required" in errors[0]

    def test_get_required_fields_violin(self):
        """Test required fields for violin chart."""
        required = get_required_fields("violin")
        assert "x" in required
        assert "y" in required

    def test_validate_config_valid_violin(self):
        """Test validation passes for valid violin config."""
        config: ChartConfig = {"chart_type": "violin", "x": "col1", "y": "col2"}
        errors = validate_config(config)
        assert len(errors) == 0

    def test_get_required_fields_strip(self):
        """Test required fields for strip chart."""
        required = get_required_fields("strip")
        assert "x" in required
        assert "y" in required

    def test_validate_config_valid_strip(self):
        """Test validation passes for valid strip config."""
        config: ChartConfig = {"chart_type": "strip", "x": "col1", "y": "col2"}
        errors = validate_config(config)
        assert len(errors) == 0

    def test_get_required_fields_density_heatmap(self):
        """Test required fields for density_heatmap chart."""
        required = get_required_fields("density_heatmap")
        assert "x" in required
        assert "y" in required

    def test_validate_config_valid_density_heatmap(self):
        """Test validation passes for valid density_heatmap config."""
        config: ChartConfig = {"chart_type": "density_heatmap", "x": "col1", "y": "col2"}
        errors = validate_config(config)
        assert len(errors) == 0

    # Phase 4: Financial Plots
    def test_get_required_fields_candlestick(self):
        """Test required fields for candlestick chart."""
        required = get_required_fields("candlestick")
        assert "x" in required
        assert "open" in required
        assert "high" in required
        assert "low" in required
        assert "close" in required

    def test_validate_config_valid_candlestick(self):
        """Test validation passes for valid candlestick config."""
        config: ChartConfig = {
            "chart_type": "candlestick",
            "x": "date",
            "open": "open_price",
            "high": "high_price",
            "low": "low_price",
            "close": "close_price",
        }
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_candlestick_missing_x(self):
        """Test validation fails for candlestick without x."""
        config: ChartConfig = {
            "chart_type": "candlestick",
            "open": "open_price",
            "high": "high_price",
            "low": "low_price",
            "close": "close_price",
        }
        errors = validate_config(config)
        assert len(errors) == 1
        assert "x is required" in errors[0]

    def test_validate_config_candlestick_missing_ohlc(self):
        """Test validation fails for candlestick without OHLC columns."""
        config: ChartConfig = {"chart_type": "candlestick", "x": "date"}
        errors = validate_config(config)
        assert len(errors) == 4  # open, high, low, close all missing
        assert any("open is required" in e for e in errors)
        assert any("high is required" in e for e in errors)
        assert any("low is required" in e for e in errors)
        assert any("close is required" in e for e in errors)

    def test_get_required_fields_ohlc(self):
        """Test required fields for ohlc chart."""
        required = get_required_fields("ohlc")
        assert "x" in required
        assert "open" in required
        assert "high" in required
        assert "low" in required
        assert "close" in required

    def test_validate_config_valid_ohlc(self):
        """Test validation passes for valid ohlc config."""
        config: ChartConfig = {
            "chart_type": "ohlc",
            "x": "date",
            "open": "open_price",
            "high": "high_price",
            "low": "low_price",
            "close": "close_price",
        }
        errors = validate_config(config)
        assert len(errors) == 0

    # ==========================================================================
    # Geo Chart Tests (scatter_geo, line_geo)
    # ==========================================================================
    
    def test_get_required_fields_scatter_geo(self):
        """Test required fields for scatter_geo chart."""
        # scatter_geo returns empty since it has special validation (lat+lon OR locations)
        required = get_required_fields("scatter_geo")
        assert len(required) == 0  # Special validation handles this

    def test_validate_config_valid_scatter_geo_with_lat_lon(self):
        """Test validation passes for scatter_geo with lat/lon."""
        config: ChartConfig = {
            "chart_type": "scatter_geo",
            "lat": "Lat",
            "lon": "Lon",
        }
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_valid_scatter_geo_with_locations(self):
        """Test validation passes for scatter_geo with locations."""
        config: ChartConfig = {
            "chart_type": "scatter_geo",
            "locations": "Country",
            "locationmode": "country names",
        }
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_scatter_geo_missing_coords(self):
        """Test validation fails for scatter_geo without coords or locations."""
        config: ChartConfig = {"chart_type": "scatter_geo"}
        errors = validate_config(config)
        assert len(errors) >= 1
        assert any("lat" in e.lower() or "lon" in e.lower() or "locations" in e.lower() for e in errors)

    def test_validate_config_valid_line_geo(self):
        """Test validation passes for line_geo with lat/lon."""
        config: ChartConfig = {
            "chart_type": "line_geo",
            "lat": "Lat",
            "lon": "Lon",
        }
        errors = validate_config(config)
        assert len(errors) == 0

    # ==========================================================================
    # Tile Map Chart Tests (scatter_map, line_map, density_map)
    # ==========================================================================
    
    def test_get_required_fields_scatter_map(self):
        """Test required fields for scatter_map chart."""
        required = get_required_fields("scatter_map")
        assert "lat" in required
        assert "lon" in required

    def test_validate_config_valid_scatter_map(self):
        """Test validation passes for scatter_map with lat/lon."""
        config: ChartConfig = {
            "chart_type": "scatter_map",
            "lat": "Lat",
            "lon": "Lon",
        }
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_scatter_map_missing_lat(self):
        """Test validation fails for scatter_map without lat."""
        config: ChartConfig = {
            "chart_type": "scatter_map",
            "lon": "Lon",
        }
        errors = validate_config(config)
        assert len(errors) >= 1
        assert any("lat" in e.lower() for e in errors)

    def test_validate_config_scatter_map_missing_lon(self):
        """Test validation fails for scatter_map without lon."""
        config: ChartConfig = {
            "chart_type": "scatter_map",
            "lat": "Lat",
        }
        errors = validate_config(config)
        assert len(errors) >= 1
        assert any("lon" in e.lower() for e in errors)

    def test_validate_config_valid_line_map(self):
        """Test validation passes for line_map with lat/lon."""
        config: ChartConfig = {
            "chart_type": "line_map",
            "lat": "Lat",
            "lon": "Lon",
        }
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_valid_density_map(self):
        """Test validation passes for density_map with lat/lon."""
        config: ChartConfig = {
            "chart_type": "density_map",
            "lat": "Lat",
            "lon": "Lon",
        }
        errors = validate_config(config)
        assert len(errors) == 0

    def test_validate_config_density_map_with_options(self):
        """Test validation passes for density_map with optional params."""
        config: ChartConfig = {
            "chart_type": "density_map",
            "lat": "Lat",
            "lon": "Lon",
            "z": "Intensity",
            "radius": 15,
            "zoom": 3,
            "title": "Density Map",
        }
        errors = validate_config(config)
        assert len(errors) == 0
