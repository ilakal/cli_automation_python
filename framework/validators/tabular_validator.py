"""Tabular data validator."""
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class TabularValidator:
    """Validate tabular data (CSV, Excel rows).
    
    Validates:
    - Required columns
    - Column types
    - Row count
    - Value constraints
    """

    @staticmethod
    def validate_columns(
        data: List[Dict[str, Any]],
        required_columns: List[str]
    ) -> List[str]:
        """Validate required columns exist.
        
        Args:
            data: List of row dictionaries
            required_columns: Required column names
            
        Returns:
            List of error messages
        """
        errors = []
        
        if not data:
            return ["No data rows found"]
        
        first_row = data[0]
        missing = set(required_columns) - set(first_row.keys())
        
        if missing:
            errors.append(f"Missing required columns: {missing}")
        
        return errors

    @staticmethod
    def validate_row_count(
        data: List[Dict[str, Any]],
        min_rows: Optional[int] = None,
        max_rows: Optional[int] = None
    ) -> List[str]:
        """Validate row count.
        
        Args:
            data: List of row dictionaries
            min_rows: Minimum required rows
            max_rows: Maximum allowed rows
            
        Returns:
            List of error messages
        """
        errors = []
        count = len(data)
        
        if min_rows is not None and count < min_rows:
            errors.append(f"Row count {count} is below minimum {min_rows}")
        
        if max_rows is not None and count > max_rows:
            errors.append(f"Row count {count} exceeds maximum {max_rows}")
        
        return errors

    @staticmethod
    def validate_column_values(
        data: List[Dict[str, Any]],
        column: str,
        allowed_values: List[Any]
    ) -> List[str]:
        """Validate column values.
        
        Args:
            data: List of row dictionaries
            column: Column name
            allowed_values: List of allowed values
            
        Returns:
            List of error messages
        """
        errors = []
        
        for row_num, row in enumerate(data, start=1):
            if column not in row:
                errors.append(f"Row {row_num}: Column '{column}' not found")
                continue
            
            value = row[column]
            if value not in allowed_values:
                errors.append(
                    f"Row {row_num}: Invalid value '{value}' in column '{column}'. "
                    f"Allowed values: {allowed_values}"
                )
        
        return errors
