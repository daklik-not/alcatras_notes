import time
import logging
from dnslib import A, QTYPE, RR, RCODE, MX, NS, SOA, CNAME, AAAA, TXT
from dnslib.server import DNSServer, BaseResolver

HOST = "0.0.0.0"                 # слушать все интерфейсы
PORT = 8053
DOMAIN = "example.com"


HONEY_SUBDOMAINS = {
    "mail":    ["10.0.0.11", "2001:db8::11"],
    "api":     ["10.0.0.3",  "2001:db8::3"],
    "dev":     ["10.0.0.4",  "2001:db8::4"],
    "staging": ["10.0.0.5",  "2001:db8::5"],
    "admin":   ["10.0.0.6",  "2001:db8::6"],
    "vpn":     ["10.0.0.7",  "2001:db8::7"],
    "ftp":     ["10.0.0.8",  "2001:db8::8"],
    "ns1":     ["10.0.0.9",  "2001:db8::9"],
    "portal":  ["10.0.0.10", "2001:db8::10"],
    "" : ["10.0.0.11", "2001:db8::11"]  # пустой поддомен (корень зоны)
}

SUBDOMAINS = {
    "www":  ["10.0.0.1",  "2001:db8::1"],
    "smtp": ["10.0.0.2",  "2001:db8::2"],
}

log = logging.getLogger("honeypot")
log.setLevel(logging.INFO)
log.addHandler(logging.FileHandler("dns_hits.log"))
log.addHandler(logging.StreamHandler())

class HoneyResolver(BaseResolver):
    def resolve(self, request, handler):
        qname = request.q.qname
        qtype = request.q.qtype
        client = handler.client_address[0] if handler else "?"

        label = str(qname).rstrip(".").lower()
        base = DOMAIN.lower()

        # отрезаем суффикс зоны; чужой домен -> None
        if label == base:
            sub = ""
        elif label.endswith("." + base):
            sub = label[: -len(base) - 1]
        else:
            sub = None

        log.info(f"{client} -> {qname} ({QTYPE[qtype]}) sub={sub!r}")

        reply = request.reply()

        if sub is None:
            reply.header.rcode = RCODE.REFUSED
            return reply                        # NXDOMAIN для чужих доменов

        ip = SUBDOMAINS.get(sub, HONEY_SUBDOMAINS.get(sub))

        if ip is None: # не смогли разрезовать поддомен, возвращаем NXDOMAIN
            reply.header.rcode = RCODE.NXDOMAIN
            return reply


        reply.header.aa = 1
        if qtype in (QTYPE.MX, QTYPE.TXT, QTYPE.NS, QTYPE.SOA):
            if sub != "":
                return reply
        if qtype == QTYPE.CNAME and sub != "www":
            return reply
        
        if qtype == QTYPE.A:
            rtype, rdata = QTYPE.A, A(ip[0])
        elif qtype == QTYPE.AAAA:
            rtype, rdata = QTYPE.AAAA, AAAA(ip[1])
        elif qtype == QTYPE.MX:
            rtype, rdata = QTYPE.MX, MX("mail.example.com", 10)
        elif qtype == QTYPE.TXT:
            rtype, rdata = QTYPE.TXT, TXT(["v=spf1 mx -all"])
        elif qtype == QTYPE.NS:
            rtype, rdata  = QTYPE.NS, NS("ns1.example.com")
        elif qtype == QTYPE.SOA:
            soa = SOA(
                mname="ns1.example.com",
                rname="admin.example.com",
                times=(2024010101, 3600, 600, 86400, 60)
            )
            rtype, rdata = QTYPE.SOA, soa
        elif qtype == QTYPE.CNAME:
            rtype, rdata = QTYPE.CNAME, CNAME("example.com")
        else:
            return reply                         

        reply.add_answer(RR(
            rname=qname,
            rtype=rtype,
            rclass=1,
            ttl=60,
            rdata=rdata,
        ))

        return reply

resolver = HoneyResolver()
server = DNSServer(resolver, port=PORT, address=HOST)
server.start_thread()
log.info(f"listening on {HOST}:{PORT}")

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    pass
finally:
    server.stop()