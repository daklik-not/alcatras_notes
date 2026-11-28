# /// script
# requires-python = ">=3.10"
# dependencies = ["scapy"]
# ///

import socket
import codecs
import base64 

dec = codecs.getincrementaldecoder("utf-8")()
port = 1337
host = ""
chunk_size = 13

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
    s.bind((host, port))
    s.listen()

    conn, addr = s.accept()
    with conn:
        final_data = []
        while True:  
            data = conn.recv(65536) 
            # как только на буфере что то появится он вернет данные
            if not data:
                break # пришел FIN
            final_data.append(dec.decode(data))
    rcv_message = "".join(final_data)
    rcv_message += "=" * ((4 - len(rcv_message) % 4) % 4)
    print(base64.b64decode(rcv_message).decode("utf-8"))
