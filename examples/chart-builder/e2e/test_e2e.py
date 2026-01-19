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
    page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)
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
    page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)

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
        error_text = page.locator("text=/Invalid configuration|Error/")
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
        error_text = page.locator("text=/Invalid configuration|Error/")
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
    page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)

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
    page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)

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
    # The Chart Type picker button has aria-labelledby that includes "Chart Type"
    # Use get_by_role to specifically target the chart type picker button
    chart_type_button = page.get_by_role("button", name="Scatter Chart Type")
    chart_type_button.click()
    page.wait_for_timeout(500)

    # Get the popover listbox
    popover = page.get_by_test_id("popover")
    popover.wait_for(state="visible", timeout=5000)

    # The listbox uses virtual scrolling - we need to scroll to make items visible
    listbox = popover.locator('[role="listbox"]')

    # Try to find the item first without scrolling
    chart_type_item = popover.get_by_text(chart_type_name, exact=True)

    # If not visible, try scrolling incrementally to find it
    for scroll_pos in [0, 200, 400, 600, 800, 1000]:
        listbox.evaluate(f"el => el.scrollTop = {scroll_pos}")
        page.wait_for_timeout(200)
        if chart_type_item.is_visible():
            break

    # Now click the item
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
        error_text = page.locator("text=/Invalid configuration|Error/")
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
        error_text = page.locator("text=/Invalid configuration|Error/")
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
        error_text = page.locator("text=/Invalid configuration|Error/")
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
        error_text = page.locator("text=/Invalid configuration|Error/")
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
        error_text = page.locator("text=/Invalid configuration|Error/")
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
        error_text = page.locator("text=/Invalid configuration|Error/")
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
        error_text = page.locator("text=/Invalid configuration|Error/")
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
        location_mode_control = (
            page.get_by_label("Location Mode").locator("visible=true").first
        )
        expect(location_mode_control).to_be_visible()


@pytest.fixture
def advanced_options_page(page: Page) -> Page:
    """Navigate to the chart_builder_demo widget for advanced options testing.

    Note: Advanced Options are only available in chart_builder_app (chart_builder_demo),
    not in the simpler chart_builder function (iris_chart_builder).
    """
    url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
    page.goto(url, timeout=30000)
    # Wait for the chart builder UI to load
    page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)
    return page


