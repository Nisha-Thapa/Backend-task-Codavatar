# app/utils.py
import bcrypt

# Hash the password before storing it
def hash_password(plain_password: str) -> str:
    """
    Hash the plain password using bcrypt and return the hashed password.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Convert bytes to string

# Verify the password by comparing the plain password with the hashed one
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that the plain password matches the hashed password.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
