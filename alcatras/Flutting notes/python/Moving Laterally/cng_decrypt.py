# cng_decrypt.py — шаг 1: получить расшифрованный AES-ключ через CNG.
#
# Запускается планировщиком от имени SYSTEM, потому что ключ
# "Google Chromekey2" лежит в системном хранилище Windows и обычному
# пользователю не виден.
#
# Что делает:
#   1) читает user_decrypted.hex (результат двух DPAPI-слоёв);
#   2) достаёт оттуда 32 байта зашифрованного AES-ключа;
#   3) просит Windows расшифровать их CNG-ключом "Google Chromekey2";
#   4) пишет результат (32 байта, hex) в cnkey.hex.
from pathlib import Path
import struct
import ctypes

BASE = Path(r"E:\chrome_cookie")

# Служебная обвязка: объявляем типы аргументов функций из ncrypt.dll,
# чтобы ctypes корректно передавал указатели на 64-битной Windows.
# В эти строки вникать не обязательно — это просто "декларации".
ncrypt = ctypes.windll.ncrypt
ncrypt.NCryptOpenStorageProvider.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_wchar_p, ctypes.c_uint]
ncrypt.NCryptOpenStorageProvider.restype = ctypes.c_long
ncrypt.NCryptOpenKey.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p), ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_uint]
ncrypt.NCryptOpenKey.restype = ctypes.c_long
ncrypt.NCryptDecrypt.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint, ctypes.c_void_p, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.c_uint]
ncrypt.NCryptDecrypt.restype = ctypes.c_long
ncrypt.NCryptFreeObject.argtypes = [ctypes.c_void_p]
ncrypt.NCryptFreeObject.restype = ctypes.c_long


def parse_blob(blob: bytes):
    """Разбираем blob из user_decrypted.hex.

    Структура после снятия двух DPAPI-слоёв:
        [4 байта: длина заголовка][заголовок][4 байта: длина данных][1 байт: флаг][данные]

    Для флага 4 "данные" = [encrypted_aes_key 32][iv 12][ciphertext 32][tag 16].
    Сейчас нам нужны только флаг и первые 32 байта (encrypted_aes_key).
    """
    header_len = struct.unpack("<I", blob[:4])[0]
    offset = 4 + header_len + 4
    flag = blob[offset]
    encrypted_aes_key = blob[offset + 1: offset + 1 + 32]
    return flag, encrypted_aes_key


def cng_decrypt(data: bytes, key_name: str) -> bytes:
    """Расшифровываем данные CNG-ключом по имени (нужно быть SYSTEM).

    NCryptDecrypt сам знает padding ключа, поэтому ничего лишнего
    указывать не требуется.
    """
    provider = ctypes.c_void_p()
    if ncrypt.NCryptOpenStorageProvider(ctypes.byref(provider), "Microsoft Software Key Storage Provider", 0) != 0:
        raise RuntimeError("не удалось открыть CNG-провайдер")

    try:
        key = ctypes.c_void_p()
        if ncrypt.NCryptOpenKey(provider, ctypes.byref(key), key_name, 0, 0) != 0:
            raise RuntimeError(f"не удалось открыть ключ {key_name}")

        try:
            # NCryptDecrypt вызываем дважды:
            #   первый раз — чтобы узнать размер результата,
            #   второй раз — собственно расшифровать.
            src = (ctypes.c_ubyte * len(data)).from_buffer_copy(data)
            size = ctypes.c_uint(0)
            rc = ncrypt.NCryptDecrypt(key, src, len(data), None, None, 0, ctypes.byref(size), 0x40)
            if rc != 0:
                raise RuntimeError(f"NCryptDecrypt (размер): {hex(rc & 0xffffffff)}")

            dst = (ctypes.c_ubyte * size.value)()
            rc = ncrypt.NCryptDecrypt(key, src, len(data), None, dst, size.value, ctypes.byref(size), 0x40)
            if rc != 0:
                raise RuntimeError(f"NCryptDecrypt: {hex(rc & 0xffffffff)}")

            return bytes(dst[:size.value])
        finally:
            ncrypt.NCryptFreeObject(key)
    finally:
        ncrypt.NCryptFreeObject(provider)


def main():
    out = BASE / "cnkey.hex"
    try:
        blob = bytes.fromhex((BASE / "user_decrypted.hex").read_text().strip())
        flag, encrypted_aes_key = parse_blob(blob)

        key_name = {3: "Google Chromekey1", 4: "Google Chromekey2"}.get(flag)
        if key_name is None:
            out.write_text(f"ERROR: неизвестный флаг {flag}")
            return

        decrypted = cng_decrypt(encrypted_aes_key, key_name)
        out.write_text(decrypted.hex())
    except Exception as e:
        out.write_text("ERROR: " + str(e))


if __name__ == "__main__":
    main()
