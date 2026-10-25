"""
Generate password hash for FIXXY
Use this to create secure password hashes for users
"""
import hashlib
import secrets

def hash_password(password):
    """Hash a password using PBKDF2-SHA256"""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 180_000)
    return salt.hex() + "$" + digest.hex()

if __name__ == "__main__":
    # Generate hash for admin123
    admin_hash = hash_password("admin123")
    print("Password hash for 'admin123':")
    print(admin_hash)
    print("\nUse this hash in the database schema or when creating admin users.")
