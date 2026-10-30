from PIL import Image
import os

SRC = '/tmp'

# screenshot asli dari emulator
shots = {
    'screen-home.webp': ('emu-home.png', 720, 84),
    'screen-history.webp': ('emu-history2.png', 720, 84),
}
for out, (src, width, quality) in shots.items():
    im = Image.open(os.path.join(SRC, src)).convert('RGB')
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(f'assets/img/{out}', 'WEBP', quality=quality, method=6)
    print(out, im.size, round(os.path.getsize(f'assets/img/{out}') / 1024), 'KB')

# potongan kartu "Makanan Hari Ini" dari layar Beranda asli
home = Image.open(os.path.join(SRC, 'emu-home.png')).convert('RGB')
card = home.crop((48, 1100, 1032, 1620))
card.resize((round(card.width * 0.9), round(card.height * 0.9)), Image.LANCZOS).save('/tmp/meals-card.png')
card.save('assets/img/meals-card.webp', 'WEBP', quality=86, method=6)
print('meals-card.webp', card.size, round(os.path.getsize('assets/img/meals-card.webp') / 1024), 'KB')
