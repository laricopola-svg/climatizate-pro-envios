# Fotos reales de instalaciones — Climatízate Pro

- `originales/`: fotos tal como llegaron (WhatsApp).
- `mejoradas/`: misma foto con mejora de luz, color y nitidez (kit/fotos.py). No se altera la instalación.

| Foto | Escena |
|---|---|
| foto_00 | Dormitorio con muro gris; unidad exterior visible en el balcón |
| foto_02 | Living con cielo de vigas y mueble oscuro |
| foto_03 | Dormitorio con respaldo capitoné (tarde) |
| foto_05 | Living con ventanal; unidad exterior en terraza |
| foto_06 | Living-comedor con cielo inclinado |
| foto_07 | Dormitorio principal blanco y luminoso |
| foto_08 | Living con cortinas roller |
| foto_10 | Dormitorio, equipo junto a ventana |
| foto_11 | Local comercial (floristería), vista interior |
| foto_13 | Fachada de floristería con unidad exterior en altura |

Uso en carruseles: lámina tipo `foto` en contenido.json, con "foto": ruta a la imagen y "pos": encuadre (CSS object-position).

## Versión HD (desde 12-11-2026)
`fotos/hd/foto_XX.jpg`: misma foto mejorada con Real-ESRGAN x4 (IA de super-resolución, sin agregar ni borrar objetos) + corrección de luz y color; lado menor ≥ 2600 px. El kit (`kit/encuadre.py`) la usa siempre en lugar de `mejoradas/` y recorta 4:5 y 9:16 con escala proporcional, sin estirar. Para una foto nueva: `python3 kit/fotos.py --hd fotos/originales/foto_XX.jpg fotos/hd/foto_XX.jpg`. Control final: `python3 kit/calidad.py <carpeta>`.
