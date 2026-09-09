"""Database automation keywords."""
import logging
from typing import Optional, List, Dict, Any

from framework.core.database import DatabaseClient

logger = logging.getLogger(__name__)


class DatabaseKeywords:
    """Keywords for database operations.
    
    Provides high-level keywords for common database operations:
    - Record counting
    - Record existence checks
    - Query execution
    - Data validation
    """

    def __init__(self, database: DatabaseClient) -> None:
        """Initialize database keywords.
        
        Args:
            database: Connected database client
        """
        self.database = database

    def record_count(self, query: str) -> int:
        """Get count from query result.
        
        Args:
            query: SQL query returning COUNT(*)
            
        Returns:
            Record count
            
        Example:
            >>> count = db_keywords.record_count(
            ...     "SELECT COUNT(*) as count FROM users"
            ... )
        """
        logger.info(f"Executing count query")
        
        rows = self.database.query(query)
        
        if rows:
            # Handle both count() and COUNT(*) as count formats
            count_key = next(
                (k for k in rows[0].keys() if 'count' in k.lower()),
                None
            )
            if count_key:
                count = rows[0][count_key]
            else:
                count = rows[0][list(rows[0].keys())[0]]
        else:
            count = 0
        
        logger.info(f"Record count: {count}")
        return count

    def record_exists(self, query: str) -> bool:
        """Check if record exists.
        
        Args:
            query: SQL query
            
        Returns:
            True if query returns at least one row
            
        Example:
            >>> exists = db_keywords.record_exists(
            ...     "SELECT 1 FROM users WHERE id = 1"
            ... )
        """
        logger.info(f"Checking if record exists")
        
        rows = self.database.query(query)
        exists = len(rows) > 0
        
        logger.info(f"Record exists: {exists}")
        return exists

    def get_records(self, query: str) -> List[Dict[str, Any]]:
        """Get all records from query.
        
        Args:
            query: SQL query
            
        Returns:
            List of records
        """
        logger.info(f"Executing query")
        rows = self.database.query(query)
        logger.info(f"Retrieved {len(rows)} records")
        return rows

    def insert_record(self, table: str, data: Dict[str, Any]) -> int:
        """Insert record into table.
        
        Args:
            table: Table name
            data: Dictionary of column:value pairs
            
        Returns:
            Number of rows affected
        """
        columns = list(data.keys())
        values = list(data.values())
        
        placeholders = ', '.join(['%s'] * len(columns))
        columns_str = ', '.join(columns)
        
        query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
        
        logger.info(f"Inserting record into {table}")
        rows_affected = self.database.execute(query, tuple(values))
        logger.info(f"Rows affected: {rows_affected}")
        
        return rows_affected

    def update_record(self, table: str, data: Dict[str, Any], where: str) -> int:
        """Update records in table.
        
        Args:
            table: Table name
            data: Dictionary of column:value pairs to update
            where: WHERE clause
            
        Returns:
            Number of rows affected
        """
        set_clauses = ', '.join([f"{k} = %s" for k in data.keys()])
        values = tuple(list(data.values()))
        
        query = f"UPDATE {table} SET {set_clauses} WHERE {where}"
        
        logger.info(f"Updating records in {table}")
        rows_affected = self.database.execute(query, values)
        logger.info(f"Rows affected: {rows_affected}")
        
        return rows_affected
