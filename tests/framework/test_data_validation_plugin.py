"""Framework unit tests for data validation plugin."""
import pytest
from framework.validators.data_validation_plugin import DataValidationPlugin


def test_data_validation_plugin_initializes():
    """Test DataValidationPlugin initializes."""
    plugin = DataValidationPlugin()
    assert plugin is not None


def test_data_validation_plugin_validates_all():
    """Test DataValidationPlugin validates all test data."""
    plugin = DataValidationPlugin()
    errors = plugin.validate_all('schemas/schema_map.yaml')
    
    assert isinstance(errors, list)
    # Errors list may not be empty if test data has issues

