# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "scapy"
# ]
# ///

'''
У меня есть 2 версии, получается книжная и моя
Эта версия лучше тем что она не зависит от версии scapy и по документации просто парсит байты
Хуже тем, что тяжело забивать байты + если порядок поменяется то все сломается

Проблема нового кода в том, что разные версии scapy по разному интерпретирую поля
и еще плохо парсят имя.

Эта версия ЗНАЧИТЕЛЬНО проще чем моя, которая наполовину написана нейронкой
Но вторая более универсальная посколько опирается на распарс Scapy а не на мой распарс
'''
from scapy.all import *
import re,struct
from pathlib import Path

def processPacket(p):
    if not p.haslayer(SMB2_Header):
        return
    cmd = p[SMB2_Header].Command
    if cmd in [5]:
        load = bytes(p[SMB2_Header].payload).decode("utf-16", errors='ignore')
        matches = re.findall("[ -~]*[.][ -~]*", load)
        if matches:
            print("File operation detected: %s" % matches)
    elif cmd == 1:
        load = bytes(p[SMB2_Header].payload)
        try:
            ind = load.index(bytes("NTLMSSP","utf-8"))
        except:
            return
        if ind> -1 and load[ind+8] == 3:
            nameLen = struct.unpack("<h",load[ind+36:ind+38])[0]
            offset = ind+struct.unpack("<I",load[ind+40:ind+44])[0]
            username = load[offset:offset+nameLen].decode("utf-16")
            print("Account access attempt: %s" % username)


dir = Path(__file__).resolve().parent
sniff(offline=f"{dir}/smb2.pcap",prn=processPacket)