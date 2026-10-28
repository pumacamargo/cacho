---
title: Edición manual Producer-style con solo audio y videos
created: 2026-10-26
updated: 2026-10-28
type: runbook
tags: [sistema, runbook, pipeline]
status: active
confidence: high
related: [ttchop-video-generation, ttchop-music-generation, acceso-remoto-pumadeskasus]
---

# Edición manual Producer-style con solo audio y videos

Este flujo sirve cuando se cuenta con **un audio aprobado por Arturo y archivos de video originales**, pero no existe una ficha de producto ni `sessions` con metadata en Firestore. No se ejecuta `runProducer()`: se prepara un montaje manual con `ttchop-server/scripts/collage_builder.py` y se entrega el MP4. No inventes ni persistas productos, sesiones o clips de catálogo. Para leer el NAS usa el alcance temporal documentado en [[acceso-remoto-pumadeskasus]]; para los flujos de collage y música existentes consulta [[ttchop-video-generation]] y [[ttchop-music-generation]].

## Procedimiento reutilizable

**Regla de recorte de movimiento (preferencia de Arturo):** no quites el último segundo ni asumas cantidad o punto de corte por defecto. Haz ese recorte solo cuando Arturo lo pida explícitamente. Si pide recortar pero no especifica cuánto o dónde, pregunta antes de editar. Si también pide conservar la voz aprobada, mantén intacto el audio y define el tratamiento visual del tramo final según su instrucción.

**Acceso NAS para nuevas tareas:** priorizar SMB directo desde el VPS según [[acceso-nas-polaris]], sin Windows intermediario. Conservar los métodos de staging/SSH descritos abajo para trabajos que necesiten Windows y para reproducir casos históricos. Esta prioridad no cambia el estado pendiente de entregas existentes ni acredita escritura directa o reapertura en FilmCraft.

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

**Imagen y montaje por corte.** Se aplicó 2× al video con `setpts=0.5*(PTS-STARTPTS)` y `hflip` solo a los fotogramas. Después se añadió una imagen cuadrada estática de 540×540 px en `x=48,y=120` sobre video 1080×1920; las imágenes no se espejaron. Orden de correspondencia: corte 01 → `img_a27753ec9718.jpg` (mujer tocándose las mejillas); corte 02 → `img_7d45a3f1d04a.jpg` (mujer con vaso de limón); corte 03 → `img_942c361c3c72.jpg` (mujer con frasco y fruta). QA visual confirmó margen visible y que no se taparan los ojos ni el gesto principal. Los originales de imagen permanecen en caché local; copias y overlays derivados están en el staging `D:\staging\filmcraft-ellis-if01-20261027\assets`. La nota anterior «No se escribieron medios a Polaris» se refería solo a ese primer pase de overlays, no al estado posterior: el paquete FilmCraft con sus 14 medios y los tres MP4 individuales previos se verificaron después en Polaris (véase abajo).

**Variantes individuales anteriores al recorte** (H.264, 1080×1920, 30 fps; AAC copiado sin cambios al añadir cada imagen; los tres archivos fueron verificados en Polaris):
- `ellis-if01-pointing-corte-01-q1-answer-test-2x-hflip-skin-image-3x-lower.mp4` — 2 588 127 bytes; SHA-256 `deef9ca0228218a19f966940de1e364c6f2acee3ba34ccc0de1a216a9ef2b81d`.
- `ellis-if01-pointing-corte-02-q2-answer-test-2x-hflip-skin-image-3x-lower.mp4` — 2 843 084 bytes; SHA-256 `392a1010d0d2c65073e6af51dd85c8a43714506896d845ab01d7e9893e3ff5fe`.
- `ellis-if01-pointing-corte-03-q3-answer-test-2x-hflip-skin-image-3x-lower.mp4` — 3 852 172 bytes; SHA-256 `3fffb2cc26f758384af1c9abc239e7b5c19703f142f00de8d47626f0e543ce57`.

