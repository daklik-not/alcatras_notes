# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pycryptodome", "cryptography"
# ]
# ///

import socket 
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from myDH import myDH, recv_exact

host = "127.0.0.1"
port = 1337

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
        # обменялся секретами с помощью самопального класса
        dh_conn = myDH(conn)
        dh_conn.self_keys_init()
        dh_conn.acceptDH()
        dh_conn.sendDH()
        general_secret = dh_conn.get_general_secret()
        print(general_secret)
        nonce_len = recv_exact(conn, 1)[0]
        data_len = recv_exact(conn , 1)[0]
        nonce = recv_exact(conn, nonce_len)
        data = recv_exact(conn , data_len)
        message = AESGCM(general_secret).decrypt(nonce, data, None)
        print(message.decode("utf-8"))





'''


def decrypt(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(data), AES.block_size)

____________________________________

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
'''
