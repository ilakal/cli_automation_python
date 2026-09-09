"""Pytest plugin for collection-time data validation."""
import logging
from pathlib import Path

from framework.validators.schema_validator import SchemaValidator

logger = logging.getLogger(__name__)


class DataValidationPlugin:
    """Pytest plugin for validating test data at collection time.
    
    Runs during pytest_sessionstart to validate all test data files
    against their schemas before any tests execute.
    """

    def validate_all(self, schema_map_path: str) -> list:
        """Validate all test data files.
        
        Args:
            schema_map_path: Path to schema_map.yaml
            
        Returns:
            List of validation error messages
        """
        logger.info("Starting collection-time data validation")
        
        validator = SchemaValidator()
        errors = validator.validate_all(schema_map_path)
        
        if errors:
            logger.error(f"Data validation found {len(errors)} errors:")
            for error in errors:
                logger.error(f"  - {error}")
        else:
            logger.info("All test data validation passed")
        
        return errors
