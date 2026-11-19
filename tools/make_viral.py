"""Láminas de alto impacto (colores vivos) para Sara Vibes.
Uso: python3 tools/make_viral.py spec.json carpeta_salida
spec: {"tema":"navidad","slides":[{"tipo":"portada","fotos":[...],"titulo":"","resaltar":"","sub":""},
       {"tipo":"idea","n":1,"para":"Para tu mamá","foto":"...","titulo":"","sub":""},
       {"tipo":"cta","titulo":"","sub":""}]}
"""
import json, os, sys, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_post as mp

GF = "/usr/share/fonts/truetype/google-fonts/"
B = GF + "Poppins-Bold.ttf"; M = GF + "Poppins-Medium.ttf"
PAL = {
    "navidad": [((198, 0, 60), (236, 0, 140)), ((120, 0, 90), (236, 0, 140)), ((210, 30, 50), (255, 120, 40))],
    "default": [((236, 0, 140), (120, 40, 220)), ((255, 90, 60), (236, 0, 140))],
}
GOLD = (255, 214, 92); WHITE = (255, 255, 255); INK = (20, 10, 30)
WA = "+56 9 7462 9490"


def grad(W, H, c1, c2):
    g = Image.new("RGB", (W, H))
    px = g.load()
    for y in range(H):
        for x in range(0, W, 4):
            t = min(1, max(0, (x / W) * 0.45 + (y / H) * 0.75))
            c = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
            for k in range(4):
                if x + k < W:
                    px[x + k, y] = c
    return g


