"""E2E tests for the hello-world example.

These tests verify the UI behavior by launching Deephaven and interacting with it via Playwright.
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
class TestHelloWorldE2E:
    """End-to-end tests for the Hello World example."""

    @pytest.mark.skip(reason="Requires running Deephaven server with example loaded")
    def test_greeting_displays(self, deephaven_page: Page):
        """Test that the greeting text is displayed."""
        # Wait for the UI to render
        deephaven_page.wait_for_timeout(2000)

        # Look for the greeting text
        greeting = deephaven_page.locator("text=Hello, Deephaven UI!")
        expect(greeting).to_be_visible()

    @pytest.mark.skip(reason="Requires running Deephaven server with example loaded")
    def test_counter_displays_initial_value(self, deephaven_page: Page):
        """Test that the counter displays the initial value of 0."""
        deephaven_page.wait_for_timeout(2000)

        counter_text = deephaven_page.locator("text=Counter: 0")
        expect(counter_text).to_be_visible()

    @pytest.mark.skip(reason="Requires running Deephaven server with example loaded")
    def test_increment_button_works(self, deephaven_page: Page):
        """Test that clicking the + button increments the counter."""
        deephaven_page.wait_for_timeout(2000)

        # Click the increment button
        increment_btn = deephaven_page.locator("button:has-text('+')")
        increment_btn.click()

        # Verify counter increased
        counter_text = deephaven_page.locator("text=Counter: 1")
        expect(counter_text).to_be_visible()

    @pytest.mark.skip(reason="Requires running Deephaven server with example loaded")
    def test_decrement_button_works(self, deephaven_page: Page):
        """Test that clicking the − button decrements the counter."""
        deephaven_page.wait_for_timeout(2000)

        # First increment to 1
        increment_btn = deephaven_page.locator("button:has-text('+')")
        increment_btn.click()

        # Then decrement
        decrement_btn = deephaven_page.locator("button:has-text('−')")
        decrement_btn.click()

        # Verify counter is back to 0
        counter_text = deephaven_page.locator("text=Counter: 0")
        expect(counter_text).to_be_visible()

    @pytest.mark.skip(reason="Requires running Deephaven server with example loaded")
    def test_reset_button_works(self, deephaven_page: Page):
        """Test that clicking Reset sets the counter back to 0."""
        deephaven_page.wait_for_timeout(2000)

        # Increment several times
        increment_btn = deephaven_page.locator("button:has-text('+')")
        for _ in range(5):
            increment_btn.click()

        # Click reset
        reset_btn = deephaven_page.locator("button:has-text('Reset')")
        reset_btn.click()

        # Verify counter is 0
        counter_text = deephaven_page.locator("text=Counter: 0")
        expect(counter_text).to_be_visible()
