# TeamFS Kennel Club – Guía de contenido

## Marca
- Criadero familiar en Chile de **dos razas**:
  - **Cane Corso** (Mastín Italiano), inscritos en **KCC – Kennel Club de Chile** (FCI).
  - **American Bully**, inscritos en **ABKC – American Bully Kennel Club**.
- Redes: Instagram @teamfsbull_kennelclub · Facebook (Página teamfsbull_kennelclub) · TikTok @teamfs_bullkennelclub
- Contacto: WhatsApp +56 9 6190 7601 · DM
- Tono: experto cinófilo cercano, directo, honesto; español de Chile; tú. Nada de promesas médicas: ante síntomas, siempre "consulta a tu veterinario".
- Referentes analizados: Cane Corso Barcelona (Juanma Morato), CastleGuard, Serafina, Del Corsoclub, Imperia Detroval (Cane Corso); Big Gemini, Blue Pride, Muscletone, Bossy Kennels, Venomline (American Bully).
  Lo que funciona: autoridad con pruebas (registros KCC/ABKC, padres, salud), educación al comprador, mitos vs realidad, salud/alimentación, vida familiar con niños.

## Personalidad: profesionales que se ríen de la vida
- Mezcla en cada semana: autoridad (registros KCC/ABKC, salud, genética) + humor cotidiano de vivir con molosos (sillones mordidos, 60 kg que se creen faldero, cara de "yo no fui", celos entre hermanos, el baño como tragedia griega).
- Regla de oro: el chiste es sobre situaciones, nunca sobre maltrato, peleas ni agresividad; siempre cierra con un dato útil o profesional ("Dato TeamFS: ...").
- Hablar como personas, no como catálogo. Preguntas al final para generar comentarios ("¿Cuál crees que fue?").
- Exponer con orgullo: logros, camadas, desafíos de crianza (cómo se elige pareja, ecografía, primeras semanas, socialización, entrega), siempre con transparencia.

## La manada (personajes recurrentes)
| Nombre | Raza | Descripción | Fotos seguras |
|---|---|---|---|
| Queen | Cane Corso hembra | La reina de la casa | (por confirmar en banco/cane-corso) |
| Skype | Cane Corso formentino | Color formentino (azul-cervato) | (por confirmar) |
| Ragnar | American Bully XL merle | El grandote, "60 kilos de disciplina" | marca/fichas/ragnar_*.jpg |
| Dakota | American Bully chocolate | Elegante, mirada seria | marca/fichas/dakota_poster.jpg, ragnar_dakota.jpg |
| Bella | American Bully merle blanco con negro | La modelo de la casa | marca/fichas/bella_*.jpg, krypto_vs_bella.jpg |
| Krypto | American Bully fawn | Pose de campeón | marca/fichas/krypto_vs_bella.jpg (izquierda), bella_krypto.jpg (derecha) |
| Kopito | American Bully cachorra, 6 meses (oct-2026), blanca de ojos celestes | La nueva, traviesa | marca/fichas/kopito_poster.jpg |
- Solo nombrar a un perro si la foto es de ese perro (fichas seguras o por color inequívoco). Si hay duda, no nombrar.
- La edad de Kopito avanza: calcular desde 6 meses en octubre 2026.

## Competencia en Chile (oct-2026)
- Criaderos de Cane Corso como Il Cane Corso (ilcanecorso.cl) y Jalo Henki (jhcc.cl, KCC) comunican con tono emotivo ("guardián natural", "elige el amor"), pero sin pruebas: no muestran registros, padres, pruebas de salud, precios ni garantías claras; textos genéricos y errores.
- Oportunidad TeamFS: transparencia y autoridad (registro KCC/ABKC visible, padres con nombre, crianza mostrada) + humor que ellos no tienen + respuesta rápida por WhatsApp.
- Club Cane Corso Chile (KCC) organiza especializadas (ej. Pirque, julio 2026): contenido de exposiciones cuando participemos.

## Formatos
- Carrusel (feed IG/FB + TikTok modo foto con música automática de TikTok): base diaria.
- Reel/video vertical 9:16 de 10–25 s (tools/make_reel.py): 3 veces por semana como mínimo (lunes, miércoles y viernes a las 20:30), con gancho en los primeros 2 s y texto grande (se ve sin sonido). Ideas: interrogatorio de la manada, "POV: tienes un moloso de 60 kg", antes/después de cachorro a adulto ("It's October again"), presentación de camada, "un día en TeamFS", mitos en 3 segundos, reacciones.
- Música: TikTok modo foto lleva música automática. En Instagram, la API de música de Metricool no está disponible para esta cuenta (probado oct-2026): para Reels, recomendar en el correo de propuesta el audio en tendencia de esa semana (buscar cada día) para que el dueño lo agregue en la app si quiere.
- Serie "Desafío de camada": anuncio de cruza (padres con registro), seguimiento semanal, nacimiento, 4–8 semanas, entrega. Pedir datos/fotos al dueño cuando haya camada.

## Calendario diario (hora Chile)
| Hora  | Pilar | Formato |
|-------|-------|---------|
| 11:00 | Educativo: salud, alimentación, crecimiento, prevención | Carrusel 5–7 láminas |
| 15:00 | Instructivo: cómo hacer algo (socializar, correa, uñas, baño, adiestramiento) | Carrusel 3–5 láminas |
| 20:30 | Recomendativo/autoridad/humor: mitos, qué exigir a un criadero, la manada, camadas | Reel lun/mié/vie; carrusel los demás días |
- Alternar razas: días pares Cane Corso a las 11:00 y 20:30, Bully a las 15:00; días impares al revés.
- No repetir tema en 14 días (revisar `state/`). Estacionalidad Chile: oct–mar calor, garrapatas, deshidratación; abr–sep frío, articulaciones, piel.
- Cierre de cada publicación: invitación a Guardar · Compartir · DM **y SIEMPRE el link de WhatsApp: 📲 Consultas por WhatsApp: https://wa.me/56961907601** (en el texto, antes de los hashtags). La lámina final (cta) muestra el botón verde "WhatsApp +56 9 6190 7601". En TikTok el link no es clicable: escribir también el número. 5–8 hashtags (#CaneCorso #CaneCorsoChile #MastinItaliano / #AmericanBully #BullyChile #ABKC / #TeamFSKennelClub).

## Diseño
- Generador: `python3 tools/make_post.py spec.json OUTDIR` (tipos de lámina: cover, point, cta). 1080×1350, azul marino + rojo + dorado, Poppins/Inter.
- Fotos: `banco/cane-corso/` y `banco/american-bully/`. Usar la foto correcta para la raza del tema. Revisar cada lámina antes de publicar (que el perro no quede tapado ni cortado).
- Imágenes públicas para Metricool: `https://raw.githubusercontent.com/laricopola-svg/climatizate-pro-envios/teamfs-media/publicaciones/<carpeta>/slide_NN.jpg`

## Flujo de aprobación
1. ~07:00 se generan las 3 publicaciones, se suben a `publicaciones/AAAA-MM-DD-hhmm-tema/`, se crean en Metricool (marca TeamFS, blogId 7551690) como **borrador** a las 11:00, 15:00 y 20:30, y se envía la propuesta a fcosotog7@gmail.com.
2. Cada hora se revisa el correo. Respuesta "OK" → los borradores pasan a programados. Respuesta con cambios → se corrige y se reenvía.
3. Estado de cada día en `state/AAAA-MM-DD.json`.
