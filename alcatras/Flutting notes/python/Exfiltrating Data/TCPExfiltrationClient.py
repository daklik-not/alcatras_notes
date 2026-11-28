# /// script
# requires-python = ">=3.10"
# dependencies = ["scapy"]
# ///

import socket

import socket
import base64

host = "127.0.0.1"   # было "" — не полагаемся на платформенное поведение
port = 1337
chunk_size = 12

data = "NBelieve it! I'm not gonna run away, and I never go back on my word. That's my ninja way! A person who never gives up is truly strong, and I will become Hokage no matter what! That is my nindo, my ninja way!"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    for i in range(0, len(data), chunk_size):
        data_to_send = data[i : i + chunk_size]
        s.sendall(base64.b64encode(data_to_send.encode("utf-8")))
    s.shutdown(socket.SHUT_WR)  # FIN — чтобы сервер увидел b"" и вышел из цикла

