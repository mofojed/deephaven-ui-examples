"""Unit tests for make_chart function.

These tests verify that make_chart correctly creates charts from configurations.
Since chart creation requires a Deephaven server, these tests focus on 
configuration validation and error handling.
"""

import sys
from pathlib import Path

# Add the chart-builder directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from chart_config import ChartConfig
from make_chart import make_chart


class TestMakeChartValidation:
    """Tests for make_chart validation behavior."""

    def test_make_chart_raises_on_missing_chart_type(self):
        """Test that make_chart raises ValueError when chart_type is missing."""
        config: ChartConfig = {"x": "col1", "y": "col2"}  # type: ignore
        
        with pytest.raises(ValueError) as exc_info:
            make_chart(None, config)  # type: ignore
        
        assert "chart_type is required" in str(exc_info.value)

    def test_make_chart_raises_on_missing_x(self):
        """Test that make_chart raises ValueError when x is missing."""
        config: ChartConfig = {"chart_type": "scatter", "y": "col2"}
        
        with pytest.raises(ValueError) as exc_info:
            make_chart(None, config)  # type: ignore
        
        assert "x is required" in str(exc_info.value)

    def test_make_chart_raises_on_missing_y(self):
        """Test that make_chart raises ValueError when y is missing."""
        config: ChartConfig = {"chart_type": "scatter", "x": "col1"}
        
        with pytest.raises(ValueError) as exc_info:
            make_chart(None, config)  # type: ignore
        
        assert "y is required" in str(exc_info.value)

    def test_make_chart_raises_on_invalid_chart_type(self):
        """Test that make_chart raises ValueError for unsupported chart type."""
        config: ChartConfig = {
            "chart_type": "invalid_type",  # type: ignore
            "x": "col1",
            "y": "col2",
        }
        
        with pytest.raises(ValueError) as exc_info:
            make_chart(None, config)  # type: ignore
        
        assert "Unsupported chart type" in str(exc_info.value)


