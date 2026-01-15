"""Playwright E2E test fixtures and Deephaven server management."""

import os
import subprocess
import sys
import time
from typing import Generator

import pytest
from playwright.sync_api import Page, expect

# Default Deephaven server settings
DEFAULT_PORT = 10000
DEFAULT_TIMEOUT = 30000  # 30 seconds


@pytest.fixture(scope="session")
def deephaven_port() -> int:
    """Return the port for the Deephaven server."""
    return int(os.environ.get("DEEPHAVEN_PORT", DEFAULT_PORT))


@pytest.fixture(scope="session")
def deephaven_base_url(deephaven_port: int) -> str:
    """Return the base URL for the Deephaven server."""
    return f"http://localhost:{deephaven_port}"


@pytest.fixture(scope="session")
def deephaven_server(deephaven_port: int) -> Generator[subprocess.Popen, None, None]:
    """Start and manage the Deephaven server for E2E tests.

    This fixture starts the server once per test session and stops it when done.
    """
    # Get project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    start_script = os.path.join(project_root, "scripts", "start_server.py")

    # Get Python executable from the virtual environment
    venv_python = os.path.join(project_root, ".venv", "bin", "python")
    python_cmd = venv_python if os.path.exists(venv_python) else sys.executable

    print(f"\nStarting Deephaven server on port {deephaven_port}...")

    # Start the server process
    process = subprocess.Popen(
        [python_cmd, start_script, "--port", str(deephaven_port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=project_root,
    )

    # Wait for server to be ready
    max_wait = 60  # seconds
    start_time = time.time()
    server_ready = False

    while time.time() - start_time < max_wait:
        try:
            import urllib.request
            url = f"http://localhost:{deephaven_port}/ide/"
            urllib.request.urlopen(url, timeout=1)
            server_ready = True
            break
        except Exception:
            time.sleep(1)

    if not server_ready:
        process.terminate()
        raise RuntimeError(f"Deephaven server failed to start within {max_wait} seconds")

    print(f"Deephaven server is ready at http://localhost:{deephaven_port}")

    yield process

    # Cleanup: stop the server
    print("\nStopping Deephaven server...")
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()


@pytest.fixture
def deephaven_page(
    page: Page, deephaven_server: subprocess.Popen, deephaven_base_url: str
) -> Page:
    """Provide a Playwright page connected to the Deephaven IDE.

    Args:
        page: The Playwright page fixture.
        deephaven_server: Ensures the server is running.
        deephaven_base_url: The base URL for the server.

    Returns:
        A Playwright page navigated to the Deephaven IDE.
    """
    # Navigate to the IDE
    page.goto(f"{deephaven_base_url}/ide/", timeout=DEFAULT_TIMEOUT)

    # Wait for the IDE to be ready (look for the console or main UI element)
    page.wait_for_load_state("networkidle", timeout=DEFAULT_TIMEOUT)

    return page


@pytest.fixture
def run_code_in_deephaven(deephaven_page: Page):
    """Provide a helper function to run code in the Deephaven console.

    Returns:
        A function that accepts Python code and executes it in Deephaven.
    """
    def _run_code(code: str) -> None:
        """Execute Python code in the Deephaven console.

        Args:
            code: Python code to execute.
        """
        # This is a simplified implementation - actual implementation
        # would need to interact with the Deephaven IDE console
        # For now, we'll use the REST API or console input
        pass

    return _run_code


# Helper functions for common E2E test operations


def wait_for_panel(page: Page, panel_name: str, timeout: int = DEFAULT_TIMEOUT) -> None:
    """Wait for a panel with the given name to appear.

    Args:
        page: The Playwright page.
        panel_name: The name of the panel to wait for.
        timeout: Maximum time to wait in milliseconds.
    """
    page.wait_for_selector(f'[data-testid="panel-{panel_name}"]', timeout=timeout)


def wait_for_table(page: Page, table_name: str, timeout: int = DEFAULT_TIMEOUT) -> None:
    """Wait for a table with the given name to appear.

    Args:
        page: The Playwright page.
        table_name: The name of the table to wait for.
        timeout: Maximum time to wait in milliseconds.
    """
    page.wait_for_selector(f'[data-testid="table-{table_name}"]', timeout=timeout)


def take_screenshot(page: Page, name: str, examples_dir: str) -> str:
    """Take a screenshot and save it to the example directory.

    Args:
        page: The Playwright page.
        name: Name for the screenshot file.
        examples_dir: Directory to save the screenshot in.

    Returns:
        Path to the saved screenshot.
    """
    screenshot_path = os.path.join(examples_dir, f"{name}.png")
    page.screenshot(path=screenshot_path)
    return screenshot_path
