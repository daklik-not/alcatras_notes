# /// script
# requires-python = ">=3.10"
# dependencies = ["scapy"]
# ///


# короче просто примитивный чекер энтропии в DNS запросах


import math
from scapy.all import *
from base64 import b64decode
from collections import Counter




def calc_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    n = len(data)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def testData(d):
    entropy = calc_entropy(d) 
    if  entropy <= 3.3:
        return "dns"
    elif entropy >= 4.5:
        return "encrypted"
    else:
        try:
            encoded = d.encode("utf-8")
            encoded += b"=" * ((4 - len(encoded) % 4) % 4) 
            decoded = b64decode(encoded, validate = True)
            return decoded.decode("utf-8")
        except:
            return False
    
def processPacket(p):
    if not p.haslayer(IP):
        return 
    
    src = p[IP].src
    dst = p[IP].dst
    
    if p.haslayer(DNS):
        # Проверяем, что это запрос (qr == 0) и что секция вопроса существует (qd is not None)
        # (qr == 1 означает ответ, там qd обычно нет)
        if p[DNS].qr == 0 and p[DNS].qd is not None:
            hostname = p[DNS].qd.qname.decode("utf-8", errors="ignore")
            d = hostname.split(".")
            
            for v in d:
                res = testData(v)
                if res == "encrypted":
                    print(f"[!] Potential encr. data in {src} -> {dst} connection (Label: {v})")
                elif res == "dns":
                    pass 
                elif res:
                    print(f"[?] Probably base64 (decoded): {res}")
                else:
                    print(f"[-] Entropy is base64-like, but cannot decode: {v}")


sniff(prn = processPacket)