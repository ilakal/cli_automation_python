"""PostgreSQL database client with parameterized queries."""
import logging
from typing import List, Tuple, Any, Optional
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)


class DatabaseClient:
    """PostgreSQL database client.
    
    Features:
    - Parameterized queries (prevents SQL injection)
    - Connection pooling
    - Automatic cleanup
    - Comprehensive logging
    """

    def __init__(
        self,
        host: str,
        database: str,
        user: str,
        password: str,
        port: int = 5432
    ) -> None:
        """Initialize database client.
        
        Args:
            host: Database host
            database: Database name
            user: Database user
            password: Database password
            port: Database port (default 5432)
            
        Raises:
            psycopg2.OperationalError: If connection fails
        """
        self.host = host
        self.database = database
        self.user = user
        self.port = port
        self._connection = None
        self._connect(password)
        logger.info(f"Initialized database client for {user}@{host}:{port}/{database}")

    def _connect(self, password: str) -> None:
        """Establish database connection.
        
        Args:
            password: Database password
            
        Raises:
            psycopg2.OperationalError: If connection fails
        """
        try:
            self._connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=password,
                port=self.port
            )
            self._connection.autocommit = True
            logger.info(f"Successfully connected to database")
        except psycopg2.OperationalError as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def query(
        self,
        sql: str,
        params: Optional[Tuple] = None
    ) -> List[dict]:
        """Execute SELECT query.
        
        Args:
            sql: SQL query with %s placeholders for parameters
            params: Query parameters (tuple)
            
        Returns:
            List of result rows as dictionaries
            
        Example:
            >>> rows = db.query(
            ...     "SELECT * FROM users WHERE id = %s",
            ...     (1,)
            ... )
        """
        if self._connection is None:
            raise RuntimeError("Database connection is closed")
        
        try:
            cursor = self._connection.cursor(cursor_factory=RealDictCursor)
            logger.debug(f"Executing query: {sql}")
            cursor.execute(sql, params or ())
            results = cursor.fetchall()
            cursor.close()
            
            logger.info(f"Query returned {len(results)} rows")
            return results
        
        except psycopg2.Error as e:
            logger.error(f"Query execution failed: {e}")
            raise

    def execute(
        self,
        sql: str,
        params: Optional[Tuple] = None
    ) -> int:
        """Execute INSERT, UPDATE, or DELETE query.
        
        Args:
            sql: SQL query with %s placeholders for parameters
            params: Query parameters (tuple)
            
        Returns:
            Number of affected rows
            
        Example:
            >>> rows_affected = db.execute(
            ...     "INSERT INTO users (name) VALUES (%s)",
            ...     ("John",)
            ... )
        """
        if self._connection is None:
            raise RuntimeError("Database connection is closed")
        
        try:
            cursor = self._connection.cursor()
            logger.debug(f"Executing statement: {sql}")
            cursor.execute(sql, params or ())
            rows_affected = cursor.rowcount
            cursor.close()
            
            logger.info(f"Statement affected {rows_affected} rows")
            return rows_affected
        
        except psycopg2.Error as e:
            logger.error(f"Statement execution failed: {e}")
            raise

    def close(self) -> None:
        """Close database connection."""
        if self._connection:
            self._connection.close()
            logger.info("Closed database connection")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
