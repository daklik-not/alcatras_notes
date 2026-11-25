# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "scapy"
# ]
# ///

import socket
import base64
from scapy.all import *

host = "127.0.0.1"

with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as s:
    s.bind(("127.0.0.1", 0))
    while True:
        # recvfrom читает полностью IP пакет 
        data, addr = s.recvfrom(65535) # addr - кортеж (ip_источника, port(здесь всегда 0))
        IP_protocol_type = data[9]
        
        if IP_protocol_type != 1: # раньше были просто SOCK_RAW, но я оставил на всякий проверку
            print("Not ICMP packet...")
            continue

        IP_f_byte = data[0]
        IHL = (IP_f_byte & 0x0F) * 4  
        # то есть извлекаем 4 бита из 1 байта и получаем длину IP заголовков
        # потом что извлеченное число это колво 4 байтовых слов, а не байт

        total_length = (data[2] << 8) | data[3] # value = старший_байт * 256 + младший_бай
        icmp_payload = data[IHL+8:total_length] # получили icmp payload
        icmp_payload = base64.b64decode(icmp_payload)
        print(icmp_payload.decode())
