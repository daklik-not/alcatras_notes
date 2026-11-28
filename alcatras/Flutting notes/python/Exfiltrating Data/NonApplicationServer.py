# /// script
# requires-python = ">=3.10"
# dependencies = ["scapy"]
# ///


from scapy.all import *

seen = set()

def printData(x):
    if x.haslayer(ICMP):
        if x[ICMP].type == 8: # запрос
            key = (x[ICMP].id, x[ICMP].seq, x[ICMP].type)
            if key in seen: return
            seen.add(key)
            d = chr(x[ICMP].code) # получили символ из байта
            print(d, end = "", flush= True)
            

sniff(iface = "lo", filter = "icmp", prn = printData)


