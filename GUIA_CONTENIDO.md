# Guía de contenido — Sara Vibes (Prendas Personalizadas DTF, Santiago)

## Marca
- Nombre: Sara Vibes · "Prendas Personalizadas". Colores: negro (#0E0E10) y fucsia (#EC008C), blanco. Logo: tools/src/logo.jpg.
- Redes: Instagram y TikTok @sara.vibespersonaliza · Facebook "Sara Vibes Personaliza".
- Contacto: WhatsApp +56 9 7462 9490 · https://wa.me/56974629490?text=Hola%20Sara%20Vibes%2C%20quiero%20cotizar · Sara.VibesPersonaliza@gmail.com
- Tono: cercano, alegre, chileno sin exagerar ("polera", "polerón", "la profe", "la tía del jardín"). Tú, frases cortas, emojis con medida.

## Reglas (de los manuales de Sara Vibes)
- NO inventar precios, plazos, stock, descuentos, promociones, testimonios, clientes ni pedidos. Si no hay precio confirmado: "Cotiza por WhatsApp".
- Plazo solo como "pide con tiempo"; nunca prometer fechas de entrega.
- Sí se puede decir: estampado DTF, eliges diseño, nombre, frase o tu propio archivo; pecho, espalda, mangas; te mostramos la maqueta antes de producir.
- Productos: poleras (algodón, dryfit, piqué, manga larga, cuello V), polerones canguro (con y sin cierre), polerón polo, buzos, shorts, línea niños; bolsas, mochilas, packs familiares, diseños por profesión.
- Fotos de personas, menores, nombres o marcas de clientes: avisar en el correo y pedir confirmación de autorización. Nunca publicar rostros de menores sin autorización explícita (evitar "Pack familia.jpeg").
- No usar en publicaciones fotos con personajes con licencia (Disney, Stitch, Minnie, Hello Kitty, Gabby, Batman, Iron Man, Saja Boys/Huntrix, BTS, Mafalda, Gato con botas, Tralalero, equipos de fútbol): solo diseños originales, frases, nombres, logos de clientes autorizados.
- Imágenes IA: solo como fondo o ilustración, marcadas como IA (isAiGenerated/isAigc) y nunca presentadas como trabajo real.

## Formatos que más alcance dan (rotar)
- Carrusel "guía" para guardar/compartir (regalos por ocasión, ideas por profesión, "qué cambia el precio", "cómo cuidar tu estampado").
- Reel corto 10–15 s con fotos/videos reales (antes/después, proceso de planchado, unboxing, "POV: pediste tu polerón con nombre"), gancho en 0–2 s, texto grande.
- Foto única de trabajo terminado + pregunta para comentar ("¿Qué nombre pondrías?", "Comenta 1, 2 o 3").
- Uniformes y poleras con logo para pymes (B2B).
- Nunca el mismo formato en el mismo horario dos días seguidos (revisar state/).

## Horarios
10:00 (educativo / guía), 15:00 (reel), 19:30 (engagement / trabajo terminado).

## Calendario Chile (noviembre–diciembre 2026)
- Fin del año escolar y regalos para profesoras/tías del jardín (fin nov – mediados dic).
- Black Friday 27–30 nov (no inventar descuentos; solo si Sara confirma una promoción).
- Navidad: guías de regalo, pijamas/poleras familiares con diseños originales, "pide con tiempo".
- Licenciaturas y polerones generacionales (dic).

## Hashtags base (máx 5 por post)
#saravibes #santiagochile #regalospersonalizados #poleronpersonalizado #polerapersonalizada #estampadodtf #ropapersonalizada #emprendimientochileno #uniformesempresa #regalosdenavidad

## Fotos del Drive
Carpeta "Sara Vibes Personalizaciones" (id 1CH6uoY0pCP3UnmTpFReTHXNgo_EhU6fb): Diseños/Trabajos realizados y subcarpetas (Día de la madre, Día del amor, Conciertos...). Registrar en state/fotos_usadas.json qué archivos se usaron (id de Drive y fecha) para no repetir en 14 días.

## Música (pedido del dueño, 17-11-2026)
- CADA publicación lleva una canción en tendencia elegida para que conecte de forma orgánica con el tema (ej.: navidad → villancico pop en tendencia; antes/después → audio del trend de transiciones; showcase lindo → audio "dreamy"). Buscarla cada día en rankings de la semana (Metricool, Later, SocialPilot, CreatorDB) y anotar en state: audio_ig ("Título Artista") y audio_motivo.
- La API de Instagram solo permite poner música a Reels. Por eso en Instagram TODA publicación sale como Reel (los carruseles/fotos se convierten en video de láminas con zoom suave, ~2,6–3 s por lámina, archivo reel.mp4 + portada.jpg) con instagramData.audioConfiguration.
- Facebook: Reel con el mismo video (la API no permite elegir música).
- TikTok: carrusel de fotos 9x16 con autoAddMusic (TikTok elige el sonido; la API no permite elegir una canción específica).

- IMPORTANTE (probado 18-11-2026): la cuenta de Instagram de Sara es de EMPRESA, y por API solo tiene acceso a la biblioteca de música comercial (sin éxitos de sellos; p. ej. "Angel of My Dreams – JADE" no está). Al programar: busca primero la canción en tendencia por título; si Metricool devuelve candidatos y ninguno es esa canción, elige de esa lista (o con otra búsqueda por estado de ánimo: "christmas", "happy", "dreamy", "upbeat", "acoustic") la pista que mejor calce con el tema y regístrala en audio_ig_usado. Primera prueba: "Rose Petal Love (Instrumental) – Shuba" (audioId 608334931793444) para el polerón de mariposas.
- TikTok: si al conectar aparece otra cuenta (ej. teamfs_bullkennelclub), es porque el navegador ya tenía esa sesión de TikTok abierta. NUNCA programar en SaraVibes si su tiktokData no es la cuenta de Sara.

## Aprobación (pedido del dueño, 18-11-2026)
- Publicaciones del 19 al 23 de noviembre de 2026: requieren OK de Sara por correo.
- Desde el 24 de noviembre de 2026: se publican solas a las 10:00, 15:00 y 19:30. El correo diario pasa a ser informativo; Sara solo responde "NO n" para cancelar o con cambios.


## Contacto (cambio del dueño, 18-11-2026)
- WhatsApp oficial de Sara Vibes para redes: **+56 9 7462 9490** → https://wa.me/56974629490?text=Hola%20Sara%20Vibes%2C%20quiero%20cotizar
- TODAS las publicaciones (Instagram, Facebook y TikTok) llevan este link de WhatsApp en el texto, y las láminas muestran el número (tools/make_post.py ya lo trae). El número anterior (+56 9 2380 7671) no se usa más en redes.

## Calidad de edición (estándar del dueño: experto en marketing digital con 15 años de experiencia)
- tools/make_post.py mejora automáticamente cada foto: reducción de ruido, superresolución con IA (FSRCNN x2, una o dos veces según tamaño), iluminación local suave (CLAHE), viveza y nitidez. Las versiones quedan en banco/mejoradas/.
- Antes de usar una foto, revisa: luz pareja, prenda nítida, diseño legible, sin cortes en cabeza/prenda. Si el ángulo es malo (foto chueca, de lejos, fondo desordenado), recórtala a la prenda, endereza, o crea un mockup profesional con IA: Canva generate-image (prenda lisa del mismo color sobre modelo o maniquí, fondo limpio de estudio) y coloca el diseño real encima; o Canva remove-background para aislar la prenda sobre un fondo de marca. Marca esas piezas como IA (isAiGenerated / isAigc) y como "imagen referencial" en el texto. Nunca cambies el diseño estampado del cliente.
- Ganchos de 0-2 s, texto grande y legible en celular, máximo 1 idea por lámina, cierre con CTA a WhatsApp.

## Música en tendencia (refuerzo 18-11-2026)
- La meta es viralidad: la música debe ser la que está en tendencia ESA semana en Reels/TikTok. En el state guarda audio_candidatos: lista ordenada de 5 canciones en tendencia ("Título Artista") que calcen con el tema.
- Al programar en Instagram, prueba los candidatos en orden (título solo y título + artista) hasta que Metricool resuelva uno. Solo si ninguno está en la biblioteca de la cuenta de empresa, usa la pista más parecida al ánimo (ver audio_respaldo).

## ESTRATEGIA 2.0 (pedido del dueño, 27-11-2026) — prevalece sobre lo anterior si hay conflicto

### Diagnóstico con datos de Metricool (19 al 27-11)
- Instagram: los Reels hechos con láminas de texto tuvieron 13–47 vistas y 9–28 de alcance; entre 28 % y 80 % de la gente pasa de largo en los primeros 3 s. Lo que más rindió fue lo que tiene **personas o una historia real**: polerón Mariposas con modelo (186 vistas), "POV: tu sobrino te dibujó" (83 vistas, 61 de alcance).
- TikTok rinde 5–20 veces más que Instagram: "POV egresados" 986 vistas, "dibujo del sobrino" 440, "¿cuál regalarías?" 347, "amigo secreto" 296. Las guías de texto quedan bajo 250.
- Facebook: casi 0. Los Reels de FB salían **sin sonido** (el video no tenía audio).
- Las "voces" que se escuchaban venían de audios "original sound" de otras cuentas usados como música en Instagram (pueden traer voces). **No usar audios "original_sound"** de terceros; solo pistas de la biblioteca comercial (audioType "music").

### Reglas nuevas
1. **Voz en off en todos los Reels/videos**: mujer latina, cálida, amable y alegre, fluida. Escribe `publicaciones/<carpeta>/voz.txt` (máx 35 palabras, frases cortas, vocabulario chileno natural: polerón, pyme, regalonear, la once, el curso, la tía del jardín; sin garabatos ni "po" forzado) y `tools/make_reel.sh` la genera con `tools/voz.py` y ajusta el ritmo de las láminas a la voz. Prioridad de voz:
   a) Si Canva `create-video` (engine **h3max**, guía "generic", audio.mode "voice-over", language "Español de Chile", accent "Chileno, de Santiago", voice_direction "mujer de 25–30 años, cálida, amable y alegre, natural y fluida, nada robótica") tiene cupo: 1 video IA al día con voz chilena.
   b) Si no: voz local `tools/voz.py` (Supertonic 3, voz femenina natural y fluida; hablante por defecto 1, se cambia con la variable VOZ_SARA=0..4). Pip: `pip install --break-system-packages sherpa-onnx soundfile`. NO usar Piper (el dueño la encontró robótica, 27-11). Escribe los guiones con frases naturales y signos de exclamación/pregunta para dar entonación; "Sara Vibes" se pronuncia "Sara Vaibs" (el script lo adapta solo).
