"""
FIXXY Database Setup Script
Creates and initializes the MySQL database with all required tables and default data
"""
import mysql.connector
from mysql.connector import Error as MySQLError
import hashlib
import secrets
from datetime import datetime

# MySQL Configuration
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"  # Change this to your MySQL password
MYSQL_DATABASE = "fixxy_store"

def hash_password(password):
    """Hash a password using PBKDF2-SHA256"""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 180_000)
    return salt.hex() + "$" + digest.hex()

def create_database():
    """Create the fixxy_store database"""
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        cursor = conn.cursor()
        
        # Drop and create database
        cursor.execute(f"DROP DATABASE IF EXISTS {MYSQL_DATABASE}")
        cursor.execute(f"CREATE DATABASE {MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✓ Database '{MYSQL_DATABASE}' created successfully")
        
        cursor.close()
        conn.close()
        return True
    except MySQLError as e:
        print(f"✗ Error creating database: {e}")
        return False

def setup_tables():
    """Create all tables and insert default data"""
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        cursor = conn.cursor()
        
        # Read and execute schema
        print("\n→ Creating tables...")
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
            
        # Split into individual statements and execute
        statements = [s.strip() for s in sql_script.split(';') if s.strip() and not s.strip().startswith('--')]
        
        for statement in statements:
            if statement.strip():
                # Skip database creation commands (already done)
                if 'DROP DATABASE' in statement or 'CREATE DATABASE' in statement or statement.strip() == 'USE fixxy_store':
                    continue
                    
                # Replace the admin user insert with properly hashed password
                if 'INSERT INTO users' in statement and 'admin' in statement:
                    admin_hash = hash_password("admin123")
                    cursor.execute("""
                        INSERT INTO users (username, password_hash, full_name, role, phone, address, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, ('admin', admin_hash, 'FIXXY Administrator', 'admin', '1234567890', 'Admin Office', datetime.now()))
                    print("  ✓ Admin user created (username: admin, password: admin123)")
                else:
                    try:
                        cursor.execute(statement)
                    except MySQLError as e:
                        if "already exists" not in str(e):
                            print(f"  Warning: {e}")
        
        conn.commit()
        print("✓ All tables created successfully")
        
        # Verify data
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        print(f"✓ {product_count} products loaded")
        
        cursor.execute("SELECT COUNT(*) FROM coupons")
        coupon_count = cursor.fetchone()[0]
        print(f"✓ {coupon_count} coupons loaded")
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
        admin_count = cursor.fetchone()[0]
        print(f"✓ {admin_count} admin user(s) created")
        
        cursor.close()
        conn.close()
        return True
        
    except MySQLError as e:
        print(f"✗ Error setting up tables: {e}")
        return False
    except FileNotFoundError:
        print("✗ Error: database/schema.sql not found")
        return False

def main():
    """Main setup function"""
    print("=" * 70)
    print("FIXXY Database Setup")
    print("=" * 70)
    print(f"\nMySQL Configuration:")
    print(f"  Host: {MYSQL_HOST}:{MYSQL_PORT}")
    print(f"  User: {MYSQL_USER}")
    print(f"  Database: {MYSQL_DATABASE}")
    print("\n" + "=" * 70)
    
    # Create database
    if not create_database():
        print("\n✗ Database setup failed!")
        return
    
    # Setup tables
    if not setup_tables():
        print("\n✗ Table setup failed!")
        return
    
    print("\n" + "=" * 70)
    print("✓ Database setup completed successfully!")
    print("=" * 70)
    print("\nDefault Admin Login:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nYou can now run the application:")
    print("  python run.py")
    print("=" * 70)

if __name__ == "__main__":
    main()
