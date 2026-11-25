# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pycryptodome"
# ]
# ///

import socket 
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

host = "127.0.0.1"
port = 1337

key = b"Sixteen byte key"

def decrypt(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(data), AES.block_size)

def recv_exact(conn, n):
    buf = b""
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("peer closed early")
        buf += chunk
    return buf

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
    # если сервер упадет, сокет останется висеть в TIME_WAIT
    # пока он висит, перезапущенный сокет не может быть использован
    # SO_REUSEADDR говорит о том, что сокен в TIME_WAIT можно повторно использовать
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    with conn:
        iv = recv_exact(conn, 16) 
        # используем самопальную функцию которая гарантирует что будет прочитано до конца
        length = recv_exact(conn, 1)[0]

        data = b""
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            data += chunk

        plaintext = decrypt(data, key, iv).decode("utf-8")[:length]
        print(f"Received: {plaintext}")
