"""
Tests for {{PROJECT_NAME}} main module.
Created: {{DATE}}
"""

import pytest
from click.testing import CliRunner

from main import main, run_application


class TestMain:
    """Test cases for main module functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_main_command_success(self):
        """Test that main command runs successfully."""
        result = self.runner.invoke(main)
        assert result.exit_code == 0
        assert "Starting {{PROJECT_NAME}}" in result.output
        assert "Application completed successfully" in result.output

    def test_main_command_with_verbose(self):
        """Test main command with verbose flag."""
        result = self.runner.invoke(main, ["--verbose"])
        assert result.exit_code == 0
        assert "Starting {{PROJECT_NAME}}" in result.output

    def test_main_command_with_config(self, tmp_path):
        """Test main command with config file."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("# Test config\n")
        
        result = self.runner.invoke(main, ["--config", str(config_file)])
        assert result.exit_code == 0
        assert f"Using config file: {config_file}" in result.output

    def test_run_application(self):
        """Test the main application logic."""
        result = run_application()
        assert result is True

    def test_main_help(self):
        """Test that help message is displayed correctly."""
        result = self.runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "{{PROJECT_NAME}} - A {{PROJECT_TYPE}} application" in result.output
        assert "--verbose" in result.output
        assert "--config" in result.output


@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        "test_item": "test_value",
        "number": 42,
        "list": [1, 2, 3]
    }


def test_sample_fixture(sample_data):
    """Test that fixtures work correctly."""
    assert sample_data["test_item"] == "test_value"
    assert sample_data["number"] == 42
    assert len(sample_data["list"]) == 3


class TestIntegration:
    """Integration tests for the application."""

    def test_full_application_flow(self):
        """Test complete application workflow."""
        runner = CliRunner()
        
        # Test that the full command works end-to-end
        result = runner.invoke(main)
        
        assert result.exit_code == 0
        assert "Starting {{PROJECT_NAME}}" in result.output
        assert "Application completed successfully" in result.output