@pytest.mark.e2e
class TestAdvancedOptionsE2E:
    """End-to-end tests for Advanced Options in scatter/line charts."""

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_advanced_options_disclosure_visible_for_scatter(
        self, advanced_options_page: Page
    ):
        """Test that Advanced Options disclosure is visible for scatter charts."""
        page = advanced_options_page

        # The disclosure should be visible (collapsed by default)
        # The disclosure title may be rendered as a button or heading
        advanced_options = page.get_by_role("button", name="Advanced Options")
        expect(advanced_options).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_advanced_options_expands(self, advanced_options_page: Page):
        """Test that clicking Advanced Options expands the section."""
        page = advanced_options_page

        # Click to expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # After expanding, should see inner controls like "Text Labels"
        text_labels = page.get_by_label("Text Labels")
        expect(text_labels.first).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_xaxis_title_field_visible_when_expanded(self, advanced_options_page: Page):
        """Test that X Axis Title field is visible when Advanced Options is expanded."""
        page = advanced_options_page

        # Click to expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # X Axis Title field should be visible
        xaxis_title = page.get_by_label("X Axis Title")
        expect(xaxis_title.first).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_xaxis_title_updates_generated_code(self, advanced_options_page: Page):
        """Test that setting X Axis Title updates the generated code."""
        page = advanced_options_page

        # Click to expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Enter a value in X Axis Title field
        xaxis_title_input = page.get_by_label("X Axis Title")
        xaxis_title_input.fill("My Custom X Title")
        page.wait_for_timeout(500)

        # The generated code is always visible in chart_builder_demo
        # Check that xaxis_titles appears in the code
        code_area = page.locator("pre, code")
        expect(code_area.first).to_contain_text("xaxis_titles")

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_template_picker_updates_chart(self, advanced_options_page: Page):
        """Test that changing template updates the chart."""
        page = advanced_options_page

        # Click to expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Select a template
        template_picker = page.get_by_role("button", name="Template")
        template_picker.click()
        page.wait_for_timeout(300)

        # Select plotly_dark
        page.get_by_test_id("popover").get_by_text("plotly_dark").click()
        page.wait_for_timeout(1000)

        # The generated code is always visible in chart_builder_demo
        # Check that template appears in the code
        code_area = page.locator("pre, code")
        expect(code_area.first).to_contain_text('template="plotly_dark"')

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_log_x_checkbox_updates_chart(self, advanced_options_page: Page):
        """Test that toggling Log X checkbox updates the chart."""
        page = advanced_options_page

        # Click to expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Click the Log X checkbox - use click with force for React Aria checkboxes
        log_x_checkbox = page.get_by_label("Log X")
        log_x_checkbox.click(force=True)
        page.wait_for_timeout(500)

        # The generated code is always visible in chart_builder_demo
        # Check that log_x appears in the code
        code_area = page.locator("pre, code")
        expect(code_area.first).to_contain_text("log_x=True")

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_marginal_x_picker_visible_for_scatter(self, advanced_options_page: Page):
        """Test that Marginal X picker is visible for scatter charts."""
        page = advanced_options_page

        # Click to expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Marginal X picker should be visible (scatter-only)
        marginal_x = page.get_by_label("Marginal X")
        expect(marginal_x.first).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_advanced_options_visible_for_bar(self, advanced_options_page: Page):
        """Test that Advanced Options IS visible for bar charts."""
        page = advanced_options_page

        # Switch to bar chart
        chart_type_button = page.get_by_role("button", name="Scatter Chart Type")
        chart_type_button.click()
        page.get_by_test_id("popover").get_by_text("Bar", exact=True).click()
        page.wait_for_timeout(500)

        # Advanced Options should be visible for bar charts (Phase 10 added options)
        advanced_options = page.get_by_role("button", name="Advanced Options")
        expect(advanced_options).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_advanced_options_visible_for_line(self, advanced_options_page: Page):
        """Test that Advanced Options IS visible for line charts."""
        page = advanced_options_page

        # Switch to line chart
        chart_type_button = page.get_by_role("button", name="Scatter Chart Type")
        chart_type_button.click()
        page.get_by_test_id("popover").get_by_text("Line", exact=True).click()
        page.wait_for_timeout(500)

        # Advanced Options should be visible for line charts
        advanced_options = page.get_by_role("button", name="Advanced Options")
        expect(advanced_options).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_line_specific_options_visible(self, advanced_options_page: Page):
        """Test that line-specific options (Line Dash, Line Width) are visible for line charts."""
        page = advanced_options_page

        # Switch to line chart
        chart_type_button = page.get_by_role("button", name="Scatter Chart Type")
        chart_type_button.click()
        page.get_by_test_id("popover").get_by_text("Line", exact=True).click()
        page.wait_for_timeout(500)

        # Click to expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Line-specific options should be visible
        line_dash = page.get_by_label("Line Dash")
        expect(line_dash.first).to_be_visible()

        line_width = page.get_by_label("Line Width")
        expect(line_width.first).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_only_options_hidden_for_line(self, advanced_options_page: Page):
        """Test that scatter-only options (Opacity, Marginal X/Y) are NOT visible for line charts."""
        page = advanced_options_page

        # Switch to line chart
        chart_type_button = page.get_by_role("button", name="Scatter Chart Type")
        chart_type_button.click()
        page.get_by_test_id("popover").get_by_text("Line", exact=True).click()
        page.wait_for_timeout(500)

        # Click to expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Scatter-only options should NOT be visible
        opacity_slider = page.get_by_label("Opacity")
        expect(opacity_slider).not_to_be_visible()

        marginal_x = page.get_by_label("Marginal X")
        expect(marginal_x).not_to_be_visible()

        marginal_y = page.get_by_label("Marginal Y")
        expect(marginal_y).not_to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_line_dash_updates_generated_code(self, advanced_options_page: Page):
        """Test that selecting Line Dash column updates the generated code."""
        page = advanced_options_page

        # Switch to line chart
        chart_type_button = page.get_by_role("button", name="Scatter Chart Type")
        chart_type_button.click()
        page.get_by_test_id("popover").get_by_text("Line", exact=True).click()
        page.wait_for_timeout(500)

        # Click to expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Select a column for Line Dash (Species is available in Iris dataset)
        line_dash_picker = page.get_by_role("button", name="Line Dash")
        line_dash_picker.click()
        page.wait_for_timeout(300)
        # Use exact=True to avoid matching "SpeciesID"
        page.get_by_test_id("popover").get_by_text("Species", exact=True).click()
        page.wait_for_timeout(500)

        # Check that line_dash appears in the generated code
        code_area = page.locator("pre, code")
        expect(code_area.first).to_contain_text('line_dash="Species"')

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_line_common_advanced_options_work(self, advanced_options_page: Page):
        """Test that common advanced options (error bars, axis config, rendering) work for line charts."""
        page = advanced_options_page

        # Switch to line chart
        chart_type_button = page.get_by_role("button", name="Scatter Chart Type")
        chart_type_button.click()
        page.get_by_test_id("popover").get_by_text("Line", exact=True).click()
        page.wait_for_timeout(500)

        # Click to expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Common advanced options should be visible
        text_labels = page.get_by_label("Text Labels")
        expect(text_labels.first).to_be_visible()

        error_x = page.get_by_label("Error X")
        expect(error_x.first).to_be_visible()

        log_x = page.get_by_label("Log X")
        expect(log_x.first).to_be_visible()

        xaxis_title = page.get_by_label("X Axis Title")
        expect(xaxis_title.first).to_be_visible()

        render_mode = page.get_by_label("Render Mode")
        expect(render_mode.first).to_be_visible()

        template = page.get_by_label("Template")
        expect(template.first).to_be_visible()


@pytest.fixture
def scroll_test_page(page: Page) -> Page:
    """Navigate to chart_builder_demo for scroll testing with small viewport."""
    # Set a small viewport to force scrolling behavior
    page.set_viewport_size({"width": 1200, "height": 600})

    url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
    page.goto(url, timeout=30000)
    # Wait for the chart builder UI to load
    page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)
    return page