2. **Gancho en 1,5 s**: la primera frase hablada y la primera imagen dicen a QUIÉN le habla ("Si eres la tía que siempre regala calcetines…", "¿Tienes una pyme y tu equipo no tiene uniforme?") o muestran el resultado final. Nada de portadas solo con texto.
3. **Personas en 2 de cada 3 piezas** (modelo, manos estampando, cliente usando la prenda). Formatos que más rinden: POV con historia, antes/después, "peel reveal" (despegar el film DTF), proceso de estampado, prueba de prenda, unboxing de pedido, "me pidieron esto en los comentarios". Las guías de texto: máximo 1 cada 2 días.
4. **Duración 8–15 s**, 3–6 cortes, texto grande y corto en pantalla.
5. **Mezcla 70 % personas / 30 % empresas**: de lunes a sábado 1 de las 3 publicaciones es para EMPRESAS (rota la hora) y el domingo las 3 son para personas (≈ 6 de 21 por semana).
   - Personas: regalos (Navidad, amigo secreto, cumpleaños, día de la madre/padre), familia a juego, parejas, mascotas, curso/licenciatura, frases con humor, nombre/inicial, deporte, verano.
   - Empresas: uniformes con logo (poleras piqué, polerones, delantales, jockeys), merchandising con UV DTF (tazas, termos, botellas, vasos, cuadernos, agendas, lápices, cajas), regalos corporativos de fin de año, kits de bienvenida, ferias y eventos, emprendedores que quieren su marca en todo.
