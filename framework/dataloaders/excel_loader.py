"""Excel data loader."""
import logging
from pathlib import Path
from typing import List, Dict, Any

from openpyxl import load_workbook

logger = logging.getLogger(__name__)


class ExcelLoader:
    """Load and parse Excel test data files.
    
    Automatically adds '_row' metadata with row number.
    Loads first sheet by default.
    """

    @staticmethod
    def load(file_path: str, sheet_name: str = None) -> List[Dict[str, Any]]:
        """Load Excel file as list of dictionaries.
        
        Args:
            file_path: Path to Excel file
            sheet_name: Sheet name to load (uses first sheet if None)
            
        Returns:
            List of dictionaries from Excel file with '_row' metadata
            
        Raises:
            FileNotFoundError: If file not found
            Exception: If Excel parsing fails
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Excel file not found: {file_path}")
        
        try:
            workbook = load_workbook(path, data_only=True)
            
            # Use provided sheet or first sheet
            if sheet_name:
                worksheet = workbook[sheet_name]
            else:
                worksheet = workbook.active
            
            data = []
            header_row = None
            
            for row_num, row in enumerate(worksheet.iter_rows(values_only=True), start=1):
                # First row is header
                if header_row is None:
                    header_row = row
                    continue
                
                # Create dictionary from row
                row_dict = {}
                for col_num, value in enumerate(row):
                    if col_num < len(header_row):
                        header = header_row[col_num]
                        if header:  # Skip None headers
                            row_dict[header] = value
                
                # Add row metadata
                row_dict['_row'] = row_num - 1  # Adjust for header row
                data.append(row_dict)
            
            logger.info(f"Loaded {len(data)} items from {file_path}")
            return data
        
        except Exception as e:
            logger.error(f"Failed to parse Excel file {file_path}: {e}")
            raise
