---
title: Edición manual Producer-style con solo audio y videos
created: 2026-10-26
updated: 2026-10-27
type: runbook
tags: [sistema, runbook, pipeline]
status: active
confidence: high
related: [ttchop-video-generation, ttchop-music-generation, acceso-remoto-pumadeskasus]
---

# Edición manual Producer-style con solo audio y videos

Este flujo sirve cuando se cuenta con **un audio aprobado por Arturo y archivos de video originales**, pero no existe una ficha de producto ni `sessions` con metadata en Firestore. No se ejecuta `runProducer()`: se prepara un montaje manual con `ttchop-server/scripts/collage_builder.py` y se entrega el MP4. No inventes ni persistas productos, sesiones o clips de catálogo. Para leer el NAS usa el alcance temporal documentado en [[acceso-remoto-pumadeskasus]]; para los flujos de collage y música existentes consulta [[ttchop-video-generation]] y [[ttchop-music-generation]].

## Procedimiento reutilizable

Si los archivos de entrada necesitan separarse primero por cambios de toma, usar [[separar-videos-nas-por-cortes]]: documenta detección/revisión visual, límites de frame, recodificación, QA y los clips Juice/EllisWhite que después se usaron en estos montajes. Separar una fuente no es lo mismo que editarla con reglas Producer.

1. **Verifica la ubicación y cada archivo.** `P:` de Polaris solo está disponible en el proceso PowerShell de `pumassh`, no en Linux ni en FFmpeg. Enumera los nombres exactos, extensiones y tamaños desde esa sesión. Si la ruta indicada no existe, inspecciona solo el directorio cercano y acepta una corrección de nombre únicamente cuando todos los archivos solicitados coincidan.
2. **Staging temporal y limitado.** Copia solo los medios elegidos a un directorio único fuera de cualquier repo. Si se requiere transferencia NAS→VPS, usa un receptor temporal enlazado únicamente a la IP Tailscale de `vps-projects`, con token aleatorio de un uso, allowlist de nombres y tope de bytes. Verifica tamaños; luego detén el receptor y elimina token, payload y medios staged. No sobrescribas ni muevas los originales.
3. **Deriva metadata de los archivos.** Ejecuta `ffprobe` en cada video y audio: duración, streams, codec, tamaño, dimensiones y frame rate. Genera y revisa un contact sheet por clips. El prompt de receta de collage recibe IDs/duraciones/trims, no ve los fotogramas; usa la inspección visual para redactar descripciones breves y ordenar hook/desarrollo. No infieras afirmaciones comerciales a partir de las imágenes.
4. **Usa el audio aprobado, no regeneres voz.** Pasa solo el audio suministrado al render. En la ruta estándar, `audioBase64` evita TTS, aunque `voiceId`, `dialogue`, `sessions` y `renderId` siguen siendo requeridos; usa un `projectId` explícito y desactiva overlay/personaje si no se pidieron. `dialogue` puede servir de contexto editorial, pero no reemplaza la pista suministrada. Los objetos de sesión/video de una solicitud pueden ser efímeros; no crees documentos falsos en `products` o `sessions` ni escribas cooldowns en `bot_productions`.
5. **Aplica y calcula las reglas de corte Producer.** Hook: aproximadamente los primeros 3 s, 3–5 clips distintos, cada uno 0,5–1,0 s de salida a 2×–3×. Desarrollo: orden coherente y cortes de 2–3 s de salida a 1,5×–4×. Duración de salida por segmento = `(trimEnd - trimStart) / speed`; cada trim debe quedar dentro de la duración real del origen. Incluye cada archivo pedido al menos una vez cuando sea físicamente posible; un clip demasiado corto puede ser solo hook.
6. **Primero prueba la ruta estándar, sin cambiar producción.** `POST /collage/create` devuelve `pending`; lee `renders/{renderId}` en el proyecto indicado hasta `done` o `failed`. Si el LLM/provider de receta falla, no sustituyas el modelo, reinicies el servidor ni despliegues. Para un pedido puntual ya autorizado, puedes usar el `collage_builder.py` existente con una receta revisada y `src` local; esto comparte el builder FFmpeg, pero **no** crea un render exitoso en Firestore ni un MP4 en Storage. Informa esta diferencia.
7. **Aísla el builder directo.** Antes de ejecutarlo, confirma que no haya otro `collage_builder.py`/FFmpeg de collage activo y revisa `/media/collage_temp`. El script usa ese directorio fijo y lo elimina tras un éxito; no lo ejecutes concurrentemente ni sobre datos ajenos.
8. **Audita la timeline final, no solo los trims intermedios.** El builder mide cada segmento antes del mux; el archivo final usa `-shortest`, que puede cortar el último video aunque el audio quede completo. Distribuye la duración para que todos los cortes de body sigan dentro de 2–3 s al final, no sobrepases la duración de audio con una receta excesiva, y compensa redondeo de frames con una extensión visual del último frame si hace falta. Compara la duración/frames de cada segmento en la receta con los tiempos de salida reales; no llames exactas a posiciones inferidas.
9. **Verifica y entrega.** Comprueba todos los IDs fuente solicitados, codecs/dimensiones/duración de ambos streams, y decodifica el MP4 completo con FFmpeg. Compara la duración de audio decodificada con el audio aprobado (no solo la duración del contenedor) y revisa fotogramas representativos. Si se pidió música, atenúa solo la música y deja intacto el audio existente; verifica nivel pico/no clipping. No apliques flip horizontal por defecto: hazlo solo ante una petición explícita, porque espeja también etiquetas y texto del empaque. Entrega el MP4, indica que no se publicó y distingue un artefacto del builder directo de un render `done` de Firestore.

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

