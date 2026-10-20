"""Genera el HTML del correo de aprobación.
Uso: python3 mail.py contenido.json ID "hora" "redes" [insight.txt] > correo.html
"""
import sys, json, html, pathlib

c = json.loads(pathlib.Path(sys.argv[1]).read_text())
ID, hora, redes = sys.argv[2], sys.argv[3], sys.argv[4]
insight = pathlib.Path(sys.argv[5]).read_text() if len(sys.argv) > 5 else ""
B = f"https://raw.githubusercontent.com/laricopola-svg/climatizate-pro-envios/carruseles/carruseles/{ID}/"
n = len(c["slides"])
e = lambda s: html.escape(s)
pre = 'style="white-space:pre-wrap;font-family:Arial,sans-serif;font-size:14px;background:#F4F9FF;padding:12px;border-radius:8px;margin:6px 0 18px"'
h3 = 'style="color:#0B1F33;margin:26px 0 8px;font-size:17px"'

slides = "".join(
    f'<p style="margin:14px 0 4px;font-size:13px;color:#55677A"><b>Lámina {i} de {n}</b></p>'
    f'<img src="{B}4x5_{i:02d}.jpg" width="540" style="width:100%;max-width:540px;border-radius:10px;display:block;border:1px solid #E1E9F2" alt="Lámina {i}">'
    for i in range(1, n + 1))
tiktok = "".join(
    f'<td style="padding:3px"><img src="{B}9x16_{i:02d}.jpg" width="120" style="width:120px;border-radius:8px;display:block" alt="TikTok {i}"></td>'
    + ("</tr><tr>" if i % 4 == 0 else "") for i in range(1, n + 1))

out = f"""<div style="font-family:Arial,sans-serif;color:#0B1F33;max-width:600px;line-height:1.5">
<div style="background:#FFF4E6;border:2px solid #FFD29A;padding:14px 16px;border-radius:10px">
<b style="font-size:16px">Para aprobar, responde este correo solo con OK.</b><br>
Si quieres cambios, responde indicando qué cambiar y no se publicará.<br>
<span style="font-size:14px">Se publicará: <b>{e(hora)}</b> en <b>{e(redes)}</b>.</span></div>

<h2 style="color:#1683E0;margin:22px 0 4px">{e(c['tema'])}</h2>
<p style="margin:0;color:#55677A;font-size:14px">Carrusel de {n} láminas · Si no ves las imágenes, pulsa "Mostrar imágenes".</p>

<h3 {h3}>Así se verá en Instagram</h3>
<img src="{B}ig_preview.jpg" width="320" style="width:320px;max-width:100%;display:block" alt="Vista previa Instagram">

<h3 {h3}>Láminas del carrusel (Instagram y Facebook, en este orden)</h3>
{slides}

<h3 {h3}>Texto que se publicará en Instagram</h3>
<pre {pre}>{e(c['captions']['instagram'])}</pre>
<h3 {h3}>Texto que se publicará en Facebook</h3>
<pre {pre}>{e(c['captions']['facebook'])}</pre>
<h3 {h3}>TikTok (modo fotos, formato vertical)</h3>
<table cellpadding="0" cellspacing="0"><tr>{tiktok}</tr></table>
<pre {pre}>{e(c['captions']['tiktok'])}</pre>
{f'<h3 {h3}>Por qué este tema</h3><p style="font-size:14px">{insight}</p>' if insight else ''}
<p style="font-size:12px;color:#55677A">ID {e(ID)} · Imágenes: <a href="https://github.com/laricopola-svg/climatizate-pro-envios/tree/carruseles/carruseles/{ID}">carpeta en GitHub</a></p>
</div>"""
print(out)
