"""Framework unit tests for tabular validator."""
import pytest
from framework.validators.tabular_validator import TabularValidator


def test_tabular_validator_validates_columns():
    """Test TabularValidator validates required columns."""
    data = [
        {'name': 'test', 'value': 123},
        {'name': 'test2', 'value': 456}
    ]
    
    errors = TabularValidator.validate_columns(
        data,
        ['name', 'value']
    )
    
    assert len(errors) == 0


def test_tabular_validator_detects_missing_columns():
    """Test TabularValidator detects missing columns."""
    data = [
        {'name': 'test'},
        {'name': 'test2'}
    ]
    
    errors = TabularValidator.validate_columns(
        data,
        ['name', 'value']
    )
    
    assert len(errors) > 0
    assert 'Missing required columns' in errors[0]


def test_tabular_validator_validates_row_count():
    """Test TabularValidator validates row count."""
    data = [{}, {}, {}]
    
    errors = TabularValidator.validate_row_count(
        data,
        min_rows=2,
        max_rows=5
    )
    
    assert len(errors) == 0


def test_tabular_validator_detects_too_few_rows():
    """Test TabularValidator detects insufficient rows."""
    data = [{}]
    
    errors = TabularValidator.validate_row_count(
        data,
        min_rows=2
    )
    
    assert len(errors) > 0
    assert 'below minimum' in errors[0]


def test_tabular_validator_detects_too_many_rows():
    """Test TabularValidator detects too many rows."""
    data = [{}, {}, {}, {}, {}]
    
    errors = TabularValidator.validate_row_count(
        data,
        max_rows=3
    )
    
    assert len(errors) > 0
    assert 'exceeds maximum' in errors[0]


def test_tabular_validator_validates_column_values():
    """Test TabularValidator validates column values."""
    data = [
        {'status': 'active'},
        {'status': 'inactive'}
    ]
    
    errors = TabularValidator.validate_column_values(
        data,
        'status',
        ['active', 'inactive']
    )
    
    assert len(errors) == 0


def test_tabular_validator_detects_invalid_values():
    """Test TabularValidator detects invalid values."""
    data = [
        {'status': 'active'},
        {'status': 'invalid'}
    ]
    
    errors = TabularValidator.validate_column_values(
        data,
        'status',
        ['active', 'inactive']
    )
    
    assert len(errors) > 0
    assert 'Invalid value' in errors[0]

