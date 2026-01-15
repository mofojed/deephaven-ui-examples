"""E2E tests for the chart-builder example.

These tests verify the chart builder UI behavior.

To run these tests:
1. Start the server: python scripts/run_example.py chart-builder
2. Set the PSK environment variable: export DH_PSK=<psk_from_server_output>
3. Run: pytest examples/chart-builder/e2e/ -v
"""

import os

import pytest
from playwright.sync_api import Page, expect


# Get PSK from environment
PSK = os.environ.get("DH_PSK", "")
BASE_URL = os.environ.get("DH_URL", "http://localhost:10000")


@pytest.fixture
def widget_page(page: Page) -> Page:
    """Navigate to the iris_chart_builder widget."""
    url = f"{BASE_URL}/iframe/widget/?name=iris_chart_builder&psk={PSK}"
    page.goto(url, timeout=30000)
    # Wait for the chart builder UI to load using exact text match
    page.get_by_text("Chart Type", exact=True).wait_for(timeout=15000)
    return page


@pytest.mark.e2e
class TestChartBuilderE2E:
    """End-to-end tests for the Chart Builder component."""

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_chart_type_picker_visible(self, widget_page: Page):
        """Test that the chart type picker is visible."""
        chart_type_picker = widget_page.get_by_text("Chart Type", exact=True)
        expect(chart_type_picker).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_column_pickers_visible(self, widget_page: Page):
        """Test that X and Y column pickers are visible."""
        x_picker = widget_page.get_by_text("X", exact=True).first
        y_picker = widget_page.get_by_text("Y", exact=True).first
        expect(x_picker).to_be_visible()
        expect(y_picker).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_group_by_picker_visible(self, widget_page: Page):
        """Test that Group By picker is visible."""
        group_by_picker = widget_page.get_by_text("Group By", exact=True)
        expect(group_by_picker).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_options_visible_by_default(self, widget_page: Page):
        """Test that scatter-specific options are visible by default."""
        # Scatter is the default chart type
        size_picker = widget_page.get_by_text("Size", exact=True)
        color_picker = widget_page.get_by_text("Color", exact=True)
        
        expect(size_picker).to_be_visible()
        expect(color_picker).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_line_options_hidden_by_default(self, widget_page: Page):
        """Test that line-specific options are hidden when scatter is selected."""
        # Line shape should not be visible when scatter is selected
        line_shape = widget_page.get_by_text("Line Shape", exact=True)
        expect(line_shape).not_to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_switch_to_line_shows_line_options(self, widget_page: Page):
        """Test that switching to line chart shows line options."""
        # Click the chart type picker and select Line
        chart_type_button = widget_page.locator("button:has-text('Scatter')")
        chart_type_button.click()
        
        # Select Line from the dropdown using the popover
        popover = widget_page.get_by_test_id("popover")
        line_option = popover.get_by_text("Line", exact=True)
        line_option.click()
        
        # Wait for UI to update
        widget_page.wait_for_timeout(500)
        
        # Now line options should be visible
        line_shape = widget_page.get_by_text("Line Shape", exact=True)
        markers_checkbox = widget_page.get_by_text("Markers", exact=True)
        
        expect(line_shape).to_be_visible()
        expect(markers_checkbox).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_switch_to_line_hides_scatter_options(self, widget_page: Page):
        """Test that switching to line chart hides scatter options."""
        # Click the chart type picker and select Line
        chart_type_button = widget_page.locator("button:has-text('Scatter')")
        chart_type_button.click()
        
        # Select Line from the dropdown using the popover
        popover = widget_page.get_by_test_id("popover")
        line_option = popover.get_by_text("Line", exact=True)
        line_option.click()
        
        # Wait for UI to update
        widget_page.wait_for_timeout(500)
        
        # Scatter options should be hidden
        size_picker = widget_page.get_by_text("Size", exact=True)
        
        expect(size_picker).not_to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_title_field_visible(self, widget_page: Page):
        """Test that the title text field is visible."""
        title_field = widget_page.get_by_text("Title", exact=True)
        expect(title_field).to_be_visible()


