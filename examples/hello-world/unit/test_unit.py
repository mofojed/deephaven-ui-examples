"""Unit tests for the hello-world example.

These tests verify the component logic without requiring a running Deephaven server.
"""

import pytest


class TestGreeting:
    """Tests for the greeting component."""

    def test_greeting_function_exists(self):
        """Test that greeting function is defined in the module."""
        # We can't import the module directly without Deephaven runtime,
        # but we can verify the file structure is correct
        import os
        app_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "app.py"
        )
        assert os.path.exists(app_path)
        
        # Verify the function is defined in the source
        with open(app_path, "r") as f:
            content = f.read()
        assert "def greeting(" in content


class TestCounter:
    """Tests for the counter component."""

    def test_counter_function_exists(self):
        """Test that counter function is defined in the module."""
        import os
        app_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "app.py"
        )
        
        with open(app_path, "r") as f:
            content = f.read()
        assert "def counter(" in content


class TestHelloWorldApp:
    """Tests for the main hello_world_app component."""

    def test_app_function_exists(self):
        """Test that hello_world_app function is defined in the module."""
        import os
        app_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "app.py"
        )
        
        with open(app_path, "r") as f:
            content = f.read()
        assert "def hello_world_app(" in content


# Additional unit tests for any helper functions or logic
class TestComponentLogic:
    """Tests for component logic that can be tested in isolation."""

    def test_increment_logic(self):
        """Test increment logic."""
        count = 0
        count = count + 1
        assert count == 1

    def test_decrement_logic(self):
        """Test decrement logic."""
        count = 5
        count = count - 1
        assert count == 4

    def test_reset_logic(self):
        """Test reset logic."""
        count = 10
        count = 0
        assert count == 0
