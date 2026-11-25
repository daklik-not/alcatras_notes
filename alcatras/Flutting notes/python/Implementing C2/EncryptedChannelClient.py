# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pycryptodome", "cryptography"
# ]
# ///

import socket, os
from myDH import myDH, recv_exact
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

host = "127.0.0.1"
port = 1337

key = b"Sixteen byte key" # строка длиной 16, в utf-8 16 байт

message = "Kaori never lies"

def recv_exact(conn, n):
    buf = b""
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("peer closed early")
        buf += chunk
    return buf

# AF_INET - IPv4 адреса
# SOCK_STREAM - потоковый(TCP) сокет

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # обменялся секретами с помощью самопального класса
    s.connect((host, port))
    dh_conn = myDH(s)
    dh_conn.self_keys_init()
    dh_conn.sendDH()
    dh_conn.acceptDH()
    general_secret = dh_conn.get_general_secret()
    print(general_secret)

    nonce = os.urandom(12)
    # AESGCM - шифрование + проверка данных
    # последний параметр это AAD
    # он находится в сети в открытом виде, при этом его смысл в том, что
    # кроме шифротекста передается еще Tag, в вычислении которого участвует AAD
    # если AAD поменять то Tag будет неверный -> то Tag не расшифруется просто
    ct = AESGCM(general_secret).encrypt(nonce, message.encode("utf-8"), None)
    nonce_len = 12
    packet = nonce_len.to_bytes(1,"big") + len(ct).to_bytes(1, "big") + nonce + ct
    s.send(packet)
    print("Packet sent....")

   
'''
Старый код с AES
def encrypt(data: str , key: bytes , iv: bytes) -> bytes:
    data_bytes = data.encode("utf-8")

    # если делать ручками то так, но не работает не с ascii буквамим
    # data += " "*(16 - len(data) % 16)
    # короче мы берем остаток от данных и просто дописываем его в конец
    # это нужно поскольку AES это блочный шифр -> общая длина должна быть кратна
    # размеру блока

    padded = pad(data_bytes, AES.block_size) # автоматически
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # AES.MODE_CBD - режим сцепления блоков
    # первый блок смешивается (xor) с IV и только потом шифруется
    # второй смешивается (xor) с результатом первого блока и потом шифруется

    return cipher.encrypt(padded)
    # собственно шифрование после превращения в байты с поомщью кодировки


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        iv = os.urandom(16)
        encrypted = encrypt(message, key, iv)
        # склеиваем всё в один буфер и шлём одним sendall — так разметку
        # на приёмнике невозможно «сдвинуть»
        packet = iv + len(message).to_bytes(1, "big") + encrypted
        print(f"Sending: {encrypted.hex()}")
        s.sendall(packet)
'''