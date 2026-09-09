"""YAML data loader."""
import logging
from pathlib import Path
from typing import List, Dict, Any

import yaml

logger = logging.getLogger(__name__)


class YamlLoader:
    """Load and parse YAML test data files."""

    @staticmethod
    def load(file_path: str) -> List[Dict[str, Any]]:
        """Load YAML file as list of dictionaries.
        
        Args:
            file_path: Path to YAML file
            
        Returns:
            List of dictionaries from YAML file
            
        Raises:
            FileNotFoundError: If file not found
            yaml.YAMLError: If YAML parsing fails
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"YAML file not found: {file_path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or []
            
            # Ensure we return a list
            if not isinstance(data, list):
                data = [data]
            
            logger.info(f"Loaded {len(data)} items from {file_path}")
            return data
        
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML file {file_path}: {e}")
            raise
