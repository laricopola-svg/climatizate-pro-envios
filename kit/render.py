"""Renderiza un carrusel de Climatízate Pro (estilo claro y luminoso).

Uso: python3 render.py contenido.json salida/
Genera en salida/:
  4x5_NN.png   1080x1350  Instagram, Facebook y LinkedIn
  9x16_NN.png  1080x1920  TikTok (modo fotos)
  linkedin.pdf            carrusel tipo documento para LinkedIn (láminas 4:5)
  textos.txt              texto de cada lámina + publicación por red, listo para copiar
"""
import json, sys, base64, pathlib, re
from playwright.sync_api import sync_playwright
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).parent))
try:
    from ilus import ILUS  # ilustraciones SVG (kit/ilus.py)
except ImportError:
    ILUS = {}

ROOT = pathlib.Path(__file__).parent
MARCA = {
    "web": "climatizatepro.cl",
    "whatsapp": "+56 9 6190 7601",
    "eslogan": "Calcula. Visualiza. Cotiza. Climatiza.",
}
ESCUDO = "data:image/png;base64," + base64.b64encode((ROOT / "assets/escudo.png").read_bytes()).decode()
BASE = ROOT
FONTS = (ROOT / "assets/fonts").resolve().as_uri()

CSS = """
@font-face{font-family:P;src:url(FONTS/Poppins-Regular.ttf);font-weight:400}
@font-face{font-family:P;src:url(FONTS/Poppins-Medium.ttf);font-weight:500}
@font-face{font-family:P;src:url(FONTS/poppins-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:P;src:url(FONTS/Poppins-Bold.ttf);font-weight:700}
@font-face{font-family:P;src:url(FONTS/poppins-latin-800-normal.woff2);font-weight:800}
:root{--navy:#0B1F33;--txt:#0B1F33;--mut:#55677A;--azul:#1683E0;--cielo:#5BB8FF;--naranja:#F28A1A;--fuego:#EE5A24;
 --card:rgba(255,255,255,.78);--borde:rgba(11,31,51,.07)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:var(--h);font-family:P,sans-serif;color:var(--txt);overflow:hidden;background:#fff}
.s{position:relative;width:1080px;height:var(--h);padding:var(--pt) 88px var(--pb);display:flex;flex-direction:column;overflow:hidden;
 background:linear-gradient(165deg,#FFFFFF 0%,#F1F8FF 50%,#FFF6EA 100%)}
.glow{position:absolute;border-radius:50%;filter:blur(90px);z-index:0}
.g1{width:720px;height:720px;right:-260px;top:-240px;background:rgba(91,184,255,.45)}
.g2{width:620px;height:620px;left:-280px;bottom:-260px;background:rgba(255,190,100,.42)}
.g3{width:380px;height:380px;right:-120px;bottom:22%;background:rgba(22,131,224,.14)}
.aire{position:absolute;inset:0;z-index:0;opacity:.55}
.s>*:not(.glow):not(.aire){position:relative;z-index:1}
.top{display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:14px;font-weight:800;font-size:27px;letter-spacing:.4px;color:var(--navy)}
.brand img{width:58px;height:auto;filter:drop-shadow(0 6px 14px rgba(11,31,51,.18))}
.brand b{background:linear-gradient(135deg,#1E6FD0,#0D4B85);border-radius:8px;padding:1px 10px;font-size:22px;color:#fff}
.num{font-weight:600;font-size:24px;color:var(--mut);background:var(--card);border:1px solid var(--borde);border-radius:99px;padding:6px 18px}
.body{flex:1;display:flex;flex-direction:column;justify-content:center}
.kicker{display:inline-flex;align-self:flex-start;align-items:center;gap:12px;font-weight:700;font-size:25px;letter-spacing:2.5px;text-transform:uppercase;
 color:var(--azul);background:rgba(22,131,224,.09);border:1px solid rgba(22,131,224,.18);padding:10px 22px;border-radius:99px;margin-bottom:26px}
.kicker::before{content:'';width:12px;height:12px;border-radius:50%;background:linear-gradient(135deg,var(--cielo),var(--naranja))}
h1{font-weight:800;font-size:94px;line-height:1.02;letter-spacing:-2px;color:var(--navy)}
h2{font-weight:800;font-size:66px;line-height:1.07;letter-spacing:-1.2px;margin-bottom:34px;color:var(--navy)}
.f{background:linear-gradient(90deg,#1683E0,#38A8FF);-webkit-background-clip:text;color:transparent}
.c{background:linear-gradient(90deg,#F7A325,#EE5A24);-webkit-background-clip:text;color:transparent}
p.lead{font-size:36px;line-height:1.42;color:var(--mut);margin-top:28px}
.items{display:flex;flex-direction:column;gap:20px}
.it{display:flex;gap:26px;align-items:flex-start;background:var(--card);border:1px solid var(--borde);border-radius:28px;padding:28px 32px;
 box-shadow:0 18px 44px rgba(22,90,160,.10)}
.ic{flex:none;width:66px;height:66px;border-radius:20px;display:grid;place-items:center;font-weight:800;font-size:30px;color:#fff;
 background:linear-gradient(135deg,#4FB3FF,#1565C0);box-shadow:0 10px 22px rgba(22,131,224,.35)}
.it.hot .ic{background:linear-gradient(135deg,#FFBE55,#F0641F);box-shadow:0 10px 22px rgba(240,120,31,.35)}
.it h3{font-weight:700;font-size:35px;line-height:1.2}
.it p{font-size:28px;line-height:1.42;color:var(--mut);margin-top:6px}
table{width:100%;border-collapse:separate;border-spacing:0 14px;font-size:36px}
td{background:var(--card);padding:26px 32px;border-top:1px solid var(--borde);border-bottom:1px solid var(--borde)}
tr{filter:drop-shadow(0 12px 22px rgba(22,90,160,.09))}
td:first-child{border-left:1px solid var(--borde);border-radius:24px 0 0 24px;font-weight:600}
td:last-child{border-right:1px solid var(--borde);border-radius:0 24px 24px 0;text-align:right;font-weight:800;color:var(--azul)}
.note{font-size:26px;color:var(--mut);margin-top:22px;line-height:1.45}
.vs{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.col{border-radius:30px;padding:34px;background:var(--card);border:1px solid var(--borde);box-shadow:0 18px 44px rgba(22,90,160,.10)}
.col h3{font-weight:800;font-size:40px;margin-bottom:18px}
.col.a{background:linear-gradient(160deg,#FFFFFF,#E3F2FF);border:2px solid rgba(22,131,224,.45)} .col.a h3{color:var(--azul)}
.col.b h3{color:var(--mut)}
.col li{font-size:29px;line-height:1.4;margin:0 0 14px 30px;color:#33475B}
.hero{display:flex;flex-direction:column;align-items:flex-start}
.big{width:290px;height:auto;margin:0 0 36px;filter:drop-shadow(0 26px 40px rgba(11,31,51,.25))}
.cta{margin-top:40px;display:inline-flex;align-items:center;gap:18px;background:linear-gradient(90deg,#1E8BEA,#1262C0);color:#fff;
 padding:28px 48px;border-radius:999px;font-weight:800;font-size:38px;box-shadow:0 18px 40px rgba(22,131,224,.40)}
.wa{margin-top:22px;font-size:32px;font-weight:600;color:var(--navy)}
.wa span{color:#1FA855}
.slogan{margin-top:26px;font-size:26px;font-weight:600;letter-spacing:.5px;color:var(--mut)}
.ilus{background:#fff;border:1px solid var(--borde);border-radius:30px;padding:14px;box-shadow:0 18px 44px rgba(22,90,160,.10);margin-top:-6px}
.ilus svg{display:block;width:100%;height:auto;border-radius:20px}
.pts{display:flex;flex-direction:column;gap:12px;margin-top:26px}
.pts div{display:flex;gap:16px;align-items:flex-start;font-size:29px;line-height:1.38;color:#33475B}
.pts div::before{content:'';flex:none;width:14px;height:14px;margin-top:14px;border-radius:50%;background:linear-gradient(135deg,var(--cielo),var(--azul))}
.precio{margin-top:24px;align-self:flex-start;display:flex;align-items:center;gap:20px;background:linear-gradient(90deg,#0D4B85,#1683E0);color:#fff;
 border-radius:24px;padding:16px 30px 16px 26px;box-shadow:0 16px 36px rgba(22,131,224,.32)}
.precio b{font-size:46px;font-weight:800;letter-spacing:-.5px}
.precio span{font-size:24px;line-height:1.3;opacity:.92}
h2.sm{font-size:58px;margin-bottom:24px}
.s.ph{padding:0;background:#0B1F33}
.s.ph>.bg{position:absolute!important;inset:0;width:100%;height:100%;object-fit:cover;z-index:0}
.s.ph>.shade{position:absolute!important;inset:0;z-index:0!important;background:linear-gradient(180deg,rgba(11,31,51,.40) 0%,rgba(11,31,51,0) 22%,rgba(11,31,51,0) 48%,rgba(11,31,51,.86) 100%)}
.s.ph>.inner{position:relative;z-index:1;height:100%;width:100%;display:flex;flex-direction:column;padding:var(--pt) 72px var(--pb)}
.ph .badge{display:inline-flex;align-items:center;gap:12px;align-self:flex-start;background:rgba(255,255,255,.92);border-radius:99px;padding:10px 24px 10px 12px;
 font-weight:800;font-size:25px;color:#0B1F33;box-shadow:0 10px 30px rgba(0,0,0,.18)}
.ph .badge img{width:46px;height:auto}
.ph .badge b{background:linear-gradient(135deg,#1E6FD0,#0D4B85);color:#fff;border-radius:7px;padding:0 9px;font-size:20px}
.ph .real{margin-left:auto;align-self:flex-start;background:rgba(11,31,51,.62);color:#fff;font-weight:600;font-size:22px;border-radius:99px;padding:10px 20px;border:1px solid rgba(255,255,255,.35)}
.ph .tophd{display:flex;align-items:flex-start}
.ph .txt{margin-top:auto;color:#fff}
.ph .txt .k{font-weight:700;font-size:24px;letter-spacing:2.5px;text-transform:uppercase;color:#9ED4FF;margin-bottom:12px}
.ph .txt h2{color:#fff;font-size:62px;margin-bottom:14px;text-shadow:0 4px 24px rgba(0,0,0,.35)}
.ph .txt p{font-size:30px;line-height:1.4;color:#E6EEF6;max-width:880px}
.ph .bar{margin-top:26px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.ph .wa{display:inline-flex;align-items:center;gap:12px;background:#1FA855;color:#fff;font-weight:800;font-size:30px;border-radius:99px;padding:14px 28px;margin:0;box-shadow:0 12px 30px rgba(31,168,85,.4)}
.ph .web{font-weight:700;font-size:27px;color:#fff;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.4);border-radius:99px;padding:12px 24px}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:25px;color:var(--mut);font-weight:500}
.foot b{color:var(--navy);font-weight:700}
.swipe{font-weight:700;color:var(--navy);background:var(--card);border:1px solid var(--borde);border-radius:99px;padding:8px 22px}
.swipe span{color:var(--naranja)}
"""

