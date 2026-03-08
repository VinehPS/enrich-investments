import pytest
from src.utils.crypto import encrypt_data, decrypt_data, get_fernet_key
from src.core.config import settings
from cryptography.fernet import Fernet

def test_fernet_key_generation_or_retrieval():
    key = get_fernet_key()
    assert key is not None
    assert len(key) >= 32

def test_encryption_decryption():
    test_string = "MySuperSecretGeminiKey123"
    
    # Store old key to restore later
    old_key = settings.SECRET_KEY
    
    try:
        # Mocking a valid length secret key for testing
        settings.SECRET_KEY = Fernet.generate_key().decode()
        
        # Test encryption
        encrypted = encrypt_data(test_string)
        assert encrypted != test_string
        assert len(encrypted) > len(test_string)
        
        # Test decryption
        decrypted = decrypt_data(encrypted)
        assert decrypted == test_string
        
    finally:
        settings.SECRET_KEY = old_key

def test_decrypt_invalid_data():
    invalid_data = "not_a_valid_fernet_token"
    result = decrypt_data(invalid_data)
    assert result is None
    
def test_encrypt_empty_string():
    assert encrypt_data("") == ""
    assert decrypt_data("") is None
