"""Factory for creating appropriate data loaders."""
import logging
from pathlib import Path
from typing import List, Dict, Any

from framework.dataloaders.yaml_loader import YamlLoader
from framework.dataloaders.json_loader import JsonLoader
from framework.dataloaders.csv_loader import CsvLoader
from framework.dataloaders.excel_loader import ExcelLoader

logger = logging.getLogger(__name__)


class LoaderFactory:
    """Factory for creating data loaders based on file type."""

    LOADERS = {
        '.yaml': YamlLoader,
        '.yml': YamlLoader,
        '.json': JsonLoader,
        '.csv': CsvLoader,
        '.xlsx': ExcelLoader,
        '.xls': ExcelLoader,
    }

    @classmethod
    def load(cls, file_path: str) -> List[Dict[str, Any]]:
        """Load data file using appropriate loader.
        
        Args:
            file_path: Path to data file
            
        Returns:
            List of dictionaries from data file
            
        Raises:
            ValueError: If file type not supported
            FileNotFoundError: If file not found
            
        Example:
            >>> factory = LoaderFactory()
            >>> data = factory.load('testdata/yaml/services.yaml')
        """
        path = Path(file_path)
        suffix = path.suffix.lower()
        
        if suffix not in cls.LOADERS:
            raise ValueError(f"Unsupported file type: {suffix}")
        
        loader_class = cls.LOADERS[suffix]
        logger.debug(f"Using {loader_class.__name__} for {file_path}")
        
        return loader_class.load(file_path)
