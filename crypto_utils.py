import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITERATIONS = 100000

def generate_salt():
    return os.urandom(16)

def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a 32-byte key from password and salt for Fernet."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_data(data: str, password: str, salt: bytes) -> bytes:
    """Encrypts string data using PBKDF2 and Fernet."""
    key = derive_key(password, salt)
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data: bytes, password: str, salt: bytes) -> str:
    """Decrypts bytes data using PBKDF2 and Fernet."""
    key = derive_key(password, salt)
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()
