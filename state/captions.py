WA = "https://wa.me/56923807671?text=Hola%20Sara%20Vibes%2C%20quiero%20cotizar"
P = {
"0": {"carpeta":"2026-11-17-2100-prueba-profe","fecha":"2026-11-17","hora":"21:00","formato":"foto","tema":"Regalo para la profe (fin de año escolar)",
 "ig":"¿Ya tienes el regalo para la profe? 🍎\n\nSe acaba el año escolar y esta bolsa personalizada es de esos regalos que sí se usan: para los cuadernos, el mercado o la playa.\n\n✏️ Con su nombre, la frase que tú elijas o el dibujo de tu peque.\n\n👉 ¿Para quién sería: la profe, la tía del jardín o el tío del furgón? Cuéntanos en los comentarios.\n\n📲 Cotiza por WhatsApp +56 9 2380 7671 (link en la bio)\nGuarda este post para no olvidarlo 💗\n\n#regaloprofesora #findeaño #regalospersonalizados #santiagochile #saravibes"},
"1": {"carpeta":"2026-11-18-1000-guia-regalos","fecha":"2026-11-18","hora":"10:00","formato":"carrusel","tema":"Guía: 4 regalos de Navidad que sí se usan",
 "ig":"🎁 4 regalos de Navidad que SÍ se usan (y no terminan en un cajón)\n\n1️⃣ Polerón con frase para la tía, la abuela o tu mejor amiga\n2️⃣ Polerón con su nombre y diseño en las mangas\n3️⃣ Bolsa para la profe o la tía del jardín\n4️⃣ Poleras con logo para tu equipo\n\n¿Cuál regalarías tú? Comenta 1, 2, 3 o 4 👇\nMándaselo a quien siempre deja los regalos para última hora 😅\n\n📲 Cotiza por WhatsApp +56 9 2380 7671 (link en la bio)\n\n#regalosdenavidad #regalospersonalizados #poleronpersonalizado #santiagochile #emprendimientochileno"},
"2": {"carpeta":"2026-11-18-1500-reel-uniformes","fecha":"2026-11-18","hora":"15:00","formato":"reel","tema":"Reel: uniformes con logo para pymes (caso taller mecánico)",
 "ig":"¿Tu equipo todavía sin polera con logo? 👕\n\nAsí quedó el uniforme de un taller mecánico: logo chico en el pecho y logo grande en la espalda con su WhatsApp. Tu uniforme también hace publicidad 😉\n\n✅ Polera piqué + estampado DTF a todo color\n✅ Te mostramos la maqueta antes de producir\n\n¿De qué rubro es tu negocio? Cuéntanos en los comentarios 👇\n\n📲 Cotiza por WhatsApp +56 9 2380 7671 (link en la bio)\n\n#uniformesempresa #polerasconlogo #pymechile #estampadodtf #santiagochile"},
"3": {"carpeta":"2026-11-18-1930-nombre-mariposas","fecha":"2026-11-18","hora":"19:30","formato":"foto","tema":"Polerón con nombre y mariposas (comenta tu nombre)",
 "ig":"Tu nombre, tus colores, tus mariposas 🦋\n\nEste polerón lleva el nombre al frente y mariposas en las mangas… y se puede hacer con el nombre y los colores que tú quieras.\n\n✍️ ¿Qué nombre pondrías en el tuyo? Escríbelo en los comentarios 👇\n\n📲 Pídelo por WhatsApp +56 9 2380 7671 (link en la bio)\n\n#poleronpersonalizado #ropapersonalizada #regalosconnombre #santiagochile #saravibes"},
}
for k,v in P.items():
    v["fb"] = v["ig"].replace("(link en la bio)", "👉 " + WA)
    v["tt"] = v["ig"]