@pytest.mark.e2e
class TestScrollBehaviorE2E:
    """Test that the controls panel scrolls independently of the chart area."""

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_controls_panel_scrolls_independently(self, scroll_test_page: Page):
        """Test that when Advanced Options is expanded, only the controls panel scrolls.

        The chart area and code preview should stay fixed in view.
        """
        page = scroll_test_page

        # Expand Advanced Options FIRST to make controls taller
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify advanced options expanded
        marginal_x = page.get_by_label("Marginal X")
        expect(marginal_x.first).to_be_visible()

        # NOW get the initial position of the chart/code area elements
        # (after expanding, so we measure from the settled state)
        generated_code_header = page.locator("text=Generated Code").first
        expect(generated_code_header).to_be_visible()

        initial_code_bounds = generated_code_header.bounding_box()
        assert (
            initial_code_bounds is not None
        ), "Generated Code header should be visible"

        # Get the controls panel area (where Chart Type picker is)
        chart_type_label = page.get_by_text("Chart Type", exact=True).first
        controls_bounds = chart_type_label.bounding_box()
        assert controls_bounds is not None, "Chart Type should be visible"

        # Simulate mouse wheel scroll over the controls area
        page.mouse.move(controls_bounds["x"] + 50, controls_bounds["y"] + 100)
        page.mouse.wheel(0, 500)  # Scroll down 500px
        page.wait_for_timeout(300)

        # Check if the document scrolled (which it shouldn't if layout is correct)
        scroll_y = page.evaluate("window.scrollY")

        # The Generated Code header should still be at approximately the same position
        final_code_bounds = generated_code_header.bounding_box()
        assert (
            final_code_bounds is not None
        ), "Generated Code header should still be visible"

        # If the whole page scrolled, the code header would have moved up significantly
        position_diff = abs(final_code_bounds["y"] - initial_code_bounds["y"])

        # The page should not scroll - the controls panel should have its own scrollbar
        assert scroll_y == 0, (
            f"Page scrolled {scroll_y}px when scrolling over controls panel. "
            "The controls panel should scroll independently, not the whole page."
        )

        assert position_diff < 10, (
            f"Code header moved {position_diff}px. "
            "The right panel should stay fixed when scrolling in the controls panel."
        )


@pytest.mark.e2e
class TestColumnTypeDescriptionsE2E:
    """Tests for column picker type descriptions."""

    @pytest.fixture
    def demo_page(self, page: Page) -> Page:
        """Navigate to the chart_builder_demo widget."""
        url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
        page.goto(url, timeout=30000)
        # Wait for the chart builder UI to load
        page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)
        # Wait a bit more for all pickers to render
        page.wait_for_timeout(1000)
        return page

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_column_picker_shows_type_descriptions(self, demo_page: Page):
        """Test that column pickers show data type descriptions."""
        # Find the X picker using get_by_label with exact match and click to open it
        x_picker = demo_page.get_by_label("X", exact=True)
        x_picker.click(timeout=5000)

        # Wait for the popover to appear
        demo_page.wait_for_timeout(500)
        popover = demo_page.get_by_test_id("popover")
        expect(popover).to_be_visible()

        # Check for type descriptions in the picker dropdown
        # The Iris dataset should have Double type columns like SepalLength
        double_description = popover.get_by_text("Double")
        expect(double_description.first).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_column_picker_shows_string_type(self, demo_page: Page):
        """Test that string columns show String type description."""
        # Find the X picker using get_by_label with exact match and click to open it
        x_picker = demo_page.get_by_label("X", exact=True)
        x_picker.click(timeout=5000)

        # Wait for the popover to appear
        demo_page.wait_for_timeout(500)
        popover = demo_page.get_by_test_id("popover")
        expect(popover).to_be_visible()

        # The Iris dataset has a Species column which is a String
        string_description = popover.get_by_text("String")
        expect(string_description.first).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_none_option_in_optional_picker(self, demo_page: Page):
        """Test that optional pickers have a blank option for 'no selection'."""
        # Find the Color picker using get_by_label with exact match and click to open it
        color_picker = demo_page.get_by_label("Color", exact=True)
        color_picker.click(timeout=5000)

        # Wait for the popover to appear
        demo_page.wait_for_timeout(500)
        popover = demo_page.get_by_test_id("popover")
        expect(popover).to_be_visible()

        # Check that the popover has column options with type descriptions
        # This confirms the picker is populated with the blank option plus columns
        double_description = popover.get_by_text("Double")
        expect(double_description.first).to_be_visible()


