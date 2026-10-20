"""Mejora fotos reales de instalaciones (luz, color, nitidez) sin alterar el contenido.

Uso: python3 fotos.py entrada.jpg salida.jpg [foco_y 0-1] [foco_x 0-1]
- Balance de blancos suave (gray world parcial)
- Exposición: niveles automáticos con recorte de 0,5% y gamma para levantar sombras
- Color: saturación +8%, contraste local suave
- Reducción de ruido leve + nitidez (unsharp mask)
- Recorte 4:5 (1080x1350) centrado en el foco indicado (por defecto, tercio superior donde suele estar el equipo)
"""
import sys
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def mejorar(im):
    im = im.convert("RGB")
    a = np.asarray(im).astype(np.float32)
    # balance de blancos parcial (50%) hacia gris neutro
    means = a.reshape(-1, 3).mean(0)
    g = means.mean()
    gain = 1 + 0.5 * (g / np.maximum(means, 1) - 1)
    a = np.clip(a * gain, 0, 255)
    # niveles por canal conjunto (percentiles)
    lo, hi = np.percentile(a, 0.5), np.percentile(a, 99.6)
    a = np.clip((a - lo) / max(hi - lo, 1) * 255, 0, 255)
    # gamma según brillo medio: levanta fotos oscuras
    mean = max(a.mean() / 255, 0.05)
    gamma = float(np.clip(np.log(0.56) / np.log(mean), 0.62, 1.0))  # apunta a una foto luminosa
    a = 255 * (a / 255) ** gamma
    a = np.clip(a * np.array([1.02, 1.0, 0.98]), 0, 255)  # toque cálido y luminoso
    im = Image.fromarray(a.astype(np.uint8))
    im = im.filter(ImageFilter.MedianFilter(3)) if min(im.size) < 900 else im
    im = im.filter(ImageFilter.UnsharpMask(radius=30, percent=22, threshold=0))  # claridad local
    im = ImageEnhance.Color(im).enhance(1.14)
    im = ImageEnhance.Contrast(im).enhance(1.05)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=90, threshold=3))  # nitidez
    return im


def recorte(im, W=1080, H=1350, fy=0.35, fx=0.5):
    w, h = im.size
    r = W / H
    if w / h > r:
        nw = int(h * r); x = int(min(max(fx * w - nw / 2, 0), w - nw)); box = (x, 0, x + nw, h)
    else:
        nh = int(w / r); y = int(min(max(fy * h - nh / 2, 0), h - nh)); box = (0, y, w, y + nh)
    return im.crop(box).resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    fy = float(sys.argv[3]) if len(sys.argv) > 3 else 0.35
    fx = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
    im = ImageOps.exif_transpose(Image.open(src))
    recorte(mejorar(im), fy=fy, fx=fx).save(out, quality=93, optimize=True)