**Unión y música.** Se concatenaron esas tres variantes en orden 01→02→03 con cortes directos, sin crossfades. Se reutilizó el instrumental aprobado `P:\Tiktok\hamaca\edits\04_tagilas\assets\audio_3dae2d554059.mp3` (30,024 s, estéreo 48 kHz; SHA-256 `c8f235579823e11227250bfb7512f2db982dfc3fdae19dc27cf07eef6932ab85`). La música pasó por `volume=0.2` y `amix=inputs=2:duration=first:dropout_transition=0:normalize=0`; corre continua durante el montaje y queda limitada a la duración del audio de voz concatenado, sin atenuar ni normalizar la voz.

Montaje anterior al recorte, preservado en `P:\Tiktok\hamaca\edits\07_ellis_if01\ellis-if01-pointing-01-02-03-with-music-0.2.mp4`: 9 233 047 bytes; SHA-256 `72c73033377875ad8a613c2f77beb6cd14b95925d9b6fdbeee3282a92fc3ca0d`; H.264 1080×1920/30 fps, 449 frames, video 14,967 s; AAC estéreo 44,1 kHz, audio 14,984 s; contenedor 14,985 s. `volumedetect`: media −19,5 dB, pico −0,9 dB, sin clipping; decodificación completa correcta. La hoja de contactos confirmó el orden, los tres overlays y ausencia de cuadros negros. Copia y SHA-256 se verificaron en Polaris. No se ejecutó Producer ni `/collage/create`; no hubo escritura a Firestore, cambios de código ni publicación.

### Actualización: recorte de movimiento y nuevo montaje, 2026-10-28

Por solicitud de Arturo, a cada uno de los tres cortes se le retiró el último segundo de movimiento (30 frames a 30 fps) y se congeló el cuadro final para conservar completo el audio aprobado. La comparación PCM confirmó que el audio de cada salida individual es idéntico al de su fuente. Los archivos individuales recortados quedaron en scratch local; al verificar Polaris no estaban presentes bajo estos nombres:

- `ellis-if01-pointing-corte-01-menos-1s-movimiento-audio-completo.mp4` — 29 037 787 bytes; SHA-256 `cfc35149d70a959403783785fd537b210dc9dc0aa7c7bea53aefb3728b1fffcc`.
- `ellis-if01-pointing-corte-02-q2-answer-test-2x-hflip-skin-image-3x-lower-menos-1s-movimiento-audio-completo.mp4` — 31 700 720 bytes; SHA-256 `d8260a32121146850de4d1c8de043bbe0bacfb3637283a67f68a9bf3dcc0ff10`.
- `ellis-if01-pointing-corte-03-q3-answer-test-2x-hflip-skin-image-3x-lower-menos-1s-movimiento-audio-completo.mp4` — 41 903 442 bytes; SHA-256 `838f8885ca2991b8ea3f9ec5cda1aa693dd1dfb5d03cfcb22648405008463007`.

Se concatenaron esas tres versiones nuevas en orden 01→02→03 y se añadió una sola pista continua del instrumental aprobado `audio_3dae2d554059.mp3` a volumen lineal 0,2. No se reinició la música en cada corte ni se aplicó ganancia adicional a las voces. El nuevo MP4, sin sobrescribir el montaje anterior, quedó en `P:\Tiktok\hamaca\edits\07_ellis_if01\ellis-if01-pointing-01-02-03-minus-1s-motion-with-music-0.2.mp4`: 12 340 702 bytes; SHA-256 `b1293e9ca54cf1d8398af8b208447e7eb7837b1b066f14b76062d485cb338f45`. H.264 1080×1920/30 fps, 449 frames (video 14,966667 s); AAC estéreo 44,1 kHz (audio/contenedor 14,973333 s; diferencia entre streams menor a un frame). La decodificación completa y la inspección visual de orden, límites de cortes, overlays y cuadros finales pasaron; se confirmó música durante las pausas. Pico medido −1,1 dB, sin clipping. Tamaño y SHA-256 se leyeron de vuelta en Polaris y coincidieron; el staging temporal se limpió después de esa comprobación.

Este MP4 es un render aplanado separado: el `.fcproj` FilmCraft no se modificó ni se actualizó con estos cortes nuevos; su reapertura en la GUI sigue pendiente. El montaje anterior permanece intacto. No se publicó ni se ejecutaron Producer, `/collage/create` o escrituras a Firestore.