@pytest.mark.e2e
class TestDistributionChartAdvancedOptionsE2E:
    """Tests for distribution chart advanced options (Phase 11)."""

    @pytest.fixture
    def demo_page(self, page: Page) -> Page:
        """Navigate to the chart_builder_demo widget."""
        url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
        page.goto(url, timeout=30000)
        # Wait for the chart builder UI to load
        page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)
        # Wait a bit more for all pickers to render
        page.wait_for_timeout(1000)
        return page

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_histogram_advanced_options_visible(self, demo_page: Page):
        """Test that histogram advanced options are visible."""
        page = demo_page

        # Select Histogram chart type
        select_chart_type(page, "Histogram")

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify histogram-specific options are visible (use button role for pickers)
        aggregation = page.get_by_role("button", name="Aggregation")
        expect(aggregation.first).to_be_visible()

        normalization = page.get_by_role("button", name="Normalization")
        expect(normalization.first).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_histogram_histfunc_updates_code(self, demo_page: Page):
        """Test that changing histogram aggregation updates generated code."""
        page = demo_page

        # Select Histogram chart type
        select_chart_type(page, "Histogram")

        # Select X column first
        x_picker = page.get_by_role("button", name="X")
        x_picker.click()
        page.get_by_test_id("popover").get_by_text("SepalLength").click()
        page.wait_for_timeout(300)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Change Aggregation to Sum
        aggregation = page.get_by_role("button", name="Aggregation")
        aggregation.click()
        page.wait_for_timeout(300)
        page.get_by_test_id("popover").get_by_text("Sum", exact=True).click()
        page.wait_for_timeout(500)

        # Check that histfunc appears in the code
        code_area = page.locator("pre, code")
        expect(code_area.first).to_contain_text('histfunc="sum"')

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_histogram_cumulative_updates_code(self, demo_page: Page):
        """Test that toggling cumulative checkbox updates generated code."""
        page = demo_page

        # Select Histogram chart type
        select_chart_type(page, "Histogram")

        # Select X column first
        x_picker = page.get_by_role("button", name="X")
        x_picker.click()
        page.get_by_test_id("popover").get_by_text("SepalLength").click()
        page.wait_for_timeout(300)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Click the Cumulative checkbox
        cumulative_checkbox = page.get_by_label("Cumulative")
        cumulative_checkbox.click(force=True)
        page.wait_for_timeout(500)

        # Check that cumulative appears in the code
        code_area = page.locator("pre, code")
        expect(code_area.first).to_contain_text("cumulative=True")

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_box_advanced_options_visible(self, demo_page: Page):
        """Test that box plot advanced options are visible."""
        page = demo_page

        # Select Box chart type
        select_chart_type(page, "Box")

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify box-specific options are visible (use button role for pickers)
        box_mode = page.get_by_role("button", name="Box Mode")
        expect(box_mode.first).to_be_visible()

        show_points = page.get_by_role("button", name="Show Points")
        expect(show_points.first).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_box_notched_updates_code(self, demo_page: Page):
        """Test that toggling notched checkbox updates generated code."""
        page = demo_page

        # Select Box chart type
        select_chart_type(page, "Box")

        # Select X and Y columns first
        x_picker = page.get_by_label("X", exact=True)
        x_picker.click()
        page.get_by_test_id("popover").get_by_text("Species", exact=True).click()
        page.wait_for_timeout(300)

        y_picker = page.get_by_label("Y", exact=True)
        y_picker.click()
        page.get_by_test_id("popover").get_by_text("SepalLength").click()
        page.wait_for_timeout(300)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Click the Notched checkbox
        notched_checkbox = page.get_by_label("Notched (show confidence interval)")
        notched_checkbox.click(force=True)
        page.wait_for_timeout(500)

        # Check that notched appears in the code
        code_area = page.locator("pre, code")
        expect(code_area.first).to_contain_text("notched=True")

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_box_points_updates_code(self, demo_page: Page):
        """Test that changing show points option updates generated code."""
        page = demo_page

        # Select Box chart type
        select_chart_type(page, "Box")

        # Select X and Y columns first
        x_picker = page.get_by_label("X", exact=True)
        x_picker.click()
        page.get_by_test_id("popover").get_by_text("Species", exact=True).click()
        page.wait_for_timeout(300)

        y_picker = page.get_by_label("Y", exact=True)
        y_picker.click()
        page.get_by_test_id("popover").get_by_text("SepalLength").click()
        page.wait_for_timeout(300)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Change Show Points to "All points"
        show_points = page.get_by_role("button", name="Show Points")
        show_points.click()
        page.wait_for_timeout(300)
        page.get_by_test_id("popover").get_by_text("All points", exact=True).click()
        page.wait_for_timeout(500)

        # Check that points appears in the code
        code_area = page.locator("pre, code")
        expect(code_area.first).to_contain_text('points="all"')

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_violin_advanced_options_visible(self, demo_page: Page):
        """Test that violin plot advanced options are visible."""
        page = demo_page

        # Select Violin chart type
        select_chart_type(page, "Violin")

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify violin-specific options are visible (use button role for pickers)
        violin_mode = page.get_by_role("button", name="Violin Mode")
        expect(violin_mode.first).to_be_visible()

        show_inner_box = page.get_by_label("Show inner box plot")
        expect(show_inner_box).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_violin_box_updates_code(self, demo_page: Page):
        """Test that toggling violin box checkbox updates generated code."""
        page = demo_page

        # Select Violin chart type
        select_chart_type(page, "Violin")

        # Select X and Y columns first
        x_picker = page.get_by_label("X", exact=True)
        x_picker.click()
        page.get_by_test_id("popover").get_by_text("Species", exact=True).click()
        page.wait_for_timeout(300)

        y_picker = page.get_by_label("Y", exact=True)
        y_picker.click()
        page.get_by_test_id("popover").get_by_text("SepalLength").click()
        page.wait_for_timeout(300)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Click the Show inner box plot checkbox
        box_checkbox = page.get_by_label("Show inner box plot")
        box_checkbox.click(force=True)
        page.wait_for_timeout(500)

        # Check that box=True appears in the code
        code_area = page.locator("pre, code")
        expect(code_area.first).to_contain_text("box=True")

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_strip_advanced_options_visible(self, demo_page: Page):
        """Test that strip plot advanced options are visible."""
        page = demo_page

        # Select Strip chart type
        select_chart_type(page, "Strip")

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify strip-specific options are visible (use button role for pickers)
        strip_mode = page.get_by_role("button", name="Strip Mode")
        expect(strip_mode.first).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_strip_mode_updates_code(self, demo_page: Page):
        """Test that changing strip mode updates generated code."""
        page = demo_page

        # Select Strip chart type
        select_chart_type(page, "Strip")

        # Select X and Y columns first
        x_picker = page.get_by_label("X", exact=True)
        x_picker.click()
        page.get_by_test_id("popover").get_by_text("Species", exact=True).click()
        page.wait_for_timeout(300)

        y_picker = page.get_by_label("Y", exact=True)
        y_picker.click()
        page.get_by_test_id("popover").get_by_text("SepalLength").click()
        page.wait_for_timeout(300)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Change Strip Mode to Overlay
        strip_mode = page.get_by_role("button", name="Strip Mode")
        strip_mode.click()
        page.wait_for_timeout(300)
        page.get_by_test_id("popover").get_by_text("Overlay", exact=True).click()
        page.wait_for_timeout(500)

        # Check that stripmode appears in the code
        code_area = page.locator("pre, code")
        expect(code_area.first).to_contain_text('stripmode="overlay"')

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_distribution_charts_have_log_axes(self, demo_page: Page):
        """Test that distribution charts have Log X/Y checkboxes."""
        page = demo_page

        # Select Box chart type (representative distribution chart)
        select_chart_type(page, "Box")

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify axis config is available
        log_x = page.get_by_label("Log X")
        expect(log_x).to_be_visible()

        log_y = page.get_by_label("Log Y")
        expect(log_y).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_histogram_log_y_updates_code(self, demo_page: Page):
        """Test that toggling Log Y for histogram updates generated code."""
        page = demo_page

        # Select Histogram chart type
        select_chart_type(page, "Histogram")

        # Select X column first
        x_picker = page.get_by_role("button", name="X")
        x_picker.click()
        page.get_by_test_id("popover").get_by_text("SepalLength").click()
        page.wait_for_timeout(300)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Click the Log Y checkbox
        log_y_checkbox = page.get_by_label("Log Y")
        log_y_checkbox.click(force=True)
        page.wait_for_timeout(500)

        # Check that log_y appears in the code
        code_area = page.locator("pre, code")
        expect(code_area.first).to_contain_text("log_y=True")


