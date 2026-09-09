"""Framework unit tests for assertions."""
import pytest
from framework.assertions.assertions import Assertions
from framework.assertions.soft_assertions import SoftAssertions


class TestAssertions:
    """Test hard assertions."""

    def test_equals_passes(self):
        """Test equals assertion passes."""
        Assertions.equals(1, 1)

    def test_equals_fails(self):
        """Test equals assertion fails."""
        with pytest.raises(AssertionError):
            Assertions.equals(1, 2)

    def test_contains_passes(self):
        """Test contains assertion passes."""
        Assertions.contains('hello world', 'world')

    def test_contains_fails(self):
        """Test contains assertion fails."""
        with pytest.raises(AssertionError):
            Assertions.contains('hello world', 'xyz')

    def test_not_empty_passes(self):
        """Test not_empty assertion passes."""
        Assertions.not_empty('value')
        Assertions.not_empty([1, 2, 3])

    def test_not_empty_fails(self):
        """Test not_empty assertion fails."""
        with pytest.raises(AssertionError):
            Assertions.not_empty('')
        with pytest.raises(AssertionError):
            Assertions.not_empty([])

    def test_greater_than_passes(self):
        """Test greater_than assertion passes."""
        Assertions.greater_than(10, 5)

    def test_greater_than_fails(self):
        """Test greater_than assertion fails."""
        with pytest.raises(AssertionError):
            Assertions.greater_than(5, 10)

    def test_command_success_passes(self):
        """Test command_success assertion passes."""
        Assertions.command_success(0)

    def test_command_success_fails(self):
        """Test command_success assertion fails."""
        with pytest.raises(AssertionError):
            Assertions.command_success(1)


class TestSoftAssertions:
    """Test soft assertions."""

    def test_soft_equals_passes(self):
        """Test soft equals passes."""
        soft = SoftAssertions()
        soft.equals(1, 1)
        soft.assert_all()

    def test_soft_equals_fails(self):
        """Test soft equals collects failure."""
        soft = SoftAssertions()
        soft.equals(1, 2)
        
        with pytest.raises(AssertionError):
            soft.assert_all()

    def test_soft_assertions_collect_multiple_failures(self):
        """Test soft assertions collect multiple failures."""
        soft = SoftAssertions()
        soft.equals(1, 2)
        soft.equals(3, 4)
        soft.contains('abc', 'xyz')
        
        with pytest.raises(AssertionError) as exc_info:
            soft.assert_all()
        
        error_msg = str(exc_info.value)
        assert '3 assertion(s) failed' in error_msg

    def test_soft_assertions_all_pass(self):
        """Test soft assertions pass when all succeed."""
        soft = SoftAssertions()
        soft.equals(1, 1)
        soft.contains('hello', 'ell')
        soft.not_empty('value')
        soft.assert_all()

