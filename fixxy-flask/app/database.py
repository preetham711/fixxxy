"""
FIXXY Database Utilities
MySQL connection and query helpers
"""
import mysql.connector
from mysql.connector import Error as MySQLError
from app.config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
from contextlib import contextmanager

class Database:
    """Database connection and query utilities"""
    
    @staticmethod
    def get_connection():
        """Create and return a MySQL connection"""
        try:
            conn = mysql.connector.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
                autocommit=False
            )
            return conn
        except MySQLError as e:
            print(f"Database connection error: {e}")
            raise
    
    @staticmethod
    @contextmanager
    def get_cursor(dictionary=True):
        """Context manager for database cursor"""
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=dictionary)
        try:
            yield conn, cursor
        except Exception as e:
            conn.rollback()
            raise
        else:
            conn.commit()
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def query(sql, params=()):
        """Execute a SELECT query and return all results"""
        with Database.get_cursor() as (conn, cursor):
            cursor.execute(sql, params)
            return cursor.fetchall()
    
    @staticmethod
    def query_one(sql, params=()):
        """Execute a SELECT query and return one result"""
        with Database.get_cursor() as (conn, cursor):
            cursor.execute(sql, params)
            return cursor.fetchone()
    
    @staticmethod
    def execute(sql, params=()):
        """Execute an INSERT/UPDATE/DELETE query"""
        with Database.get_cursor() as (conn, cursor):
            cursor.execute(sql, params)
            return cursor.lastrowid
    
    @staticmethod
    def execute_many(sql, params_list):
        """Execute multiple INSERT/UPDATE/DELETE queries"""
        with Database.get_cursor() as (conn, cursor):
            cursor.executemany(sql, params_list)
            return cursor.rowcount
    
    @staticmethod
    def get_setting(key, default=""):
        """Get a setting value by key"""
        row = Database.query_one("SELECT `value` FROM settings WHERE `key`=%s", (key,))
        return row["value"] if row else default
    
    @staticmethod
    def set_setting(key, value):
        """Set or update a setting value"""
        Database.execute(
            "INSERT INTO settings(`key`,`value`) VALUES(%s,%s) "
            "ON DUPLICATE KEY UPDATE `value`=VALUES(`value`)",
            (key, str(value))
        )

# Helper functions for common queries
def get_all_products(category=None, search=None, exclude_water_wash=False):
    """Get all products with optional filtering"""
    sql = "SELECT * FROM products WHERE active=1"
    params = []
    
    if exclude_water_wash:
        sql += " AND category != 'Water Wash'"
    
    if category and category != "All Categories":
        sql += " AND category=%s"
        params.append(category)
    
    if search:
        sql += " AND (name LIKE %s OR category LIKE %s OR description LIKE %s)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term, search_term])
    
    sql += " ORDER BY category, name"
    return Database.query(sql, tuple(params))

def get_product_by_id(product_id):
    """Get a single product by ID"""
    return Database.query_one("SELECT * FROM products WHERE id=%s", (product_id,))

def get_all_categories():
    """Get all unique product categories"""
    results = Database.query("SELECT DISTINCT category FROM products WHERE active=1 ORDER BY category")
    return [row["category"] for row in results]

def get_active_coupons():
    """Get all active coupons"""
    return Database.query("SELECT * FROM coupons WHERE active=1 ORDER BY code")

def get_coupon(code):
    """Get a coupon by code"""
    return Database.query_one("SELECT * FROM coupons WHERE UPPER(code)=%s AND active=1", (code.upper(),))

def get_user_by_username(username):
    """Get a user by username"""
    return Database.query_one("SELECT * FROM users WHERE LOWER(username)=LOWER(%s)", (username,))

def get_user_by_id(user_id):
    """Get a user by ID"""
    return Database.query_one("SELECT * FROM users WHERE id=%s", (user_id,))

def get_user_vehicles(user_id):
    """Get all vehicles for a user"""
    return Database.query("SELECT * FROM vehicles WHERE user_id=%s ORDER BY created_at DESC", (user_id,))

def get_user_orders(user_id, limit=None):
    """Get orders for a user"""
    sql = "SELECT * FROM orders WHERE user_id=%s ORDER BY created_at DESC"
    if limit:
        sql += f" LIMIT {limit}"
    return Database.query(sql, (user_id,))

def get_order_by_id(order_id):
    """Get an order by ID"""
    return Database.query_one("SELECT * FROM orders WHERE id=%s", (order_id,))

def get_order_items(order_id):
    """Get all items for an order"""
    return Database.query("SELECT * FROM order_items WHERE order_id=%s", (order_id,))

def get_all_orders(limit=None):
    """Get all orders (admin)"""
    sql = "SELECT * FROM orders ORDER BY created_at DESC"
    if limit:
        sql += f" LIMIT {limit}"
    return Database.query(sql)

def get_low_stock_products(threshold=10):
    """Get products with low stock"""
    return Database.query(
        "SELECT * FROM products WHERE category != 'Water Wash' AND stock < %s AND active=1 ORDER BY stock",
        (threshold,)
    )

def get_product_stats():
    """Get product statistics"""
    stats = {}
    stats['total_products'] = Database.query_one(
        "SELECT COUNT(*) as count FROM products WHERE category != 'Water Wash' AND active=1"
    )['count']
    stats['total_stock'] = Database.query_one(
        "SELECT COALESCE(SUM(stock), 0) as total FROM products WHERE category != 'Water Wash' AND active=1"
    )['total']
    stats['low_stock_count'] = Database.query_one(
        "SELECT COUNT(*) as count FROM products WHERE category != 'Water Wash' AND stock < 10 AND active=1"
    )['count']
    stats['total_services'] = Database.query_one(
        "SELECT COUNT(*) as count FROM products WHERE category = 'Water Wash' AND active=1"
    )['count']
    return stats

def get_order_stats():
    """Get order statistics"""
    stats = {}
    stats['total_orders'] = Database.query_one("SELECT COUNT(*) as count FROM orders")['count']
    stats['total_revenue'] = Database.query_one(
        "SELECT COALESCE(SUM(grand_total), 0) as total FROM orders"
    )['total']
    stats['total_customers'] = Database.query_one(
        "SELECT COUNT(*) as count FROM users WHERE role='customer'"
    )['count']
    return stats
