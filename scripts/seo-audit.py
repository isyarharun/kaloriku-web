import json
import re
from pathlib import Path

for rel in ["index.html", "en/index.html"]:
    p = Path(rel)
    html = p.read_text(encoding="utf-8")
    head = html.split("</head>")[0]
    print("=" * 70)
    print(rel)
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    desc = re.search(r'<meta name="description" content="([^"]*)"', head)
    canon = re.search(r'<link rel="canonical" href="([^"]*)"', head)
    hreflang = re.findall(r'hreflang="([^"]+)" href="([^"]+)"', head)
    og = re.findall(r'<meta property="(og:[^"]+)" content="([^"]*)"', head)
    tw = re.findall(r'<meta name="(twitter:[^"]+)" content="([^"]*)"', head)
    robots = re.search(r'<meta name="robots" content="([^"]*)"', head)
    viewport = re.search(r'<meta name="viewport" content="([^"]*)"', head)
    lang = re.search(r'<html lang="([^"]+)"', html).group(1)
    imgs = re.findall(r"<img[^>]*>", html)
    lazy = sum(1 for i in imgs if 'loading="lazy"' in i)
    noalt = sum(1 for i in imgs if 'alt=' not in i)
    print(f"lang            : {lang}")
    print(f"title           : {title.group(1)!r} ({len(title.group(1))} chars)")
    print(f"description     : {len(desc.group(1)) if desc else 'MISSING'} chars")
    print(f"canonical       : {canon.group(1) if canon else 'MISSING'}")
    print(f"hreflang        : {hreflang if hreflang else 'MISSING'}")
    print(f"robots          : {robots.group(1) if robots else 'MISSING (default index,follow)'}")
    print(f"viewport        : {viewport.group(1) if viewport else 'MISSING'}")
    print(f"og tags         : {[k for k, _ in og]}")
    print(f"twitter tags    : {[k for k, _ in tw]}")
    print(f"h1/h2/h3        : {len(re.findall(r'<h1[ >]', html))}/{len(re.findall(r'<h2[ >]', html))}/{len(re.findall(r'<h3[ >]', html))}")
    print(f"images          : {len(imgs)} (tanpa alt: {noalt}, lazy: {lazy})")
    blocks = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)
    print(f"JSON-LD blocks  : {len(blocks)}")
    for b in blocks:
        try:
            data = json.loads(b)
            print(f"  @type={data.get('@type')} keys={sorted(data.keys())}")
        except Exception as e:
            print("  INVALID JSON-LD:", e)

print("=" * 70)
print("robots.txt:\n" + Path("robots.txt").read_text(encoding="utf-8"))
for f in ["sitemap.xml", "CNAME"]:
    print(f"{f} exists:", Path(f).exists())
