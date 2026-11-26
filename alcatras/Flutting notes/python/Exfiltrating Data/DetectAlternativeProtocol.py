# /// script
# requires-python = ">=3.10"
# dependencies = ["scapy"]
# ///


# короче просто примитивный чекер энтропии в DNS запросах

from scapy.all import *
from basey64 import b64decode
from pandas import Series
from scipy.stats import entropy
from collections import Counter

threshold = 100

def calc_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    n = len(data)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def testData(d):
    if calc_entropy(d) > threshold:
        return "ecnrypted"
    try:
        decoded = b64decode(d)
        return decoded
    except:
        return False
    
def processPacket(p):
    if p.haslayer(IP):
        src = p[IP].src
        dst = p[IP].dst
    else:
        return 
    
    if p.haslayer(DNS):
        hostname = p[DNS].qd.qname.decode("utf-8")
        d = hostname.split(".")
        for v in d :
            res = testData(v)
            if res == "ecnrypted":
                print(f"Potential encr. data in {src, dst} connection")
            elif res:
                print("Typical DNS packet")

sniff(prn = processPacket)