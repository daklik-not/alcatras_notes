# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pycryptodome"
# ]
# ///
import socket, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
host = "127.0.0.1"
port = 1337

key = b"Sixteen byte key" # строка длиной 16, в utf-8 16 байт


def encrypt(data: str , key: bytes , iv: bytes) -> bytes:
    data_bytes = data.encode("utf-8")
    '''
    # если делать ручками то так, но не работает не с ascii буквамим
    # data += " "*(16 - len(data) % 16)
    # короче мы берем остаток от данных и просто дописываем его в конец
    # это нужно поскольку AES это блочный шифр -> общая длина должна быть кратна
    # размеру блока
    '''
    padded = pad(data_bytes, AES.block_size) # автоматически
    cipher = AES.new(key, AES.MODE_CBC, iv) 
    '''
    # AES.MODE_CBD - режим сцепления блоков
    # первый блок смешивается (xor) с IV и только потом шифруется
    # второй смешивается (xor) с результатом первого блока и потом шифруется
    '''
    return cipher.encrypt(padded)
    # собственно шифрование после превращения в байты с поомщью кодировки

message = "Kaori"

# AF_INET - IPv4 адреса
# SOCK_STREAM - потоковый(TCP) сокет
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    iv = os.urandom(16)
    encrypted = encrypt(message, key, iv)
    # склеиваем всё в один буфер и шлём одним sendall — так разметку
    # на приёмнике невозможно «сдвинуть»
    packet = iv + len(message).to_bytes(1, "big") + encrypted
    print(f"Sending: {encrypted.hex()}")
    s.sendall(packet)
    