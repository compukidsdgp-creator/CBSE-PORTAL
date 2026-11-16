"""Build the site favicons from the CBSEMock logo (cap + book emblem on a white disc with a blue ring)."""
from PIL import Image, ImageDraw
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
src = Image.open(ROOT / 'formula-posts/_cbsemock_logo_circle.png').convert('RGBA')
# keep only the emblem: drop everything that isn't the cap/book (the pale background and the outer ring)
px = src.load()
for y in range(src.height):
    for x in range(src.width):
        r, g, b, a = px[x, y]
        if (r > 200 and g > 215 and b > 225) or ((x - 627) ** 2 + (y - 627) ** 2 > 520 ** 2):
            px[x, y] = (255, 255, 255, 0)
emb = src.crop((195, 140, 1055, 735))
emb = emb.crop(emb.getbbox())

def make(size, ring=True):
    S = size * 4
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if ring:
        rw = int(S * 0.06)
        d.ellipse((0, 0, S - 1, S - 1), fill=(22, 94, 214, 255))
        d.ellipse((rw, rw, S - 1 - rw, S - 1 - rw), fill=(255, 255, 255, 255))
        w = int(S * 0.74)
    else:                                      # maskable icon: full-bleed white square, emblem in the safe zone
        d.rectangle((0, 0, S, S), fill=(255, 255, 255, 255)); w = int(S * 0.62)
    h = int(emb.height * w / emb.width)
    im.alpha_composite(emb.resize((w, h), Image.LANCZOS), ((S - w) // 2, (S - h) // 2))
    return im.resize((size, size), Image.LANCZOS)

make(48).save(ROOT / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
make(32).save(ROOT / 'favicon-32x32.png'); make(16).save(ROOT / 'favicon-16x16.png')
make(96).save(ROOT / 'favicon-96x96.png')
a = make(180, ring=False); bg = Image.new('RGB', a.size, 'white'); bg.paste(a, mask=a); bg.save(ROOT / 'apple-touch-icon.png')
make(192).save(ROOT / 'android-chrome-192x192.png'); make(512).save(ROOT / 'android-chrome-512x512.png')
make(512, ring=False).save(ROOT / 'maskable-512x512.png')
print('favicons written')
