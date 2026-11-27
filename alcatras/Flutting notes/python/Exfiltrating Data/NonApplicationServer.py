# /// script
# requires-python = ">=3.10"
# dependencies = ["scapy"]
# ///


from scapy.all import *

def printData(x):
    if x.haslayer(ICMP):
        d = chr(x[ICMP].code) # получили символ из байта
        print(d, end = "", flush= True)

sniff(iface = "lo", filter = "icmp", prn = printData)


