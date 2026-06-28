import bcrypt
import hashlib


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with SHA-256 pre-hashing.
    Handles passwords of ANY length.
    """
    # Pre-hash with SHA-256 to handle any length password
    pre_hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    # Hash with bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pre_hashed.encode('utf-8'), salt)
    
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its bcrypt hash.
    """
    # Pre-hash the plain password the same way
    pre_hashed = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    
    # Verify with bcrypt
    return bcrypt.checkpw(pre_hashed.encode('utf-8'), hashed_password.encode('utf-8'))