class TestMakeChartCreation:
    """Tests for actual chart creation with real data."""

    def test_make_scatter_chart(self):
        """Test creating a basic scatter chart."""
        import deephaven.plot.express as dx
        
        table = dx.data.iris()
        config: ChartConfig = {
            "chart_type": "scatter",
            "x": "SepalLength",
            "y": "SepalWidth",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_scatter_chart_with_by(self):
        """Test creating a scatter chart with color grouping."""
        import deephaven.plot.express as dx
        
        table = dx.data.iris()
        config: ChartConfig = {
            "chart_type": "scatter",
            "x": "SepalLength",
            "y": "SepalWidth",
            "by": "Species",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_scatter_chart_with_options(self):
        """Test creating a scatter chart with size and color options."""
        import deephaven.plot.express as dx
        
        table = dx.data.iris()
        config: ChartConfig = {
            "chart_type": "scatter",
            "x": "SepalLength",
            "y": "SepalWidth",
            "by": "Species",
            "title": "Iris Scatter",
            "size": "PetalLength",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_line_chart(self):
        """Test creating a basic line chart."""
        import deephaven.plot.express as dx
        
        table = dx.data.stocks()
        config: ChartConfig = {
            "chart_type": "line",
            "x": "Timestamp",
            "y": "Price",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_line_chart_with_by(self):
        """Test creating a line chart with grouping."""
        import deephaven.plot.express as dx
        
        table = dx.data.stocks()
        config: ChartConfig = {
            "chart_type": "line",
            "x": "Timestamp",
            "y": "Price",
            "by": "Sym",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_line_chart_with_options(self):
        """Test creating a line chart with markers and line shape."""
        import deephaven.plot.express as dx
        
        table = dx.data.stocks()
        config: ChartConfig = {
            "chart_type": "line",
            "x": "Timestamp",
            "y": "Price",
            "by": "Sym",
            "title": "Stock Prices",
            "markers": True,
            "line_shape": "hvh",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_bar_chart(self):
        """Test creating a basic bar chart."""
        import deephaven.plot.express as dx
        
        table = dx.data.tips()
        config: ChartConfig = {
            "chart_type": "bar",
            "x": "Day",
            "y": "TotalBill",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_bar_chart_horizontal(self):
        """Test creating a horizontal bar chart."""
        import deephaven.plot.express as dx
        
        table = dx.data.tips()
        config: ChartConfig = {
            "chart_type": "bar",
            "x": "Day",
            "y": "TotalBill",
            "orientation": "h",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_bar_chart_with_by(self):
        """Test creating a bar chart with grouping."""
        import deephaven.plot.express as dx
        
        table = dx.data.tips()
        config: ChartConfig = {
            "chart_type": "bar",
            "x": "Day",
            "y": "TotalBill",
            "by": "Smoker",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_area_chart(self):
        """Test creating a basic area chart."""
        import deephaven.plot.express as dx
        
        table = dx.data.stocks()
        config: ChartConfig = {
            "chart_type": "area",
            "x": "Timestamp",
            "y": "Price",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_area_chart_with_by(self):
        """Test creating an area chart with grouping."""
        import deephaven.plot.express as dx
        
        table = dx.data.stocks()
        config: ChartConfig = {
            "chart_type": "area",
            "x": "Timestamp",
            "y": "Price",
            "by": "Sym",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_pie_chart(self):
        """Test creating a basic pie chart."""
        import deephaven.plot.express as dx
        
        table = dx.data.tips()
        config: ChartConfig = {
            "chart_type": "pie",
            "names": "Day",
            "values": "TotalBill",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_pie_chart_with_title(self):
        """Test creating a pie chart with title."""
        import deephaven.plot.express as dx
        
        table = dx.data.tips()
        config: ChartConfig = {
            "chart_type": "pie",
            "names": "Day",
            "values": "TotalBill",
            "title": "Tips by Day",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    # Phase 3: Distribution Plots
    def test_make_histogram_with_x(self):
        """Test creating a histogram with x column."""
        import deephaven.plot.express as dx
        
        table = dx.data.iris()
        config: ChartConfig = {
            "chart_type": "histogram",
            "x": "SepalLength",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_histogram_with_y(self):
        """Test creating a histogram with y column."""
        import deephaven.plot.express as dx
        
        table = dx.data.iris()
        config: ChartConfig = {
            "chart_type": "histogram",
            "y": "SepalLength",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_histogram_with_nbins(self):
        """Test creating a histogram with nbins option."""
        import deephaven.plot.express as dx
        
        table = dx.data.iris()
        config: ChartConfig = {
            "chart_type": "histogram",
            "x": "SepalLength",
            "nbins": 20,
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_histogram_with_by(self):
        """Test creating a histogram with grouping."""
        import deephaven.plot.express as dx
        
        table = dx.data.iris()
        config: ChartConfig = {
            "chart_type": "histogram",
            "x": "SepalLength",
            "by": "Species",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_box_chart(self):
        """Test creating a basic box chart."""
        import deephaven.plot.express as dx
        
        table = dx.data.iris()
        config: ChartConfig = {
            "chart_type": "box",
            "x": "Species",
            "y": "SepalLength",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_box_chart_with_by(self):
        """Test creating a box chart with grouping."""
        import deephaven.plot.express as dx
        
        table = dx.data.tips()
        config: ChartConfig = {
            "chart_type": "box",
            "x": "Day",
            "y": "TotalBill",
            "by": "Smoker",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_violin_chart(self):
        """Test creating a basic violin chart."""
        import deephaven.plot.express as dx
        
        table = dx.data.iris()
        config: ChartConfig = {
            "chart_type": "violin",
            "x": "Species",
            "y": "SepalLength",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_violin_chart_with_by(self):
        """Test creating a violin chart with grouping."""
        import deephaven.plot.express as dx
        
        table = dx.data.tips()
        config: ChartConfig = {
            "chart_type": "violin",
            "x": "Day",
            "y": "TotalBill",
            "by": "Sex",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_strip_chart(self):
        """Test creating a basic strip chart."""
        import deephaven.plot.express as dx
        
        table = dx.data.iris()
        config: ChartConfig = {
            "chart_type": "strip",
            "x": "Species",
            "y": "SepalLength",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_strip_chart_with_by(self):
        """Test creating a strip chart with grouping."""
        import deephaven.plot.express as dx
        
        table = dx.data.tips()
        config: ChartConfig = {
            "chart_type": "strip",
            "x": "Day",
            "y": "TotalBill",
            "by": "Smoker",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_density_heatmap(self):
        """Test creating a basic density heatmap."""
        import deephaven.plot.express as dx
        
        table = dx.data.iris()
        config: ChartConfig = {
            "chart_type": "density_heatmap",
            "x": "SepalLength",
            "y": "SepalWidth",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_density_heatmap_with_title(self):
        """Test creating a density heatmap with title."""
        import deephaven.plot.express as dx
        
        table = dx.data.iris()
        config: ChartConfig = {
            "chart_type": "density_heatmap",
            "x": "SepalLength",
            "y": "SepalWidth",
            "title": "Iris Density",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    # Phase 4: Financial Plots
    def test_make_candlestick(self):
        """Test creating a basic candlestick chart."""
        import deephaven.plot.express as dx
        
        table = dx.data.stocks()
        config: ChartConfig = {
            "chart_type": "candlestick",
            "x": "Timestamp",
            "open": "Price",
            "high": "Price",
            "low": "Price",
            "close": "Price",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_candlestick_with_ohlc_sample(self):
        """Test creating a candlestick chart with proper OHLC data."""
        # Import the OHLC sample data creator from app.py
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from app import _create_ohlc_sample
        
        table = _create_ohlc_sample()
        config: ChartConfig = {
            "chart_type": "candlestick",
            "x": "Day",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_ohlc(self):
        """Test creating a basic OHLC chart."""
        import deephaven.plot.express as dx
        
        table = dx.data.stocks()
        config: ChartConfig = {
            "chart_type": "ohlc",
            "x": "Timestamp",
            "open": "Price",
            "high": "Price",
            "low": "Price",
            "close": "Price",
        }
        
        chart = make_chart(table, config)
        assert chart is not None

    def test_make_ohlc_with_ohlc_sample(self):
        """Test creating an OHLC chart with proper OHLC data."""
        # Import the OHLC sample data creator from app.py
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from app import _create_ohlc_sample
        
        table = _create_ohlc_sample()
        config: ChartConfig = {
            "chart_type": "ohlc",
            "x": "Day",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
        }
        
        chart = make_chart(table, config)
        assert chart is not None
