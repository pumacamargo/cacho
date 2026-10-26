---
title: Edición manual Producer-style con solo audio y videos
created: 2026-10-26
updated: 2026-10-26
type: runbook
tags: [sistema, runbook, pipeline]
status: active
confidence: high
related: [ttchop-video-generation, ttchop-music-generation, acceso-remoto-pumadeskasus]
---

# Edición manual Producer-style con solo audio y videos

Este flujo sirve cuando se cuenta con **un audio aprobado por Arturo y archivos de video originales**, pero no existe una ficha de producto ni `sessions` con metadata en Firestore. No se ejecuta `runProducer()`: se prepara un montaje manual con `ttchop-server/scripts/collage_builder.py` y se entrega el MP4. No inventes ni persistas productos, sesiones o clips de catálogo. Para leer el NAS usa el alcance temporal documentado en [[acceso-remoto-pumadeskasus]]; para los flujos de collage y música existentes consulta [[ttchop-video-generation]] y [[ttchop-music-generation]].

## Procedimiento reutilizable

1. **Verifica la ubicación y cada archivo.** `P:` de Polaris solo está disponible en el proceso PowerShell de `pumassh`, no en Linux ni en FFmpeg. Enumera los nombres exactos, extensiones y tamaños desde esa sesión. Si la ruta indicada no existe, inspecciona solo el directorio cercano y acepta una corrección de nombre únicamente cuando todos los archivos solicitados coincidan.
2. **Staging temporal y limitado.** Copia solo los medios elegidos a un directorio único fuera de cualquier repo. Si se requiere transferencia NAS→VPS, usa un receptor temporal enlazado únicamente a la IP Tailscale de `vps-projects`, con token aleatorio de un uso, allowlist de nombres y tope de bytes. Verifica tamaños; luego detén el receptor y elimina token, payload y medios staged. No sobrescribas ni muevas los originales.
3. **Deriva metadata de los archivos.** Ejecuta `ffprobe` en cada video y audio: duración, streams, codec, tamaño, dimensiones y frame rate. Genera y revisa un contact sheet por clips. El prompt de receta de collage recibe IDs/duraciones/trims, no ve los fotogramas; usa la inspección visual para redactar descripciones breves y ordenar hook/desarrollo. No infieras afirmaciones comerciales a partir de las imágenes.
4. **Usa el audio aprobado, no regeneres voz.** Pasa solo el audio suministrado al render. En la ruta estándar, `audioBase64` evita TTS, aunque `voiceId`, `dialogue`, `sessions` y `renderId` siguen siendo requeridos; usa un `projectId` explícito y desactiva overlay/personaje si no se pidieron. `dialogue` puede servir de contexto editorial, pero no reemplaza la pista suministrada. Los objetos de sesión/video de una solicitud pueden ser efímeros; no crees documentos falsos en `products` o `sessions` ni escribas cooldowns en `bot_productions`.
5. **Aplica y calcula las reglas de corte Producer.** Hook: aproximadamente los primeros 3 s, 3–5 clips distintos, cada uno 0,5–1,0 s de salida a 2×–3×. Desarrollo: orden coherente y cortes de 2–3 s de salida a 1,5×–4×. Duración de salida por segmento = `(trimEnd - trimStart) / speed`; cada trim debe quedar dentro de la duración real del origen. Incluye cada archivo pedido al menos una vez cuando sea físicamente posible; un clip demasiado corto puede ser solo hook.
6. **Primero prueba la ruta estándar, sin cambiar producción.** `POST /collage/create` devuelve `pending`; lee `renders/{renderId}` en el proyecto indicado hasta `done` o `failed`. Si el LLM/provider de receta falla, no sustituyas el modelo, reinicies el servidor ni despliegues. Para un pedido puntual ya autorizado, puedes usar el `collage_builder.py` existente con una receta revisada y `src` local; esto comparte el builder FFmpeg, pero **no** crea un render exitoso en Firestore ni un MP4 en Storage. Informa esta diferencia.
7. **Aísla el builder directo.** Antes de ejecutarlo, confirma que no haya otro `collage_builder.py`/FFmpeg de collage activo y revisa `/media/collage_temp`. El script usa ese directorio fijo y lo elimina tras un éxito; no lo ejecutes concurrentemente ni sobre datos ajenos.
8. **Audita la timeline final, no solo los trims intermedios.** El builder mide cada segmento antes del mux; el archivo final usa `-shortest`, que puede cortar el último video aunque el audio quede completo. Distribuye la duración para que todos los cortes de body sigan dentro de 2–3 s al final, no sobrepases la duración de audio con una receta excesiva, y compensa redondeo de frames con una extensión visual del último frame si hace falta. Compara la duración/frames de cada segmento en la receta con los tiempos de salida reales; no llames exactas a posiciones inferidas.
9. **Verifica y entrega.** Comprueba todos los IDs fuente solicitados, codecs/dimensiones/duración de ambos streams, y decodifica el MP4 completo con FFmpeg. Compara la duración de audio decodificada con el audio aprobado (no solo la duración del contenedor) y revisa fotogramas representativos. Si se pidió música, atenúa solo la música y deja intacto el audio existente; verifica nivel pico/no clipping. Entrega el MP4, indica que no se publicó y distingue un artefacto del builder directo de un render `done` de Firestore.