@pytest.fixture
def ohlc_widget_page(page: Page) -> Page:
    """Navigate to the chart_builder_demo widget and select OHLC dataset."""
    url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
    page.goto(url, timeout=30000)
    # Wait for the chart builder UI to load using exact text match
    page.get_by_text("Chart Type", exact=True).wait_for(timeout=15000)
    
    # Select the OHLC sample dataset
    dataset_picker = page.locator("button:has-text('Iris')")
    dataset_picker.click()
    # Use the popover menu item specifically
    page.get_by_test_id("popover").get_by_text("Stocks OHLC (1min)").click()
    page.wait_for_timeout(1000)  # Wait for dataset to load
    
    return page


@pytest.mark.e2e
class TestOHLCChartE2E:
    """End-to-end tests for OHLC and Candlestick charts."""

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_candlestick_chart_renders(self, ohlc_widget_page: Page):
        """Test that candlestick chart renders with OHLC data."""
        page = ohlc_widget_page
        
        # Select Candlestick chart type
        chart_type_button = page.locator("button:has-text('Scatter')")
        chart_type_button.click()
        # Use the popover menu item specifically
        page.get_by_test_id("popover").get_by_text("Candlestick").click()
        page.wait_for_timeout(500)
        
        # Select X column (BinnedTimestamp)
        x_picker = page.get_by_role("button", name="X (Date/Time)")
        x_picker.click()
        page.get_by_test_id("popover").get_by_text("BinnedTimestamp").first.click()
        page.wait_for_timeout(300)
        
        # Select Open column
        open_picker = page.get_by_role("button", name="Open")
        open_picker.click()
        page.get_by_test_id("popover").get_by_text("Open").first.click()
        page.wait_for_timeout(300)
        
        # Select High column
        high_picker = page.get_by_role("button", name="High")
        high_picker.click()
        page.get_by_test_id("popover").get_by_text("High").first.click()
        page.wait_for_timeout(300)
        
        # Select Low column
        low_picker = page.get_by_role("button", name="Low")
        low_picker.click()
        page.get_by_test_id("popover").get_by_text("Low").first.click()
        page.wait_for_timeout(300)
        
        # Select Close column
        close_picker = page.get_by_role("button", name="Close")
        close_picker.click()
        page.get_by_test_id("popover").get_by_text("Close").first.click()
        page.wait_for_timeout(1000)
        
        # Verify no error message is displayed
        error_text = page.locator('text=/Invalid configuration|Error/')
        expect(error_text).not_to_be_visible()
        
        # Verify chart is rendered (check for plotly chart element)
        chart_element = page.locator(".plotly, .js-plotly-plot, [class*='chart'], svg")
        expect(chart_element.first).to_be_visible(timeout=10000)

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_ohlc_chart_renders(self, ohlc_widget_page: Page):
        """Test that OHLC chart renders with OHLC data."""
        page = ohlc_widget_page
        
        # Select OHLC chart type
        chart_type_button = page.locator("button:has-text('Scatter')")
        chart_type_button.click()
        # Use the popover menu item specifically - OHLC is exact match
        page.get_by_test_id("popover").get_by_text("OHLC", exact=True).click()
        page.wait_for_timeout(500)
        
        # Select X column (BinnedTimestamp)
        x_picker = page.get_by_role("button", name="X (Date/Time)")
        x_picker.click()
        page.get_by_test_id("popover").get_by_text("BinnedTimestamp").first.click()
        page.wait_for_timeout(300)
        
        # Select Open column
        open_picker = page.get_by_role("button", name="Open")
        open_picker.click()
        page.get_by_test_id("popover").get_by_text("Open").first.click()
        page.wait_for_timeout(300)
        
        # Select High column
        high_picker = page.get_by_role("button", name="High")
        high_picker.click()
        page.get_by_test_id("popover").get_by_text("High").first.click()
        page.wait_for_timeout(300)
        
        # Select Low column
        low_picker = page.get_by_role("button", name="Low")
        low_picker.click()
        page.get_by_test_id("popover").get_by_text("Low").first.click()
        page.wait_for_timeout(300)
        
        # Select Close column
        close_picker = page.get_by_role("button", name="Close")
        close_picker.click()
        page.get_by_test_id("popover").get_by_text("Close").first.click()
        page.wait_for_timeout(1000)
        
        # Verify no error message is displayed
        error_text = page.locator('text=/Invalid configuration|Error/')
        expect(error_text).not_to_be_visible()
        
        # Verify chart is rendered
        chart_element = page.locator(".plotly, .js-plotly-plot, [class*='chart'], svg")
        expect(chart_element.first).to_be_visible(timeout=10000)


