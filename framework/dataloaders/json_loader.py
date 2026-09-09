"""JSON data loader."""
import logging
import json
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class JsonLoader:
    """Load and parse JSON test data files."""

    @staticmethod
    def load(file_path: str) -> List[Dict[str, Any]]:
        """Load JSON file as list of dictionaries.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            List of dictionaries from JSON file
            
        Raises:
            FileNotFoundError: If file not found
            json.JSONDecodeError: If JSON parsing fails
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Ensure we return a list
            if not isinstance(data, list):
                data = [data]
            
            logger.info(f"Loaded {len(data)} items from {file_path}")
            return data
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON file {file_path}: {e}")
            raise
