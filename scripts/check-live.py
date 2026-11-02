#!/usr/bin/env python3
"""Verifikasi situs setelah deploy. Pakai: python3 scripts/check-live.py kaloriku.id"""
import sys
import urllib.request
import urllib.error
import ssl

HOST = sys.argv[1] if len(sys.argv) > 1 else "kaloriku.id"
BASE = f"https://{HOST}"
CTX = ssl.create_default_context()

CHECKS = [
    ("/", 200),
    ("/en/", 200),
    ("/css/style.css", 200),
    ("/assets/img/screen-home.webp", 200),
    ("/assets/img/og.jpg", 200),
    ("/robots.txt", 200),
    ("/sitemap.xml", 200),
    ("/app-ads.txt", 200),
    ("/halaman-tidak-ada", 404),
]


def fetch(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "kaloriku-check/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20, context=CTX) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers)
    except Exception as e:
        return None, str(e).encode(), {}


ok = True
print(f"== {BASE}")
for path, want in CHECKS:
    status, body, headers = fetch(path)
    mark = "OK " if status == want else "!! "
    if status != want:
        ok = False
    extra = ""
    if path == "/app-ads.txt" and status == 200:
        extra = f" | {body.decode(errors='replace').strip()[:60]}"
    if path == "/robots.txt" and status == 200:
        extra = " | " + " ".join(body.decode(errors="replace").split())[:90]
    print(f"{mark}{status} (harap {want}) {path}{extra}")

status, body, headers = fetch("/")
html = body.decode(errors="replace")
head = html.split("</head>")[0]
for needle, label in [
    (f'<link rel="canonical" href="{BASE}/"', "canonical"),
    (f'hreflang="en" href="{BASE}/en/"', "hreflang en"),
    (f'"url": "{BASE}/"', "JSON-LD url"),
    ("faq-schema", "FAQ schema"),
    ("max-image-preview:large", "robots meta"),
]:
    found = needle in html
    ok = ok and found
    print(("OK " if found else "!! ") + f"{label}: {'ada' if found else 'TIDAK ADA'}")

status, body, _ = fetch("/sitemap.xml")
sm = body.decode(errors="replace")
print(("OK " if "<urlset" in sm else "!! ") + f"sitemap: {'valid' if '<urlset' in sm else 'tidak valid'}")

print("\nHASIL:", "SEMUA LULUS" if ok else "ADA YANG PERLU DIPERBAIKI")
sys.exit(0 if ok else 1)
