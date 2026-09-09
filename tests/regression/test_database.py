"""Regression tests for database functionality."""
import pytest


@pytest.mark.regression
def test_database_client_initialization(database):
    """Test that database client initializes."""
    assert database is not None
    assert database.host is not None
    assert database.database is not None


@pytest.mark.regression
def test_database_keywords_initialization(database_keywords):
    """Test that database keywords initialize."""
    assert database_keywords is not None

