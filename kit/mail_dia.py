"""Correo de aprobación diario con 1 o 2 piezas (Reel y/o carrusel).

Uso:
  python3 mail_dia.py --dia "hoy miércoles" [--reel reels/<ID>/contenido.json] [--carrusel carruseles/<ID>/contenido.json]
                      [--insight insight.txt] > correo.html
Horas: las toma de "hora" en cada contenido.json (por defecto Reel 19:00, carrusel 12:00).
Incluye la línea de control que lee la tarea publicadora:
  PIEZAS: 1=reel:<ID>@HH:MM · 2=carrusel:<ID>@HH:MM
"""
import argparse, json, html, pathlib

RAW = "https://raw.githubusercontent.com/laricopola-svg/climatizate-pro-envios/carruseles/"
e = html.escape
PRE = 'style="white-space:pre-wrap;font-family:Arial,sans-serif;font-size:14px;background:#F4F9FF;padding:12px;border-radius:8px;margin:6px 0 18px"'
H3 = 'style="color:#0B1F33;margin:22px 0 8px;font-size:16px"'


def caps(c):
    return "".join(f'<h3 {H3}>Texto {red}</h3><pre {PRE}>{e(c["captions"][k])}</pre>'
                   for k, red in (("instagram", "Instagram"), ("facebook", "Facebook"), ("tiktok", "TikTok")) if c["captions"].get(k))


def fila(urls, w=120):
    celdas = "".join(f'<td style="padding:3px"><img src="{u}" width="{w}" style="width:{w}px;border-radius:8px;display:block" alt=""></td>'
                     + ("</tr><tr>" if (i + 1) % 4 == 0 else "") for i, u in enumerate(urls))
    return f'<table cellpadding="0" cellspacing="0"><tr>{celdas}</tr></table>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dia", required=True)
    ap.add_argument("--reel")
    ap.add_argument("--carrusel")
    ap.add_argument("--insight")
    a = ap.parse_args()
    piezas, bloques, n = [], [], 0
    if a.reel:
        c = json.loads(pathlib.Path(a.reel).read_text())
        n += 1
        ID, hora = c.get("id") or c["fecha"], c.get("hora", "19:00")
        B = f"{RAW}reels/{ID}/"
        k = len(c["escenas"])
        piezas.append((n, "reel", ID, hora))
        bloques.append(f"""<div style="border-top:3px solid #1683E0;margin-top:26px;padding-top:10px">
<p style="margin:0;font-size:13px;color:#1683E0;font-weight:bold;letter-spacing:1px">PIEZA {n} · REEL · {e(a.dia)} {e(hora)}</p>
<h2 style="margin:4px 0 6px;font-size:21px">{e(c['tema'])}</h2>
<p style="margin:0 0 10px;font-size:14px;color:#55677A">Instagram: Reel con audio «{e(c.get('audio_ig') or 'sin audio')}» · Facebook: Reel · TikTok: modo fotos con música automática · {k} escenas</p>
<a href="{B}reel.mp4"><img src="{B}portada.jpg" width="260" style="width:260px;border-radius:12px;display:block" alt="Portada del Reel"></a>
<p style="font-size:14px"><a href="{B}reel.mp4"><b>▶ Ver el video completo</b></a> (se abre en el navegador)</p>
<h3 {H3}>Escenas</h3>{fila([f'{B}9x16_{i:02d}.jpg' for i in range(1, k + 1)])}
{caps(c)}</div>""")
    if a.carrusel:
        c = json.loads(pathlib.Path(a.carrusel).read_text())
        n += 1
        ID = c.get("id") or pathlib.Path(a.carrusel).parent.name
        hora = c.get("hora", "12:00")
        B = f"{RAW}carruseles/{ID}/"
        k = len(c["slides"])
        piezas.append((n, "carrusel", ID, hora))
        bloques.append(f"""<div style="border-top:3px solid #F28A1A;margin-top:26px;padding-top:10px">
<p style="margin:0;font-size:13px;color:#F28A1A;font-weight:bold;letter-spacing:1px">PIEZA {n} · CARRUSEL · {e(a.dia)} {e(hora)}</p>
<h2 style="margin:4px 0 6px;font-size:21px">{e(c['tema'])}</h2>
<p style="margin:0 0 10px;font-size:14px;color:#55677A">Instagram y Facebook: carrusel 4:5 · TikTok: modo fotos 9:16 con música automática · {k} láminas</p>
<img src="{B}ig_preview.jpg" width="300" style="width:300px;max-width:100%;display:block" alt="Vista previa">
<h3 {H3}>Láminas</h3>{fila([f'{B}4x5_{i:02d}.jpg' for i in range(1, k + 1)], 130)}
{caps(c)}</div>""")
    if not piezas:
        raise SystemExit("Indica --reel y/o --carrusel")
    control = " · ".join(f"{i}={t}:{ID}@{h}" for i, t, ID, h in piezas)
    opciones = "OK aprueba todo" + ("".join(f" · OK {i} aprueba solo la pieza {i}" for i, *_ in piezas) if len(piezas) > 1 else "")
    insight = pathlib.Path(a.insight).read_text().strip() if a.insight and pathlib.Path(a.insight).exists() else ""
    print(f"""<div style="font-family:Arial,sans-serif;color:#0B1F33;max-width:620px;line-height:1.5">
<div style="background:#FFF4E6;border:2px solid #FFD29A;padding:14px 16px;border-radius:10px">
<b style="font-size:16px">Responde este correo con OK para publicar.</b><br>
{e(opciones)}. Si quieres cambios, escribe qué cambiar y no se publicará.<br>
<span style="font-size:14px">Se publicará {e(a.dia)}: {e(', '.join(f'pieza {i} a las {h}' for i, _, _, h in piezas))} en Instagram, Facebook y TikTok.</span></div>
{''.join(bloques)}
{f'<h3 {H3}>Por qué estos temas</h3><p style="font-size:14px">{e(insight)}</p>' if insight else ''}
<p style="font-size:11px;color:#8899AA;margin-top:24px">PIEZAS: {e(control)}</p>
</div>""")


if __name__ == "__main__":
    main()
