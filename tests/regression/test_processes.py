"""Regression tests for processes."""
import pytest
from framework.dataloaders.loader_factory import LoaderFactory
from framework.validators.tabular_validator import TabularValidator


@pytest.mark.regression
def test_processes_data_structure():
    """Test that processes data has required structure."""
    loader = LoaderFactory()
    processes = loader.load('testdata/csv/processes.csv')
    
    assert processes is not None
    assert len(processes) > 0
    
    # Check required columns
    errors = TabularValidator.validate_columns(
        processes,
        ['process_name', 'pid', 'status']
    )
    assert len(errors) == 0


@pytest.mark.regression
@pytest.mark.parametrize('process_data', 
    LoaderFactory().load('testdata/csv/processes.csv'),
    ids=lambda x: x.get('process_name', 'unknown')
)
def test_process_has_required_fields(process_data):
    """Test that each process has required fields."""
    assert 'process_name' in process_data
    assert 'pid' in process_data
    assert 'status' in process_data
    assert '_row' in process_data  # CSV metadata
    
    # Validate values
    assert process_data['process_name'] is not None
    assert len(str(process_data['process_name'])) > 0
    assert process_data['status'] in ['running', 'stopped', 'sleeping']