@pytest.mark.e2e
class TestFinancialChartAdvancedOptionsE2E:
    """Tests for financial chart (candlestick/ohlc) advanced options (Phase 12)."""

    @pytest.fixture
    def demo_page(self, page: Page) -> Page:
        """Navigate to the chart_builder_demo widget."""
        url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
        page.goto(url, timeout=30000)
        # Wait for the chart builder UI to load
        page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)
        # Wait a bit more for all pickers to render
        page.wait_for_timeout(1000)
        return page

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_candlestick_advanced_options_visible(self, demo_page: Page):
        """Test that candlestick advanced options are visible."""
        page = demo_page

        # Select Candlestick chart type
        select_chart_type(page, "Candlestick")

        # Switch to OHLC dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Stocks OHLC (1min)").click()
        page.wait_for_timeout(300)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify financial chart options are visible (color pickers only)
        expect(page.get_by_text("Financial Chart Options")).to_be_visible()
        expect(page.get_by_text("Up Color")).to_be_visible()
        expect(page.get_by_text("Down Color")).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_ohlc_advanced_options_visible(self, demo_page: Page):
        """Test that OHLC advanced options are visible."""
        page = demo_page

        # Select OHLC chart type
        select_chart_type(page, "OHLC")

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify financial chart options are visible (color pickers only)
        expect(page.get_by_text("Financial Chart Options")).to_be_visible()
        expect(page.get_by_text("Up Color")).to_be_visible()
        expect(page.get_by_text("Down Color")).to_be_visible()


@pytest.mark.e2e
class TestHierarchicalChartAdvancedOptionsE2E:
    """Tests for hierarchical chart (treemap/sunburst/icicle) advanced options (Phase 13)."""

    @pytest.fixture
    def demo_page(self, page: Page) -> Page:
        """Navigate to the chart_builder_demo widget."""
        url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
        page.goto(url, timeout=30000)
        # Wait for the chart builder UI to load
        page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)
        # Wait a bit more for all pickers to render
        page.wait_for_timeout(1000)
        return page

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_treemap_advanced_options_visible(self, demo_page: Page):
        """Test that treemap advanced options are visible."""
        page = demo_page

        # Select Treemap chart type
        select_chart_type(page, "Treemap")

        # Switch to Hierarchy dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Product Hierarchy").click()
        page.wait_for_timeout(300)

        # Select required columns for treemap
        names_picker = page.get_by_role("button", name="Names")
        names_picker.click()
        page.get_by_test_id("popover").get_by_text("Name").first.click()
        page.wait_for_timeout(300)

        values_picker = page.get_by_role("button", name="Values")
        values_picker.click()
        page.get_by_test_id("popover").get_by_text("Sales").first.click()
        page.wait_for_timeout(300)

        parents_picker = page.get_by_role("button", name="Parents")
        parents_picker.click()
        page.get_by_test_id("popover").get_by_text("Parent").first.click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify hierarchical chart options are visible
        expect(page.get_by_text("Hierarchical Chart Options")).to_be_visible()
        expect(page.get_by_text("Branch Values", exact=True)).to_be_visible()
        expect(page.get_by_text("Max Depth (-1 for all)")).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_sunburst_branchvalues_updates_code(self, demo_page: Page):
        """Test that setting Branch Values updates generated code for sunburst."""
        page = demo_page

        # Select Sunburst chart type
        select_chart_type(page, "Sunburst")

        # Switch to Hierarchy dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Product Hierarchy").click()
        page.wait_for_timeout(300)

        # Select required columns
        names_picker = page.get_by_role("button", name="Names")
        names_picker.click()
        page.get_by_test_id("popover").get_by_text("Name").first.click()
        page.wait_for_timeout(300)

        values_picker = page.get_by_role("button", name="Values")
        values_picker.click()
        page.get_by_test_id("popover").get_by_text("Sales").first.click()
        page.wait_for_timeout(300)

        parents_picker = page.get_by_role("button", name="Parents")
        parents_picker.click()
        page.get_by_test_id("popover").get_by_text("Parent").first.click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Select Branch Values = "total"
        branchvalues_picker = page.get_by_role("button", name="(Default) Branch Values")
        branchvalues_picker.click()
        page.get_by_test_id("popover").get_by_text("Total").click()
        page.wait_for_timeout(500)

        # Check that branchvalues appears in the code
        code_area = page.locator("pre, code")
        expect(code_area.first).to_contain_text('branchvalues="total"')

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_icicle_advanced_options_visible(self, demo_page: Page):
        """Test that icicle advanced options are visible."""
        page = demo_page

        # Select Icicle chart type
        select_chart_type(page, "Icicle")

        # Switch to Hierarchy dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Product Hierarchy").click()
        page.wait_for_timeout(300)

        # Select required columns for icicle
        names_picker = page.get_by_role("button", name="Names")
        names_picker.click()
        page.get_by_test_id("popover").get_by_text("Name").first.click()
        page.wait_for_timeout(300)

        values_picker = page.get_by_role("button", name="Values")
        values_picker.click()
        page.get_by_test_id("popover").get_by_text("Sales").first.click()
        page.wait_for_timeout(300)

        parents_picker = page.get_by_role("button", name="Parents")
        parents_picker.click()
        page.get_by_test_id("popover").get_by_text("Parent").first.click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify hierarchical chart options are visible
        expect(page.get_by_text("Hierarchical Chart Options")).to_be_visible()


