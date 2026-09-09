"""Soft assertions for test validation."""
import logging
from typing import Any, Optional, List

logger = logging.getLogger(__name__)


class SoftAssertions:
    """Soft assertions collect failures without stopping.
    
    All failures are collected and reported at the end via assert_all().
    """

    def __init__(self) -> None:
        """Initialize soft assertions."""
        self.failures: List[str] = []

    def equals(
        self,
        actual: Any,
        expected: Any,
        message: Optional[str] = None
    ) -> None:
        """Soft assert values are equal.
        
        Args:
            actual: Actual value
            expected: Expected value
            message: Optional assertion message
        """
        if actual != expected:
            msg = message or f"Values not equal: {actual} != {expected}"
            self.failures.append(msg)
            logger.warning(f"Soft assertion failed: {msg}")
        else:
            logger.info(f"Soft assertion passed: {actual} == {expected}")

    def contains(
        self,
        haystack: str,
        needle: str,
        message: Optional[str] = None
    ) -> None:
        """Soft assert string contains substring.
        
        Args:
            haystack: String to search in
            needle: Substring to find
            message: Optional assertion message
        """
        if needle not in haystack:
            msg = message or f"'{needle}' not found in '{haystack}'"
            self.failures.append(msg)
            logger.warning(f"Soft assertion failed: {msg}")
        else:
            logger.info(f"Soft assertion passed: '{needle}' found in text")

    def not_empty(
        self,
        value: Any,
        message: Optional[str] = None
    ) -> None:
        """Soft assert value is not empty.
        
        Args:
            value: Value to check
            message: Optional assertion message
        """
        if not value:
            msg = message or f"Value is empty"
            self.failures.append(msg)
            logger.warning(f"Soft assertion failed: {msg}")
        else:
            logger.info(f"Soft assertion passed: value is not empty")

    def greater_than(
        self,
        actual: float,
        expected: float,
        message: Optional[str] = None
    ) -> None:
        """Soft assert value is greater than expected.
        
        Args:
            actual: Actual value
            expected: Expected threshold
            message: Optional assertion message
        """
        if actual <= expected:
            msg = message or f"{actual} is not greater than {expected}"
            self.failures.append(msg)
            logger.warning(f"Soft assertion failed: {msg}")
        else:
            logger.info(f"Soft assertion passed: {actual} > {expected}")

    def assert_all(self) -> None:
        """Assert all collected assertions passed.
        
        Raises:
            AssertionError: If any soft assertion failed
        """
        if self.failures:
            msg = f"{len(self.failures)} assertion(s) failed:\n" + "\n".join(
                f"  - {f}" for f in self.failures
            )
            logger.error(msg)
            raise AssertionError(msg)
        
        logger.info("All soft assertions passed")