6. **Catálogo ampliado (todo lo que se puede personalizar)**:
   - DTF textil: poleras algodón, piqué, dryfit, manga larga, polerones canguro y con cierre, buzos, shorts, chaquetas, delantales, jockeys/gorros, bolsas tote, mochilas de tela, ropa de bebé y niños, bandanas de mascota, uniformes.
   - UV DTF: tazas, termos, botellas, vasos y frascos de vidrio, mugs metálicos, cuadernos y agendas, lápices, llaveros, cajas y packaging, carcasas, macetas, tablas, placas, artículos de oficina y de hogar.
   - No inventes precios, plazos, stock ni promociones. Si mencionas un producto que no está en el Drive, dilo como "también personalizamos…" y "imagen referencial".
7. **Imágenes de campaña con IA** (Canva `generate-image`, PORTRAIT_4_5 o PORTRAIT_9_16): sesiones en exterior (parque, playa, terraza, calle de barrio de Santiago con luz de tarde), en estudio (fondo de color de marca, luz suave) o lifestyle (oficina, cocina, living navideño). Personas latinas de distintas edades, ropa con diseños ORIGINALES (frases, nombres, mariposas, logos inventados), nunca marcas ni personajes con licencia, nunca niños como protagonistas de anuncios. Máximo 4 imágenes IA por día para Sara (el cupo de Canva se comparte con TeamFS). Marca "isAiGenerated": true / "isAigc": true y pon "(Imagen referencial creada con IA)" en el texto. Si Canva no tiene cupo, usa fotos reales del Drive y regístralo en el state.
8. **Audio por red**:
   - Instagram con voz: `audioConfiguration` con una pista instrumental de la biblioteca comercial (audioType "music"), `audioVolume` 18, `videoVolume` 100. Sin voz: `audioVolume` 100, `videoVolume` 0.
   - Facebook: Reel con el mismo video (ahora con voz).
   - TikTok: prueba A/B. Video con voz (`autoAddMusic` false) contra carrusel de fotos con `autoAddMusic` true. Anota en el state `tiktok_formato` ("video" o "fotos") y compara las vistas cada semana.
9. **Primera hora**: el correo a Sara recuerda responder los comentarios en los primeros 60 min (la velocidad de interacción decide si el Reel se muestra a más gente).
10. **Competencia**: las tiendas de estampado de Santiago publican sobre todo catálogo y marketplaces, sin métricas públicas. Lo que se viraliza en el rubro (guías de Printify y Gelato 2026) es el proceso o "reveal" del estampado, el gancho "no lo encontré, así que lo hice", la respuesta a un comentario con un pedido a medida y los regalos con reacción. No cites métricas de terceros que no veas.