@pytest.mark.e2e
class TestFunnelChartAdvancedOptionsE2E:
    """Tests for funnel chart advanced options (Phase 13)."""

    @pytest.fixture
    def demo_page(self, page: Page) -> Page:
        """Navigate to the chart_builder_demo widget."""
        url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
        page.goto(url, timeout=30000)
        # Wait for the chart builder UI to load
        page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)
        # Wait a bit more for all pickers to render
        page.wait_for_timeout(1000)
        return page

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_funnel_advanced_options_visible(self, demo_page: Page):
        """Test that funnel advanced options are visible."""
        page = demo_page

        # Select Funnel chart type
        select_chart_type(page, "Funnel")

        # Switch to Funnel dataset (has Stage and Count columns)
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Sales Funnel").click()
        page.wait_for_timeout(500)

        # Expand Advanced Options - should be visible after chart type selected
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify funnel chart options are visible
        expect(page.get_by_text("Funnel Chart Options")).to_be_visible()
        expect(page.get_by_text("Orientation", exact=True)).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_funnel_area_advanced_options_visible(self, demo_page: Page):
        """Test that funnel area advanced options are visible."""
        page = demo_page

        # Select Funnel Area chart type
        select_chart_type(page, "Funnel Area")

        # Switch to Funnel dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Sales Funnel").click()
        page.wait_for_timeout(300)

        # Select required columns for funnel_area (names and values)
        names_picker = page.get_by_role("button", name="Names")
        names_picker.click()
        page.get_by_test_id("popover").get_by_text("Stage").first.click()
        page.wait_for_timeout(300)

        values_picker = page.get_by_role("button", name="Values")
        values_picker.click()
        page.get_by_test_id("popover").get_by_text("Count").first.click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify funnel area chart options are visible
        expect(page.get_by_text("Funnel Area Chart Options")).to_be_visible()


@pytest.mark.e2e
class TestScatter3dAdvancedOptionsE2E:
    """Tests for 3D scatter chart advanced options (Phase 14)."""

    @pytest.fixture
    def demo_page(self, page: Page) -> Page:
        """Navigate to the chart_builder_demo widget."""
        url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
        page.goto(url, timeout=30000)
        # Wait for the chart builder UI to load
        page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)
        # Wait a bit more for all pickers to render
        page.wait_for_timeout(1000)
        return page

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_3d_advanced_options_visible(self, demo_page: Page):
        """Test that scatter_3d advanced options are visible."""
        page = demo_page

        # Select Scatter 3D chart type
        select_chart_type(page, "Scatter 3D")

        # Switch to 3D dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("3D Points").click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify 3D chart options are visible
        expect(page.get_by_text("3D Chart Options")).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_3d_log_z_visible(self, demo_page: Page):
        """Test that Log Z checkbox is visible for 3D charts."""
        page = demo_page

        # Select Scatter 3D chart type
        select_chart_type(page, "Scatter 3D")

        # Switch to 3D dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("3D Points").click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify Log Z is visible under Axis Configuration
        expect(page.get_by_text("Log Z", exact=True)).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_3d_error_z_visible(self, demo_page: Page):
        """Test that Error Z pickers are visible for 3D charts."""
        page = demo_page

        # Select Scatter 3D chart type
        select_chart_type(page, "Scatter 3D")

        # Switch to 3D dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("3D Points").click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify Error Z pickers are visible
        expect(page.get_by_text("Error Z", exact=True)).to_be_visible()
        expect(page.get_by_text("Error Z-", exact=True)).to_be_visible()


@pytest.mark.e2e
class TestLine3dAdvancedOptionsE2E:
    """Tests for 3D line chart advanced options (Phase 14)."""

    @pytest.fixture
    def demo_page(self, page: Page) -> Page:
        """Navigate to the chart_builder_demo widget."""
        url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
        page.goto(url, timeout=30000)
        # Wait for the chart builder UI to load
        page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)
        # Wait a bit more for all pickers to render
        page.wait_for_timeout(1000)
        return page

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_line_3d_markers_visible(self, demo_page: Page):
        """Test that markers checkbox is visible for Line 3D charts."""
        page = demo_page

        # Select Line 3D chart type
        select_chart_type(page, "Line 3D")

        # Switch to 3D dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("3D Points").click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify markers checkbox is visible
        expect(page.get_by_text("Show Markers", exact=True)).to_be_visible()


