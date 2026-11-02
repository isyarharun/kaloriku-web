import socket
import sys

SERVERS = {
    "com": "whois.verisign-grs.com",
    "app": "whois.nic.google",
    "id": "whois.id",
    "my.id": "whois.id",
    "web.id": "whois.id",
}


def query(domain: str, server: str) -> str:
    s = socket.create_connection((server, 43), timeout=15)
    s.sendall((domain + "\r\n").encode())
    chunks = []
    while True:
        data = s.recv(4096)
        if not data:
            break
        chunks.append(data)
    s.close()
    return b"".join(chunks).decode("utf-8", "replace")


for domain in sys.argv[1:]:
    tld = domain.split(".", 1)[1].lower()
    server = SERVERS.get(tld) or SERVERS.get(tld.split(".")[-1], "whois.iana.org")
    try:
        text = query(domain, server)
    except Exception as e:
        print(f"{domain:22s} ERROR {e}")
        continue
    low = text.lower()
    free = any(k in low for k in ["no match", "not found", "no data found", "domain not found", "available"])
    status = "TERSEDIA?" if free else "TERPAKAI"
    print("=" * 60)
    print(f"{domain:22s} {status}  (via {server})")
    for line in text.splitlines():
        if any(k in line.lower() for k in ["domain name", "registrar", "status", "expir", "created", "no match", "not found"]):
            print("   ", line.strip()[:110])
