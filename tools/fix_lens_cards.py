"""Correct the lens formula in the held CBSEMock cards (mirror formula → 1/v − 1/u = 1/f)."""
import cv2, numpy as np, os
H = 'formula-posts/hold/'
OUT = '/home/claude/fix/out/'
os.makedirs(OUT, exist_ok=True)

def load(n): return cv2.imread(H + n + '.jpg')

def erase(img, x0, y0, x1, y1, pad=6):
    m = np.zeros(img.shape[:2], np.uint8)
    m[y0 - pad:y1 + pad + 1, x0 - pad:x1 + pad + 1] = 255
    return cv2.inpaint(img, m, 12, cv2.INPAINT_TELEA)

def stroke_colour(img, box):
    x0, y0, x1, y1 = box
    px = img[y0:y1, x0:x1].reshape(-1, 3)
    px = px[np.argsort(px.astype(int).sum(1))]
    return px[-max(1, len(px) // 12):].mean(0)       # the brightest pixels = the stroke's own colour

def bar(img, x0, y0, x1, y1, colour, glow=0.35):
    """Anti-aliased rounded bar with a faint glow, drawn at 4× and blended in."""
    S = 4
    h, w = img.shape[:2]
    m = np.zeros((h * S, w * S), np.uint8)
    r = max(1, (y1 - y0) * S // 3) if (x1 - x0) > (y1 - y0) else max(1, (x1 - x0) * S // 3)
    cv2.rectangle(m, (x0 * S + r, y0 * S), (x1 * S - r, y1 * S), 255, -1)
    cv2.rectangle(m, (x0 * S, y0 * S + r), (x1 * S, y1 * S - r), 255, -1)
    for cx, cy in ((x0 * S + r, y0 * S + r), (x1 * S - r, y0 * S + r), (x0 * S + r, y1 * S - r), (x1 * S - r, y1 * S - r)):
        cv2.circle(m, (cx, cy), r, 255, -1)
    m = cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA).astype(float) / 255
    g = cv2.GaussianBlur(m, (0, 0), 6) * glow
    a = np.clip(np.maximum(m, g), 0, 1)[..., None]
    out = img.astype(float) * (1 - a) + np.array(colour)[None, None, :] * a
    return out.astype(np.uint8)

def plus_to_minus(img, bbox, hbar, eq_box):
    """bbox = the whole '+' (x0,y0,x1,y1); hbar = (y0,y1) of its horizontal bar; eq_box = a box around '=' for colour."""
    col = stroke_colour(img, eq_box)
    img = erase(img, *bbox)
    return bar(img, bbox[0], hbar[0], bbox[2], hbar[1], col)

def save(img, n):
    cv2.imwrite(OUT + n + '.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 95])

if __name__ == '__main__':
    n = '02_Concept8_Lens_2_Lens_Formula'
    save(plus_to_minus(load(n), (634, 638, 707, 716), (673, 681), (365, 650, 445, 700)), n)
    n = '02_Concept8_Lens_5_Lens_Recap'
    save(plus_to_minus(load(n), (597, 710, 660, 774), (739, 745), (400, 720, 460, 770)), n)
    n = '05_NeonYellow_FormulaFlash_Physics_Lens_Formula'
    save(plus_to_minus(load(n), (633, 494, 682, 543), (515, 522), (420, 500, 470, 540)), n)
    print('done 3')


def minus_to_plus(img, x0, y0, x1, y1, eq_box):
    """'−' at (x0,y0)-(x1,y1) → '+' of the same width and stroke."""
    col = stroke_colour(img, eq_box)
    img = erase(img, x0, y0, x1, y1, pad=4)
    t = y1 - y0 + 1
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    half = (x1 - x0) // 2
    img = bar(img, x0, y0, x1, y1 + 1, col, glow=0.25)
    return bar(img, cx - t // 2, cy - half, cx - t // 2 + t, cy + half, col, glow=0.25)


def fix_slide3():
    n = '02_Concept8_Lens_3_Lens_Calculation'
    img = load(n)
    img = minus_to_plus(img, 483, 604, 530, 609, (290, 590, 340, 620))     # 1/v = 1/f + 1/u
    img = minus_to_plus(img, 494, 817, 540, 821, (290, 800, 340, 835))     # = 1/10 + (1/−30)
    save(img, n)


def fix_card04():
    """1/u + 1/v = 1/f  →  1/v − 1/u = 1/f : swap the two denominators, then + → −."""
    n = '04_Concept8_Physics_Lens_Formula'
    img = load(n)
    # same-size boxes around each letter (centred on their own glyph)
    def box(x0, y0, x1, y1, w=58, h=52):
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        return cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2
    bu, bv = box(347, 1048, 387, 1089), box(527, 1048, 564, 1089)
    pu = img[bu[1]:bu[3], bu[0]:bu[2]].copy()
    pv = img[bv[1]:bv[3], bv[0]:bv[2]].copy()
    # paste with a feathered mask so the patch edges vanish into the background
    def paste(dst, patch, b):
        h, w = patch.shape[:2]
        m = np.zeros((h, w), np.float32); m[6:-6, 6:-6] = 1
        m = cv2.GaussianBlur(m, (0, 0), 3)[..., None]
        region = dst[b[1]:b[3], b[0]:b[2]].astype(np.float32)
        dst[b[1]:b[3], b[0]:b[2]] = (region * (1 - m) + patch.astype(np.float32) * m).astype(np.uint8)
    img = erase(img, 347, 1048, 387, 1089, pad=5)
    img = erase(img, 527, 1048, 564, 1089, pad=5)
    paste(img, pv, bu)
    paste(img, pu, bv)
    img = plus_to_minus(img, (437, 994, 483, 1040), (1014, 1019), (620, 1005, 680, 1030))
    save(img, n)