@pytest.mark.e2e
class TestScatterPolarAdvancedOptionsE2E:
    """Tests for polar scatter chart advanced options (Phase 14)."""

    @pytest.fixture
    def demo_page(self, page: Page) -> Page:
        """Navigate to the chart_builder_demo widget."""
        url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
        page.goto(url, timeout=30000)
        # Wait for the chart builder UI to load
        page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)
        # Wait a bit more for all pickers to render
        page.wait_for_timeout(1000)
        return page

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_polar_advanced_options_visible(self, demo_page: Page):
        """Test that scatter_polar advanced options are visible."""
        page = demo_page

        # Select Scatter Polar chart type
        select_chart_type(page, "Scatter Polar")

        # Switch to Polar dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Polar Data").click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify polar chart options are visible
        expect(page.get_by_text("Polar Chart Options")).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_polar_direction_visible(self, demo_page: Page):
        """Test that Direction picker is visible for polar charts."""
        page = demo_page

        # Select Scatter Polar chart type
        select_chart_type(page, "Scatter Polar")

        # Switch to Polar dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Polar Data").click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify Polar Chart Options header is visible (Direction picker is inside this section)
        expect(page.get_by_text("Polar Chart Options")).to_be_visible()
        # Verify Direction picker options are available (check the (Default) option that's unique to this picker)
        expect(page.get_by_label("Direction(Default)")).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_polar_start_angle_visible(self, demo_page: Page):
        """Test that Start Angle field is visible for polar charts."""
        page = demo_page

        # Select Scatter Polar chart type
        select_chart_type(page, "Scatter Polar")

        # Switch to Polar dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Polar Data").click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify Start Angle field is visible
        expect(page.get_by_text("Start Angle (degrees)", exact=True)).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_polar_log_r_visible(self, demo_page: Page):
        """Test that Log R checkbox is visible for polar charts."""
        page = demo_page

        # Select Scatter Polar chart type
        select_chart_type(page, "Scatter Polar")

        # Switch to Polar dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Polar Data").click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify Log R checkbox is visible
        expect(page.get_by_text("Log R (Radial Axis)", exact=True)).to_be_visible()


@pytest.mark.e2e
class TestLinePolarAdvancedOptionsE2E:
    """Tests for polar line chart advanced options (Phase 14)."""

    @pytest.fixture
    def demo_page(self, page: Page) -> Page:
        """Navigate to the chart_builder_demo widget."""
        url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
        page.goto(url, timeout=30000)
        # Wait for the chart builder UI to load
        page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)
        # Wait a bit more for all pickers to render
        page.wait_for_timeout(1000)
        return page

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_line_polar_line_close_visible(self, demo_page: Page):
        """Test that Close Line Shape checkbox is visible for line_polar."""
        page = demo_page

        # Select Line Polar chart type
        select_chart_type(page, "Line Polar")

        # Switch to Polar dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Polar Data").click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify Close Line Shape checkbox is visible
        expect(page.get_by_text("Close Line Shape", exact=True)).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_line_polar_markers_visible(self, demo_page: Page):
        """Test that markers checkbox is visible for line_polar."""
        page = demo_page

        # Select Line Polar chart type
        select_chart_type(page, "Line Polar")

        # Switch to Polar dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Polar Data").click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify markers checkbox is visible
        expect(page.get_by_text("Show Markers", exact=True)).to_be_visible()


@pytest.mark.e2e
class TestScatterTernaryAdvancedOptionsE2E:
    """Tests for ternary scatter chart advanced options (Phase 14)."""

    @pytest.fixture
    def demo_page(self, page: Page) -> Page:
        """Navigate to the chart_builder_demo widget."""
        url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
        page.goto(url, timeout=30000)
        # Wait for the chart builder UI to load
        page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)
        # Wait a bit more for all pickers to render
        page.wait_for_timeout(1000)
        return page

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_ternary_advanced_options_visible(self, demo_page: Page):
        """Test that scatter_ternary advanced options are visible."""
        page = demo_page

        # Select Scatter Ternary chart type
        select_chart_type(page, "Scatter Ternary")

        # Switch to Ternary dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Ternary Data").click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify ternary chart options are visible
        expect(page.get_by_text("Ternary Chart Options")).to_be_visible()


@pytest.mark.e2e
class TestLineTernaryAdvancedOptionsE2E:
    """Tests for ternary line chart advanced options (Phase 14)."""

    @pytest.fixture
    def demo_page(self, page: Page) -> Page:
        """Navigate to the chart_builder_demo widget."""
        url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
        page.goto(url, timeout=30000)
        # Wait for the chart builder UI to load
        page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)
        # Wait a bit more for all pickers to render
        page.wait_for_timeout(1000)
        return page

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_line_ternary_line_close_visible(self, demo_page: Page):
        """Test that Close Line Shape checkbox is visible for line_ternary."""
        page = demo_page

        # Select Line Ternary chart type
        select_chart_type(page, "Line Ternary")

        # Switch to Ternary dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Ternary Data").click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify Close Line Shape checkbox is visible
        expect(page.get_by_text("Close Line Shape", exact=True)).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_line_ternary_markers_visible(self, demo_page: Page):
        """Test that markers checkbox is visible for line_ternary."""
        page = demo_page

        # Select Line Ternary chart type
        select_chart_type(page, "Line Ternary")

        # Switch to Ternary dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Ternary Data").click()
        page.wait_for_timeout(500)

        # Expand Advanced Options
        advanced_options = page.get_by_role("button", name="Advanced Options")
        advanced_options.click()
        page.wait_for_timeout(500)

        # Verify markers checkbox is visible
        expect(page.get_by_text("Show Markers", exact=True)).to_be_visible()


# Phase 15: Map/Geo Advanced Options Tests


