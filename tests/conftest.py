"""Pytest configuration and fixtures for deephaven-ui-examples."""

import os
import sys

import pytest

# Add the project root to the path so examples can be imported
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "e2e: mark test as an end-to-end test")


@pytest.fixture(scope="session")
def project_root() -> str:
    """Return the project root directory."""
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def examples_dir(project_root: str) -> str:
    """Return the examples directory."""
    return os.path.join(project_root, "examples")
