# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

import socket 
HOST, PORT = "127.0.0.1", 23

with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 1 параметр это уровень настроек, есть SOL_SOCKET, SOL_TCP(поведение TCP), IPROTO_IP
    # 2 параметр это сами настройки:
        # man7.org/linux/man-pages/man7/socket.7.html
        # man7.org/linux/man-pages/man7/tcp.7.html
        # man7.org/linux/man-pages/man7/ip.7.html
    # конкретно здесб SO_REUSEADDR позволяет сделать bind на порт, который в TIME_WAIT
    s.bind((HOST, PORT))
    s.listen(1) # 1 - размер очереди ожидающих подключений
    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    # сonn - новый сокет для клиентского соединения
    # addr - кортеж (host, port) клиента
    print(f"Server connection from {addr}")
    with conn:
        conn.sendall(b"login: ")
        user = conn.recv(1024)
        conn.sendall(b"Password: ")
        pw = conn.recv(1024)
        conn.sendall(b"Login incorrect\r\n")
        print(f"Server got user={user!r} password={pw!r}")
        