from PIL import Image
import os

# dish photo cropped from the in-app scan result screenshot
im = Image.open('assets/src-scan.png').convert('RGB')
crop = im.crop((70, 240, 1010, 940))
crop.save('assets/img/dish.webp', 'WEBP', quality=86, method=6)
print('dish.webp', crop.size, round(os.path.getsize('assets/img/dish.webp') / 1024), 'KB')

# 2x retina variant for large screens
crop.resize((1410, 1050), Image.LANCZOS).save('assets/img/dish@1.5x.webp', 'WEBP', quality=82, method=6)
print('dish@1.5x', round(os.path.getsize('assets/img/dish@1.5x.webp') / 1024), 'KB')
