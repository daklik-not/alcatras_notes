# /// script
# requires-python = ">=3.10"
# dependencies = ["scapy"]
# ///

# тип ICMP запроса, а code - более подробное описание
# например тип 3(Destination Unreachable), а code = (0 Net Unreachable)

from collections import Counter
import math
from base64 import b64decode
from scapy.all import *

typecode = { ... }  

def calc_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    n = len(data)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def testData(data):
    entropy = calc_entropy(data)
    if entropy <= 3.3:
        return "dns"
    elif entropy >= 4.5:
        return "encrypted"
    else:
        try:
            encoded = data if isinstance(data, bytes) else data.encode("utf-8")
            encoded += b"=" * ((4 - len(encoded) % 4) % 4)
            decoded = b64decode(encoded, validate=True)
            return decoded.decode("utf-8")
        except Exception:
            return False


def checkData(data):
    res = testData(data)
    if res == "encrypted":
        print(f"[!] Potential encr. data")
    elif res == "dns":
        pass
    elif res:
        print(f"[?] Probably base64 (decoded): {res}")
    else:
        print(f"[-] Entropy is base64-like, but cannot decode: {data!r}")

def testICMP(p):
    t = p[ICMP].type
    c = p[ICMP].code
    if t in typecode:
        if not c in typecode[t]:
            print(f"Anomalous code detected: {c}")
    else:
        print(f"Anomalous type detected {t}")

def processPacket(p):
    if p.haslayer(ICMP):
        testICMP(p)
    elif p.haslayer(TCP):
        if p.haslayer(Raw):
            # это bytes — но после фикса testData выше корректно обрабатывается
            data = p[Raw].load
            checkData(data)

sniff(iface = "lo", prn = processPacket)