## Caso verificado: Juice Discount, 2026-10-26

### Entradas y metadata derivada

Los medios usados en el montaje inicial fueron la narración japonesa que se generó a partir del texto de Arturo, se aceleró a 1,5× y Arturo aprobó, más estos cinco MP4; no se usó ficha de catálogo, producto, sesión ni metadata previa de Firestore. Las duraciones y descripciones visuales que siguen se derivaron de `ffprobe` y del contact sheet. La ruta escrita inicialmente no coincidía exactamente con el nombre en Polaris: los archivos estaban en `P:\Tiktok\hamaca\edits\02_JuiceDiscount\` (no `02_juiceDiscout`). Se verificaron por nombre y tamaño antes de transferir.

| Archivo | Tamaño | Duración | Video |
|---|---:|---:|---|
| `Juice_corte_04.mp4` | 895 799 bytes | 1,599 s | H.264, 720×1280, 120 fps |
| `Juice_corte_05_parte_01.mp4` | 2 925 038 bytes | 5,702 s | H.264, 720×1280, 30 fps |
| `Juice_corte_05_parte_02.mp4` | 3 007 395 bytes | 5,702 s | H.264, 720×1280, 30 fps |
| `Juice_corte_05_parte_03.mp4` | 2 739 313 bytes | 5,702 s | H.264, 720×1280, 30 fps |
| `Juice_corte_05_parte_04.mp4` | 2 782 915 bytes | 5,702 s | H.264, 720×1280, 30 fps |

Los cinco MP4 de origen también tenían audio AAC, pero `collage_builder.py` elimina el audio de cada clip (`-an`) y monta la pista aprobada por separado. No se ejecutó `runProducer()` ni se modificó código.

### Intento estándar y fallback

Se intentó `POST /collage/create` en el proyecto `ttchop`, pero el job terminó `failed` antes de producir video: OpenRouter devolvió 404 porque el modelo configurado `o4-mini-2025-04-16` no estaba disponible o no tenía acceso. El intento dejó el documento fallido `renders/render_manual_juice_20261026_001`; no produjo un asset en Storage. No se cambió ni reinició el servicio.

Para completar el pedido puntual, se inspeccionó que no hubiera otro builder activo ni datos en `/media/collage_temp`, y se ejecutó una receta manual con rutas locales mediante el `scripts/collage_builder.py` existente. Todos los clips pedidos aparecen al menos una vez. Los rangos/velocidades de entrada fueron:

- **Hook:** `Juice_corte_04` 0,05–1,55 s a 2,5×; `parte_01` 0,70–2,62 s a 2,4×; `parte_02` 1,00–2,92 s a 2,4×; `parte_03` 0,20–2,12 s a 2,4×.
- **Body:** `parte_01` 0,50–4,79 s a 2×; `parte_02` 0,60–4,89 s a 2×; `parte_03` 1,00–5,29 s a 2×; `parte_04` 0,50–4,79 s a 2×.

El builder midió los cortes pre-mux del hook en 0,592 + 0,867 + 0,867 + 0,867 s y los cuatro cortes de body en 2,233 s cada uno. La suma medida pre-mux fue 12,125 s, mientras la pista de voz decodificaba 11,531 s. `-shortest` terminó el video a 11,520 s; por ello, el último segmento visual quedó recortado respecto a sus 2,233 s medidos pre-mux. **No se debe afirmar que los cuatro cortes de body conservaron 2–3 s cada uno en el MP4 final.** La hoja de contactos final no mostró cuadros negros ni un encuadre severamente cortado; no se hizo un render correctivo adicional.

### Música y salida entregada

Después, Arturo pidió añadir el instrumental de celebración que había proporcionado, con volumen de música a 0,6× y sin bajar la pista existente del video. Se mezcló con FFmpeg usando `volume=0.6` solo en la música y `amix` con `normalize=0`; se copió el stream H.264 sin recodificar (`-c:v copy`). La música se limitó a la duración del audio original. El audio AAC existente quedó sin atenuación en el grafo de mezcla.

QA de esa salida: H.264 1080×1920/25 fps, stream de video 11,520 s; audio AAC mono 48 kHz, 11,540 s; contenedor 11,541 s. El pico medido de la mezcla fue −0,5 dB, sin clipping en la decodificación completa. La salida se adjuntó en Telegram y no se publicó. Los originales del NAS se dejaron intactos; los medios, token de transferencia y payload temporales se borraron tras verificar el MP4 local. Los MP4 de salida se conservaron solo en el scratch del perfil, no en Cacho ni en el repo del servidor.

## Enlaces relacionados

- [[ttchop-video-generation]] — collage manual con catálogo y otros flujos de video.
- [[ttchop-music-generation]] — generación separada de música con ElevenLabs Music.
- [[acceso-remoto-pumadeskasus]] — acceso temporal al NAS Polaris mediante `pumassh`.
