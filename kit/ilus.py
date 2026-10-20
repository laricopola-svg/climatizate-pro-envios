"""Ilustraciones SVG de Climatízate Pro (estilo claro). Se insertan en render.py."""

NAVY = "#0B1F33"; MUT = "#55677A"; AZUL = "#1683E0"; NAR = "#F28A1A"; VERDE = "#1FA855"
COBRE = "#C9783A"; COBRE2 = "#EBA46B"; CABLE = "#3B4E63"; BORDE = "#AFC2D6"

DEFS = """<defs>
<pattern id="hatch" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<rect width="14" height="14" fill="#E6EDF5"/><line x1="0" y1="0" x2="0" y2="14" stroke="#C7D5E3" stroke-width="5"/></pattern>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#DDF0FF"/><stop offset="1" stop-color="#F6FBFF"/></linearGradient>
<linearGradient id="calido" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFBE55"/><stop offset="1" stop-color="#F0641F"/></linearGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="8" stdDeviation="9" flood-color="#165AA0" flood-opacity=".16"/></filter>
</defs>"""


def txt(x, y, s, size=22, w=600, color=NAVY, anchor="start", ls=0):
    return f'<text x="{x}" y="{y}" font-family="P" font-size="{size}" font-weight="{w}" fill="{color}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>'


def interior(x, y, w=280, h=86):
    return (f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#fff" stroke="{BORDE}" stroke-width="2.5"/></g>'
            f'<rect x="{x+22}" y="{y+h-24}" width="{w-44}" height="7" rx="3.5" fill="#D5E2EE"/>'
            f'<circle cx="{x+w-26}" cy="{y+22}" r="5" fill="{AZUL}"/>')


def exterior(x, y, w=200, h=150):
    r = h * 0.32; cx = x + w * 0.42; cy = y + h / 2
    vents = "".join(f'<line x1="{x+w-46+k*11}" y1="{y+24}" x2="{x+w-46+k*11}" y2="{y+h-24}" stroke="#C3D1DF" stroke-width="4" stroke-linecap="round"/>' for k in range(3))
    return (f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#F4F7FA" stroke="{BORDE}" stroke-width="2.5"/></g>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="#B8C7D6" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.18}" fill="#B8C7D6"/>'
            f'<path d="M{cx} {cy-r*0.8} L{cx} {cy+r*0.8} M{cx-r*0.8} {cy} L{cx+r*0.8} {cy}" stroke="#D2DDE8" stroke-width="3"/>{vents}')


def tuberia(d, dash=False, color=COBRE):
    if dash:
        return f'<path d="{d}" fill="none" stroke="{NAR}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="16 11"/>'
    return (f'<path d="{d}" fill="none" stroke="{CABLE}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" transform="translate(-13 13)"/>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{COBRE2}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


def pill(x, y, w, h, texto, fill="#fff", color=NAVY, stroke="#D6E2EE", size=21, anchor_mid=True):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            + txt(x + w / 2, y + h / 2 + size * 0.36, texto, size, 700, color, "middle"))


def muro(x, h=520, w=40):
    return f'<rect x="{x}" y="0" width="{w}" height="{h}" fill="url(#hatch)"/><line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="#C7D5E3" stroke-width="2"/><line x1="{x+w}" y1="0" x2="{x+w}" y2="{h}" stroke="#C7D5E3" stroke-width="2"/>'


