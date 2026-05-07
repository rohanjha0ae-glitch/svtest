import json
import os
import pathlib
import shutil
from typing import cast
from .crypto_utils import generate_salt, encrypt_data, decrypt_data

import sys

# PyInstaller compatibility: store vault.enc next to the executable
if getattr(sys, 'frozen', False):
    # Running as a PyInstaller executable
    APPLICATION_PATH = pathlib.Path(sys.executable).parent
else:
    # Running as a local Python script
    APPLICATION_PATH = pathlib.Path(__file__).parent.parent

VAULT_FILE = str(APPLICATION_PATH / "vault.enc")

class VaultManager:
    def __init__(self, vault_path=VAULT_FILE):
        self.vault_path = vault_path
        self.salt: bytes | None = None
        self.data = []

    def vault_exists(self):
        return os.path.exists(self.vault_path)

    def initialize_vault(self, password):
        """Creates a new vault with an initial empty list."""
        self.salt = generate_salt()
        self.data = []
        self.save_vault(password)

    def load_vault(self, password):
        """Loads and decrypts the vault file."""
        with open(self.vault_path, "rb") as f:
            self.salt = f.read(16)
            encrypted_payload = f.read()
        
        decrypted_json = decrypt_data(encrypted_payload, password, self.salt)
        self.data = json.loads(decrypted_json)
        return self.data

    def save_vault(self, password):
        """Encrypts and saves the current data to the vault file atomically."""
        if self.salt is None:
            raise ValueError("Salt must be set before saving the vault")
        salt = cast(bytes, self.salt)
        json_data = json.dumps(self.data)
        encrypted_payload = encrypt_data(json_data, password, salt)
        
        temp_path = self.vault_path + ".tmp"
        with open(temp_path, "wb") as f:
            f.write(salt)
            f.write(encrypted_payload)
        
        # Atomic replace
        if os.path.exists(self.vault_path):
            backup_path = self.vault_path + ".bak"
            shutil.copy2(self.vault_path, backup_path)
        
        os.replace(temp_path, self.vault_path)

    def add_entry(self, entry):
        self.data.append(entry)

    def update_entry(self, idx, entry):
        """Replaces the entry at the given index."""
        self.data[idx] = entry

    def delete_entry(self, idx):
        """Removes the entry at the given index."""
        self.data.pop(idx)

    def get_entries(self):
        return self.data
