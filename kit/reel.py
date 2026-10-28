"""Genera un Reel/TikTok vertical (1080x1920) de Climatízate Pro.

Uso: python3 reel.py spec.json salida/
spec.json:
{
 "tema": "...",
 "escenas": [
   {"foto": "/ruta/foto.jpg" | null, "pos": [0.5, 0.4],   # centro del encuadre (x,y 0-1)
    "titulo": "Texto grande (gancho o idea)", "sub": "texto secundario opcional",
    "chip": "1 · ECO+" (opcional), "dur": 2.6, "zoom": "in" | "out"}
 ],
 "nota": "Funciones según modelo y control",   # letra chica opcional (última escena)
 "etiqueta": "Instalación real"   # etiqueta arriba a la derecha en escenas con foto (o "Imagen referencial" si es IA)
}
Genera en salida/: reel.mp4 (H.264 + pista de audio silenciosa, 30 fps), portada.jpg,
y 9x16_NN.jpg (un fotograma final por escena, para TikTok modo fotos).
Zonas seguras: el texto queda entre y=300 y y=1450 (arriba y abajo quedan libres para la interfaz).
Voz en off: si existe salida/voz/voz.json (kit/voz_local.py, voz fija M2), cada escena dura exactamente su
locución (+0,15 s de entrada y 0,4 s de respiro), aparecen subtítulos palabra a palabra sincronizados con la voz
(la palabra dicha en naranjo) y la voz se mezcla con EQ, compresión suave y un toque de sala, a -14 LUFS.
"""
import json, sys, subprocess, pathlib, math, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = pathlib.Path(__file__).parent
W, H, FPS = 1080, 1920, 30
F = ROOT / "assets/fonts"
NAVY, AZUL, NAR, BLANCO = (11, 31, 51), (22, 131, 224), (242, 138, 26), (255, 255, 255)


def font(n, s):
    return ImageFont.truetype(str(F / n), s)


FT = font("Poppins-Bold.ttf", 84)
FS = font("Poppins-Medium.ttf", 44)
FC = font("Poppins-Bold.ttf", 40)
FN = font("Poppins-Regular.ttf", 28)
FB = font("Poppins-Bold.ttf", 34)
FSUB = font("Poppins-Bold.ttf", 60)
VOZ_INICIO, VOZ_COLA = 0.15, 0.40  # la voz entra 0,15 s después del corte y deja 0,4 s de respiro
LOGO = Image.open(ROOT / "assets/escudo.png").convert("RGBA")
LOGO = LOGO.resize((120, int(120 * LOGO.height / LOGO.width)), Image.LANCZOS)


def wrap(d, txt, f, maxw):
    lines = []
    for par in txt.split("\n"):
        cur = ""
        for w in par.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) <= maxw:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def fondo(sc):
    if sc.get("foto"):
        im = Image.open(sc["foto"]).convert("RGB")
        s = max(W / im.width, H / im.height) * 1.18  # margen para el zoom
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        return im
    # fondo de marca: degradado azul -> naranjo suave
    g = Image.new("RGB", (int(W * 1.18), int(H * 1.18)))
    d = ImageDraw.Draw(g)
    for y in range(g.height):
        t = y / g.height
        c = tuple(int(a + (b - a) * t) for a, b in zip((235, 245, 255), (255, 240, 222)))
        d.line([(0, y), (g.width, y)], fill=c)
    g = g.filter(ImageFilter.GaussianBlur(2))
    return g


def encuadre(bg, sc, p):
    """Ken Burns: p de 0 a 1."""
    z0, z1 = (1.0, 1.12) if sc.get("zoom", "in") == "in" else (1.12, 1.0)
    z = z0 + (z1 - z0) * (0.5 - 0.5 * math.cos(math.pi * p))
    cw, ch = bg.width / 1.18 / z, bg.height / 1.18 / z
    px, py = sc.get("pos", [0.5, 0.5])
    x = min(max(px * bg.width - cw / 2, 0), bg.width - cw)
    y = min(max(py * bg.height - ch / 2, 0), bg.height - ch)
    return bg.crop((int(x), int(y), int(x + cw), int(y + ch))).resize((W, H), Image.BILINEAR)