AIRE = """<svg class=aire viewBox="0 0 1080 1350" preserveAspectRatio="none"><g fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round">
<path d="M-40 300 C 240 220, 420 380, 700 300 S 1060 220, 1140 280"/><path d="M-40 360 C 260 290, 440 450, 720 360 S 1060 300, 1140 340" opacity=".7"/>
<path d="M-40 1080 C 260 1010, 480 1150, 760 1070 S 1060 1010, 1140 1050" opacity=".8"/></g></svg>"""


def slide(s, i, n):
    t = s["tipo"]
    if t == "portada":
        body = f"""<div class=hero><img class=big src="{ESCUDO}"><div class=kicker>{s.get('kicker','')}</div>
        <h1>{s['titulo']}</h1><p class=lead>{s.get('texto','')}</p></div>"""
    elif t == "lista":
        its = "".join(f"""<div class="it {'hot' if x.get('calor') else ''}"><div class=ic>{x.get('icono', k+1)}</div>
        <div><h3>{x['t']}</h3>{f"<p>{x['d']}</p>" if x.get('d') else ''}</div></div>""" for k, x in enumerate(s["items"]))
        body = f"<div class=kicker>{s.get('kicker','')}</div><h2>{s['titulo']}</h2><div class=items>{its}</div>"
    elif t == "tabla":
        rows = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in s["filas"])
        body = f"""<div class=kicker>{s.get('kicker','')}</div><h2>{s['titulo']}</h2><table>{rows}</table>
        <p class=note>{s.get('nota','')}</p>"""
    elif t == "versus":
        a, b = s["a"], s["b"]
        li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
        body = f"""<div class=kicker>{s.get('kicker','')}</div><h2>{s['titulo']}</h2><div class=vs>
        <div class="col a"><h3>{a['t']}</h3><ul>{li(a['xs'])}</ul></div>
        <div class="col b"><h3>{b['t']}</h3><ul>{li(b['xs'])}</ul></div></div><p class=note>{s.get('nota','')}</p>"""
    elif t == "ilustracion":
        svg = ILUS[s["dibujo"]]() if s.get("dibujo") in ILUS else ""
        pts = "".join(f"<div>{x}</div>" for x in s.get("puntos", []))
        pr = f"<div class=precio><b>{s['precio']}</b><span>{s.get('precio_det','')}</span></div>" if s.get("precio") else ""
        body = f"""<div class=kicker>{s.get('kicker','')}</div><h2 class=sm>{s['titulo']}</h2><div class=ilus>{svg}</div>
        <div class=pts>{pts}</div>{pr}"""
    elif t == "foto":
        fp = (BASE / s["foto"]) if not pathlib.Path(s["foto"]).is_absolute() else pathlib.Path(s["foto"])
        bg = "data:image/jpeg;base64," + base64.b64encode(fp.read_bytes()).decode()
        pos = s.get("pos", "center")
        txt = ""
        if s.get("titulo") or s.get("texto"):
            txt = (f"<div class=k>{s.get('kicker','')}</div>" if s.get("kicker") else "") + \
                  (f"<h2>{s['titulo']}</h2>" if s.get("titulo") else "") + (f"<p>{s['texto']}</p>" if s.get("texto") else "")
        wa = '<svg width="30" height="30" viewBox="0 0 24 24" fill="#fff"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2.1 1-2.4c.3-.3.6-.3.8-.3h.6c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.7-.1l1.9.9c.3.1.5.2.5.3.1.2.1.6-.1 1.1z"/></svg>'
        return f"""<div class="s ph"><img class=bg src="{bg}" style="object-position:{pos}"><div class=shade></div>
        <div class=inner><div class=tophd><div class=badge><img src="{ESCUDO}">CLIMATÍZATE <b>PRO</b></div>
        {f'<div class=real>{s.get("etiqueta","Instalación real · Santiago")}</div>' if s.get("etiqueta", True) else ''}</div>
        <div class=txt>{txt}<div class=bar><span class=wa>{wa}{MARCA['whatsapp']}</span><span class=web>{MARCA['web']}</span></div></div></div></div>"""
    elif t == "cta":
        body = f"""<div class=hero><img class=big src="{ESCUDO}"><div class=kicker>{s.get('kicker','')}</div>
        <h1 style="font-size:78px">{s['titulo']}</h1><p class=lead>{s.get('texto','')}</p>
        <div class=cta>{s.get('boton', 'Cotiza en ' + MARCA['web'])}</div>
        <div class=wa>WhatsApp <span>{MARCA['whatsapp']}</span></div><div class=slogan>{MARCA['eslogan']}</div></div>"""
    swipe = "<span class=swipe>Desliza <span>→</span></span>" if i < n else "<span class=swipe>Guárdalo <span>★</span></span>"
    return f"""<div class=s><div class="glow g1"></div><div class="glow g2"></div><div class="glow g3"></div>{AIRE}
    <div class=top><div class=brand><img src="{ESCUDO}">CLIMATÍZATE <b>PRO</b></div><div class=num>{i:02d}/{n:02d}</div></div>
    <div class=body>{body}</div>
    <div class=foot><span><b>{MARCA['web']}</b> · Santiago</span>{swipe}</div></div>"""


