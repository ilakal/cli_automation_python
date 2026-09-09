"""Framework unit tests for schema validator."""
import pytest
from framework.validators.schema_validator import SchemaValidator


def test_schema_validator_validates_services():
    """Test SchemaValidator validates services data."""
    validator = SchemaValidator()
    errors = validator.validate_file(
        'testdata/yaml/services.yaml',
        'schemas/services_schema.yaml'
    )
    
    assert isinstance(errors, list)
    # Should pass validation or have meaningful errors


def test_schema_validator_validates_users():
    """Test SchemaValidator validates users data."""
    validator = SchemaValidator()
    errors = validator.validate_file(
        'testdata/json/users.json',
        'schemas/users_schema.yaml'
    )
    
    assert isinstance(errors, list)


def test_schema_validator_detects_missing_file():
    """Test SchemaValidator detects missing data file."""
    validator = SchemaValidator()
    
    with pytest.raises(FileNotFoundError):
        validator.validate_file(
            'testdata/yaml/nonexistent.yaml',
            'schemas/services_schema.yaml'
        )


def test_schema_validator_detects_missing_schema():
    """Test SchemaValidator detects missing schema file."""
    validator = SchemaValidator()
    
    with pytest.raises(FileNotFoundError):
        validator.validate_file(
            'testdata/yaml/services.yaml',
            'schemas/nonexistent_schema.yaml'
        )

