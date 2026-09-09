"""Configuration manager for environment-specific settings."""
import logging
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages environment-specific configuration.
    
    Loads YAML configuration files for different environments (qa, stage, prod)
    and provides access to configuration values using dot notation.
    """

    def __init__(self, environment: str) -> None:
        """Initialize configuration manager.
        
        Args:
            environment: Environment name (qa, stage, prod)
            
        Raises:
            FileNotFoundError: If configuration file not found
            yaml.YAMLError: If YAML parsing fails
        """
        self.environment = environment
        self.config_path = Path("config") / f"{environment}.yaml"
        self._config: Dict[str, Any] = {}
        self._load_config()
        logger.info(f"Initialized ConfigManager for environment: {environment}")

    def _load_config(self) -> None:
        """Load configuration from YAML file.
        
        Raises:
            FileNotFoundError: If configuration file not found
            yaml.YAMLError: If YAML parsing fails
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f) or {}
            logger.debug(f"Loaded configuration from {self.config_path}")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get configuration value using dot notation.
        
        Args:
            key: Configuration key using dot notation (e.g., 'servers.server1.host')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
            
        Example:
            >>> config = ConfigManager('qa')
            >>> host = config.get('servers.server1.host')
        """
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            if default is not None:
                return default
            logger.warning(f"Configuration key not found: {key}")
            return None

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration.
        
        Returns:
            Complete configuration dictionary
        """
        return self._config.copy()
