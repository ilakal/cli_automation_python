"""Secrets manager for loading credentials from environment variables."""
import logging
from typing import Optional

from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)


class SecretsManager:
    """Manages secrets loaded from .env file.
    
    Never logs sensitive values. All secrets are loaded at initialization
    from the .env file (or environment variables).
    """

    def __init__(self, env_file: str = '.env') -> None:
        """Initialize secrets manager.
        
        Args:
            env_file: Path to .env file
        """
        load_dotenv(env_file)
        logger.info(f"Initialized SecretsManager from {env_file}")

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get secret value from environment.
        
        Args:
            key: Environment variable name
            default: Default value if key not found
            
        Returns:
            Secret value or default
            
        Note:
            Never logs the value of secrets for security
        """
        value = os.getenv(key, default)
        
        if value is None:
            logger.warning(f"Secret not found: {key}")
        else:
            logger.debug(f"Retrieved secret: {key}")
        
        return value

    def get_required(self, key: str) -> str:
        """Get required secret value.
        
        Args:
            key: Environment variable name
            
        Returns:
            Secret value
            
        Raises:
            ValueError: If secret not found
        """
        value = self.get(key)
        
        if value is None:
            raise ValueError(f"Required secret not found: {key}")
        
        return value
