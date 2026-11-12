"""Encuadre profesional de fotos para láminas (4:5, 9:16) y Reels (9:16), sin deformar nunca la imagen.

Reglas:
- Siempre se usa la versión HD de la foto si existe (fotos/hd/foto_XX.jpg, generada con kit/hd.py),
  aunque la ruta indicada sea fotos/mejoradas/ o fotos/originales/.
- La imagen solo se recorta y se escala de forma proporcional (misma escala en ancho y alto) con LANCZOS.
- Modo "cubrir" (por defecto): llena el formato recortando lo que sobra, centrado en "pos".
- Modo "completa": la foto entera, ajustada al ancho, sobre un fondo de la misma foto desenfocado y
  oscurecido (para fotos horizontales donde el recorte vertical dejaría fuera parte de la instalación).
- Si una foto sin versión HD tuviera que agrandarse más de 1,5 veces para "cubrir", se usa "completa"
  automáticamente para no publicar una imagen pixelada.
"""
import pathlib, re
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageDraw

MAX_AGRANDAR = 1.5


def ruta_hd(p):
    p = pathlib.Path(p)
    for base in (p.parent.parent / "hd", p.parent / "hd", p.parent):
        q = base / p.name
        if q.exists() and q.parent.name == "hd":
            return q
    return p


def abrir(p):
    q = ruta_hd(p)
    return ImageOps.exif_transpose(Image.open(q)).convert("RGB"), q


def leer_pos(pos, defecto=(0.5, 0.5)):
    """Acepta [x, y] (0-1), "60% 30%", "center"."""
    if pos is None or pos == "center":
        return defecto
    if isinstance(pos, (list, tuple)):
        return float(pos[0]), float(pos[1])
    n = re.findall(r"(-?[\d.]+)%", str(pos))
    if len(n) >= 2:
        return float(n[0]) / 100, float(n[1]) / 100
    return defecto


def caja(w, h, W, H, px, py, css=False):
    """Recorte de proporción W:H dentro de w x h. css=True: px,py como object-position de CSS
    (fracción del sobrante); css=False: px,py como centro del recorte."""
    r = W / H
    cw, ch = (h * r, h) if w / h > r else (w, w / r)
    if css:
        x, y = (w - cw) * px, (h - ch) * py
    else:
        x, y = px * w - cw / 2, py * h - ch / 2
    x = min(max(x, 0), w - cw); y = min(max(y, 0), h - ch)
    return (x, y, x + cw, y + ch)


def agrandamiento(im, W, H):
    return max(W / im.width, H / im.height)


def cubrir(im, W, H, pos=None, css=False):
    px, py = leer_pos(pos)
    b = caja(im.width, im.height, W, H, px, py, css)
    return im.resize((W, H), Image.LANCZOS, box=b, reducing_gap=3.0)


def completa(im, W, H, arriba=None, alto_max=None, radio=28):
    """Foto entera ajustada al ancho (márgenes 0), sobre fondo desenfocado de la misma foto."""
    fondo = cubrir(im, W // 4, H // 4).filter(ImageFilter.GaussianBlur(14)).resize((W, H), Image.BICUBIC)
    fondo = ImageEnhance.Brightness(fondo).enhance(0.62)
    alto_max = alto_max or int(H * 0.62)
    s = min(W / im.width, alto_max / im.height)
    fw, fh = round(im.width * s), round(im.height * s)
    fg = im.resize((fw, fh), Image.LANCZOS, reducing_gap=3.0)
    y = arriba if arriba is not None else (H - fh) // 2
    x = (W - fw) // 2
    if fw < W and radio:
        m = Image.new("L", (fw, fh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, fw - 1, fh - 1), radio, fill=255)
        sombra = Image.new("L", (W, H), 0); ImageDraw.Draw(sombra).rounded_rectangle((x, y + 14, x + fw, y + fh + 14), radio, fill=150)
        fondo.paste((0, 0, 0), (0, 0), sombra.filter(ImageFilter.GaussianBlur(22)))
        fondo.paste(fg, (x, y), m)
    else:
        fondo.paste(fg, (x, y))
    return fondo


def encuadrar(path, W, H, pos=None, ajuste="auto", css=False, arriba=None, alto_max=None):
    """Devuelve una imagen RGB de exactamente W x H, sin deformar."""
    im, q = abrir(path)
    if ajuste == "auto":
        ajuste = "completa" if (q.parent.name != "hd" and agrandamiento(im, W, H) > MAX_AGRANDAR) else "cubrir"
    if ajuste == "completa":
        return completa(im, W, H, arriba, alto_max)
    return cubrir(im, W, H, pos, css)