# =============================================================================
# Map/Geo Chart Tests
# =============================================================================

@pytest.fixture
def flights_widget_page(page: Page) -> Page:
    """Navigate to the chart_builder_demo widget and select Flights dataset."""
    url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
    page.goto(url, timeout=30000)
    # Wait for the chart builder UI to load using exact text match
    page.get_by_text("Chart Type", exact=True).wait_for(timeout=15000)
    
    # Select the Flights dataset
    dataset_picker = page.locator("button:has-text('Iris')")
    dataset_picker.click()
    # Use the popover menu item specifically
    page.get_by_test_id("popover").get_by_text("Flights").click()
    page.wait_for_timeout(1000)  # Wait for dataset to load
    
    return page


@pytest.fixture
def outages_widget_page(page: Page) -> Page:
    """Navigate to the chart_builder_demo widget and select Outages dataset."""
    url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
    page.goto(url, timeout=30000)
    # Wait for the chart builder UI to load using exact text match
    page.get_by_text("Chart Type", exact=True).wait_for(timeout=15000)
    
    # Select the Outages dataset
    dataset_picker = page.locator("button:has-text('Iris')")
    dataset_picker.click()
    # Use the popover menu item specifically
    page.get_by_test_id("popover").get_by_text("Outages").click()
    page.wait_for_timeout(1000)  # Wait for dataset to load
    
    return page


def select_chart_type(page: Page, chart_type_name: str):
    """Helper to select a chart type from the dropdown, scrolling if needed.
    
    The chart type dropdown uses virtual scrolling, so items at the bottom
    of the list aren't rendered until we scroll to them.
    """
    # The Chart Type picker button displays the current selection (default is "Scatter")
    # Look for a button with "Scatter" text (the default selected chart type)
    chart_type_button = page.locator("button:has-text('Scatter')")
    chart_type_button.click()
    page.wait_for_timeout(500)
    
    # Get the popover listbox
    popover = page.get_by_test_id("popover")
    popover.wait_for(state="visible", timeout=5000)
    
    # The listbox uses virtual scrolling - we need to scroll to make items visible
    listbox = popover.locator('[role="listbox"]')
    
    # Scroll the listbox to the bottom to trigger rendering of all items
    # Map chart types are near the bottom of the list
    listbox.evaluate("el => el.scrollTop = el.scrollHeight")
    page.wait_for_timeout(300)
    
    # Now find and click the chart type item
    chart_type_item = popover.get_by_text(chart_type_name, exact=True)
    chart_type_item.click()
    page.wait_for_timeout(500)


