from cryptography.fernet import Fernet

from src.core.config import settings


def get_fernet_key() -> str:
    """Gets the secret key or generates a new one if not available yet."""
    if not settings.SECRET_KEY or len(settings.SECRET_KEY) < 32:
        # Just a fallback if local environment isn't properly set up for fernet
        # production should STRICTLY use a valid FERNET KEY in environments
        key = Fernet.generate_key()
        return key.decode()
    return settings.SECRET_KEY


def encrypt_data(data: str) -> str:
    if not data:
        return ""
    f = Fernet(settings.SECRET_KEY.encode())
    encrypted = f.encrypt(data.encode())
    return encrypted.decode()


def decrypt_data(encrypted_data: str) -> str | None:
    if not encrypted_data:
        return None
    try:
        f = Fernet(settings.SECRET_KEY.encode())
        decrypted = f.decrypt(encrypted_data.encode())
        return decrypted.decode()
    except Exception:
        # Returns None instead of crashing if key rotated or corrupted
        return None