def capa_texto(sc, idx, total, nota):
    """Devuelve (capa RGBA, alto) con chip + título + sub en una tarjeta."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    maxw = W - 2 * 110
    tl = wrap(tmp, sc.get("titulo", ""), FT, maxw)
    sl = wrap(tmp, sc["sub"], FS, maxw) if sc.get("sub") else []
    h = 70 + (78 if sc.get("chip") else 0) + len(tl) * 98 + (24 + len(sl) * 60 if sl else 0) + 50
    card = Image.new("RGBA", (W - 2 * 60, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([0, 0, card.width - 1, h - 1], 44, fill=(255, 255, 255, 236))
    y = 50
    x = 50
    if sc.get("chip"):
        cw = d.textlength(sc["chip"], font=FC) + 56
        d.rounded_rectangle([x, y, x + cw, y + 62], 31, fill=AZUL if idx % 2 else NAR)
        d.text((x + 28, y + 6), sc["chip"], font=FC, fill=BLANCO)
        y += 78
    for l in tl:
        d.text((x, y), l, font=FT, fill=NAVY)
        y += 98
    if sl:
        y += 24
        for l in sl:
            d.text((x, y), l, font=FS, fill=(55, 75, 95))
            y += 60
    return card


def marca(fr, idx, total, nota, ultima, foto=True, etiqueta=None):
    d = ImageDraw.Draw(fr)
    on = (255, 255, 255, 235) if foto else NAVY + (235,)
    off = (255, 255, 255, 110) if foto else NAVY + (60,)
    if foto and etiqueta:
        ew = d.textlength(etiqueta, font=FN)
        d.rounded_rectangle([W - 60 - ew - 36, 182, W - 60, 230], 24, fill=(11, 31, 51, 190))
        d.text((W - 60 - ew - 18, 189), etiqueta, font=FN, fill=BLANCO)
    # logo + nombre arriba (zona segura superior ~ y=150)
    fr.alpha_composite(LOGO, (60, 150))
    d.rounded_rectangle([196, 176, 196 + d.textlength("Climatízate Pro", font=FB) + 40, 236], 30, fill=(255, 255, 255, 225))
    d.text((216, 182), "Climatízate Pro", font=FB, fill=NAVY)
    # barra de progreso (favorece ver hasta el final)
    x0, x1, y = 60, W - 60, 296
    seg = (x1 - x0 - (total - 1) * 10) / total
    for i in range(total):
        a = x0 + i * (seg + 10)
        d.rounded_rectangle([a, y, a + seg, y + 10], 5, fill=on if i <= idx else off)
    if ultima:
        t = "climatizatepro.cl · WhatsApp +56 9 6190 7601"
        tw = d.textlength(t, font=FS)
        d.rounded_rectangle([(W - tw) / 2 - 30, 1530, (W + tw) / 2 + 30, 1606], 38, fill=NAVY + (240,))
        d.text(((W - tw) / 2, 1540), t, font=FS, fill=BLANCO)
        if nota:
            nw = d.textlength(nota, font=FN)
            d.text(((W - nw) / 2, 1620), nota, font=FN, fill=(255, 255, 255, 235) if foto else (55, 75, 95), stroke_width=2 if foto else 0, stroke_fill=(0, 0, 0, 160))


def tiempos_palabras(texto, inicio, dur):
    """Reparte la duración real de la locución entre las palabras (por largo + pausas de puntuación)."""
    pals = texto.split()
    pesos = [len(re.sub(r"\W", "", w)) + 2 + (4 if re.search(r"[.?!…:]$", w) else 2 if w.endswith(",") else 0) for w in pals]
    tot, t, res = sum(pesos) or 1, inicio, []
    for w, pz in zip(pals, pesos):
        d = dur * pz / tot
        res.append((w, t, t + d))
        t += d
    return res


def trozos(pals, maxp=4):
    """Agrupa en bloques de hasta 4 palabras, cortando en la puntuación (estilo subtítulo de TikTok)."""
    g, cur = [], []
    for i, p in enumerate(pals):
        cur.append(i)
        if len(cur) >= maxp or re.search(r"[.,?!…:]$", p[0]):
            g.append(cur)
            cur = []
    if cur:
        g.append(cur)
    return g


def subtitulo(fr, pals, grupos, t, y):
    """Dibuja el bloque de palabras que se está diciendo; la palabra actual va en naranjo."""
    act = next((i for i, (_, a, b) in enumerate(pals) if a <= t < b), None)
    if act is None:
        if not pals or t < pals[0][1]:
            return
        act = len(pals) - 1 if t >= pals[-1][2] - 0.01 else None
        if act is None:
            return
    g = next(gr for gr in grupos if act in gr)
    d = ImageDraw.Draw(fr)
    ws = [pals[i][0] for i in g]
    esp = d.textlength(" ", font=FSUB)
    anchos = [d.textlength(w, font=FSUB) for w in ws]
    total = sum(anchos) + esp * (len(ws) - 1)
    x = (W - total) / 2
    for i, w, a in zip(g, ws, anchos):
        col = NAR if i == act else BLANCO
        d.text((x, y), w, font=FSUB, fill=col, stroke_width=7, stroke_fill=(11, 31, 51))
        x += a + esp


def mezclar_voz(out, esc, voz):
    """Pista de voz: cada locución empieza 0,15 s después de su escena; resto en silencio."""
    partes, ins = [], []
    for i, (sc, v) in enumerate(zip(esc, voz)):
        d = int(sc.get("dur", 2.6) * FPS) / FPS
        if v:
            ins += ["-i", str(out / "voz" / v["archivo"])]
            k = len(ins) // 2 - 1
            partes.append(f"[{k}:a]aformat=sample_rates=44100:channel_layouts=stereo,adelay={int(VOZ_INICIO*1000)}|{int(VOZ_INICIO*1000)},apad,atrim=0:{d:.3f},asetpts=N/SR/TB[s{i}]")
        else:
            partes.append(f"anullsrc=channel_layout=stereo:sample_rate=44100,atrim=0:{d:.3f}[s{i}]")
    cadena = "".join(f"[s{i}]" for i in range(len(esc)))
    filtro = ";".join(partes) + f";{cadena}concat=n={len(esc)}:v=0:a=1,"
    # cadena "de estudio": limpia graves, quita sibilancia, calidez + presencia, compresión suave y un toque de sala
    filtro += ("highpass=f=80,deesser=i=0.35,equalizer=f=180:t=q:w=1:g=2,equalizer=f=3200:t=q:w=1.4:g=1.5,"
               "acompressor=threshold=-21dB:ratio=2.2:attack=10:release=150:makeup=2,"
               "aecho=0.85:0.5:18|32:0.08|0.05[voz]")
    tmp = out / "reel_mudo.mp4"
    wav = out / "voz_mezcla.wav"
    # 1) pista de voz procesada
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", filtro, "-map", "[voz]", "-ar", "44100", str(wav)])
    if r.returncode:
        print("AVISO: no se pudo procesar la voz; el Reel queda sin voz")
        return
    # 2) medir sonoridad real y llevarla a -14 LUFS (estándar de Reels/TikTok) con limitador
    m = subprocess.run(["ffmpeg", "-i", str(wav), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    i_lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1])
    gan = max(-6.0, min(18.0, -14.0 - i_lufs))
    (out / "reel.mp4").rename(tmp)
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-i", str(wav), "-filter_complex",
                        f"[1:a]volume={gan:.2f}dB,alimiter=limit=0.79:attack=5:release=50:level=false[a]",
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest",
                        "-movflags", "+faststart", str(out / "reel.mp4")])
    wav.unlink(missing_ok=True)
    if r.returncode:
        tmp.rename(out / "reel.mp4")
        print("AVISO: no se pudo mezclar la voz; el Reel queda sin voz")
    else:
        tmp.unlink()
        print(f"OK voz mezclada (ganancia {gan:+.1f} dB)")


def main(spec_path, out):
    spec = json.loads(pathlib.Path(spec_path).read_text())
    out = pathlib.Path(out)
    out.mkdir(parents=True, exist_ok=True)
    esc = spec["escenas"]
    nota = spec.get("nota", "")
    vj = out / "voz" / "voz.json"
    voz = json.loads(vj.read_text())["escenas"] if vj.exists() else None
    if voz:
        for sc, v in zip(esc, voz):
            if v:
                sc["dur"] = round(VOZ_INICIO + v["dur"] + VOZ_COLA, 3)
        esc[-1]["dur"] = max(esc[-1]["dur"], esc[-1]["dur"] + 0.6)  # cierre: un respiro antes del loop
    total_frames = sum(int(s.get("dur", 2.6) * FPS) for s in esc)
    dur = total_frames / FPS
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-t", f"{dur:.2f}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "128k", "-shortest", str(out / "reel.mp4")]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i, sc in enumerate(esc):
        bg = fondo(sc)
        con_voz = bool(voz and voz[i])
        card = capa_texto(dict(sc, sub=None) if con_voz and i < len(esc) - 1 else sc, i, len(esc), nota)
        n = int(sc.get("dur", 2.6) * FPS)
        ultima = i == len(esc) - 1
        cy = sc.get("y", 1440 - card.height if sc.get("foto") else (H - card.height) // 2)
        cy = max(300, min(cy, 1450 - card.height))
        pals = tiempos_palabras(sc.get("voz", ""), VOZ_INICIO, voz[i]["dur"]) if con_voz else []
        grupos = trozos(pals)
        ysub = (cy - 120) if ultima or not sc.get("foto") else 1462
        last = None
        for k in range(n):
            p = k / max(n - 1, 1)
            fr = encuadre(bg, sc, p).convert("RGBA")
            # oscurecer suave arriba/abajo para legibilidad del logo y barra
            # animación de entrada de la tarjeta (0.25 s): sube + aparece
            a = min(1, k / (FPS * 0.25))
            ease = 1 - (1 - a) ** 3
            c = card.copy()
            if ease < 1:
                c.putalpha(c.getchannel("A").point(lambda v: int(v * ease)))
            fr.alpha_composite(c, (60, int(cy + 60 * (1 - ease))))
            marca(fr, i, len(esc), nota, ultima, bool(sc.get('foto')), sc.get('etiqueta', spec.get('etiqueta')))
            if pals:
                subtitulo(fr, pals, grupos, k / FPS, ysub)
            rgb = fr.convert("RGB")
            ff.stdin.write(rgb.tobytes())
            last = rgb
        last.save(out / f"9x16_{i + 1:02d}.jpg", quality=92)
        if i == 0:
            last.save(out / "portada.jpg", quality=92)
    ff.stdin.close()
    ff.wait()
    if ff.returncode:
        sys.exit("ffmpeg falló")
    if voz:
        mezclar_voz(out, esc, voz)
    print(f"OK {out/'reel.mp4'} {dur:.1f}s, {len(esc)} escenas")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
