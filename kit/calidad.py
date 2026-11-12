"""Control de calidad antes de publicar: python3 kit/calidad.py <carpeta> [<carpeta> ...]

Revisa láminas (4x5_NN, 9x16_NN), ig_preview, portada y reel.mp4 y termina con código 1 si algo no
cumple el estándar profesional:
- Tamaño exacto: 4x5 = 1080x1350, 9x16 / portada = 1080x1920 (nada estirado ni con bordes).
- Sin paleta reducida: PNG en RGB/RGBA (nunca modo "P" ni cuantizado), JPG con calidad >= 90 y sin
  submuestreo de color fuerte en láminas (texto nítido).
- Fotos usadas (contenido.json) con versión HD en fotos/hd/ (aviso si no la hay).
- reel.mp4: H.264 High, yuv420p, 1080x1920, 30 fps, >= 3 Mbps de video, audio AAC.
"""
import json, pathlib, re, subprocess, sys
from PIL import Image

TAM = {"4x5": (1080, 1350), "9x16": (1080, 1920), "portada": (1080, 1920)}


STD_LUM = [16, 11, 10, 16, 24, 40, 51, 61, 12, 12, 14, 19, 26, 58, 60, 55, 14, 13, 16, 24, 40, 57, 69, 56,
           14, 17, 22, 29, 51, 87, 80, 62, 18, 22, 37, 56, 68, 109, 103, 77, 24, 35, 55, 64, 81, 104, 113, 92,
           49, 64, 78, 87, 103, 121, 120, 101, 72, 92, 95, 98, 112, 100, 103, 99]


def calidad_jpg(im):
    """Estima la calidad IJG (1-100) a partir de la tabla de cuantización de luminancia."""
    q = getattr(im, "quantization", None)
    if not q:
        return None
    escala = sum(q[0]) / sum(STD_LUM) * 100
    return round(100 - escala / 2) if escala <= 100 else round(5000 / escala)


def revisar(d):
    errores, avisos = [], []
    d = pathlib.Path(d)
    for f in sorted(d.iterdir()):
        k = f.stem.split("_")[0] if f.stem != "portada" else "portada"
        if f.suffix.lower() not in (".png", ".jpg", ".jpeg") or k not in TAM:
            continue
        im = Image.open(f)
        if im.size != TAM[k]:
            errores.append(f"{f.name}: {im.size[0]}x{im.size[1]}, debe ser {TAM[k][0]}x{TAM[k][1]}")
        if f.suffix == ".png" and im.mode not in ("RGB", "RGBA"):
            errores.append(f"{f.name}: PNG en modo {im.mode} (paleta reducida): genera de nuevo sin cuantizar")
        if f.suffix.lower() in (".jpg", ".jpeg"):
            q = calidad_jpg(im)
            if q is not None and q < 88:
                errores.append(f"{f.name}: JPG de calidad ≈{q}, usa quality=95")
            try:
                from PIL import JpegImagePlugin
                ss = JpegImagePlugin.get_sampling(im)
                if ss == 2 and k in ("4x5", "9x16") and d.parent.name == "carruseles":
                    avisos.append(f"{f.name}: submuestreo 4:2:0 (texto menos nítido); usa subsampling=0")
            except Exception:
                pass
    cj = d / "contenido.json"
    if cj.exists():
        data = json.loads(cj.read_text())
        fotos = [s.get("foto") for s in data.get("slides", []) + data.get("escenas", []) if s.get("foto")]
        for p in fotos:
            n = pathlib.Path(p).name
            hd = [x for x in pathlib.Path(__file__).resolve().parent.parent.glob(f"fotos/hd/{n}")]
            if not hd:
                avisos.append(f"{n}: sin versión HD (fotos/hd/); se usará ajuste 'completa' si hace falta agrandar")
    mp4 = d / "reel.mp4"
    if mp4.exists():
        r = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(mp4)],
                           capture_output=True, text=True)
        info = json.loads(r.stdout or "{}")
        v = next((s for s in info.get("streams", []) if s["codec_type"] == "video"), None)
        a = next((s for s in info.get("streams", []) if s["codec_type"] == "audio"), None)
        if not v:
            errores.append("reel.mp4: sin pista de video")
        else:
            if (v["width"], v["height"]) != (1080, 1920):
                errores.append(f"reel.mp4: {v['width']}x{v['height']}, debe ser 1080x1920")
            if v.get("codec_name") != "h264" or v.get("pix_fmt") != "yuv420p":
                errores.append(f"reel.mp4: {v.get('codec_name')}/{v.get('pix_fmt')}, debe ser h264/yuv420p")
            fps = eval(v.get("r_frame_rate", "0/1")) if re.match(r"^\d+/\d+$", v.get("r_frame_rate", "")) else 0
            if abs(fps - 30) > 0.5:
                errores.append(f"reel.mp4: {fps:.2f} fps, debe ser 30")
            br = int(v.get("bit_rate") or info.get("format", {}).get("bit_rate") or 0)
            if br and br < 3_000_000:
                errores.append(f"reel.mp4: {br/1e6:.1f} Mbps de video (mín. 3): no recomprimas el video (usa el de kit/reel.py)")
        if not a:
            errores.append("reel.mp4: sin pista de audio")
    return errores, avisos


if __name__ == "__main__":
    mal = False
    for d in sys.argv[1:]:
        e, w = revisar(d)
        for x in w: print(f"AVISO {d}: {x}")
        for x in e: print(f"ERROR {d}: {x}")
        mal |= bool(e)
        if not e: print(f"OK {d}: calidad profesional")
    sys.exit(1 if mal else 0)
