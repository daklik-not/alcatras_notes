from scapy.all import *

import ipaddress
ports = [25,80,53,443,445,8080,8443]

def SynScan(host):
    ans,unans = sr(
        scapy.all.IP(dst=host)/ # / - наложение слоев. это перегруженный оператор, который возвращает инкапсулированные пакеты
        scapy.all.TCP(sport=33333,dport=ports,flags="S")
        ,timeout=2,verbose=0)
    print(f'Open ports at {host}')
    for (s, r) in ans:
        if s[TCP].dport == r[TCP].sport and r[TCP].flags=="SA":
            print(s[TCP].dport)
            
def DNSScan(host):
    ans, unans = sr (
        IP(dst=host)/
        UDP(dport=53)/
        DNS(rd=1, qd=DNSQR(qname="google.com"))
        # rd=1 - сходи узнай, если не знаешь
        # кроме qd(question) есть еще ns(спроси у авторитетных серверов)
        , timeout=2, verbose=0)
    if ans and ans[UDP]:
        print(f'DNS Server at {host}')
        
host = input("Enter IP Address: ")
try:
    ipaddress.ip_address(host)
except:
    print("Invalid address")
    exit(-1)

SynScan(host)
DNSScan(host)
```

from scapy.all import *

ip = "172.26.32.1"
ports = [53, 80]
honeys = [8080,8443]

blocked = []

def analyzePackets(p):
    global blocked # в питоне надо явно указывать обращение к глобальным переменнм
    if p.haslayer(IP):
        response = (
            Ether(src=p[Ether].dst, dst=p[Ether].src)/\
            IP(src=p[IP].dst, dst=p[IP].src)/\
            TCP(sport=p[TCP].dport, dport=p[TCP].sport, ack=p[TCP].seq+1)
        )
        source = p[IP].src
    else:
        response = (
            Ether(src=p[Ether].dst) /
            IPv6(src=p[IPv6].dst, dst=p[IPv6].src) /
            TCP(sport=p[TCP].dport, dport=p[TCP].sport, ack=p[TCP].seq + 1)
        )
        source = p[IPv6].src
    if p[TCP].flags != "S":
        return
    port = p[TCP].dport
    if source in blocked:
        if port in ports:
            response[TCP].flags = "RA"
            print("Sending Reset")
        elif port in honeys:
            response[TCP].flags = "SA"
        else:
            return
        sendp(response, verbose = False)
    else:
        if port not in ports:
            blocked += [source]
            if port in honeys:
                response[TCP].flags = "SA"
                sendp(response, verbose = False)

f = "dst host "+ip+" and tcp"
sniff(filter=f, prn=analyzePackets)