"""Pytest configuration and global fixtures."""
import os
import logging
from pathlib import Path
from typing import Generator

import pytest
from framework.core.config_manager import ConfigManager
from framework.core.secrets_manager import SecretsManager
from framework.core.ssh_client import SSHClient
from framework.core.command_executor import CommandExecutor
from framework.core.database import DatabaseClient
from framework.keywords.server_keywords import ServerKeywords
from framework.keywords.database_keywords import DatabaseKeywords
from framework.keywords.filesystem_keywords import FilesystemKeywords
from framework.assertions.soft_assertions import SoftAssertions
from framework.validators.data_validation_plugin import DataValidationPlugin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Environment to run tests against: qa, stage, prod"
    )


def pytest_configure(config):
    """Configure pytest."""
    # Store environment in config
    config.env = config.getoption("--env")
    logger.info(f"Configured pytest for environment: {config.env}")


def pytest_sessionstart(session):
    """Run data validation at session start."""
    logger.info("Starting test session")
    
    schema_map_path = Path("schemas/schema_map.yaml")
    if schema_map_path.exists():
        plugin = DataValidationPlugin()
        all_errors = plugin.validate_all(str(schema_map_path))
        
        if all_errors:
            logger.error("Data validation failed with errors:")
            for error in all_errors:
                logger.error(f"  {error}")
            pytest.exit("Data validation failed. See errors above.", 1)
        else:
            logger.info("Data validation passed successfully")
    else:
        logger.warning(f"Schema map not found at {schema_map_path}")


@pytest.fixture(scope="session")
def env(request) -> str:
    """Get the configured environment."""
    return request.config.env


@pytest.fixture(scope="session")
def config(env) -> ConfigManager:
    """Provide configuration manager."""
    return ConfigManager(env)


@pytest.fixture(scope="session")
def secrets() -> SecretsManager:
    """Provide secrets manager."""
    return SecretsManager()


@pytest.fixture(scope="function")
def ssh_client(config, secrets) -> Generator[SSHClient, None, None]:
    """Provide connected SSH client."""
    server_config = config.get("servers.server1")
    
    client = SSHClient(
        hostname=server_config.get("host"),
        port=server_config.get("port", 22),
        username=server_config.get("username"),
        key_filename=secrets.get("SSH_KEY_PATH"),
        known_hosts_file=secrets.get("SSH_KNOWN_HOSTS_PATH")
    )
    
    yield client
    
    client.close()


@pytest.fixture(scope="function")
def executor(ssh_client) -> CommandExecutor:
    """Provide command executor."""
    return CommandExecutor(ssh_client=ssh_client)


@pytest.fixture(scope="function")
def database(config, secrets) -> Generator[DatabaseClient, None, None]:
    """Provide database client."""
    db_config = config.get("database")
    
    db = DatabaseClient(
        host=db_config.get("host"),
        port=db_config.get("port", 5432),
        database=db_config.get("name"),
        user=db_config.get("username", secrets.get("DB_USERNAME")),
        password=secrets.get("DB_PASSWORD")
    )
    
    yield db
    
    db.close()


@pytest.fixture(scope="function")
def server_keywords(ssh_client) -> ServerKeywords:
    """Provide server keywords."""
    return ServerKeywords(ssh_client=ssh_client)


@pytest.fixture(scope="function")
def database_keywords(database) -> DatabaseKeywords:
    """Provide database keywords."""
    return DatabaseKeywords(database=database)


@pytest.fixture(scope="function")
def filesystem_keywords(ssh_client) -> FilesystemKeywords:
    """Provide filesystem keywords."""
    return FilesystemKeywords(ssh_client=ssh_client)


@pytest.fixture(scope="function")
def soft_assertions() -> SoftAssertions:
    """Provide soft assertions."""
    return SoftAssertions()


@pytest.fixture(scope="function")
def test_user() -> dict:
    """Provide test user data."""
    return {
        "username": "testuser",
        "password": "TestPassword123!",
        "email": "testuser@example.com",
        "role": "user"
    }
