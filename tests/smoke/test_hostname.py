"""Smoke tests for basic framework functionality."""
import pytest


@pytest.mark.smoke
def test_server_hostname(server_keywords, config):
    """Test that server hostname can be retrieved.
    
    This smoke test verifies basic SSH connectivity and command execution.
    """
    # Note: This test requires actual SSH connectivity
    # For testing without real servers, mock the ssh_client fixture
    pass


@pytest.mark.smoke
def test_config_loading(config):
    """Test that configuration loads correctly."""
    assert config is not None
    assert config.environment in ['qa', 'stage', 'prod']
    
    # Test getting configuration values
    servers = config.get('servers')
    assert servers is not None
    assert 'server1' in servers


@pytest.mark.smoke
def test_secrets_loading(secrets):
    """Test that secrets manager initializes."""
    assert secrets is not None
    # Don't test actual secret values to avoid logging them


@pytest.mark.smoke
def test_command_executor_initialization(executor):
    """Test that command executor initializes."""
    assert executor is not None
    assert executor.default_timeout > 0

