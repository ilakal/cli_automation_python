"""Database cleanup utilities."""
import logging
from typing import List

from framework.core.database import DatabaseClient

logger = logging.getLogger(__name__)


class DatabaseCleanup:
    """Utilities for cleaning up test data.
    
    Use in test teardown or fixtures to clean up created data.
    """

    def __init__(self, database: DatabaseClient) -> None:
        """Initialize cleanup handler.
        
        Args:
            database: Database client
        """
        self.database = database

    def truncate_table(self, table_name: str) -> None:
        """Truncate table data.
        
        Args:
            table_name: Table to truncate
        """
        logger.info(f"Truncating table: {table_name}")
        self.database.execute(f"TRUNCATE TABLE {table_name}")

    def delete_records(self, table_name: str, where_clause: str) -> int:
        """Delete records matching criteria.
        
        Args:
            table_name: Table to delete from
            where_clause: WHERE clause
            
        Returns:
            Number of rows deleted
        """
        logger.info(f"Deleting from {table_name} where {where_clause}")
        rows_affected = self.database.execute(
            f"DELETE FROM {table_name} WHERE {where_clause}"
        )
        return rows_affected

    def restore_table_state(self, table_name: str, backup_data: List[dict]) -> None:
        """Restore table to backup state.
        
        Args:
            table_name: Table to restore
            backup_data: Backup data to restore
        """
        logger.info(f"Restoring table {table_name}")
        self.truncate_table(table_name)
        
        for record in backup_data:
            columns = list(record.keys())
            placeholders = ', '.join(['%s'] * len(columns))
            columns_str = ', '.join(columns)
            values = tuple(record.values())
            
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            self.database.execute(query, values)
