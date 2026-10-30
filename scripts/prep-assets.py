from PIL import Image, ImageDraw, ImageFilter, ImageChops
import os

# Sumber asli (bukan bagian dari folder deploy):
#   ~/Documents/projects/kaloriku-web-src/
#     src-logo.png  = KaloriKu_Logo.png (1254, latar putih)
#     src-mark.png  = kaloriku-splash-logo.png (512, sudah transparan)
#     src-home.png, src-scan.png = screenshot 1080x2340
SRC = os.environ.get('KALORIKU_SRC', os.path.expanduser('~/Documents/projects/kaloriku-web-src'))


def q_save(im, path, colors=256):
    """PNG berpalet: ikon gradien tetap mulus, ukuran turun ~90%."""
    im.convert('RGBA').quantize(colors=colors, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG).save(path, optimize=True)


# ---------- logo: buang latar putih lewat flood fill dari keempat sudut ----------
im = Image.open(os.path.join(SRC, 'src-logo.png')).convert('RGB')
flood = im.copy()
for xy in [(0, 0), (im.width - 1, 0), (0, im.height - 1), (im.width - 1, im.height - 1)]:
    ImageDraw.floodfill(flood, xy, (255, 0, 255), thresh=30)

diff = ImageChops.difference(flood, Image.new('RGB', im.size, (255, 0, 255))).convert('L')
alpha_img = diff.point(lambda v: 0 if v < 6 else 255).filter(ImageFilter.GaussianBlur(0.8))
rgba = im.convert('RGBA')
rgba.putalpha(alpha_img)

bbox = alpha_img.point(lambda v: 255 if v > 8 else 0).getbbox()
print('logo bbox', bbox, 'orig', im.size)
logo = rgba.crop(bbox)
side = max(logo.size)
canvas = Image.new('RGBA', (side, side), (0, 0, 0, 0))
canvas.paste(logo, ((side - logo.width) // 2, (side - logo.height) // 2), logo)

q_save(canvas.resize((512, 512), Image.LANCZOS), 'assets/img/logo-512.png')
q_save(canvas.resize((192, 192), Image.LANCZOS), 'assets/img/logo-192.png')
canvas.resize((180, 180), Image.LANCZOS).save('assets/img/logo-180.png', optimize=True)
canvas.resize((32, 32), Image.LANCZOS).save('assets/img/logo-32.png', optimize=True)
canvas.resize((512, 512), Image.LANCZOS).save('assets/img/logo-512.webp', 'WEBP', quality=88, method=6)

# ---------- mark saja (ikon splash, sudah punya alpha) ----------
mk = Image.open(os.path.join(SRC, 'src-mark.png')).convert('RGBA')
bb = mk.getchannel('A').getbbox()
mk = mk.crop(bb)
print('mark bbox', bb)
side = max(mk.size)
c = Image.new('RGBA', (side, side), (0, 0, 0, 0))
c.paste(mk, ((side - mk.width) // 2, (side - mk.height) // 2), mk)
q_save(c.resize((192, 192), Image.LANCZOS), 'assets/img/mark-192.png')
c.resize((192, 192), Image.LANCZOS).save('assets/img/mark-192.webp', 'WEBP', quality=88, method=6)

# ---------- screenshot -> webp 720w ----------
for name, out in [('src-home.png', 'assets/img/screen-home.webp'), ('src-scan.png', 'assets/img/screen-scan.webp')]:
    shot = Image.open(os.path.join(SRC, name)).convert('RGB')
    shot = shot.resize((720, round(shot.height * 720 / shot.width)), Image.LANCZOS)
    shot.save(out, 'WEBP', quality=84, method=6)
    print(out, shot.size, round(os.path.getsize(out) / 1024), 'KB')
