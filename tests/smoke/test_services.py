"""Smoke tests for services."""
import pytest


@pytest.mark.smoke
def test_services_data_loads(config):
    """Test that services test data loads correctly."""
    from framework.dataloaders.loader_factory import LoaderFactory
    
    loader = LoaderFactory()
    services = loader.load('testdata/yaml/services.yaml')
    
    assert services is not None
    assert len(services) > 0
    assert 'name' in services[0]
    assert 'status' in services[0]

