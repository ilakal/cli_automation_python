"""Framework unit tests for LoaderFactory."""
import pytest
from pathlib import Path
from framework.dataloaders.loader_factory import LoaderFactory


def test_loader_factory_yaml():
    """Test LoaderFactory loads YAML files."""
    loader = LoaderFactory()
    data = loader.load('testdata/yaml/services.yaml')
    
    assert data is not None
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'name' in data[0]


def test_loader_factory_json():
    """Test LoaderFactory loads JSON files."""
    loader = LoaderFactory()
    data = loader.load('testdata/json/users.json')
    
    assert data is not None
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'username' in data[0]


def test_loader_factory_csv():
    """Test LoaderFactory loads CSV files with metadata."""
    loader = LoaderFactory()
    data = loader.load('testdata/csv/processes.csv')
    
    assert data is not None
    assert isinstance(data, list)
    assert len(data) > 0
    
    # CSV loader should add _row metadata
    for row in data:
        assert '_row' in row
        assert isinstance(row['_row'], int)


def test_loader_factory_unsupported_format():
    """Test LoaderFactory raises error for unsupported format."""
    loader = LoaderFactory()
    
    with pytest.raises(ValueError, match="Unsupported file type"):
        loader.load('testdata/unknown.txt')


def test_loader_factory_missing_file():
    """Test LoaderFactory raises error for missing file."""
    loader = LoaderFactory()
    
    with pytest.raises(FileNotFoundError, match="not found"):
        loader.load('testdata/yaml/nonexistent.yaml')

