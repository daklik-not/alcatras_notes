# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "icmplib"
# ]
# ///

from icmplib import ping
import base64
SERVER_IP = "127.0.0.1"  # IP другой машины/VM, не этой системы

payloads = [
    b"Kaori never lies",
    b"Kaori tells the truth",
    b"Kaori was here",
    b"Your lie in April",
    b"Spring is coming",
    b"Can I lie one more time?",
    b"Kaori plays violin",
]

for payload in payloads:
    payload = base64.b64encode(payload)

    result = ping(SERVER_IP, payload=payload, count=4)
    print(result)
    print(result.is_alive, result.packets_sent, result.packets_received)