FORMATOS = {"4x5": (1350, 72, 64), "9x16": (1920, 230, 330)}  # alto, padding sup, padding inf (zonas seguras TikTok)


def plano(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


def textos(data):
    out = [f"TEMA: {data['tema']}", ""]
    for i, s in enumerate(data["slides"], 1):
        out.append(f"--- Lámina {i} ({s['tipo']}) ---")
        for k in ("kicker", "titulo", "texto"):
            if s.get(k): out.append(plano(s[k]))
        for x in s.get("items", []): out.append(f"• {plano(x['t'])}" + (f": {plano(x['d'])}" if x.get("d") else ""))
        for a, b in s.get("filas", []): out.append(f"• {a} → {b}")
        for lado in ("a", "b"):
            if s.get(lado): out.append(f"{s[lado]['t']}: " + " / ".join(s[lado]["xs"]))
        for x in s.get("puntos", []): out.append(f"• {plano(x)}")
        if s.get("precio"): out.append(f"Valor: {s['precio']} ({s.get('precio_det','')})")
        if s.get("nota"): out.append(plano(s["nota"]))
        if s["tipo"] == "cta": out.append(f"{s.get('boton', 'Cotiza en ' + MARCA['web'])} · WhatsApp {MARCA['whatsapp']}")
        out.append("")
    nombres = {"instagram": "INSTAGRAM", "facebook": "FACEBOOK", "tiktok": "TIKTOK", "linkedin": "LINKEDIN"}
    for red, nombre in nombres.items():
        if data.get("captions", {}).get(red):
            out += [f"===== PUBLICACIÓN {nombre} =====", data["captions"][red], ""]
    return "\n".join(out)


def main(src, out):
    global BASE
    BASE = pathlib.Path(src).resolve().parent
    data = json.loads(pathlib.Path(src).read_text())
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    n = len(data["slides"])
    with sync_playwright() as p:
        b = p.chromium.launch()
        for fmt, (h, pt, pb) in FORMATOS.items():
            pg = b.new_page(viewport={"width": 1080, "height": h})
            for i, s in enumerate(data["slides"], 1):
                doc = (f"<html><head><meta charset=utf-8><style>{CSS.replace('FONTS', FONTS)}"
                       f":root{{--h:{h}px;--pt:{pt}px;--pb:{pb}px}}</style></head><body>{slide(s, i, n)}</body></html>")
                f = out / "tmp.html"; f.write_text(doc)
                pg.goto(f.resolve().as_uri()); pg.wait_for_load_state("load"); pg.wait_for_timeout(300)
                pg.screenshot(path=str(out / f"{fmt}_{i:02d}.png"))
            pg.close()
        b.close()
    (out / "tmp.html").unlink()
    imgs = [Image.open(out / f"4x5_{i:02d}.png").convert("RGB") for i in range(1, n + 1)]
    imgs[0].save(out / "linkedin.pdf", save_all=True, append_images=imgs[1:], resolution=144)
    (out / "textos.txt").write_text(textos(data))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
