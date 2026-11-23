# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "scapy",
# ]
# ///

from scapy.all import *
from scapy.layers.http import *
from pathlib import Path
decoy_domains = [".fake.com"]
def processHTTP(p):
    if p.haslayer(HTTPRequest):
        if p[HTTPRequest].Cookie:
            host = p[HTTPRequest].Host.decode()
            decoy = [host.endswith(d) for d in 
decoy_domains]
            if True in decoy:
                print(host, p[IP].src)

file_dir = Path(__file__).resolve().parent
sniff(offline=fr"{file_dir}/smb2.pcap",prn=processHTTP) 