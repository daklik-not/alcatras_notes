# /// script
# requires-python = ">=3.10"
# dependencies = ["scapy", "cryptography"]
# ///

from pathlib import Path
import os
from DataEncryption import decryptFile

key = b"Spring is coming"


directory = Path(__file__).resolve().parent / "EncryptedFiles"
files = [p for p in directory.rglob("*") if p.is_file()]

for f_name in files:
    decryptFile(f_name, key)