def sparkles(d, W, H, seed, n=12):
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.choice([rnd.randint(10, 60), rnd.randint(W - 60, W - 10), rnd.randint(0, W)])
        y = rnd.randint(0, H) if x < 70 or x > W - 70 else rnd.choice([rnd.randint(5, 40), rnd.randint(H - 60, H - 10)])
        r = rnd.choice([3, 4, 6, 9])
        col = rnd.choice([GOLD, WHITE, (255, 190, 230)])
        d.line([(x - r * 2, y), (x + r * 2, y)], fill=col, width=2)
        d.line([(x, y - r * 2), (x, y + r * 2)], fill=col, width=2)
        d.ellipse([x - r // 2, y - r // 2, x + r // 2, y + r // 2], fill=col)


def card(img, w, h, pos=(0.5, 0.5), angle=0, border=14):
    ph = mp.cover(img, w, h, pos)
    c = Image.new("RGB", (w + 2 * border, h + 2 * border), WHITE)
    c.paste(ph, (border, border))
    c = mp.rounded(c, 30)
    if angle:
        c = c.rotate(angle, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", c.size, (0, 0, 0, 0))
    a = c.split()[3].point(lambda v: 110 if v else 0)
    sh.putalpha(a)
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    return c, sh


def paste_card(canvas, img, xy, w, h, pos=(0.5, 0.5), angle=0):
    c, sh = card(img, w, h, pos, angle)
    canvas.paste(sh, (xy[0] + 10, xy[1] + 22), sh)
    canvas.paste(c, xy, c)
    return c.size


def text_block(d, text, font_path, maxw, maxh, start, x, y, fill, align="left", W=None, hl=None, spacing=1.05):
    f, lines, s = mp.fit_text(d, text, font_path, maxw, maxh, start, 40, spacing)
    for l in lines:
        lx = x if align == "left" else (W - d.textlength(l, font=f)) / 2
        col = GOLD if hl and any(h.lower() in l.lower() for h in hl) else fill
        # sombra
        d.text((lx + 3, y + 4), l, font=f, fill=(60, 0, 40))
        d.text((lx, y), l, font=f, fill=col)
        y += int(s * spacing)
    return y


def pill(d, text, x, y, size=34, bg=GOLD, fg=INK, center_W=None):
    f = ImageFont.truetype(B, size)
    tw = d.textlength(text, font=f)
    if center_W:
        x = (center_W - tw - 56) / 2
    d.rounded_rectangle([x, y, x + tw + 56, y + size + 30], (size + 30) // 2, fill=bg)
    d.text((x + 28, y + 12), text, font=f, fill=fg)
    return y + size + 30


def footer(c, d, W, H):
    d.rectangle([0, H - 92, W, H], fill=INK)
    f = ImageFont.truetype(M, 30)
    t = f"@sara.vibespersonaliza   ·   WhatsApp {WA}"
    d.text(((W - d.textlength(t, font=f)) / 2, H - 70), t, font=f, fill=WHITE)


def render(s, W, H, i, total, pal):
    c1, c2 = pal[i % len(pal)]
    c = grad(W, H, c1, c2).convert("RGB")
    d = ImageDraw.Draw(c)
    sparkles(d, W, H - 92, i * 7 + 1)
    pad = 70
    tall = H > 1500
    if s["tipo"] == "portada":
        y = pill(d, s.get("chip", "NAVIDAD 2026"), pad, 70, 34)
        y = text_block(d, s["titulo"], B, W - 2 * pad, 360 if not tall else 520, 104 if not tall else 120, pad, y + 26, WHITE, hl=[s.get("resaltar", "")])
        fotos = [mp.enhance(f) for f in s["fotos"]]
        top = y + (70 if tall else 30)
        avail = H - 92 - 110 - top
        cw = int((W - 2 * pad) / 2.35)
        ch = min(int(cw * (1.75 if tall else 1.3)), avail - 60)
        xs = [pad - 10, (W - cw) // 2, W - pad - cw - 10]
        ang = [6, -2, -7]
        offs = [40, 0, 50]
        for k, img in enumerate(fotos[:3]):
            paste_card(c, img, (xs[k], top + offs[k]), cw, ch, (0.5, 0.45), ang[k])
        d = ImageDraw.Draw(c)
        pill(d, s.get("sub", "Desliza y elige"), 0, H - 92 - 100, 36, WHITE, (198, 0, 60), center_W=W)
    elif s["tipo"] == "idea":
        d.text((pad, 50), f"{s['n']:02d}", font=ImageFont.truetype(B, 150), fill=(255, 255, 255, 60))
        d.text((pad + 4, 52), f"{s['n']:02d}", font=ImageFont.truetype(B, 150), fill=GOLD)
        pill(d, s["para"], pad + 250, 105, 36, WHITE, (198, 0, 60))
        y = text_block(d, s["titulo"], B, W - 2 * pad, 220, 70, pad, 245, WHITE)
        if s.get("sub"):
            f = ImageFont.truetype(M, 34)
            y += 34
            for l in mp.wrap(d, s["sub"], f, W - 2 * pad):
                d.text((pad, y), l, font=f, fill=(255, 235, 245))
                y += 46
        top = y + 30
        bh = H - 92 - 50 - top
        bw = W - 2 * pad - 28
        bw = min(bw, int(bh * 1.05)) if not tall else bw
        x = (W - bw - 28) // 2
        img = mp.enhance(s["foto"])
        paste_card(c, img, (x, top), bw, bh - 28, tuple(s.get("pos", (0.5, 0.5))), s.get("angulo", -2))
    elif s["tipo"] == "cta":
        lg = mp.logo_badge(260)
        c.paste(lg, ((W - 260) // 2, int(H * (0.12 if tall else 0.06))), lg)
        d = ImageDraw.Draw(c)
        y = int(H * (0.12 if tall else 0.06)) + 300
        y = text_block(d, s["titulo"], B, W - 2 * pad, 330, 84, pad, y, WHITE, "center", W, hl=s.get("resaltar"))
        f = ImageFont.truetype(M, 38)
        for l in mp.wrap(d, s.get("sub", ""), f, W - 2 * pad):
            d.text(((W - d.textlength(l, font=f)) / 2, y + 14), l, font=f, fill=(255, 235, 245))
            y += 52
        y = pill(d, f"WhatsApp {WA}", 0, y + 50, 46, GOLD, INK, center_W=W)
        pill(d, "Guarda este post · Comparte", 0, y + 30, 32, WHITE, (198, 0, 60), center_W=W)
    footer(c, d, W, H)
    return c


def main():
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    pal = PAL.get(spec.get("tema", "default"), PAL["default"])
    for fmt, (W, H) in {"4x5": (1080, 1350), "9x16": (1080, 1920)}.items():
        for i, s in enumerate(spec["slides"], 1):
            render(s, W, H, i - 1, len(spec["slides"]), pal).save(os.path.join(out, f"{fmt}_{i:02d}.jpg"), quality=94, subsampling=0, optimize=True)
    print("ok", out)


if __name__ == "__main__":
    main()