**Construcción FilmCraft local, 2026-10-27:** se creó el proyecto `D:\staging\filmcraft-ellis-if01-20261027\Ellis-IF01-Layered.fcproj` con FilmCraft CLI 0.9.0. La secuencia 1080×1920/30 fps tiene 449 frames (14,967 s): V1 contiene los tres videos; V2, tres PNG transparentes independientes; A1, las tres preguntas y tres instancias de la respuesta común; A2, la música aprobada a volumen lineal 0,2 (−13,9794 dB). Los 14 medios del paquete se copiaron a `assets/` y se verificaron por tamaño/SHA-256. El export `Ellis-IF01-Layered-preview.mp4` es H.264 1080×1920/30 fps, AAC estéreo 48 kHz; el CLI reportó `offlineMedia:[]`, la decodificación pasó y el pico fue −0,7 dB, sin clipping. SHA-256 del `.fcproj` original: `90369D3F98F03758A72E8BFC54AA224228DAB2E68941924CDAEA75DE8E86B6B9`; del preview: `988b1329685f8725bf1bc2581b207fd1f4735e8c151e194e16bfc023f8bad502`. No se publicó.

**Estado al 2026-10-27 (histórico):** la entrega era local-only; la lectura del destino `P:\Tiktok\hamaca\edits\07_ellis_if01` falló con `pumassh: Not enough memory resources are available to process this command`. En ese momento no se había escrito al NAS y el proyecto aún apuntaba a `D:\staging`; no interpretar esto como el estado actual. Conserva el staging hasta completar las verificaciones GUI.

