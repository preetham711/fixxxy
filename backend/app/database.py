"""
Database Connection and Session Management
Handles MySQL connection using mysql-connector-python
"""
import mysql.connector
from mysql.connector import Error as MySQLError, pooling
from contextlib import contextmanager
from typing import Generator, Dict, List, Optional, Any
from app.core.config import settings


class Database:
    """Database connection manager with connection pooling"""
    
    def __init__(self):
        """Initialize database configuration"""
        self.config = {
            'host': settings.MYSQL_HOST,
            'port': settings.MYSQL_PORT,
            'user': settings.MYSQL_USER,
            'password': settings.MYSQL_PASSWORD,
            'database': settings.MYSQL_DATABASE,
            'autocommit': False,
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'raise_on_warnings': False
        }
        
        # Create connection pool
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name="fixxy_pool",
                pool_size=10,
                pool_reset_session=True,
                **self.config
            )
        except MySQLError as e:
            print(f"Error creating connection pool: {e}")
            self.pool = None
    
    def get_connection(self):
        """
        Get a connection from the pool.
        Returns a mysql.connector connection object.
        """
        if self.pool:
            return self.pool.get_connection()
        else:
            return mysql.connector.connect(**self.config)
    
    @contextmanager
    def get_db(self) -> Generator:
        """
        Context manager for database connections.
        Automatically commits on success, rolls back on error, and closes connection.
        
        Usage:
            with db.get_db() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users")
                result = cursor.fetchall()
                cursor.close()
        """
        conn = None
        try:
            conn = self.get_connection()
            yield conn
            conn.commit()
        except MySQLError as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def query(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return all results as list of dictionaries.
        
        Args:
            sql: SQL query string
            params: Query parameters tuple
            
        Returns:
            List of dictionaries representing rows
        """
        with self.get_db() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params)
            result = cursor.fetchall()
            cursor.close()
            return result
    
    def query_one(self, sql: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """
        Execute a SELECT query and return one result as dictionary or None.
        
        Args:
            sql: SQL query string
            params: Query parameters tuple
            
        Returns:
            Dictionary representing the row, or None if not found
        """
        with self.get_db() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params)
            result = cursor.fetchone()
            cursor.close()
            return result
    
    def execute(self, sql: str, params: tuple = ()) -> int:
        """
        Execute an INSERT/UPDATE/DELETE query.
        
        Args:
            sql: SQL query string
            params: Query parameters tuple
            
        Returns:
            Last inserted row ID (for INSERT) or affected rows count
        """
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
    
    def execute_many(self, sql: str, params_list: List[tuple]) -> int:
        """
        Execute multiple INSERT/UPDATE/DELETE queries in batch.
        
        Args:
            sql: SQL query string
            params_list: List of parameter tuples
            
        Returns:
            Number of affected rows
        """
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.executemany(sql, params_list)
            affected = cursor.rowcount
            cursor.close()
            return affected
    
    def test_connection(self) -> bool:
        """
        Test database connection.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self.get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                cursor.close()
            return True
        except MySQLError:
            return False


# Create global database instance
db = Database()


def get_db_connection():
    """
    Dependency for FastAPI routes to get database connection.
    
    Usage:
        @app.get("/users")
        def get_users(conn = Depends(get_db_connection)):
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            cursor.close()
            return users
    """
    conn = db.get_connection()
    try:
        yield conn
    finally:
        conn.close()
