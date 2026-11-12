"""Mejora de resolución con IA (Real-ESRGAN) para fotos reales de instalaciones.

Uso: python3 hd.py entrada.jpg salida.jpg [--modelo x4plus|general] [--lado 2600]
- Escala x4 con Real-ESRGAN y luego reduce con LANCZOS hasta que el lado menor mida --lado px
  (así el recorte 9:16 o 4:5 nunca necesita agrandarse).
- No inventa ni borra objetos: solo reconstruye nitidez y quita ruido/artefactos de WhatsApp.
- Pesos: RealESRGAN_x4plus.pth / realesr-general-x4v3.pth (github.com/xinntao/Real-ESRGAN, licencia BSD-3),
  se descargan solos a kit/modelos/ la primera vez (no se suben al repositorio).
- Requiere PyTorch (pip install torch). x4plus tarda ~4 min por foto en CPU; "general" ~15 s.
"""
import argparse, pathlib, sys
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from PIL import Image, ImageOps

HERE = pathlib.Path(__file__).resolve().parent / "modelos"
PESOS = {  # (archivo, url oficial, sha256)
    "x4plus": ("RealESRGAN_x4plus.pth", "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",
               "4fa0d38905f75ac06eb49a7951b426670021be3018265fd191d2125df9d682f1"),
    "general": ("realesr-general-x4v3.pth", "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth",
                "8dc7edb9ac80ccdc30c3a5dca6616509367f05fbc184ad95b731f05bece96292"),
}


def pesos(modelo):
    import hashlib, urllib.request
    nombre, url, sha = PESOS[modelo]
    f = HERE / nombre
    if not f.exists():
        HERE.mkdir(parents=True, exist_ok=True)
        print(f"Descargando {nombre} ...", file=sys.stderr)
        urllib.request.urlretrieve(url, f)
    if hashlib.sha256(f.read_bytes()).hexdigest() != sha:
        f.unlink(); sys.exit(f"{nombre}: suma de verificación incorrecta")
    return f


class RDB(nn.Module):
    def __init__(s, nf=64, gc=32):
        super().__init__()
        s.conv1 = nn.Conv2d(nf, gc, 3, 1, 1); s.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1)
        s.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1); s.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1)
        s.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1); s.l = nn.LeakyReLU(0.2, True)

    def forward(s, x):
        x1 = s.l(s.conv1(x)); x2 = s.l(s.conv2(torch.cat((x, x1), 1)))
        x3 = s.l(s.conv3(torch.cat((x, x1, x2), 1))); x4 = s.l(s.conv4(torch.cat((x, x1, x2, x3), 1)))
        return s.conv5(torch.cat((x, x1, x2, x3, x4), 1)) * 0.2 + x


class RRDB(nn.Module):
    def __init__(s, nf=64):
        super().__init__(); s.rdb1, s.rdb2, s.rdb3 = RDB(nf), RDB(nf), RDB(nf)

    def forward(s, x):
        return s.rdb3(s.rdb2(s.rdb1(x))) * 0.2 + x


class RRDBNet(nn.Module):
    def __init__(s, nf=64, nb=23):
        super().__init__()
        s.conv_first = nn.Conv2d(3, nf, 3, 1, 1); s.body = nn.Sequential(*[RRDB(nf) for _ in range(nb)])
        s.conv_body = nn.Conv2d(nf, nf, 3, 1, 1); s.conv_up1 = nn.Conv2d(nf, nf, 3, 1, 1)
        s.conv_up2 = nn.Conv2d(nf, nf, 3, 1, 1); s.conv_hr = nn.Conv2d(nf, nf, 3, 1, 1)
        s.conv_last = nn.Conv2d(nf, 3, 3, 1, 1); s.l = nn.LeakyReLU(0.2, True)

    def forward(s, x):
        f = s.conv_first(x); f = f + s.conv_body(s.body(f))
        f = s.l(s.conv_up1(F.interpolate(f, scale_factor=2, mode="nearest")))
        f = s.l(s.conv_up2(F.interpolate(f, scale_factor=2, mode="nearest")))
        return s.conv_last(s.l(s.conv_hr(f)))


class SRVGG(nn.Module):
    def __init__(s, nf=64, nc=32, up=4):
        super().__init__(); s.up = up
        b = [nn.Conv2d(3, nf, 3, 1, 1), nn.PReLU(nf)]
        for _ in range(nc): b += [nn.Conv2d(nf, nf, 3, 1, 1), nn.PReLU(nf)]
        b += [nn.Conv2d(nf, 3 * up * up, 3, 1, 1)]
        s.body = nn.ModuleList(b); s.ps = nn.PixelShuffle(up)

    def forward(s, x):
        o = x
        for m in s.body: o = m(o)
        return s.ps(o) + F.interpolate(x, scale_factor=s.up, mode="nearest")


def cargar(modelo):
    net, f = (RRDBNet() if modelo == "x4plus" else SRVGG()), pesos(modelo)
    sd = torch.load(f, map_location="cpu", weights_only=True)
    sd = sd.get("params_ema", sd.get("params", sd))
    net.load_state_dict(sd, strict=True); return net.eval()


@torch.no_grad()
def escalar(net, im, tile=256, pad=12):
    a = torch.from_numpy(np.asarray(im.convert("RGB"), dtype=np.float32) / 255).permute(2, 0, 1)[None]
    _, _, h, w = a.shape; out = torch.zeros(1, 3, h * 4, w * 4)
    for y in range(0, h, tile):
        for x in range(0, w, tile):
            y0, x0, y1, x1 = max(y - pad, 0), max(x - pad, 0), min(y + tile + pad, h), min(x + tile + pad, w)
            r = net(a[:, :, y0:y1, x0:x1])
            ty, tx = (y - y0) * 4, (x - x0) * 4
            th, tw = (min(y + tile, h) - y) * 4, (min(x + tile, w) - x) * 4
            out[:, :, y * 4:y * 4 + th, x * 4:x * 4 + tw] = r[:, :, ty:ty + th, tx:tx + tw]
    o = (out[0].clamp(0, 1).permute(1, 2, 0).numpy() * 255).round().astype(np.uint8)
    return Image.fromarray(o)


def hd(src, dst, modelo="x4plus", lado=2600):
    torch.set_num_threads(max(torch.get_num_threads(), 2))
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    big = escalar(cargar(modelo), im)
    s = lado / min(big.size)
    if s < 1: big = big.resize((round(big.width * s), round(big.height * s)), Image.LANCZOS)
    big.save(dst, quality=95, subsampling=0, optimize=True)
    return big.size


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--modelo", default="x4plus", choices=["x4plus", "general"]); ap.add_argument("--lado", type=int, default=2600)
    a = ap.parse_args(); print(hd(a.src, a.dst, a.modelo, a.lado))
