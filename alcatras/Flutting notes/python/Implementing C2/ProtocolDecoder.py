# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "scapy"
# ]
# ///

from scapy.all import *
from scapy.layers.http import *
from base64 import b64decode
from pathlib import Path
import re

b64regex = r"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{8,}={0,2}(?![A-Za-z0-9+/=])"

def extractData(data):
    data = data.decode("utf-8")
    data = data.strip()
    #print(data)
    matches = re.findall(b64regex, data) # нашли все похожее на b64
    for match in matches:
        if len(match) == 0:
            continue
        try:
            if not len(match) % 4 == 0:
                # типо если 4 - 4 % 4, то будет 4 поэтому еще раз делаем взятие
                padnum = (4 - len(match) % 4) % 4 
                match += b"=" * padnum
            decoded = b64decode(match, validate=True).decode("utf-8")
            print(f"Probable base64: {decoded}")
            if len(decoded) > 5 and decoded.isprintable():
                print(f"Decoded {decoded}")
        except:
            print(f"Cannot decode: {match}")
            continue

def extractHTTP(p):
    fields = None
    if p.haslayer(HTTPRequest):
        fields = p[HTTPRequest].fields
    else:
        fields = p[HTTPResponse].fields
    #print(fields.keys())
    for f in fields:
        data = fields[f] # извлекли поле по ключу
        #print(data)
        if isinstance(data, bytes): # если это строка
            extractData(data)
        elif isinstance(data, dict): # словарь
            for d in data:
                extractData(data[d])
        elif isinstance(data,list) or isinstance(data, tuple): # список или кортеж
            for d in data:
                extractData(d)

def extractICMP(p):
    if p.haslayer(Raw):
        data = p[Raw].load
        decoded_data =  data.decode()
        print(b64decode(decoded_data))

def analyzePackets(p):
    if p.haslayer(HTTPRequest) or p.haslayer(HTTPResponse):
        # p.show() - подробно выводит все пакеты
        extractHTTP(p)
    elif p.haslayer(ICMP):
        extractICMP(p)

        
sniff(iface="lo", prn=analyzePackets) 

# sudo /home/daklik_not/.local/bin/uv run Implementing\ C2/ProtocolDecoder.py 