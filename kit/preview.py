"""Genera una vista previa realista de la publicación en Instagram (para el correo de aprobación).

Uso: python3 preview.py contenido.json carpeta_png/ salida.jpg [n_lamina]
Dibuja un teléfono con la publicación tal como se verá en el feed de @climatizatepro:
cabecera con logo, lámina 4:5, puntos del carrusel, íconos y el texto (cortado con "más", como en la app).
"""
import sys, json, base64, pathlib, html
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
FONTS = (ROOT / "assets/fonts").resolve().as_uri()


def b64(p):
    return "data:image/" + ("png" if str(p).endswith("png") else "jpeg") + ";base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()


def main(src, pngdir, out, idx=1):
    c = json.loads(pathlib.Path(src).read_text())
    n = len(c["slides"])
    cap = c["captions"]["instagram"]
    first = html.escape(cap.split("\n")[0])
    lam = b64(pathlib.Path(pngdir) / f"4x5_{idx:02d}.png")
    logo = b64(ROOT / "assets/escudo.png")
    dots = "".join(f'<i class="{"on" if k == idx else ""}"></i>' for k in range(1, min(n, 9) + 1))
    page = f"""<html><head><meta charset=utf-8><style>
@font-face{{font-family:P;src:url({FONTS}/Poppins-Regular.ttf);font-weight:400}}
@font-face{{font-family:P;src:url({FONTS}/poppins-latin-600-normal.woff2);font-weight:600}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:900px;height:1420px;background:linear-gradient(160deg,#EEF6FF,#FFF4E6);display:grid;place-items:center;font-family:-apple-system,"Segoe UI",P,sans-serif}}
.phone{{width:640px;height:1330px;background:#111;border-radius:72px;padding:18px;box-shadow:0 40px 80px rgba(11,31,51,.28)}}
.scr{{width:100%;height:100%;background:#fff;border-radius:56px;overflow:hidden;display:flex;flex-direction:column}}
.status{{height:70px;display:flex;justify-content:space-between;align-items:center;padding:14px 46px 0;font-weight:600;font-size:22px}}
.bar{{height:72px;display:flex;align-items:center;justify-content:space-between;padding:0 26px;border-bottom:1px solid #eee}}
.bar b{{font-family:"Snell Roundhand","Brush Script MT",cursive;font-size:38px;font-weight:600}}
.head{{display:flex;align-items:center;gap:14px;padding:16px 20px}}
.av{{width:58px;height:58px;border-radius:50%;padding:3px;background:linear-gradient(45deg,#F9CE34,#EE2A7B,#6228D7)}}
.av div{{width:100%;height:100%;border-radius:50%;background:#fff url({logo}) center/80% no-repeat;border:2px solid #fff}}
.user{{font-weight:600;font-size:22px}} .user small{{display:block;font-weight:400;font-size:18px;color:#555}}
.dotsm{{margin-left:auto;font-size:30px;letter-spacing:2px}}
.img{{position:relative;width:604px;height:755px;background:#eee}}
.img img{{width:100%;height:100%;display:block}}
.cnt{{position:absolute;top:16px;right:16px;background:rgba(0,0,0,.7);color:#fff;font-size:20px;padding:5px 14px;border-radius:99px}}
.acts{{display:flex;align-items:center;gap:26px;padding:16px 22px 6px;font-size:36px}}
.acts .bm{{margin-left:auto}}
.dots{{display:flex;justify-content:center;gap:6px;margin-top:-34px;margin-bottom:12px}}
.dots i{{width:9px;height:9px;border-radius:50%;background:#c8c8c8}} .dots i.on{{background:#0095F6}}
.likes{{padding:6px 22px;font-weight:600;font-size:22px}}
.cap{{padding:4px 22px;font-size:22px;line-height:1.4}} .cap b{{font-weight:600}} .cap span{{color:#8e8e8e}}
.time{{padding:8px 22px;font-size:18px;color:#8e8e8e}}
.nav{{margin-top:auto;height:96px;border-top:1px solid #eee;display:flex;justify-content:space-around;align-items:center;font-size:34px}}
</style></head><body><div class=phone><div class=scr>
<div class=status><span>10:22</span><span>●●● ▮</span></div>
<div class=bar><b>Instagram</b><span style="display:flex;gap:18px"><svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg><svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 3L10 14"/><path d="M21 3l-7 18-4-7-7-4z"/></svg></span></div>
<div class=head><div class=av><div></div></div><div class=user>climatizatepro<small>Santiago, Chile</small></div><div class=dotsm>···</div></div>
<div class=img><img src="{lam}"><div class=cnt>{idx}/{n}</div></div>
<div class=acts><span><svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg></span><span><svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12a8 8 0 1 1-3.2-6.4A8 8 0 0 1 20 12z"/><path d="M20 20l-2.5-3"/></svg></span><span><svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 3L10 14"/><path d="M21 3l-7 18-4-7-7-4z"/></svg></span><span class=bm><svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12v18l-6-5-6 5z"/></svg></span></div>
<div class=dots>{dots}</div>
<div class=likes>Vista previa · aún no publicado</div>
<div class=cap><b>climatizatepro</b> {first} <span>… más</span></div>
<div class=time>Hace un momento</div>
<div class=nav><span>⌂</span><span>⌕</span><span>⊕</span><span>▷</span><span>◯</span></div>
</div></div></body></html>"""
    tmp = pathlib.Path(out).with_suffix(".html"); tmp.write_text(page)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 900, "height": 1420})
        pg.goto(tmp.resolve().as_uri()); pg.wait_for_timeout(300)
        pg.screenshot(path=str(out), type="jpeg", quality=88); b.close()
    tmp.unlink()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 1)
