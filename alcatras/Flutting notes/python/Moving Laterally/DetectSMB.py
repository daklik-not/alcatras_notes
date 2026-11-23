# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "scapy"
# ]
# ///

from scapy.all import *
from scapy.layers.smb2 import SMB2_Header, SMB2_Create_Request  # ИСПРАВЛЕНО: SMB2_Create_Request использовался, но не импортировался -> NameError
from scapy.layers.ntlm import NTLM_AUTHENTICATE
import struct, re
from pathlib import Path
from scapy.all import sniff
from scapy.sessions import TCPSession
from collections import defaultdict
pkt_counter = 0
files_guuid = defaultdict(str)
files_messageid = defaultdict(str)
def extractSessionSetup(load):
        ind = load.find(b"NTLMSSP")
        if ind == -1: 
            print("  [Auth] NTLMSSP не найден")
            return

        ntlm_raw = load[ind:]

        if len(ntlm_raw) < 12:
            return

        msg_type = struct.unpack("<I", ntlm_raw[8:12])[0]
        print(f"  [Auth] Найден NTLMSSP, Type: {msg_type}")

        if msg_type != 3:
            return

        try:
            ntlm_pkt = NTLM_AUTHENTICATE(ntlm_raw)

            user = ntlm_pkt.UserName if ntlm_pkt.UserName else "Unknown"
            dom = ntlm_pkt.DomainName if ntlm_pkt.DomainName else "Unknown"
            host = ntlm_pkt.Workstation if ntlm_pkt.Workstation else "Unknown"  # ИСПРАВЛЕНО: в scapy поле называется Workstation, не HostName -> AttributeError

            print(f"  [NTLM] User: {dom}\\{user} | Host: {host}")

            if ntlm_pkt.NtChallengeResponse:
                print(f"  [NTLM] NtChallengeResponse: {bytes(ntlm_pkt.NtChallengeResponse).hex()}")  # ИСПРАВЛЕНО: поле может быть не raw bytes, а StrLenField/объект scapy -> оборачиваем в bytes() перед .hex(), иначе AttributeError в некоторых версиях

        except Exception as e:
            print(f"  [NTLM Parse Error]: {e}")

def extractFileCreation(p):
    if p.haslayer(SMB2_Create_Request): 
        raw_name = b""
        buf = p[SMB2_Create_Request].Buffer
        if isinstance(buf, (list, tuple)): # является ли buf list или tuple
            for item in buf:
                if (
                    isinstance(item, (list, tuple))
                    and item[0] == "Name"
                ):
                    val = item[1]
                    files_messageid[p[SMB2_Header].MID]=val
    elif p.haslayer(SMB2_Create_Response):
        guuid = bytes(p[SMB2_Create_Response].FileId).hex()
        msid = p[SMB2_Header].MID
        filename = files_messageid[msid]
        files_guuid[guuid] = filename
        print(f"File Created: {guuid}:{filename}")

def extractFileWrite(p):
    if not p.haslayer(SMB2_Write_Request): return None
    file_guuid = p[SMB2_Write_Request].FileId
    print(f"Write to file:{file_guuid}")

    
def processPacket(p):
    try:
        global pkt_counter
        if not p.haslayer(SMB2_Header):
            return 

        pkt_counter += 1
        cmd = p[SMB2_Header].Command

        try:
            load = bytes(p[SMB2_Header].payload)
        except Exception:
            return

        if cmd == 5: extractFileCreation(p) 
        if cmd == 1: extractSessionSetup(load)
        if cmd == 9: extractFileWrite(p)
    except Exception as e:
        pass
   

filedir = Path(__file__).resolve().parent
pcap_path = filedir / "smb2.pcap"

print(f"Читаем файл: {pcap_path}")
packets = sniff(offline=str(pcap_path), prn=processPacket)