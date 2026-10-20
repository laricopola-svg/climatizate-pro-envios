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

## Calendario diario (hora Chile)
| Hora  | Pilar | Formato |
|-------|-------|---------|
| 11:00 | Educativo: salud, alimentación, crecimiento, prevención | Carrusel 5–7 láminas |
| 15:00 | Instructivo: cómo hacer algo (socializar, correa, uñas, baño, adiestramiento) | Carrusel 3–5 láminas |
| 20:30 | Recomendativo/autoridad: mitos, qué exigir a un criadero, estándar de raza, ejemplares TeamFS con registro | Carrusel o imagen única |
- Alternar razas: días pares Cane Corso a las 11:00 y 20:30, Bully a las 15:00; días impares al revés.
- No repetir tema en 14 días (revisar `state/`). Estacionalidad Chile: oct–mar calor, garrapatas, deshidratación; abr–sep frío, articulaciones, piel.
- Cierre de cada publicación: invitación a Guardar · Compartir · DM. 5–8 hashtags (#CaneCorso #CaneCorsoChile #MastinItaliano / #AmericanBully #BullyChile #ABKC / #TeamFSKennelClub).

## Diseño
- Generador: `python3 tools/make_post.py spec.json OUTDIR` (tipos de lámina: cover, point, cta). 1080×1350, azul marino + rojo + dorado, Poppins/Inter.
- Fotos: `banco/cane-corso/` y `banco/american-bully/`. Usar la foto correcta para la raza del tema. Revisar cada lámina antes de publicar (que el perro no quede tapado ni cortado).
- Imágenes públicas para Metricool: `https://raw.githubusercontent.com/laricopola-svg/climatizate-pro-envios/teamfs-media/publicaciones/<carpeta>/slide_NN.jpg`

## Flujo de aprobación
1. ~07:00 se generan las 3 publicaciones, se suben a `publicaciones/AAAA-MM-DD-hhmm-tema/`, se crean en Metricool (marca TeamFS, blogId 7551690) como **borrador** a las 11:00, 15:00 y 20:30, y se envía la propuesta a fcosotog7@gmail.com.
2. Cada hora se revisa el correo. Respuesta "OK" → los borradores pasan a programados. Respuesta con cambios → se corrige y se reenvía.
3. Estado de cada día en `state/AAAA-MM-DD.json`.