Después, Arturo pidió añadir el instrumental de celebración. Las versiones se hicieron sucesivamente a 0,6× y 0,4×; tras indicar que la música seguía muy alta, pidió y aprobó una última versión a 0,2×. Cada mezcla se regeneró desde el video base sin música y el archivo instrumental original, no atenuando repetidamente una mezcla previa. Solo la música recibió `volume=0.2`; la pista existente de voz/audio pasó sin ganancia y `amix` usó `normalize=0`. La música quedó limitada a la duración del audio base. Arturo pidió explícitamente el flip horizontal en la versión de 0,4×; la versión final de 0,2× conservó ese efecto. El flip afecta los fotogramas (incluidos textos del empaque), no los streams de audio; no se aplica por defecto.

QA de la última salida: H.264 1080×1920/25 fps, video 11,520 s; AAC mono 48 kHz, audio 11,540 s; contenedor 11,541 s; 10 649 478 bytes. En la música a 0,2×, `volumedetect` midió −28,8 dB promedio/−14,2 dB pico; el audio original base midió −18,3/−1,8 dB y la mezcla final −17,7/−0,5 dB, sin clipping y con decodificación FFmpeg exitosa. La salida se adjuntó en Telegram y no se publicó. Los originales del NAS se dejaron intactos; medios, token de transferencia y payload temporales se borraron. Los MP4 quedaron solo en el scratch del perfil, no en Cacho ni en el repo del servidor.

## Caso verificado: ELLISS Shining Shot, 2026-10-26

