"""Assertions for test validation."""
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class Assertions:
    """Hard assertions for test validation.
    
    Assertions fail immediately and stop test execution.
    """

    @staticmethod
    def equals(
        actual: Any,
        expected: Any,
        message: Optional[str] = None
    ) -> None:
        """Assert values are equal.
        
        Args:
            actual: Actual value
            expected: Expected value
            message: Optional assertion message
            
        Raises:
            AssertionError: If values not equal
        """
        if actual != expected:
            msg = message or f"Values not equal: {actual} != {expected}"
            logger.error(msg)
            raise AssertionError(msg)
        logger.info(f"Assertion passed: {actual} == {expected}")

    @staticmethod
    def contains(
        haystack: str,
        needle: str,
        message: Optional[str] = None
    ) -> None:
        """Assert string contains substring.
        
        Args:
            haystack: String to search in
            needle: Substring to find
            message: Optional assertion message
            
        Raises:
            AssertionError: If needle not in haystack
        """
        if needle not in haystack:
            msg = message or f"'{needle}' not found in '{haystack}'"
            logger.error(msg)
            raise AssertionError(msg)
        logger.info(f"Assertion passed: '{needle}' found in text")

    @staticmethod
    def not_empty(
        value: Any,
        message: Optional[str] = None
    ) -> None:
        """Assert value is not empty.
        
        Args:
            value: Value to check
            message: Optional assertion message
            
        Raises:
            AssertionError: If value is empty
        """
        if not value:
            msg = message or f"Value is empty"
            logger.error(msg)
            raise AssertionError(msg)
        logger.info(f"Assertion passed: value is not empty")

    @staticmethod
    def greater_than(
        actual: float,
        expected: float,
        message: Optional[str] = None
    ) -> None:
        """Assert value is greater than expected.
        
        Args:
            actual: Actual value
            expected: Expected threshold
            message: Optional assertion message
            
        Raises:
            AssertionError: If actual <= expected
        """
        if actual <= expected:
            msg = message or f"{actual} is not greater than {expected}"
            logger.error(msg)
            raise AssertionError(msg)
        logger.info(f"Assertion passed: {actual} > {expected}")

    @staticmethod
    def less_than(
        actual: float,
        expected: float,
        message: Optional[str] = None
    ) -> None:
        """Assert value is less than expected.
        
        Args:
            actual: Actual value
            expected: Expected threshold
            message: Optional assertion message
            
        Raises:
            AssertionError: If actual >= expected
        """
        if actual >= expected:
            msg = message or f"{actual} is not less than {expected}"
            logger.error(msg)
            raise AssertionError(msg)
        logger.info(f"Assertion passed: {actual} < {expected}")

    @staticmethod
    def command_success(
        exit_code: int,
        message: Optional[str] = None
    ) -> None:
        """Assert command executed successfully.
        
        Args:
            exit_code: Command exit code
            message: Optional assertion message
            
        Raises:
            AssertionError: If exit_code != 0
        """
        if exit_code != 0:
            msg = message or f"Command failed with exit code {exit_code}"
            logger.error(msg)
            raise AssertionError(msg)
        logger.info(f"Assertion passed: command successful")
