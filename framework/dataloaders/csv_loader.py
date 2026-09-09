"""CSV data loader."""
import logging
import csv
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class CsvLoader:
    """Load and parse CSV test data files.
    
    Automatically adds '_row' metadata with row number.
    """

    @staticmethod
    def load(file_path: str) -> List[Dict[str, Any]]:
        """Load CSV file as list of dictionaries.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            List of dictionaries from CSV file with '_row' metadata
            
        Raises:
            FileNotFoundError: If file not found
            csv.Error: If CSV parsing fails
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        
        try:
            data = []
            
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row_num, row in enumerate(reader, start=1):
                    # Add row metadata
                    row['_row'] = row_num
                    data.append(row)
            
            logger.info(f"Loaded {len(data)} items from {file_path}")
            return data
        
        except csv.Error as e:
            logger.error(f"Failed to parse CSV file {file_path}: {e}")
            raise