@pytest.mark.e2e
class TestMapChartE2E:
    """End-to-end tests for Map/Geo charts."""

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_map_chart_renders(self, flights_widget_page: Page):
        """Test that scatter_map chart renders with flights data."""
        page = flights_widget_page
        
        # Select Scatter Map chart type
        select_chart_type(page, "Scatter Map")
        
        # Select Lat column
        lat_picker = page.get_by_role("button", name="Lat")
        lat_picker.click()
        page.get_by_test_id("popover").get_by_text("Lat", exact=True).first.click()
        page.wait_for_timeout(300)
        
        # Select Lon column
        lon_picker = page.get_by_role("button", name="Lon")
        lon_picker.click()
        page.get_by_test_id("popover").get_by_text("Lon", exact=True).first.click()
        page.wait_for_timeout(1000)
        
        # Verify no error message is displayed
        error_text = page.locator('text=/Invalid configuration|Error/')
        expect(error_text).not_to_be_visible()
        
        # Verify chart is rendered (check for plotly chart element)
        chart_element = page.locator(".plotly, .js-plotly-plot, [class*='chart'], svg")
        expect(chart_element.first).to_be_visible(timeout=10000)

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_map_with_size_color(self, flights_widget_page: Page):
        """Test scatter_map chart with size and color options."""
        page = flights_widget_page
        
        # Select Scatter Map chart type
        select_chart_type(page, "Scatter Map")
        
        # Select Lat column
        lat_picker = page.get_by_role("button", name="Lat")
        lat_picker.click()
        page.get_by_test_id("popover").get_by_text("Lat", exact=True).first.click()
        page.wait_for_timeout(300)
        
        # Select Lon column
        lon_picker = page.get_by_role("button", name="Lon")
        lon_picker.click()
        page.get_by_test_id("popover").get_by_text("Lon", exact=True).first.click()
        page.wait_for_timeout(300)
        
        # Select Size column (Speed)
        size_picker = page.get_by_role("button", name="Size")
        size_picker.click()
        page.get_by_test_id("popover").get_by_text("Speed").first.click()
        page.wait_for_timeout(300)
        
        # Select Color column (Speed)
        color_picker = page.get_by_role("button", name="Color")
        color_picker.click()
        page.get_by_test_id("popover").get_by_text("Speed").first.click()
        page.wait_for_timeout(1000)
        
        # Verify no error message is displayed
        error_text = page.locator('text=/Invalid configuration|Error/')
        expect(error_text).not_to_be_visible()
        
        # Verify chart is rendered
        chart_element = page.locator(".plotly, .js-plotly-plot, [class*='chart'], svg")
        expect(chart_element.first).to_be_visible(timeout=10000)

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_line_map_chart_renders(self, flights_widget_page: Page):
        """Test that line_map chart renders with flights data."""
        page = flights_widget_page
        
        # Select Line Map chart type
        select_chart_type(page, "Line Map")
        
        # Select Lat column
        lat_picker = page.get_by_role("button", name="Lat")
        lat_picker.click()
        page.get_by_test_id("popover").get_by_text("Lat", exact=True).first.click()
        page.wait_for_timeout(300)
        
        # Select Lon column
        lon_picker = page.get_by_role("button", name="Lon")
        lon_picker.click()
        page.get_by_test_id("popover").get_by_text("Lon", exact=True).first.click()
        page.wait_for_timeout(1000)
        
        # Verify no error message is displayed
        error_text = page.locator('text=/Invalid configuration|Error/')
        expect(error_text).not_to_be_visible()
        
        # Verify chart is rendered
        chart_element = page.locator(".plotly, .js-plotly-plot, [class*='chart'], svg")
        expect(chart_element.first).to_be_visible(timeout=10000)

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_density_map_chart_renders(self, outages_widget_page: Page):
        """Test that density_map chart renders with outages data."""
        page = outages_widget_page
        
        # Select Density Map chart type
        select_chart_type(page, "Density Map")
        
        # Select Lat column
        lat_picker = page.get_by_role("button", name="Lat")
        lat_picker.click()
        page.get_by_test_id("popover").get_by_text("Lat", exact=True).first.click()
        page.wait_for_timeout(300)
        
        # Select Lon column
        lon_picker = page.get_by_role("button", name="Lon")
        lon_picker.click()
        page.get_by_test_id("popover").get_by_text("Lon", exact=True).first.click()
        page.wait_for_timeout(1000)
        
        # Verify no error message is displayed
        error_text = page.locator('text=/Invalid configuration|Error/')
        expect(error_text).not_to_be_visible()
        
        # Verify chart is rendered
        chart_element = page.locator(".plotly, .js-plotly-plot, [class*='chart'], svg")
        expect(chart_element.first).to_be_visible(timeout=10000)

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_density_map_with_z_radius(self, outages_widget_page: Page):
        """Test density_map chart with Z (intensity) and radius options."""
        page = outages_widget_page
        
        # Select Density Map chart type
        select_chart_type(page, "Density Map")
        
        # Select Lat column
        lat_picker = page.get_by_role("button", name="Lat")
        lat_picker.click()
        page.get_by_test_id("popover").get_by_text("Lat", exact=True).first.click()
        page.wait_for_timeout(300)
        
        # Select Lon column
        lon_picker = page.get_by_role("button", name="Lon")
        lon_picker.click()
        page.get_by_test_id("popover").get_by_text("Lon", exact=True).first.click()
        page.wait_for_timeout(300)
        
        # Select Z (Intensity) column (Severity)
        z_picker = page.get_by_role("button", name="Z (Intensity)")
        z_picker.click()
        page.get_by_test_id("popover").get_by_text("Severity").first.click()
        page.wait_for_timeout(1000)
        
        # Verify no error message is displayed
        error_text = page.locator('text=/Invalid configuration|Error/')
        expect(error_text).not_to_be_visible()
        
        # Verify chart is rendered
        chart_element = page.locator(".plotly, .js-plotly-plot, [class*='chart'], svg")
        expect(chart_element.first).to_be_visible(timeout=10000)

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_geo_chart_renders(self, flights_widget_page: Page):
        """Test that scatter_geo chart renders with flights data."""
        page = flights_widget_page
        
        # Select Scatter Geo chart type
        select_chart_type(page, "Scatter Geo")
        
        # Select Lat column
        lat_picker = page.get_by_role("button", name="Lat")
        lat_picker.click()
        page.get_by_test_id("popover").get_by_text("Lat", exact=True).first.click()
        page.wait_for_timeout(300)
        
        # Select Lon column
        lon_picker = page.get_by_role("button", name="Lon")
        lon_picker.click()
        page.get_by_test_id("popover").get_by_text("Lon", exact=True).first.click()
        page.wait_for_timeout(1000)
        
        # Verify no error message is displayed
        error_text = page.locator('text=/Invalid configuration|Error/')
        expect(error_text).not_to_be_visible()
        
        # Verify chart is rendered
        chart_element = page.locator(".plotly, .js-plotly-plot, [class*='chart'], svg")
        expect(chart_element.first).to_be_visible(timeout=10000)

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_line_geo_chart_renders(self, flights_widget_page: Page):
        """Test that line_geo chart renders with flights data."""
        page = flights_widget_page
        
        # Select Line Geo chart type
        select_chart_type(page, "Line Geo")
        
        # Select Lat column
        lat_picker = page.get_by_role("button", name="Lat")
        lat_picker.click()
        page.get_by_test_id("popover").get_by_text("Lat", exact=True).first.click()
        page.wait_for_timeout(300)
        
        # Select Lon column
        lon_picker = page.get_by_role("button", name="Lon")
        lon_picker.click()
        page.get_by_test_id("popover").get_by_text("Lon", exact=True).first.click()
        page.wait_for_timeout(1000)
        
        # Verify no error message is displayed
        error_text = page.locator('text=/Invalid configuration|Error/')
        expect(error_text).not_to_be_visible()
        
        # Verify chart is rendered
        chart_element = page.locator(".plotly, .js-plotly-plot, [class*='chart'], svg")
        expect(chart_element.first).to_be_visible(timeout=10000)

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_map_controls_visible_for_scatter_map(self, flights_widget_page: Page):
        """Test that map-specific controls (Lat, Lon, Zoom) are visible for scatter_map."""
        page = flights_widget_page
        
        # Select Scatter Map chart type
        select_chart_type(page, "Scatter Map")
        
        # Verify map-specific controls are visible
        # Use locator with text match for the label, then find the associated button
        lat_control = page.get_by_label("Lat").locator("visible=true").first
        expect(lat_control).to_be_visible()
        
        lon_control = page.get_by_label("Lon").locator("visible=true").first
        expect(lon_control).to_be_visible()
        
        # Verify Zoom control is visible
        zoom_control = page.get_by_label("Zoom").locator("visible=true").first
        expect(zoom_control).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_geo_controls_visible_for_scatter_geo(self, flights_widget_page: Page):
        """Test that geo-specific controls (Lat, Lon, Locations, Location Mode) are visible."""
        page = flights_widget_page
        
        # Select Scatter Geo chart type
        select_chart_type(page, "Scatter Geo")
        
        # Verify geo-specific controls are visible
        lat_control = page.get_by_label("Lat").locator("visible=true").first
        expect(lat_control).to_be_visible()
        
        lon_control = page.get_by_label("Lon").locator("visible=true").first
        expect(lon_control).to_be_visible()
        
        # Verify Locations picker is visible
        locations_control = page.get_by_label("Locations").locator("visible=true").first
        expect(locations_control).to_be_visible()
        
        # Verify Location Mode picker is visible
        location_mode_control = page.get_by_label("Location Mode").locator("visible=true").first
        expect(location_mode_control).to_be_visible()
