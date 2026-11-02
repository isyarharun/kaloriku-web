import html as htmllib
import json
import re
from pathlib import Path

BLOCK = '<script type="application/ld+json" id="faq-schema">\n{}\n</script>'


def strip_tags(s: str) -> str:
    return htmllib.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def build(path: Path) -> int:
    html = path.read_text(encoding="utf-8")
    section = re.search(r'<section[^>]*id="faq".*?</section>', html, re.S)
    if not section:
        raise SystemExit(f"FAQ section not found in {path}")
    pairs = re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", section.group(0), re.S)
    if not pairs:
        raise SystemExit(f"no FAQ pairs found in {path}")
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": strip_tags(q),
                "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)},
            }
            for q, a in pairs
        ],
    }
    payload = BLOCK.format(json.dumps(data, ensure_ascii=False, indent=2))
    # hapus blok lama (kalau ada), lalu sisipkan sebelum </head>
    html = re.sub(r'<script type="application/ld\+json" id="faq-schema">.*?</script>\n?', "", html, flags=re.S)
    html = html.replace("</head>", payload + "\n</head>", 1)
    path.write_text(html, encoding="utf-8")
    return len(pairs)


for rel in ["index.html", "en/index.html"]:
    n = build(Path(rel))
    print(f"{rel}: {n} pertanyaan -> FAQPage schema")