**Actualización de entrega NAS, 2026-10-28:** el paquete portable está en `P:\Tiktok\hamaca\edits\07_ellis_if01\filmcraft-ellis-if01-20261027\`; los medios están en `P:\Tiktok\hamaca\edits\07_ellis_if01\assets\`. SHA-256 del proyecto portable: `41fb0eb7386e3aa8c520385d826bc9e63aee3c82381d7e6d6a8eb8538f31713a`; del preview: `988b1329685f8725bf1bc2581b207fd1f4735e8c151e194e16bfc023f8bad502`. Se verificaron los 14 medios contra tamaño/SHA-256 del manifest y 14 rutas `P:`/cero rutas `D:` en el `.fcproj`. El staging original permanece con 14 medios. El transporte fue una ruta temporal Windows/SSH por IP Tailscale; no es una reparación permanente del `pumassh` por nombre corto ni una prueba de escritura SMB directa. Falta reabrir el `.fcproj` final en la GUI interactiva para validar medios online; no publicado. Para el inventario por caso, consulta [[ttchop-filmcraft-video-tests]].

### Nuevo test: Ellis hair, preguntas 01–03, 2026-10-28

**Parámetros aprobados:** los tres cortes se exportaron primero como videos separados. Para cada uno se usa el video a 2×, se retira 1 s de movimiento (30 frames a 30 fps) cuando Arturo lo pide, y se aplica `hflip` al video antes de añadir la imagen; las imágenes no se espejan. El overlay correspondiente es 540×540 px en `x=48,y=120`. Las locuciones japonesas se aceleran individualmente a 1,5× y después se inserta una pausa fija de 0,3 s entre pregunta y respuesta común; la pausa no se acelera. Se descarta el audio de cámara. Los renders individuales de esta tanda no llevan música; para el montaje final solicitado por Arturo se agregó el instrumental aprobado como una sola pista continua, sin atenuar las voces. Se conserva el texto completo de voz y se revisa por separado cualquier cola entre video y locución antes de exportar.

Guiones: pregunta 01 `[curious] 髪が広がってまとまらない？`, pregunta 02 `[curious] サラサラの髪、憧れない？`, pregunta 03 `[curious] 髪のパサつき、気にならない？`; respuesta común `[excited] オレンジのカートをチェック！`. Los originales `Pointing_corte_01.mp4`–`03.mp4` de `06_Pointing` no se movieron ni alteraron. PNGs derivados: `hair_overlay_01_frizz.png`, `hair_overlay_02_silky.png` y `hair_overlay_03_dry_ends.png`.

- **Clip 01, final aprobado:** `pointing-hair-frizz-01-hflip-minus-1s-motion-voice-1.5x.mp4`, solo en scratch local `/root/.hermes/profiles/ttchop_robot/cache/scratch/ellis-hair-video-20261028/outputs/`; 3 298 106 bytes, SHA-256 `37bd72cd15a826104ca205be386787fb7fee8f5b3369fc738290a5a4505843d3`. H.264 1080×1920/30 fps, 97 frames/3,233333 s; AAC mono 44,1 kHz/3,224467 s. Voz completa, pausa conservada, pico −0,9 dB, decodificación completa y QA visual correctos; sin cola congelada perceptible.
- **Clip 02, final verificado:** `pointing-hair-silky-02-hflip-minus-1s-motion-voice-1.5x.mp4`, en el mismo scratch; 4 087 716 bytes, SHA-256 `ebeeb113091b75309d1957f57f7df019d054d98f62398aafa84af3bf58ff49eb`. H.264 1080×1920/30 fps, 105 frames/3,500 s; AAC mono 44,1 kHz/3,500 s. La voz acelerada y la pausa duran 3,136122 s; se añadió después 0,363878 s de silencio para completar la duración del video (el audio y el video se midieron por separado). Pico −0,9 dB, sin clipping; decodificación y contact sheet correctos. El overlay de cabello sedoso no tapa el rostro ni el gesto principal.
- **Clip 03, final según elección de Arturo:** `pointing-hair-dry-ends-03-hflip-minus-1s-motion-voice-1.5x-silence-tail.mp4`, en el mismo scratch; 6 089 148 bytes, SHA-256 `02fd6a6db962edc03d3bc37c0b7a3e675fcd2dc88ae634ca9aff44ab41c6f8a0`. H.264 1080×1920/30 fps, 157 frames/5,233333 s; AAC mono 44,1 kHz/5,233333 s. La locución 03+respuesta dura 3,070385 s y se añadieron 2,162948 s de silencio al audio; el video sigue en movimiento durante esa cola, como pidió Arturo. Pico −0,9 dB, cola AAC verificada en silencio, decodificación completa y contact sheet correctos.

Las salidas individuales 01–03 son renders locales aplanados, no proyectos FilmCraft; permanecen en scratch local. No se publicaron y no se ejecutaron Producer, `/collage/create` ni escrituras a Firestore.

**Montaje final con música continua, 2026-10-28:** `ellis-hair-pointing-01-02-03-with-music-0.2-20261028.mp4`, verificado en `P:\Tiktok\hamaca\edits\07_ellis_if01\` y en `/root/.hermes/profiles/ttchop_robot/cache/scratch/ellis-hair-video-20261028/outputs/ellis-hair-pointing-01-02-03-with-music-0.2-20261028.mp4`; 9 589 479 bytes, SHA-256 `8a347e9b290db0429a2392434979232e2b3754f12152f51e750d5a660a5e469b`. Se concatenaron los clips finales en orden 01→02→03, con cortes directos. Música: `P:\Tiktok\hamaca\edits\04_tagilas\assets\audio_3dae2d554059.mp3`, 30,024 s, estéreo/48 kHz, SHA-256 `c8f235579823e11227250bfb7512f2db982dfc3fdae19dc27cf07eef6932ab85`; ganancia lineal `volume=0.2`, música continua y limitada a la duración del montaje. No se atenuó ni normalizó la voz. Para alinear el audio del clip 01 con su video se añadió únicamente 0,008866 s de silencio tras la voz completa.

El montaje final es H.264 1080×1920/30 fps, 359 frames/11,966667 s; AAC estéreo/44,1 kHz, 11,966667 s. QA: decodificación completa; contact sheet sin cuadros negros y cortes/overlays limpios; música presente en las colas silenciosas; pico PCM −0,66 dBFS y 0 muestras saturadas. El hash y tamaño se leyeron de vuelta en Polaris; staging temporal eliminado tras esa verificación. Es un MP4 aplanado, no se modificó el proyecto FilmCraft ni se publicó.

### Hook alternativo Ellis IF01: belleza interior, clip 01, 2026-10-28

Arturo pidió solo el primero de tres guiones nuevos y especificó reutilizar los videos originales de `06_Pointing` con el tratamiento de los clips recientes. Fuente `P:\Tiktok\hamaca\edits\06_Pointing\Pointing_corte_01.mp4` (9 241 817 bytes; SHA-256 `f0b297d43bdab627ba4ba210569b9aee3ef97eaac33f38dbe69bafcaee315450`); original intacto. La primera entrega fue una versión inicial que reutilizó el stream visual ya aprobado del clip 01 anterior: video 2×, `hflip`, quitar 1 s/30 frames de movimiento y overlay `hair_overlay_01_frizz.png` de 540×540 px en `x=48,y=120`, sin espejar la imagen. En esa versión se conservó el stream visual anterior sin recodificar; después Arturo pidió una imagen específica para este hook.

Guion nuevo: `[curious] 内側からキレイになりたい？` → `[excited] オレンジのカートをチェック！`. La nueva pregunta se sintetizó con el helper `textToSpeech` de `ttchop-server/pipeline/elevenlabs.js` (PumaVoice01 `ve7BOdejheJbgrBriBx4`, `eleven_v3`) y se postprocesó a 1,5×. Se reutilizó la respuesta común aprobada; pausa fija de 0,3 s. Sin música. Secuencia de voz: 3,181270 s; se completó el video con 0,052063 s de silencio.

MP4 aplanado de la primera entrega: `/root/.hermes/profiles/ttchop_robot/cache/scratch/ellis-if01-script-variants-20261028/outputs/pointing-inner-beauty-01-hflip-minus-1s-motion-voice-1.5x.mp4`. Copia histórica en Polaris: `P:\Tiktok\hamaca\edits\07_ellis_if01\pointing-inner-beauty-01-hflip-minus-1s-motion-voice-1.5x.mp4`. Tamaño 3 303 002 bytes; SHA-256 `f12252f30fbf8d52a627a883519563c61e7b2a7aebc2198e0fb541c3ca0e03b1`. H.264 1080×1920/30 fps, 97 frames/3,233333 s; AAC mono/44,1 kHz. Pico −0,90 dBFS, cero muestras saturadas, decodificación completa. La entrega actual con imagen propia está registrada a continuación; la versión inicial se conservó.

### Imágenes nuevas y clip 01 actualizado, 2026-10-28

Arturo proporcionó tres prompts: (1) mujer japonesa adulta en una cocina matutina con un vaso de agua; (2) retrato cercano de mujer japonesa adulta con expresión curiosa y dedo en la barbilla; (3) uvas Shine Muscat en primer plano con una mujer sonriente desenfocada. Kie.ai `bytedance/seedream-v4-text-to-image`, `square_hd`, `1K`, un trabajo por prompt. IDs `0c86d893860be39064542f6170043635`, `533ea7a56824eafad90b679787d2f323`, `12434cf3cd5cbf5758bc55195c98397c`; `creditsConsumed` real 5 por trabajo, total 15. Las tres salidas fueron inspeccionadas: cuadradas, sin texto, logos, envases ni collage.

PNGs finales 540×540 (no espejear; overlay en `x=48,y=120`):
- `ellis-if01-inner-beauty-01-540x540.png` — 604 732 bytes; SHA-256 `eaee1ded1c2a2aa23c97651a68d9f86cdcb604762040ab5233cc29dedd4ad14f`.
- `ellis-if01-l-cystine-02-540x540.png` — 714 116 bytes; SHA-256 `b0653455ca793a7abd8ee2325ea74b1615259d6baf12f7026e7bce947bd4a957`.
- `ellis-if01-muscat-03-540x540.png` — 662 274 bytes; SHA-256 `c8d24573269b924033a3077e303e2ec91111a379ea975fcea414ea396b01eb1e`.

Para el clip 01 se regeneró solo el video: `hflip` antes del overlay 01 nuevo; se conservaron velocidad visual 2×, recorte explícito de 1 s, voz 1,5×, pausa de 0,3 s, cola silenciosa de 0,052063 s y ausencia de música/cámara. La pista AAC se remuxeó desde la primera entrega con stream copy; el hash de paquetes de audio permaneció idéntico (`db765645d3f170ec792767df32af7199783448896c70cbe9698fd74ae7cf9439`). QA visual: cuadro nuevo no espejado en `x=48,y=120`, sin tapar la cara ni el gesto principal. Full decode correcto; H.264 1080×1920/30 fps, 97 frames/3,233333 s; AAC mono/44,1 kHz, 3,232993 s; pico −0,90 dBFS (audio sin cambios).

Versión actual local: `/root/.hermes/profiles/ttchop_robot/cache/scratch/ellis-inner-beauty-overlays-20261028/outputs/pointing-inner-beauty-01-hflip-minus-1s-motion-voice-1.5x-new-square-image-corrected.mp4`. Entrega canónica en Polaris: `P:\Tiktok\hamaca\edits\07_ellis_if01\pointing-inner-beauty-01-hflip-minus-1s-motion-voice-1.5x-new-square-image-corrected.mp4`; 3 440 492 bytes; SHA-256 `769243dd46cd0a346a52f617978490a6282c8d07fba59d8738ff9d9f1a1f6958`. Los tres PNGs anteriores también se copiaron a esa carpeta; lecturas de vuelta confirmaron tamaños y hashes. Se conserva la primera versión. Entregado como MP4 aplanado más PNGs individuales; no se creó proyecto FilmCraft ni se publicó.

### Clip 02 actualizado: L-シスチン, 2026-10-28

Arturo autorizó continuar con el clip 02 y su overlay correspondiente. Fuente `P:\Tiktok\hamaca\edits\06_Pointing\Pointing_corte_02.mp4` (10 110 058 bytes; SHA-256 `390f2b884f6a063b28b346e1e4a9f112f8f84839495996939cdf4b44d5991809`); original intacto. Guion: `[curious] L-シスチンって聞いたことある？` → `[excited] オレンジのカートをチェック！`. Se aplicó video 2×, `hflip` antes del overlay `ellis-if01-l-cystine-02-540x540.png` (540×540, `x=48,y=120`, no espejado), recorte de 1 s de movimiento, voz 1,5× y pausa de 0,3 s. Sin audio de cámara ni música.

MP4 local: `/root/.hermes/profiles/ttchop_robot/cache/scratch/ellis-inner-beauty-overlays-20261028/outputs/pointing-l-cystine-02-hflip-minus-1s-motion-voice-1.5x-with-image.mp4`. Polaris: `P:\Tiktok\hamaca\edits\07_ellis_if01\pointing-l-cystine-02-hflip-minus-1s-motion-voice-1.5x-with-image.mp4`; 3 801 605 bytes; SHA-256 `b6aadc2ad5709f6f903485d1f52de1027bc667fdc65e4e4a46e31ad93f0dbe1b`. H.264 1080×1920/30 fps, 105 frames/3,5 s; AAC mono/44,1 kHz/3,5 s. Se remuxeó el audio aprobado del render de guion anterior con `-c:a copy`; hash de paquetes idéntico (`ca569f1748151d9f6ad7ffb81e164a36b14d905b5b01d732708432ec5f860b17`). Full decode, pico −0,9 dBFS, cero clipping y contact sheet correctos; overlay no tapa la cara ni el gesto. SMB verificó tamaño/hash de vuelta; no publicado.

### Clip 03: preflight de cola, pendiente de decisión

La imagen `ellis-if01-muscat-03-540x540.png` está lista y verificada, pero el clip 03 actualizado no se ha renderizado ni entregado. El render de guion existente dura 5,233 s y su pista tiene aproximadamente 2,54 s de silencio al final mientras sigue el movimiento. Como esa cola es mucho más larga que la del clip 01, falta la decisión de Arturo: conservarla o recortar el movimiento para terminar cerca del final de la voz. No asumir que la decisión de otro guion autoriza este cambio.

## Enlaces relacionados

- [[ttchop-video-generation]] — collage manual con catálogo y otros flujos de video.
- [[ttchop-music-generation]] — generación separada de música con ElevenLabs Music.
- [[acceso-remoto-pumadeskasus]] — acceso temporal al NAS Polaris mediante `pumassh`.
