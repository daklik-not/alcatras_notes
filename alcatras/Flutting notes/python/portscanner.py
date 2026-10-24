from scapy.all import * 

import ipaddress

ports = [25, 80, 53, 443, 445, 8080, 8443]

def SynScan(host):
    ans,unans = sr(
        IP(dst=host) /
        TCP(sport=33333, dport=ports, flags="S")
        , timeout=2, verbose=0)
    