def basica():
    return (f'<svg viewBox="0 0 900 520">{DEFS}'
            f'<rect x="0" y="0" width="520" height="520" fill="#FBFDFF"/><rect x="560" y="0" width="340" height="520" fill="url(#sky)"/>'
            + muro(520) +
            f'<line x1="0" y1="470" x2="520" y2="470" stroke="#D6E2EE" stroke-width="3"/><line x1="560" y1="470" x2="900" y2="470" stroke="#C9D8E6" stroke-width="3"/>'
            + txt(36, 46, "INTERIOR", 18, 700, MUT, ls=3) + txt(596, 46, "EXTERIOR", 18, 700, MUT, ls=3)
            + tuberia("M462 142 H612 Q624 142 624 154 V300 Q624 312 636 312 H662")
            + interior(180, 100) + exterior(660, 250, 200, 150)
            + f'<rect x="690" y="400" width="14" height="70" fill="#C7D5E3"/><rect x="816" y="400" width="14" height="70" fill="#C7D5E3"/>'
            + txt(320, 222, "Unidad interior", 22, 700, NAVY, "middle") + txt(760, 502, "Unidad exterior", 21, 700, NAVY, "middle")
            + f'<rect x="590" y="66" width="292" height="62" rx="16" fill="#fff" stroke="{COBRE}" stroke-width="2.5"/>'
            + txt(736, 94, "≈ 2 m de tubería de cobre", 19, 700, NAVY, "middle") + txt(736, 117, "y cordones eléctricos", 19, 500, MUT, "middle")
            + pill(36, 380, 300, 56, "✓  Incluido en el precio", "#E9F8EF", VERDE, "#BFE8CF", 22)
            + '</svg>')


def distancia():
    p1 = (muro(205, 520, 26)
          + tuberia("M190 132 H246 V300 H262")
          + interior(30, 104, 170, 60) + exterior(258, 250, 140, 110)
          + txt(215, 52, "Unidades cerca", 24, 800, NAVY, "middle")
          + pill(40, 420, 350, 56, "✓  Instalación básica", "#E9F8EF", VERDE, "#BFE8CF", 22))
    p2 = (muro(665, 520, 26)
          + tuberia("M650 132 H730 V215")
          + tuberia("M730 215 V230 H858 V330", dash=True)
          + interior(495, 104, 150, 60) + exterior(770, 330, 110, 90)
          + txt(685, 52, "Unidades más lejos", 24, 800, NAVY, "middle")
          + f'<rect x="490" y="408" width="270" height="84" rx="20" fill="#FFF4E6" stroke="#FFD29A" stroke-width="2"/>'
          + txt(625, 442, "+ Extensión de tuberías", 21, 800, "#C25E0A", "middle") + txt(625, 472, "adicional, se cotiza", 19, 500, MUT, "middle"))
    return (f'<svg viewBox="0 0 900 520">{DEFS}<rect width="900" height="520" fill="#FBFDFF"/>'
            f'<line x1="450" y1="20" x2="450" y2="500" stroke="#D6E2EE" stroke-width="2" stroke-dasharray="8 8"/>{p1}{p2}</svg>')


def canaleta():
    def panel(x, con):
        body = f'<rect x="{x}" y="20" width="410" height="480" rx="26" fill="#F6F9FC" stroke="#E1E9F2" stroke-width="2"/>'
        body += interior(x + 60, 70, 270, 80)
        px = x + 300
        if con:
            body += (f'<g filter="url(#sh)"><rect x="{px-22}" y="150" width="46" height="300" rx="6" fill="#fff" stroke="#C9D6E3" stroke-width="2.5"/></g>'
                     f'<line x1="{px-10}" y1="160" x2="{px-10}" y2="440" stroke="#EEF3F8" stroke-width="3"/>')
            body += txt(x + 205, 488, "Con canaleta 100×50", 23, 800, AZUL, "middle")
            body += f'<circle cx="{x+372}" cy="58" r="22" fill="{VERDE}"/>' + txt(x + 372, 66, "✓", 24, 800, "#fff", "middle")
        else:
            body += (f'<path d="M{px-10} 150 C{px+30} 210 {px-40} 260 {px} 320 S{px+20} 400 {px-6} 450" fill="none" stroke="#B9C8D8" stroke-width="7" stroke-linecap="round"/>'
                     f'<path d="M{px} 150 C{px+40} 215 {px-30} 265 {px+12} 325 S{px+32} 405 {px+8} 450" fill="none" stroke="{COBRE}" stroke-width="9" stroke-linecap="round"/>'
                     f'<path d="M{px+12} 150 C{px+50} 220 {px-18} 270 {px+24} 330 S{px+44} 410 {px+20} 450" fill="none" stroke="{CABLE}" stroke-width="4" stroke-linecap="round"/>'
                     + "".join(f'<rect x="{px-14}" y="{yy}" width="44" height="12" rx="3" fill="#9FB3C8" opacity=".75" transform="rotate(-12 {px+8} {yy+6})"/>' for yy in (225, 345)))
            body += txt(x + 205, 488, "Sin canaleta", 23, 800, MUT, "middle")
        return body
    return f'<svg viewBox="0 0 900 520">{DEFS}{panel(15, False)}{panel(475, True)}</svg>'


