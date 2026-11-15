from scapy.all import *
from base64 import b64decode 
import re


def ExtractFTP(packet):
    payload = packet[Raw].load.decode("utf-8").rstrip()
    if payload[:4] == 'USER':
        print(f"FTP Username: {packet[IP].dst, payload[5:]}")
    elif payload[:4] == 'PASS':
        print(f"FTP Password: {packet[IP].dst, payload[5:]}")

awaitingLogin = []
awaitingPassword = []
# у этого telnet есть проблемы с тем, что добавляются IAC байты, которые автоматически вводятся
# такое мой сервер не умеет обрабатывать.
def ExtractTelnet(packet):
    try:
        payload = packet[Raw].load.decode("utf-8").rstrip()
    except:
        return 
    if packet[TCP].sport == 23: # server is source
        connData = [packet[IP].src, packet[TCP].sport]
        if payload[:5] == "login":
            awaitingLogin.append(connData)
            return
        elif payload[:8] == "Password":
            awaitingPassword.append(connData)
            return
    else: # client is source
        connData = [packet[IP].dst, packet[TCP].dport]
        if connData in awaitingLogin:
            print(packet[IP].dst, payload)
            awaitingLogin.remove(connData)
        elif connData in awaitingPassword:
            print(packet[IP].dst, payload)
            awaitingPassword.remove(connData)

email_regex = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-" \
"Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
unmatched = []

email_regex = r'[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*'
def ExtractSMTP(packet):
    payload = packet[Raw].load.decode("utf-8", errors="ignore").strip()
    if packet[TCP].dport == 25:
        if payload.startswith("MAIL FROM:") or payload.startswith("RCPT TO:"):
            print(f"[SMTP] {packet[IP].src} -> {payload}")
        elif payload.startswith("AUTH LOGIN") or payload == "334 VXNlcm5hbWU6":
            print(f"[SMTP] {packet[IP].src} -> Обнаружена авторизация")
        else:
            try:
                decoded = b64decode(payload).decode("utf-8")
                if decoded.isprintable():
                    print(f"[SMTP] {packet[IP].src} -> {decoded}")
            except:
                pass #


# ну короче эти 2 работают но много шума, поскольку я не писал типо жестких фильтров никаких 
# в этом не сильно много смысла потому что это просто страдания по распарсу и страдания по
# чтению документации
def ExtractPOP3(packet):
    if not (packet.haslayer(IP) and packet.haslayer(TCP) and packet.haslayer(Raw)):
        return
    payload = packet[Raw].load.decode("utf-8", errors = "ignore").strip()
    if packet[TCP].dport == 110:
        if payload.startswith("USER"):
            print(f"POP3 {packet[IP].src, packet[IP].dst} payload: {payload}")
        if payload.startswith("PASS"):
            print(f"POP3 {packet[IP].src, packet[IP].dst} payload: {payload}")


def ExtractIMAP(packet):
    if not (packet.haslayer(IP) and packet.haslayer(TCP) and packet.haslayer(Raw)):
        return
    payload = packet[Raw].load.decode("utf-8", errors = "ignore").strip()
    if packet[TCP].dport == 143:
        if "LOGIN" in payload:
            tag, _ , email, password = payload.split(" ", 3)
            # 3 - ограничение парсинга
            print(email, password)



def call_extract(file_name):
    global awaitingLogin, awaitingPassword
    awaitingLogin.clear()
    awaitingPassword.clear()
    
    print(f"\n--- {file_name} ---")
    packets = rdpcap(file_name)
    
    for packet in packets:
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            tcp = packet[TCP]
            
            if tcp.dport == 21 or tcp.sport == 21:
                ExtractFTP(packet)
            elif tcp.dport == 25 or tcp.sport == 25:
                ExtractSMTP(packet)
            elif tcp.sport == 23 or tcp.dport == 23:
                ExtractTelnet(packet)

for pcap_file in ["telnet.pcapng", "ftp.pcapng", "smtp.pcapng"]:
    call_extract(pcap_file)