El producto se identifica por el diálogo japonés proporcionado por Arturo; no se usó ficha de producto ni metadata de catálogo/sesión en Firestore. Los clips se leyeron desde `P:\Tiktok\hamaca\edits\03_ellisWhiteDiscount\`:

| Archivo | Tamaño | Video origen |
|---|---:|---|
| `EllisWhite_corte_01.mp4` | 3 679 181 bytes | 6,111 s, 720×1280, 120 fps |
| `EllisWhite_corte_02.mp4` | 6 535 890 bytes | 11,989 s, 720×1280, 60 fps |
| `EllisWhite_corte_04.mp4` | 6 707 777 bytes | 12,400 s, 720×1280, 30 fps |

### Voz y script de montaje

La voz se generó con la función existente `textToSpeech` de `ttchop-server/pipeline/elevenlabs.js`, PumaVoice01 (`ve7BOdejheJbgrBriBx4`), modelo `eleven_v3`, salida MP3 44,1 kHz/128 kbps y settings del Producer (`stability:0`, `style:0`, `similarity_boost:0`, `use_speaker_boost:true`, `speed:0.5`). El MP3 inicial duró 17,633 s; luego se aceleró 1,5× con FFmpeg (`-filter:a atempo=1.5 -codec:a libmp3lame -b:a 128k`) a `elliss-shining-shot-producer-voice-1.5x.mp3` (11,781 s de contenedor; 11,744 s PCM decodificado).

Los montajes usaron directamente el script existente `ttchop-server/scripts/collage_builder.py` con recetas JSON temporales y rutas `src` locales. No se ejecutó `runProducer()` ni `/collage/create`; no se crearon documentos `products`, `sessions` o `renders` en Firestore, ni se cambió código. El builder retiró el audio nativo de los clips y usó la narración aprobada.

### Tres versiones entregadas

1. **`elliss-white-discount-producer-edit.mp4`** — usó `EllisWhite_corte_01.mp4`, `EllisWhite_corte_02.mp4` y `EllisWhite_corte_04.mp4` más la narración; sin música ni flip. Receta de 3 segmentos hook y 4 body. El builder midió hooks de 1,008, 1,050 y 1,067 s (ligeramente mayores que el límite de 1 s), y body de 2,200, 2,200, 2,267 y 2,200 s; no se rehízo esta versión. FFmpeg volvió a muxear la voz aprobada y extendió el último frame. QA final: H.264 1080×1920/25 fps, video 11,800 s, AAC mono 44,1 kHz, 11,744 s; 9 384 015 bytes.
2. **`elliss-white-discount-02-04-hflip.mp4`** — solo `EllisWhite_corte_02.mp4` y `EllisWhite_corte_04.mp4` más la misma voz; flip horizontal solicitado explícitamente, sin música. Receta de 3 hooks y 3 body; se reutilizó un momento distinto de `corte_04` para el tercer beat del hook porque solo había dos archivos permitidos. Duraciones medidas: hooks 0,933 s cada uno; body 2,867, 3,000 y 3,000 s. FFmpeg aplicó `hflip` únicamente al video y extendió el último frame para preservar la voz. QA: H.264 1080×1920/25 fps, video 11,760 s, AAC mono 44,1 kHz, 11,744 s; 10 252 448 bytes.
3. **`elliss-white-discount-02-04-hflip-with-music-0.2x.mp4`** — misma edición #2, clips y flip; añadido el instrumental de celebración usado en Juice Discount (`audio_3dae2d554059.mp3`) a `volume=0.2`. FFmpeg copió el stream H.264 y mezcló solo la pista de música con `amix=inputs=2:duration=first:dropout_transition=0:normalize=0`; no se redujo la ganancia de la voz. QA: 1080×1920, 11,760 s, AAC mono 48 kHz, pico −0,7 dB, sin clipping; 10 241 441 bytes.

Las tres salidas se entregaron en Telegram y no se publicaron. Las copias NAS, staging y recetas temporales se limpiaron; las salidas no se guardaron en Cacho ni en el repo del servidor.

### Caso verificado: Ellis if01, tres videos con imágenes y música, 2026-10-27

**Fuentes y voz.** Se copiaron (sin mover ni alterar los originales) `Pointing_corte_01.mp4`, `Pointing_corte_02.mp4` y `Pointing_corte_03.mp4` desde `P:\Tiktok\hamaca\edits\06_Pointing\` a `P:\Tiktok\hamaca\edits\07_ellis_if01\`. Se reutilizaron cuatro audios aprobados, generados con PumaVoice01/`eleven_v3` y postprocesados con `atempo=1.5`: `ellis-if01-question-01-skin-health-ja.mp3`, `ellis-if01-question-02-vitamin-c-ja.mp3`, `ellis-if01-question-03-inner-care-ja.mp3` y la respuesta común `ellis-if01-answer-orange-cart-ja.mp3`. Los textos fueron `[curious] 肌の健康、気になってる？`, `[curious] ビタミンC、足りてる？`, `[curious] インナーケア、始めてみたい？` y `[excited] オレンジのカートをチェック！`. Cada pieza combina su pregunta, 0,300 s de silencio y la respuesta común; se retiró el audio de cámara. No se cambió más la velocidad de las voces.

**Imagen y montaje por corte.** Se aplicó 2× al video con `setpts=0.5*(PTS-STARTPTS)` y `hflip` solo a los fotogramas. Después se añadió una imagen cuadrada estática de 540×540 px en `x=48,y=120` sobre video 1080×1920; las imágenes no se espejaron. Orden de correspondencia: corte 01 → `img_a27753ec9718.jpg` (mujer tocándose las mejillas); corte 02 → `img_7d45a3f1d04a.jpg` (mujer con vaso de limón); corte 03 → `img_942c361c3c72.jpg` (mujer con frasco y fruta). QA visual confirmó margen visible y que no se taparan los ojos ni el gesto principal. Los originales de imagen permanecen en caché local; copias y overlays derivados están en el staging `D:\staging\filmcraft-ellis-if01-20261027\assets`. No se escribieron medios a Polaris.

**Variantes individuales finales** (H.264, 1080×1920, 30 fps; AAC copiado sin cambios al añadir cada imagen):
- `ellis-if01-pointing-corte-01-q1-answer-test-2x-hflip-skin-image-3x-lower.mp4` — 2 588 127 bytes; SHA-256 `deef9ca0228218a19f966940de1e364c6f2acee3ba34ccc0de1a216a9ef2b81d`.
- `ellis-if01-pointing-corte-02-q2-answer-test-2x-hflip-skin-image-3x-lower.mp4` — 2 843 084 bytes; SHA-256 `392a1010d0d2c65073e6af51dd85c8a43714506896d845ab01d7e9893e3ff5fe`.
- `ellis-if01-pointing-corte-03-q3-answer-test-2x-hflip-skin-image-3x-lower.mp4` — 3 852 172 bytes; SHA-256 `3fffb2cc26f758384af1c9abc239e7b5c19703f142f00de8d47626f0e543ce57`.

**Unión y música.** Se concatenaron esas tres variantes en orden 01→02→03 con cortes directos, sin crossfades. Se reutilizó el instrumental aprobado `P:\Tiktok\hamaca\edits\04_tagilas\assets\audio_3dae2d554059.mp3` (30,024 s, estéreo 48 kHz; SHA-256 `c8f235579823e11227250bfb7512f2db982dfc3fdae19dc27cf07eef6932ab85`). La música pasó por `volume=0.2` y `amix=inputs=2:duration=first:dropout_transition=0:normalize=0`; corre continua durante el montaje y queda limitada a la duración del audio de voz concatenado, sin atenuar ni normalizar la voz.

Salida final en `P:\Tiktok\hamaca\edits\07_ellis_if01\ellis-if01-pointing-01-02-03-with-music-0.2.mp4`: 9 233 047 bytes; SHA-256 `72c73033377875ad8a613c2f77beb6cd14b95925d9b6fdbeee3282a92fc3ca0d`; H.264 1080×1920/30 fps, 449 frames, video 14,967 s; AAC estéreo 44,1 kHz, audio 14,984 s; contenedor 14,985 s. `volumedetect`: media −19,5 dB, pico −0,9 dB, sin clipping; decodificación completa correcta. La hoja de contactos confirmó el orden, los tres overlays y ausencia de cuadros negros. Copia y SHA-256 se verificaron en Polaris. No se ejecutó Producer ni `/collage/create`; no hubo escritura a Firestore, cambios de código ni publicación.

**Estado FilmCraft, 2026-10-27:** se creó el proyecto local `D:\staging\filmcraft-ellis-if01-20261027\Ellis-IF01-Layered.fcproj` con FilmCraft CLI 0.9.0. La secuencia 1080×1920/30 fps tiene 449 frames (14,967 s): V1 contiene los tres videos; V2, tres PNG transparentes independientes; A1, las tres preguntas y tres instancias de la respuesta común; A2, la música aprobada a volumen lineal 0,2 (−13,9794 dB). Los 14 medios del paquete se copiaron a `assets/` y se verificaron por tamaño/SHA-256. El export `Ellis-IF01-Layered-preview.mp4` es H.264 1080×1920/30 fps, AAC estéreo 48 kHz; el CLI reportó `offlineMedia:[]`, la decodificación pasó y el pico fue −0,7 dB, sin clipping. SHA-256 del `.fcproj`: `90369D3F98F03758A72E8BFC54AA224228DAB2E68941924CDAEA75DE8E86B6B9`; del preview: `988b1329685f8725bf1bc2581b207fd1f4735e8c151e194e16bfc023f8bad502`. No se publicó.

La entrega permanece **local-only**: no se transfirió a Polaris. La última lectura del destino `P:\Tiktok\hamaca\edits\07_ellis_if01` falló con `pumassh: Not enough memory resources are available to process this command`; no se escribió al NAS y el error no prueba falta de RAM física. El proyecto aún referencia `D:\staging`; transferencia, relink y reapertura en la GUI interactiva de FilmCraft quedan pendientes. Conserva el staging hasta completar esas verificaciones. El proyecto MAGINA Tagiras de `04_tagilas` es otro caso; consulta el inventario de [[ttchop-filmcraft-video-tests]].

## Enlaces relacionados

- [[ttchop-video-generation]] — collage manual con catálogo y otros flujos de video.
- [[ttchop-music-generation]] — generación separada de música con ElevenLabs Music.
- [[acceso-remoto-pumadeskasus]] — acceso temporal al NAS Polaris mediante `pumassh`.