def soporte():
    def suelo(x0, x1, y):
        return f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="20" fill="url(#hatch)"/><line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#B8C7D6" stroke-width="3"/>'
    hierro = "#5B6B7C"
    p1 = (f'<rect x="15" y="20" width="410" height="480" rx="26" fill="url(#sky)"/>'
          f'<rect x="35" y="20" width="34" height="450" fill="url(#hatch)"/>' + suelo(15, 425, 450)
          + exterior(110, 120, 230, 150)
          + f'<path d="M69 274 H330 M69 380 L250 274" stroke="{hierro}" stroke-width="10" stroke-linecap="round"/>'
          + f'<path d="M69 274 L69 380" stroke="{hierro}" stroke-width="10" stroke-linecap="round"/>'
          + txt(240, 410, "En altura, en muro", 23, 800, NAVY, "middle"))
    p2 = (f'<rect x="475" y="20" width="410" height="480" rx="26" fill="url(#sky)"/>' + suelo(475, 885, 410)
          + exterior(565, 220, 230, 150)
          + f'<rect x="575" y="370" width="210" height="16" rx="4" fill="{hierro}"/><rect x="590" y="386" width="22" height="24" fill="{hierro}"/><rect x="748" y="386" width="22" height="24" fill="{hierro}"/>'
          + txt(680, 470, "Sobre piso", 23, 800, NAVY, "middle"))
    return f'<svg viewBox="0 0 900 520">{DEFS}{p1}{p2}</svg>'


def electrico():
    return (f'<svg viewBox="0 0 900 520">{DEFS}<rect x="10" y="10" width="880" height="500" rx="26" fill="#F6F9FC" stroke="#E1E9F2" stroke-width="2"/>'
            + interior(50, 150, 270, 84)
            # cordón incluido (1,5 m)
            + f'<path d="M320 190 H470" stroke="{CABLE}" stroke-width="6" stroke-linecap="round"/>'
            # canaleta 10x20 con cordón adicional
            + f'<g filter="url(#sh)"><path d="M470 178 H800 V400 H780 V200 H470 Z" fill="#fff" stroke="{NAR}" stroke-width="3" stroke-linejoin="round"/></g>'
            + f'<path d="M470 190 H790 V395" fill="none" stroke="{CABLE}" stroke-width="4" stroke-linecap="round" stroke-dasharray="2 9"/>'
            # enchufe
            + f'<g filter="url(#sh)"><rect x="752" y="398" width="76" height="92" rx="16" fill="#fff" stroke="{BORDE}" stroke-width="2.5"/></g>'
            + f'<circle cx="778" cy="444" r="6" fill="{CABLE}"/><circle cx="802" cy="444" r="6" fill="{CABLE}"/>'
            # cotas
            + f'<path d="M320 120 V140 M470 120 V140 M320 130 H470" stroke="{VERDE}" stroke-width="3"/>'
            + txt(395, 108, "≈ 1,5 m incluido", 20, 800, VERDE, "middle")
            + f'<path d="M470 120 V140 M800 120 V140 M470 130 H800" stroke="{NAR}" stroke-width="3"/>'
            + txt(635, 108, "Metros adicionales", 20, 800, "#C25E0A", "middle")
            + txt(185, 268, "Unidad interior", 21, 700, NAVY, "middle")
            + txt(735, 444, "Punto eléctrico", 20, 700, NAVY, "end") + txt(735, 470, "(enchufe)", 18, 500, MUT, "end")
            + f'<rect x="380" y="300" width="330" height="96" rx="22" fill="#FFF4E6" stroke="#FFD29A" stroke-width="2"/>'
            + txt(545, 338, "Cordón + canaleta 10×20", 21, 800, "#C25E0A", "middle")
            + txt(545, 372, "$12.000 por metro adicional", 21, 600, NAVY, "middle")
            + '</svg>')


ILUS = {"basica": basica, "distancia": distancia, "canaleta": canaleta, "soporte": soporte, "electrico": electrico}