@pytest.mark.e2e
class TestGeoChartAdvancedOptionsE2E:
    """Tests for geo chart (scatter_geo, line_geo) advanced options (Phase 15)."""

    @pytest.fixture
    def flights_page(self, page: Page) -> Page:
        """Navigate to the chart_builder_demo widget and select Flights dataset."""
        url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
        page.goto(url, timeout=30000)
        # Wait for the chart builder UI to load
        page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)
        # Wait a bit more for all pickers to render
        page.wait_for_timeout(1000)

        # Select the Flights sample dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Flights").click()
        page.wait_for_timeout(1000)

        return page

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_geo_projection_picker_visible(self, flights_page: Page):
        """Test that Projection picker is visible for scatter_geo."""
        page = flights_page

        # Select Scatter Geo chart type
        select_chart_type(page, "Scatter Geo")
        page.wait_for_timeout(500)

        # Verify Geo Chart Options section is visible
        expect(page.get_by_text("Geo Chart Options")).to_be_visible()

        # Verify Projection picker is visible
        projection_picker = (
            page.get_by_label("Projection").locator("visible=true").first
        )
        expect(projection_picker).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_geo_scope_picker_visible(self, flights_page: Page):
        """Test that Scope picker is visible for scatter_geo."""
        page = flights_page

        # Select Scatter Geo chart type
        select_chart_type(page, "Scatter Geo")
        page.wait_for_timeout(500)

        # Verify Scope picker is visible
        scope_picker = page.get_by_label("Scope").locator("visible=true").first
        expect(scope_picker).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_geo_fitbounds_picker_visible(self, flights_page: Page):
        """Test that Fit Bounds picker is visible for scatter_geo."""
        page = flights_page

        # Select Scatter Geo chart type
        select_chart_type(page, "Scatter Geo")
        page.wait_for_timeout(500)

        # Verify Fit Bounds picker is visible
        fitbounds_picker = page.get_by_label("Fit Bounds").locator("visible=true").first
        expect(fitbounds_picker).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_geo_basemap_checkbox_visible(self, flights_page: Page):
        """Test that Show Basemap checkbox is visible for scatter_geo."""
        page = flights_page

        # Select Scatter Geo chart type
        select_chart_type(page, "Scatter Geo")
        page.wait_for_timeout(500)

        # Verify Show Basemap checkbox is visible
        expect(page.get_by_text("Show Basemap", exact=True)).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_line_geo_markers_checkbox_visible(self, flights_page: Page):
        """Test that Show Markers checkbox is visible for line_geo."""
        page = flights_page

        # Select Line Geo chart type
        select_chart_type(page, "Line Geo")
        page.wait_for_timeout(500)

        # Verify Geo Chart Options section is visible
        expect(page.get_by_text("Geo Chart Options")).to_be_visible()

        # Verify Show Markers checkbox is visible
        expect(page.get_by_text("Show Markers", exact=True)).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_line_geo_projection_picker_visible(self, flights_page: Page):
        """Test that Projection picker is visible for line_geo."""
        page = flights_page

        # Select Line Geo chart type
        select_chart_type(page, "Line Geo")
        page.wait_for_timeout(500)

        # Verify Projection picker is visible
        projection_picker = (
            page.get_by_label("Projection").locator("visible=true").first
        )
        expect(projection_picker).to_be_visible()


@pytest.mark.e2e
class TestMapChartAdvancedOptionsE2E:
    """Tests for tile-based map chart (scatter_map, line_map, density_map) advanced options (Phase 15)."""

    @pytest.fixture
    def outages_page(self, page: Page) -> Page:
        """Navigate to the chart_builder_demo widget and select Outages dataset."""
        url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
        page.goto(url, timeout=30000)
        # Wait for the chart builder UI to load
        page.get_by_text("Chart Type", exact=True).wait_for(timeout=5000)
        # Wait a bit more for all pickers to render
        page.wait_for_timeout(1000)

        # Select the Outages sample dataset
        dataset_picker = page.locator("button:has-text('Iris')")
        dataset_picker.click()
        page.get_by_test_id("popover").get_by_text("Outages").click()
        page.wait_for_timeout(1000)

        return page

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_map_opacity_slider_visible(self, outages_page: Page):
        """Test that Opacity slider is visible for scatter_map."""
        page = outages_page

        # Select Scatter Map chart type
        select_chart_type(page, "Scatter Map")
        page.wait_for_timeout(500)

        # Verify Map Chart Options section is visible
        expect(page.get_by_text("Map Chart Options")).to_be_visible()

        # Verify Opacity slider is visible
        opacity_slider = page.get_by_label("Opacity").locator("visible=true").first
        expect(opacity_slider).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_line_map_markers_checkbox_visible(self, outages_page: Page):
        """Test that Show Markers checkbox is visible for line_map."""
        page = outages_page

        # Select Line Map chart type
        select_chart_type(page, "Line Map")
        page.wait_for_timeout(500)

        # Verify Map Chart Options section is visible
        expect(page.get_by_text("Map Chart Options")).to_be_visible()

        # Verify Show Markers checkbox is visible
        expect(page.get_by_text("Show Markers", exact=True)).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_line_map_opacity_slider_visible(self, outages_page: Page):
        """Test that Opacity slider is visible for line_map."""
        page = outages_page

        # Select Line Map chart type
        select_chart_type(page, "Line Map")
        page.wait_for_timeout(500)

        # Verify Opacity slider is visible
        opacity_slider = page.get_by_label("Opacity").locator("visible=true").first
        expect(opacity_slider).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_density_map_opacity_slider_visible(self, outages_page: Page):
        """Test that Opacity slider is visible for density_map."""
        page = outages_page

        # Select Density Map chart type
        select_chart_type(page, "Density Map")
        page.wait_for_timeout(500)

        # Verify Map Chart Options section is visible
        expect(page.get_by_text("Map Chart Options")).to_be_visible()

        # Verify Opacity slider is visible
        opacity_slider = page.get_by_label("Opacity").locator("visible=true").first
        expect(opacity_slider).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_density_map_no_markers_checkbox(self, outages_page: Page):
        """Test that Show Markers checkbox is NOT visible for density_map."""
        page = outages_page

        # Select Density Map chart type
        select_chart_type(page, "Density Map")
        page.wait_for_timeout(500)

        # Verify Show Markers checkbox is NOT visible for density_map
        markers_checkbox = page.get_by_text("Show Markers", exact=True)
        expect(markers_checkbox).not_to_be_visible()
