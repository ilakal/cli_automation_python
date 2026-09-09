"""Regression tests for servers."""
import pytest


@pytest.mark.regression
def test_servers_config_exists(config):
    """Test that servers are configured."""
    servers = config.get('servers')
    assert servers is not None
    assert len(servers) > 0


@pytest.mark.regression
def test_server1_configuration(config):
    """Test server1 has required configuration."""
    server1 = config.get('servers.server1')
    assert server1 is not None
    assert 'host' in server1
    assert 'port' in server1
    assert 'username' in server1

