"""Generador de láminas Sara Vibes (4:5 feed y 9:16 stories/TikTok).
Uso: python3 make.py spec.json carpeta_salida
spec: {"slides":[{"tipo":"portada|foto|cta","foto":"ruta","pos":[x,y],"chip":"","titulo":"","sub":""}]}
"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

PINK = (236, 0, 140)
BLACK = (14, 14, 16)
WHITE = (255, 255, 255)
GF = "/usr/share/fonts/truetype/google-fonts/"
BOLD = GF + "Poppins-Bold.ttf"
MED = GF + "Poppins-Medium.ttf"
REG = GF + "Poppins-Regular.ttf"
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "src", "logo.jpg")
WA = "WhatsApp +56 9 7462 9490"
IG = "@sara.vibespersonaliza"


# ---------- Mejora de foto (luz, color, nitidez, resolución con IA) ----------
_CACHE = {}
MODELS = os.path.join(HERE, "models")


def _sr(img_bgr):
    """Superresolución x2 con IA (EDSR; FSRCNN si EDSR no está o la imagen es grande)."""
    import cv2
    h, w = img_bgr.shape[:2]
    for name, algo in (("FSRCNN_x2.pb", "fsrcnn"),):
        mp = os.path.join(MODELS, name)
        if not os.path.exists(mp) or (algo == "edsr" and max(h, w) > 1300):
            continue
        try:
            sr = cv2.dnn_superres.DnnSuperResImpl_create()
            sr.readModel(mp)
            sr.setModel(algo, 2)
            return sr.upsample(img_bgr)
        except Exception:
            continue
    return cv2.resize(img_bgr, (w * 2, h * 2), interpolation=cv2.INTER_LANCZOS4)


def enhance(path):
    """Corrige iluminación (CLAHE), viveza, reduce ruido,
    sube resolución con IA si la foto es chica y aplica nitidez. Devuelve PIL RGB."""
    if path in _CACHE:
        return _CACHE[path].copy()
    disk = os.path.join(os.path.dirname(os.path.abspath(path)), "mejoradas", os.path.splitext(os.path.basename(path))[0] + ".png")
    if os.path.exists(disk) and os.path.getmtime(disk) >= os.path.getmtime(path):
        _CACHE[path] = Image.open(disk).convert("RGB")
        return _CACHE[path].copy()
    if os.environ.get("NOENHANCE"):
        return Image.open(path).convert("RGB")
    import cv2
    import numpy as np
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        return Image.open(path).convert("RGB")
    img = cv2.fastNlMeansDenoisingColored(img, None, 3, 3, 7, 21)
    if max(img.shape[:2]) < 1800:
        img = _sr(img)
        if max(img.shape[:2]) < 1500:
            img = _sr(img)
    # iluminación: CLAHE en L
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l2 = cv2.createCLAHE(clipLimit=1.2, tileGridSize=(3, 3)).apply(l)
    l = cv2.addWeighted(l, 0.55, l2, 0.45, 0)
    img = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)
    # viveza suave
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    s_ = hsv[..., 1]
    hsv[..., 1] = np.clip(s_ + (255 - s_) * 0.10 * (s_ / 255), 0, 255)
    img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    # nitidez (unsharp mask)
    blur = cv2.GaussianBlur(img, (0, 0), 1.2)
    img = cv2.addWeighted(img, 1.35, blur, -0.35, 0)
    out = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    _CACHE[path] = out
    try:
        os.makedirs(os.path.dirname(disk), exist_ok=True)
        out.save(disk)
    except Exception:
        pass
    return out.copy()


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, maxw):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            t = (cur + " " + w).strip()
            if draw.textlength(t, font=fnt) <= maxw:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def fit_text(draw, text, path, maxw, maxh, start, minsize=30, spacing=1.12):
    size = start
    while size >= minsize:
        f = font(path, size)
        lines = wrap(draw, text, f, maxw)
        h = int(len(lines) * size * spacing)
        if h <= maxh and all(draw.textlength(l, font=f) <= maxw for l in lines):
            return f, lines, size
        size -= 2
    f = font(path, minsize)
    return f, wrap(draw, text, f, maxw), minsize


def draw_lines(draw, lines, f, size, x, y, fill, align="left", width=None, spacing=1.12, hl=None):
    for i, l in enumerate(lines):
        lx = x
        if align == "center":
            lx = x + (width - draw.textlength(l, font=f)) / 2
        if hl and any(h.lower() in l.lower() for h in hl):
            draw.text((lx, y), l, font=f, fill=PINK)
        else:
            draw.text((lx, y), l, font=f, fill=fill)
        y += int(size * spacing)
    return y


def cover(img, w, h, pos=(0.5, 0.5)):
    """Recorte proporcional (sin estirar) centrado en pos."""
    iw, ih = img.size
    s = max(w / iw, h / ih)
    nw, nh = int(iw * s + 0.5), int(ih * s + 0.5)
    im = img.resize((nw, nh), Image.LANCZOS)
    cx, cy = pos[0] * nw, pos[1] * nh
    l = int(min(max(cx - w / 2, 0), nw - w))
    t = int(min(max(cy - h / 2, 0), nh - h))
    return im.crop((l, t, l + w, t + h))


def contain(img, w, h):
    iw, ih = img.size
    s = min(w / iw, h / ih)
    return img.resize((int(iw * s), int(ih * s)), Image.LANCZOS)


def rounded(img, r):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, img.size[0] - 1, img.size[1] - 1], r, fill=255)
    out = Image.new("RGBA", img.size)
    out.paste(img, (0, 0), m)
    return out


def logo_badge(size):
    lg = Image.open(LOGO).convert("RGB").resize((size, size), Image.LANCZOS)
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).ellipse([0, 0, size - 1, size - 1], fill=255)
    out = Image.new("RGBA", (size, size))
    out.paste(lg, (0, 0), m)
    return out


def footer(canvas, d, W, H):
    d.rectangle([0, H - 86, W, H], fill=BLACK)
    d.rectangle([0, H - 90, W, H - 86], fill=PINK)
    f = font(MED, 30)
    t = f"{IG}   ·   {WA}"
    d.text(((W - d.textlength(t, font=f)) / 2, H - 66), t, font=f, fill=WHITE)


def slide(s, W, H, idx, total):
    c = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(c)
    tipo = s.get("tipo", "foto")
    pad = 70
    if tipo in ("portada", "full"):
        im = enhance(s["foto"])
        bg = cover(im, W, H, s.get("pos", (0.5, 0.5)))
        c.paste(bg, (0, 0))
        # degradado inferior para legibilidad
        grad = Image.new("L", (1, H))
        for y in range(H):
            grad.putpixel((0, y), int(max(0, (y - H * 0.38) / (H * 0.62)) ** 1.2 * 235))
        shade = Image.new("RGB", (W, H), BLACK)
        c.paste(shade, (0, 0), grad.resize((W, H)))
        d = ImageDraw.Draw(c)
        y_end = H - 120
        if s.get("chip"):
            fc = font(BOLD, 32)
            tw = d.textlength(s["chip"], font=fc)
            d.rounded_rectangle([pad, 70, pad + tw + 48, 70 + 62], 31, fill=PINK)
            d.text((pad + 24, 80), s["chip"], font=fc, fill=WHITE)
        fsub, lsub, ssub = fit_text(d, s.get("sub", ""), MED, W - 2 * pad, 200, 40, 28) if s.get("sub") else (None, [], 0)
        hsub = int(len(lsub) * ssub * 1.2)
        ft, lt, st = fit_text(d, s["titulo"], BOLD, W - 2 * pad, int(H * 0.36), 96 if H > 1500 else 84, 44, 1.08)
        ht = int(len(lt) * st * 1.08)
        y = y_end - hsub - ht - (24 if lsub else 0)
        y = draw_lines(d, lt, ft, st, pad, y, WHITE, spacing=1.08, hl=s.get("resaltar"))
        if lsub:
            draw_lines(d, lsub, fsub, ssub, pad, y + 24, (235, 235, 235), spacing=1.2)
        b = logo_badge(150)
        c.paste(b, (W - 150 - 40, 40), b)
    elif tipo == "foto":
        top = 70
        if s.get("chip"):
            fc = font(BOLD, 34)
            tw = d.textlength(s["chip"], font=fc)
            d.rounded_rectangle([pad, top, pad + tw + 48, top + 64], 32, fill=PINK)
            d.text((pad + 24, top + 10), s["chip"], font=fc, fill=WHITE)
            top += 90
        ft, lt, st = fit_text(d, s["titulo"], BOLD, W - 2 * pad, 200, 60, 36, 1.1)
        y = draw_lines(d, lt, ft, st, pad, top, WHITE, spacing=1.1, hl=s.get("resaltar"))
        y += 16
        if s.get("sub"):
            fs, ls, ss = fit_text(d, s["sub"], REG, W - 2 * pad, 130, 34, 26, 1.2)
            y = draw_lines(d, ls, fs, ss, pad, y, (220, 220, 220), spacing=1.2) + 10
        box_t = y + 14
        box_b = H - 120
        bw, bh = W - 2 * pad, box_b - box_t
        im = enhance(s["foto"])
        if s.get("ajuste") == "completa":
            ph = contain(im, bw, bh)
            back = cover(im, bw, bh).filter(ImageFilter.GaussianBlur(28))
            back = Image.blend(back, Image.new("RGB", back.size, BLACK), 0.35)
            back.paste(ph, ((bw - ph.size[0]) // 2, (bh - ph.size[1]) // 2))
            ph = back
        else:
            ph = cover(im, bw, bh, s.get("pos", (0.5, 0.5)))
        ph = rounded(ph, 36)
        d.rounded_rectangle([pad - 6, box_t - 6, pad + bw + 5, box_t + bh + 5], 40, fill=PINK)
        c.paste(ph, (pad, box_t), ph)
        b = logo_badge(120)
        c.paste(b, (W - 120 - 30, box_t + bh - 120 - 20), b)
    elif tipo == "cta":
        top = int(H * (0.2 if H > 1500 else 0.08))
        b = logo_badge(300)
        c.paste(b, ((W - 300) // 2, top), b)
        y = top + 340
        ft, lt, st = fit_text(d, s["titulo"], BOLD, W - 2 * pad, 330, 72, 40, 1.1)
        y = draw_lines(d, lt, ft, st, pad, y, WHITE, "center", W - 2 * pad, 1.1, hl=s.get("resaltar"))
        if s.get("sub"):
            fs, ls, ss = fit_text(d, s["sub"], REG, W - 2 * pad, 200, 38, 28, 1.25)
            y = draw_lines(d, ls, fs, ss, pad, y + 26, (225, 225, 225), "center", W - 2 * pad, 1.25)
        fb = font(BOLD, 40)
        t = "WhatsApp: +56 9 7462 9490"
        tw = d.textlength(t, font=fb)
        bx = (W - tw - 90) / 2
        by = min(y + 60, H - 260)
        d.rounded_rectangle([bx, by, bx + tw + 90, by + 92], 46, fill=PINK)
        d.text((bx + 45, by + 18), t, font=fb, fill=WHITE)
    if total > 1 and tipo != "cta" and not os.environ.get("NOCOUNT"):
        f = font(MED, 28)
        t = f"{idx}/{total}"
        d.text((W - pad - d.textlength(t, font=f), 84 if tipo == "foto" else 210), t, font=f, fill=(200, 200, 200))
    footer(c, d, W, H)
    return c


def main():
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    sl = spec["slides"]
    for fmt, (W, H) in {"4x5": (1080, 1350), "9x16": (1080, 1920)}.items():
        for i, s in enumerate(sl, 1):
            img = slide(s, W, H, i, len(sl))
            img.save(os.path.join(out, f"{fmt}_{i:02d}.jpg"), quality=93, subsampling=0, optimize=True)
    print("ok", out, len(sl))


if __name__ == "__main__":
    main()
