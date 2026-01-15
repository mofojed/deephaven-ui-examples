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
    # Wait for the chart builder UI to load
    page.wait_for_selector("text=Chart Type", timeout=15000)
    return page


@pytest.mark.e2e
class TestChartBuilderE2E:
    """End-to-end tests for the Chart Builder component."""

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_chart_type_picker_visible(self, widget_page: Page):
        """Test that the chart type picker is visible."""
        chart_type_picker = widget_page.locator("text=Chart Type")
        expect(chart_type_picker).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_column_pickers_visible(self, widget_page: Page):
        """Test that X and Y column pickers are visible."""
        x_picker = widget_page.locator("text=X Column")
        y_picker = widget_page.locator("text=Y Column")
        expect(x_picker).to_be_visible()
        expect(y_picker).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_group_by_picker_visible(self, widget_page: Page):
        """Test that Group By picker is visible."""
        group_by_picker = widget_page.locator("text=Group By")
        expect(group_by_picker).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_scatter_options_visible_by_default(self, widget_page: Page):
        """Test that scatter-specific options are visible by default."""
        # Scatter is the default chart type
        size_picker = widget_page.locator("text=Size Column")
        symbol_picker = widget_page.locator("text=Symbol Column")
        color_picker = widget_page.locator("text=Color Column")
        
        expect(size_picker).to_be_visible()
        expect(symbol_picker).to_be_visible()
        expect(color_picker).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_line_options_hidden_by_default(self, widget_page: Page):
        """Test that line-specific options are hidden when scatter is selected."""
        # Line shape should not be visible when scatter is selected
        line_shape = widget_page.locator("text=Line Shape")
        expect(line_shape).not_to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_switch_to_line_shows_line_options(self, widget_page: Page):
        """Test that switching to line chart shows line options."""
        # Click the chart type picker and select Line
        chart_type_button = widget_page.locator("button:has-text('Scatter')")
        chart_type_button.click()
        
        # Select Line from the dropdown
        line_option = widget_page.locator("text=Line").first
        line_option.click()
        
        # Wait for UI to update
        widget_page.wait_for_timeout(500)
        
        # Now line options should be visible
        line_shape = widget_page.locator("text=Line Shape")
        markers_checkbox = widget_page.locator("text=Show Markers")
        
        expect(line_shape).to_be_visible()
        expect(markers_checkbox).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_switch_to_line_hides_scatter_options(self, widget_page: Page):
        """Test that switching to line chart hides scatter options."""
        # Click the chart type picker and select Line
        chart_type_button = widget_page.locator("button:has-text('Scatter')")
        chart_type_button.click()
        
        # Select Line from the dropdown
        line_option = widget_page.locator("text=Line").first
        line_option.click()
        
        # Wait for UI to update
        widget_page.wait_for_timeout(500)
        
        # Scatter options should be hidden
        size_picker = widget_page.locator("text=Size Column")
        symbol_picker = widget_page.locator("text=Symbol Column")
        
        expect(size_picker).not_to_be_visible()
        expect(symbol_picker).not_to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_title_field_visible(self, widget_page: Page):
        """Test that the title text field is visible."""
        title_field = widget_page.locator("text=Chart Title")
        expect(title_field).to_be_visible()


@pytest.fixture
def ohlc_widget_page(page: Page) -> Page:
    """Navigate to the chart_builder_demo widget and select OHLC dataset."""
    url = f"{BASE_URL}/iframe/widget/?name=chart_builder_demo&psk={PSK}"
    page.goto(url, timeout=30000)
    # Wait for the chart builder UI to load
    page.wait_for_selector("text=Chart Type", timeout=15000)
    
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
