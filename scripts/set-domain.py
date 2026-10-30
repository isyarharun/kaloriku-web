#!/usr/bin/env python3
"""Suntikkan domain final ke halaman statis + buat sitemap & CNAME.

Pakai:
    python3 scripts/set-domain.py kaloriku.id
    python3 scripts/set-domain.py https://kaloriku.id

Idempoten: blok <!--seo:start--> ... <!--seo:end--> diganti ulang setiap kali.
Tanpa argumen: hanya menampilkan domain yang sedang terpasang.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARK_START = "<!--seo:start-->"
MARK_END = "<!--seo:end-->"
PAGES = [(ROOT / "index.html", "/", "id"), (ROOT / "en" / "index.html", "/en/", "en")]


def normalize(arg: str) -> str:
    arg = arg.strip().rstrip("/")
    if not arg.startswith("http"):
        arg = "https://" + arg
    return arg


def seo_block(base: str, path: str, lang: str) -> str:
    other = "/en/" if lang == "id" else "/"
    lines = [
        MARK_START,
        f'<link rel="canonical" href="{base}{path}">',
        f'<link rel="alternate" hreflang="id" href="{base}/">',
        f'<link rel="alternate" hreflang="en" href="{base}/en/">',
        f'<link rel="alternate" hreflang="x-default" href="{base}/">',
        f'<meta property="og:url" content="{base}{path}">',
        f'<meta property="og:image" content="{base}/assets/img/og.jpg">',
        f'<meta property="og:image:type" content="image/jpeg">',
        f'<meta property="og:image:width" content="1200">',
        f'<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="KaloriKu — AI calorie tracker built for Indonesian food">',
        f'<meta name="twitter:image" content="{base}/assets/img/og.jpg">',
        MARK_END,
    ]
    return "\n".join(lines)


def update_page(file: Path, base: str, path: str, lang: str) -> None:
    html = file.read_text(encoding="utf-8")
    block = seo_block(base, path, lang)
    if MARK_START in html and MARK_END in html:
        html = re.sub(
            re.escape(MARK_START) + r".*?" + re.escape(MARK_END),
            block,
            html,
            count=1,
            flags=re.S,
        )
    else:
        html = html.replace("</head>", block + "\n</head>", 1)
    file.write_text(html, encoding="utf-8")


def write_sitemap(base: str) -> None:
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>{base}/</loc>
    <xhtml:link rel="alternate" hreflang="id" href="{base}/"/>
    <xhtml:link rel="alternate" hreflang="en" href="{base}/en/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{base}/"/>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{base}/en/</loc>
    <xhtml:link rel="alternate" hreflang="id" href="{base}/"/>
    <xhtml:link rel="alternate" hreflang="en" href="{base}/en/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{base}/"/>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>
"""
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")


def write_cname(base: str) -> None:
    host = re.sub(r"^https?://", "", base).split("/")[0]
    (ROOT / "CNAME").write_text(host + "\n", encoding="utf-8")


def write_robots(base: str) -> None:
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n", encoding="utf-8"
    )


def main() -> int:
    if len(sys.argv) < 2:
        current = []
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        m = re.search(r'<link rel="canonical" href="([^"]+)"', html)
        if m:
            current.append(f"Domain terpasang: {m.group(1)}")
        if (ROOT / "CNAME").exists():
            current.append(f"CNAME: {(ROOT / 'CNAME').read_text().strip()}")
        print("\n".join(current) or "Domain belum dipasang. Jalankan: python3 scripts/set-domain.py <domain>")
        return 0

    base = normalize(sys.argv[1])
    if not re.match(r"^https://[a-z0-9.-]+\.[a-z]{2,}$", base):
        print(f"Domain tidak valid: {base}")
        return 1

    for file, path, lang in PAGES:
        update_page(file, base, path, lang)
    write_sitemap(base)
    write_cname(base)
    write_robots(base)
    print(f"Terpasang: {base}")
    print("Diubah: index.html, en/index.html, sitemap.xml, CNAME, robots.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
