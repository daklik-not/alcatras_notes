Есть активное(взаимодействие со средой) и пассивное - например, поиск в открытых источниках.
Этот код с помощью библиотеки scapy реализует syn scan на основе открытых портов, а также реализует  DNSScan - если на устройстве с IP хост запущен DNS сервер, то он сможет разрезолвить google.com
```
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


Код ниже пытается блокировать подозрительные SYN запросы, основывая на той логике, что если кто-то пытается обратиться к порту, который не является стандартным, то ему просто посылается RST. Но при этом, чтобы обмануть атакующего специально оставляют несколько портов открытыми, чтобы он увидел их

Также мы фактически заново генерируем пакет, восстанавливая мак-адрес получателя, его IP и порты, даже увеличиваем seq_number + 1;
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
```

Пример кода, который перебирает доменные имена по словарю, после чего пытается найти IP связанные с ними, и потом через эти IP с помощью ReverseDNS пытается найти еще поддомены
```
import dns.exception
import dns.resolver
import socket
from collections import defaultdict

RESOLVER =  dns.resolver.Resolver()
RESOLVER.nameservers = ["8.8.8.8"]
RESOLVER.port = 53
RESOLVER.timeout = 1.5
RESOLVER.lifetime = 3.0

domains = defaultdict(set)  # специальный словарь, который защищен от обращения по несуществующуему ключу
visited = set() # просто множество


def ReverseDNS(ip):
    try:
        name, aliases, _ = socket.gethostbyaddr(ip)
        return [name] + list(aliases)
    except (socket.herror, socket.gaierror, socket.timeout, OSError):
        return []

def DNSRequest(domain, depth=0, max_depth=3):
    if domain in visited or depth > max_depth:
        return 
    visited.add(domain)

    try:
        answers = RESOLVER.resolve(domain, "A")
    except (dns.resolver.NXDOMAIN, # домен не существует
            dns.resolver.NoAnswer, # домен существует, но нет записи нужного типа
            dns.resolver.NoNameservers, # не 1 сервер не смог дать ответ
            dns.resolver.LifetimeTimeout, # общее время на весь запрос истекло
            dns.exception.DNSException # общий класс для всех исключений
            ):
        return
    addresses = [a.to_text() for a in answers]
    domains[domain].update(addresses) # метод множества

    for ip in addresses:
        for ptr_name in ReverseDNS(ip):
            domains[ptr_name].add(ip)
            DNSRequest(ptr_name, depth + 1, max_depth)

def HostSearch(base, dictionary, nums):
    # даем домен, и перебираем типовые поддомены из словаря
    for word in dictionary:
        DNSRequest(f"{word}.{base}")
        if nums:
            for i in range(10): # для хостов типо server1.tx_domain
                DNSRequest(f"{word}{i}.{base}")

if __name__ == "__main__":
    with open("dns_search.txt") as f:
        dictionary = f.read().splitlines()

    HostSearch("google.com", dictionary, nums=False)

    for name in sorted(domains):
        print(f"{name} : {sorted(domains[name])}")
```

```
import time
import logging
from dnslib import A, QTYPE, RR
from dnslib.server import DNSServer, BaseResolver

HOST = "0.0.0.0"                 # слушать все интерфейсы
PORT = 8053
DOMAIN = "example.com"
HONEYIP = "10.0.0.0"

SUBDOMAINS = {
    "www":  "10.0.0.1",
    "smtp": "10.0.0.2",
}

log = logging.getLogger("honeypot")
log.setLevel(logging.INFO)
log.addHandler(logging.FileHandler("dns_hits.log"))
log.addHandler(logging.StreamHandler())

class HoneyResolver(BaseResolver):
    def resolve(self, request, handler):
        qname = request.q.qname
        qtype = request.q.qtype
        client = handler.client_address[0] if handler else "?"

        label = str(qname).rstrip(".").lower()
        base = DOMAIN.lower()

        # отрезаем суффикс зоны; чужой домен -> None
        if label == base:
            sub = ""
        elif label.endswith("." + base):
            sub = label[: -len(base) - 1]
        else:
            sub = None

        log.info(f"{client} -> {qname} ({QTYPE[qtype]}) sub={sub!r}")

        reply = request.reply()

        if sub is None:
            return reply                        # NXDOMAIN для чужих доменов

        if qtype != QTYPE.A:
            return reply                        # NODATA для не A

        reply.header.aa = 1
        ip = SUBDOMAINS.get(sub, HONEYIP)
        reply.add_answer(RR(
            rname=qname,
            rtype=QTYPE.A,
            rclass=1,
            ttl=60,
            rdata=A(ip),
        ))
        return reply

resolver = HoneyResolver()
server = DNSServer(resolver, port=PORT, address=HOST)
server.start_thread()
log.info(f"listening on {HOST}:{PORT}")

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    pass
finally:
    server.stop()
```



``