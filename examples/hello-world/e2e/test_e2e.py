"""E2E tests for the hello-world example.

These tests verify the UI behavior by launching Deephaven and interacting with it via Playwright.

To run these tests:
1. Start the server: python scripts/run_example.py hello-world
2. Set the PSK environment variable: export DH_PSK=<psk_from_server_output>
3. Run: pytest examples/hello-world/e2e/ -v
"""

import os

import pytest
from playwright.sync_api import Page, expect


# Get PSK from environment, default for local testing
PSK = os.environ.get("DH_PSK", "")
BASE_URL = os.environ.get("DH_URL", "http://localhost:10000")


@pytest.fixture
def widget_page(page: Page) -> Page:
    """Navigate to the hello_world widget iframe."""
    url = f"{BASE_URL}/iframe/widget/?name=hello_world&psk={PSK}"
    page.goto(url, timeout=30000)
    # Wait for the widget to fully render - look for the actual greeting text
    page.wait_for_selector("text=Hello, Deephaven UI!", timeout=15000)
    return page


@pytest.mark.e2e
class TestHelloWorldE2E:
    """End-to-end tests for the Hello World example."""

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_greeting_displays(self, widget_page: Page):
        """Test that the greeting text is displayed."""
        greeting = widget_page.locator("text=Hello, Deephaven UI!")
        expect(greeting).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_counter_displays_initial_value(self, widget_page: Page):
        """Test that the counter displays the initial value of 0."""
        counter_text = widget_page.locator("text=Counter: 0")
        expect(counter_text).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_increment_button_works(self, widget_page: Page):
        """Test that clicking the + button increments the counter."""
        # Click the increment button
        increment_btn = widget_page.locator("button:has-text('+')")
        increment_btn.click()

        # Verify counter increased
        counter_text = widget_page.locator("text=Counter: 1")
        expect(counter_text).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_decrement_button_works(self, widget_page: Page):
        """Test that clicking the − button decrements the counter."""
        # First increment to 1
        increment_btn = widget_page.locator("button:has-text('+')")
        increment_btn.click()

        # Then decrement
        decrement_btn = widget_page.locator("button:has-text('−')")
        decrement_btn.click()

        # Verify counter is back to 0
        counter_text = widget_page.locator("text=Counter: 0")
        expect(counter_text).to_be_visible()

    @pytest.mark.skipif(not PSK, reason="DH_PSK environment variable not set")
    def test_reset_button_works(self, widget_page: Page):
        """Test that clicking Reset sets the counter back to 0."""
        # Increment several times
        increment_btn = widget_page.locator("button:has-text('+')")
        for _ in range(5):
            increment_btn.click()

        # Click reset
        reset_btn = widget_page.locator("button:has-text('Reset')")
        reset_btn.click()

        # Verify counter is 0
        counter_text = widget_page.locator("text=Counter: 0")
        expect(counter_text).to_be_visible()
