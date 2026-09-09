"""Schema validator using JSON Schema."""
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

import yaml
from jsonschema import Draft202012Validator, ValidationError

logger = logging.getLogger(__name__)


class SchemaValidator:
    """Validate data against JSON Schema.
    
    Provides detailed error reporting with:
    - File paths
    - Dataset paths (for nested structures)
    - Row numbers (for tabular data)
    - Aggregated failure reporting
    """

    @staticmethod
    def load_schema(schema_path: str) -> Dict[str, Any]:
        """Load JSON Schema from YAML file.
        
        Args:
            schema_path: Path to schema YAML file
            
        Returns:
            Schema dictionary
            
        Raises:
            FileNotFoundError: If schema file not found
            yaml.YAMLError: If YAML parsing fails
        """
        path = Path(schema_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            schema = yaml.safe_load(f)
        
        return schema

    @staticmethod
    def validate_file(
        data_path: str,
        schema_path: str
    ) -> List[str]:
        """Validate single data file against schema.
        
        Args:
            data_path: Path to data file
            schema_path: Path to schema file
            
        Returns:
            List of error messages (empty if valid)
        """
        errors = []
        
        try:
            # Load data
            data_file = Path(data_path)
            if data_file.suffix.lower() == '.yaml' or data_file.suffix.lower() == '.yml':
                with open(data_file, 'r') as f:
                    data = yaml.safe_load(f) or []
            elif data_file.suffix.lower() == '.json':
                import json
                with open(data_file, 'r') as f:
                    data = json.load(f)
            else:
                data = []
            
            # Ensure list
            if not isinstance(data, list):
                data = [data]
            
            # Load schema
            schema = SchemaValidator.load_schema(schema_path)
            validator = Draft202012Validator(schema)
            
            # Validate each item
            for row_num, item in enumerate(data, start=1):
                for error in validator.iter_errors(item):
                    path = '.'.join(str(p) for p in error.absolute_path) or 'root'
                    errors.append(
                        f"{data_path}[row {row_num}].{path}: {error.message}"
                    )
        
        except Exception as e:
            errors.append(f"Error validating {data_path}: {e}")
        
        return errors

    @staticmethod
    def validate_all(schema_map_path: str) -> List[str]:
        """Validate all data files against schema map.
        
        Args:
            schema_map_path: Path to schema_map.yaml
            
        Returns:
            List of all error messages
        """
        all_errors = []
        
        try:
            with open(schema_map_path, 'r') as f:
                schema_map = yaml.safe_load(f) or {}
        except Exception as e:
            return [f"Error loading schema map: {e}"]
        
        # Validate each file
        for data_file, schema_file in schema_map.items():
            data_path = Path("testdata") / "yaml" / data_file
            
            # Try different directories
            if not data_path.exists():
                data_path = Path("testdata") / "json" / data_file
            if not data_path.exists():
                data_path = Path("testdata") / "csv" / data_file
            if not data_path.exists():
                data_path = Path("testdata") / "excel" / data_file
            
            if not data_path.exists():
                all_errors.append(f"Data file not found: {data_file}")
                continue
            
            schema_path = Path("schemas") / schema_file
            if not schema_path.exists():
                all_errors.append(f"Schema file not found: {schema_file}")
                continue
            
            errors = SchemaValidator.validate_file(
                str(data_path),
                str(schema_path)
            )
            all_errors.extend(errors)
        
        return all_errors
