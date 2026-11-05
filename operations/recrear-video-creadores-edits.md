---
title: Recrear un video de creador (tiktok/hamaca/edits)
created: 2026-11-01
updated: 2026-11-01
type: runbook
tags: [runbook, almacen, red, tailscale, pipeline]
status: active
confidence: high
related: [estudio-creadores-fuentes-datos, acceso-nas-polaris, ttchop-raw-asset-manual-edit, ttchop-video-generation]
---

# Recrear un video de creador (tiktok/hamaca/edits)

Procedimiento repetible para **recrear un video de Asu/Sora**: partir del video de
referencia, sacar su guion y su desglose audiovisual, escribir una variación del guion,
generar los audios y montar el video con el pipeline de `ttchop-server`.
Caso verificado de punta a punta: `01_squishy01` (2026-11-01). Ver también
[[estudio-creadores-fuentes-datos]], [[acceso-nas-polaris]] y
[[ttchop-raw-asset-manual-edit]].

## Estructura de carpetas en el NAS

`\\Polaris\Projects\Tiktok\hamaca\edits\<NN_nombre>\`

- `input/` — el video de referencia (p. ej. `snaptik_<id>_v3.mp4`) **y** los entregables del
  análisis (transcript + desgloses), más la lista de shots (`<NN_nombre>_shots.html` + `shots/` con
  los GIFs) cuando se preparó la grabación.
- `assets/audio/` — los audios generados (TTS), por línea y unidos.
- `assets/video/` — el material propio (clips grabados por Arturo).
- Raíz de la carpeta — el montaje final (`<NN_nombre>_edit*.mp4`), la portada
  (`<NN_nombre>_cover.png`), el **frame del thumbnail** (`<NN_nombre>_endcard_frame.png`) y los
  artefactos reproducibles: `<NN_nombre>_props.json` y `<NN_nombre>_recipe_matched.json`.

## Herramienta y artefactos de referencia

- **Toolkit versionado:** `ttchop-server/scripts/creators/` (rama del repo: **`master`**, que es su
  rama por defecto) — `build_recipe_from_plan.py` (receta desde un plan duración→clip, mide las
  duraciones con `ffprobe`), `measure_caption_style.py` (mide la banda del caption del creador),
  `extract_clip_frames.sh` (un frame por clip para la hoja de contacto) y `nas/{put,get,list_dir}.py`
  (SMB al NAS con credenciales validadas y hash de vuelta). El `README.md` de esa carpeta dice qué
  corre en qué host; los helpers SMB corren en **vps-tools** con el venv
  `/root/.venvs/nas-smb/bin/python` (trae `smbclient` — probado en vivo contra el NAS:
  `list_dir` y `get` funcionan y el hash bajado coincide). Usarlos en vez de reescribirlos.
  Verificado: `build_recipe_from_plan.py` **reproduce exactamente** el recetario del caso
  `01_squishy01` (los 17 clips con sus `trimStart`/`trimEnd`, delta 0).
- **Ejemplos reales por caso** (en la raíz de la carpeta del caso, en el NAS): `<NN_nombre>_props.json`
  (props completos de la composición `caption-overlay`) y `<NN_nombre>_recipe_matched.json` (recetario
  del montaje emparejado, plano↔clip). Copiarlos como plantilla para el video siguiente.
- **Toolkit de la lista de shots (para grabar):** `ttchop-server/scripts/creators/shotlist/` —
  transcripción del caso, cortes + frames, GIFs por shot, HTML y publicación por FTPS; con
  `shotlist.example.json` como plantilla real. Procedimiento en **§3b**.

## 0. Dónde corre cada cosa (infra)

- **Transcripción + frames de inspección:** en la PC `PumaDeskAsus` (tiene faster-whisper con
  GPU). Los medios no se copian al VPS.
- **Montaje:** en `vps-projects` con `ttchop-server`. Ese host **no** tiene credenciales del NAS,
  así que se monta el share (abajo).
- Crear el montaje una sola vez y reutilizarlo; el paso 5 lo documenta.

### Montar el NAS en vps-projects (una vez; read-only)

`ttchop-server` corre en `vps-projects`, que hoy no tenía cliente CIFS ni credenciales del NAS.
Consecuencia: para renderizar clips del NAS sin descargarlos hay que montar el share.

```bash
# 1) cliente
apt-get install -y cifs-utils

# 2) credenciales: pasar user/pass de /root/.config/pumassh/polaris.json (vps-tools)
#    por stdin de SSH cifrado a un archivo 600 en vps-projects. Nunca imprimirlas.
#    (en vps-tools) python3 -c "...print('username=…'); print('password=…')" | ssh … "umask 077; cat > /root/.smb-polaris.cred"

# 3) montaje
mount -t cifs //100.91.254.118/Projects /mnt/polaris \
  -o credentials=/root/.smb-polaris.cred,ro,vers=3.0,seal,uid=0,gid=0,noserverino
```

- **No usar `iocharset=utf8`**: falta el módulo `nls_utf8` y el mount falla con *error 79*
  (“Can not access a needed shared library”). Sin ese flag monta bien.
- TCP/445 del NAS ya responde desde vps-projects y el kernel 6.8 sí trae CIFS.
- Verificar leyendo un archivo y comparando su SHA-256 con una copia conocida.

## 1. Transcribir el audio del video de referencia (en la PC)

Se reutiliza el entorno del estudio de creadores: venv `D:\staging\hermes-transcription\venv`,
modelo `faster-whisper small` en `…\model`, `language=ja`, `beam_size=5`, `vad_filter=True`,
`device=cuda`. Las credenciales del NAS viajan por **stdin cifrado** y el script las lee con
`sys.stdin.read()` (con `readline()` falla porque el JSON es multilínea).

- Salida: transcript plano + segmentos con `start/end` (los tiempos del ASR son la base de todo
  lo que sigue).
- **Conservar el texto dudoso tal cual** y marcar los avisos de ASR; no corregir en silencio.
- Duración del audio de referencia = la referencia para ritmo (en `01_squishy01`: 25.82 s).

## 2. Desglose del original: script · recordings · video editing

Mismo formato que el estudio (ver [[estudio-creadores-fuentes-datos]] y el workspace
`creator-recording-editing` de Developer):

1. **Cortes candidatos:** detección de cambio de contenido
   (`ffmpeg -vf "select=gt(scene\,0.27),showinfo"`) → intervalos con sus duraciones.
   Son candidatos automáticos, **no** una EDL confirmada.
2. **Script:** movimientos por línea (hook, problem/desire, product introduction,
   feature→benefit, experience/proof, offer/urgency, closing/CTA) + avisos de ASR.
   Lo que se afirma en el audio (precios, descuentos, stock, “lo compré N veces”) son **claims
   del habla, no hechos verificados**.
3. **Recordings** por intervalo: `Shot`, `Angle`, `Camera Movement`, `DOF`, `Description`.
4. **Video editing** por intervalo: `Duration`, `Sequence`, `Post Movement`, `Video Speed`,
   `Subtitles`, `Headlines`, `Placement`, `Graphics/Images`, `Transitions`.
5. Si no es medible, se marca `NOT_ASSESSABLE`/`UNKNOWN` (velocidad y zoom digital casi siempre
   lo son). Muestrear 2 fps basta para clasificar y deja evidencia (frame + tiempo).

## 3. Escribir la variación del guion

- Misma estructura, mismas cifras, **palabras cambiadas**. Una línea por idea, en el idioma del
  original (japonés), con traducción al español para revisión.
- Sustituir lo que no se puede sostener: quitar testimonios personales no verificados
  (p. ej. “lo compré 4 veces”) y **no inventar porcentajes de descuento** — dejar la oferta
  genérica (“muy buena oferta”) o usar el % real de la campaña vigente.

## 3b. Lista de shots para grabar (HTML con GIFs)

Cuando hay que **grabar material propio**, antes del montaje se produce una **lista de shots**: un
recorte animado del original por cada intervalo, con qué grabar y cuánto debe durar. Se publica como
HTML para consultarlo desde el celular durante la grabación. Resultado real de `02_blanket`: 25
tomas · 26.6 s · 6 grupos · ~4 MB de GIFs.

Herramientas: `ttchop-server/scripts/creators/shotlist/` (con `shotlist.example.json` como plantilla
real del caso `02_blanket`).

1. **Transcripción** (PC): `transcribe_creator_ref.py <caso>` — baja la referencia del NAS por SMB
   (credenciales por `stdin`) y hace el ASR.
2. **Cortes y frames** (PC con ffmpeg): `analyze_ref_shots.py <video> <dir_salida> [umbral=0.27]` →
   `intervals.json` + **un frame en el punto medio de cada intervalo** + hoja de contacto.
   Los cortes son candidatos automáticos, no una EDL confirmada.
3. **Revisar y describir** (esto es criterio, no automatizable): mirar los frames uno por uno y
   escribir, por intervalo, `encuadre · ángulo · acción corta`, y **agrupar por tipo de toma** en un
   `shotlist.json` (parte de `shotlist.example.json`).
4. **GIFs**: `make_shot_gifs.py <video> <dir_shots> <dir_salida> 180 6` → `sNN.gif`
   (6 fps · 180 px · 64 colores · dither bayer). Fusiona los cortes falsos igual que el HTML.
5. **HTML**: `build_shotlist_html.py <dir_shots> <salida.html> <caso>` → tarjetas pequeñas con
   `duración · encuadre` + una línea de acción, **número rojo = su lugar en la edición**, selector
   **Agrupado / Por orden**, y el GIF animado con una miniatura embebida como respaldo.
6. **Publicar** (vps-tools): `publish_ftp.py put` (HTML) y `putmany` (los GIFs a `shots/`) en
   `/public_html/uploads/vps2/creators-research/<caso>/`, con lectura de vuelta; después verificar la
   URL por HTTP (200 + tamaño) y abrirla.
7. **Guardar copia en el NAS**: `input/<caso>_shots.html` + `input/shots/`.

Ejemplo publicado:
`https://lemonsushi.com/uploads/vps2/creators-research/02_blanket/02_blanket_shots.html`

Pitfalls:
- **Los frames van en el punto medio del shot**, no al inicio. Verificación usada: comparar el frame
  guardado con el del inicio y con el de la mitad (diferencia media de píxeles: ~1 = mismo cuadro,
  >10 = otro momento).
- **Un corte falso de 0.03 s desfasa la numeración**: si las descripciones se indexan por el número
  ya fusionado, cada shot se describe con la toma siguiente (en `02_blanket` apareció “celular” donde
  había un **libro** y un “unboxing” que no existía). Describir siempre por **frame del original**.
- **No inventar tomas que el original no tiene.** Si una línea habla de algo que no se ve (p. ej.
  「丸洗いもOK」 y no hay lavadora en el video), la lista refleja solo lo que hay; si se quiere añadir
  una toma propia, se marca como **extra**.
- Los GIFs van como archivos aparte (el HTML queda ligero) **con respaldo embebido**, para que el
  archivo suelto siga sirviendo sin conexión.

## 4. Generar los audios

- Voz **PumaVoice01** (`ve7BOdejheJbgrBriBx4`) y los **defaults del server**
  (`eleven_v3`, `mp3_44100_128`, `speed 0.5`), una toma por línea.
- Subir por línea (`line_NN.mp3`) y un unido, a `assets/audio/`.
- El default sale lento; para acercarse al ritmo del creador se acelera por línea con
  **`atempo`** (preserva el tono) y se une:
  - `1.4×` y `1.5×` unidos sin pausas ≈ ritmo del original;
  - “un poco más de espacio”: insertar **0.3 s** de silencio real (`anullsrc`) entre líneas.
- Medir siempre con `ffprobe`; comparar contra el audio de referencia.

## 5. Montar el video con ttchop-server

El builder es `ttchop-server/scripts/collage_builder.py`; recibe un **recipe JSON**:

```json
{"ffmpegRecipe": {
  "meta":  {"outputPath": "/root/<work>/out/<nombre>.mp4", "width": 1080, "height": 1920},
  "audio": {"src": "/mnt/polaris/…/assets/audio/<audio>.mp3"},
  "clips": [{"clipId":"s01","role":"body","src":"/mnt/polaris/…/assets/video/<clip>.mp4",
             "trimStart":2.664,"trimEnd":4.864,"speed":1.0}, …]}}
```

Reglas aprendidas:

1. **Duraciones:** para imitar el original, usar las duraciones de sus intervalos. Si el audio
   dura distinto, **escalar todas las duraciones por `audio_dur / suma_original`** (así el total
   cuadra y `-shortest` no recorta nada), o absorber la diferencia en el último plano.
2. **Velocidad natural (`1.0`)** cuando el original no tiene rampas.
3. **Empatar por contenido, no por orden de archivo:** extraer un fotograma de cada clip
   propio, verlos en una hoja de contacto e igualar cada plano del original con el clip que más
   se le parece (caja, presentación en mano, apretar, mesa, cadena, colgado de mochila…).
   Si no existe la toma (p. ej. “estirar”), usar la más cercana y **decirlo**.
4. `trimStart` ~0.5 s si al clip le sobra metraje (evita arranques en falso movimiento).
5. Comprobar que `/media/collage_temp` esté libre antes de lanzar (el builder usa ese directorio
   compartido y lo borra al terminar; no correr dos a la vez).
6. El builder escala/recorta a **1080×1920 (crop central)**: los clips horizontales 1920×1080 se
   recortan a vertical. Guardar los originales.

Ejecutar: `python3 scripts/collage_builder.py <recipe.json>` desde el repo.
Es **lento** cuando lee por CIFS; lanzarlo siempre en segundo plano. Con el escalado
**lanczos** (que el builder usa hoy para el ajuste a 1080×1920, commit `370d022`) tarda del
orden de **40 s por clip**: 25 tomas ≈ **16–18 min**.

**Nombres de los clips propios.** Arturo suele **numerar sus grabaciones por el número de shot**
de la lista (`1A`, `1B`, `2A`… `25A`). Cuando lo haga, el recetario es directo: **shot N → `<N>A.mp4`**;
si algún número no tiene archivo, se reutiliza el clip más parecido (él autoriza repetir tomas).
Verificar la asignación **contra el contenido** (hoja de contacto) antes de montar: el nombre no
garantiza que el plano coincida con el de la referencia.

## 6. QA y entrega

- `ffprobe` de ambos streams, decodificación completa, `volumedetect` (pico sin clipping),
  hoja de contacto y comparación de secuencia contra el original.
- Dejar el MP4 en la raíz de la carpeta del caso en el NAS y verificar el hash de vuelta.
- Es un **artefacto del builder directo**, no un render de Firestore. **No publicar** sin
  autorización explícita de Arturo.

## 7. Subtítulos y overlays

Estilo del original (medido píxel a píxel en 8 fotogramas a 720×1280): **no** es texto blanco con
contorno.

- **El caption es un sticker**: caja **blanca con esquinas redondeadas** y **texto oscuro** en
  negrita; ancho = texto + `2·padX`, alto = línea + `2·padY`, `borderRadius ≈ alto·0.42`, sombra suave.
- **Un solo renglón** y texto **corto** (4–10 caracteres), no la frase hablada completa.
- Centro vertical del caption en **≈26.3 % del alto** (a 1080×1920 → `y≈505`), centrado en x.
- Tamaños de referencia a 1080 de ancho: fuente ≈48, `padX` 26, `padY` 16.
- Al final del video: etiqueta «ここからチェック» (blanca con contorno oscuro, a la izquierda),
  **flecha roja con contorno blanco apuntando hacia abajo** y un **disclaimer** pequeño al pie
  («※クーポンや価格、割引率は投稿時点での情報です»).
- Los tiempos de cada caption se sacan del **audio real** (p. ej. `silencedetect` para localizar
  las pausas), no de estimaciones.

### Cómo se derivan los captions (regla)

- **Un caption por LÍNEA del guion**, no por plano: en `01_squishy01` hay 12 líneas → 12 captions,
  aunque el montaje tenga 17 planos. Dos o tres planos seguidos comparten caption.
- Texto = **frase-clave corta que resume esa línea** (4–10 caracteres: 「在庫復活」「ぷにぷに」
  「チェーン付き」「無くなる前にゲット」), no la frase hablada completa ni su traducción literal.
- Tiempos = **límites de la línea en el audio final**, y **encadenados**: cada caption dura hasta el
  inicio del siguiente (`end` de uno = `start` del próximo) para que no parpadee durante las pausas.
- Referencia real y completa: `01_squishy01_props.json` en la carpeta del caso en el NAS (props
  enteros de la composición, con los 12 captions, `tag`, `arrow`, `disc` y `endCard`).

### Opción elegida: Remotion (composición `caption-overlay`)

`ttchop-post_templates` incorpora una composición genérica **`caption-overlay`** en `main`:

- `src/CaptionOverlay.jsx` + registro en `src/Root.jsx` (1080×1920, fps 30, `durationInFrames`
  = fps × duración).
- Props: `videoSrc` (archivo dentro de `public/`, que está **gitignored** — nunca se commitea
  media), `captions[{text,start,end}]`, `pill{fontSize,padX,padY,radiusRatio,centerY,fg,bg}`,
  `tag{lines,start,end,x,y,fontSize}`, `arrow{start,end,x,y}`, `disc{text,start,end,x,y,fontSize}`.
  El ancho del texto cuenta caracteres ASCII como medio ancho (el `7` de «おまけが7個…»).
- Render: copiar el video base (p. ej. desde el NAS montado) a `public/` y ejecutar

  ```bash
  cd /root/projects/ttchop/ttchop-post_templates
  npx remotion render index.ts caption-overlay <salida>.mp4 --props=/tmp/props.json --crf=18
  ```

- Ventajas: queda **versionado y reutilizable** (para la siguiente recreación solo cambian los
  props) y permite animaciones por frame.
- **Audio:** Remotion entrega el audio en **estéreo y ~3 dB más bajo** que el base. La solución
  aplicada es **remuxear el audio original** (copia bit-exacta) sobre el render, no un ajuste de la
  composición:

  ```bash
  npx remotion render index.ts caption-overlay out_raw.mp4 --props=props.json   # render (video + overlays)
  ffmpeg -i out_raw.mp4 -i <video_base>.mp4 -map 0:v -map 1:a -c:v copy -c:a copy out.mp4
  ```

  Resultado verificado: mono, mean −18.2 dB / pico −1.8 dB (idéntico al base). Conservar el `_raw`.
- **Flecha del tag:** se ancla **por construcción** al bloque de texto (centro horizontal = centro
  del texto; borde superior `gap`≈18 px por debajo del texto), con `arrow.dx`/`dy` opcionales para
  ajustes. Antes usaba una `x/y` fija y quedaba desalineada.
- **Tipografía:** la pila de fuentes empieza por `KeinannMaruPOPjp` («けいなん丸ポップ体JP»,
  redondeada, la más parecida al original). Esa familia **solo tiene peso Regular**, así que el
  caption y el tag usan **`fontWeight: 400`** (configurable por prop): con `700` el navegador
  **sintetiza** la negrita (faux bold) y los trazos se ven engrosados y sucios. `Noto Sans CJK JP`
  sí tiene Bold real si en algún momento se quiere negrita auténtica.

### Thumbnail / portada al final (`endCard`)

Arturo pidió una **portada al estilo de las de Asu** (producto + texto) visible **en el último frame**
del video. Estilo de referencia: texto **blanco con contorno oscuro, sin caja**, 2 líneas centradas
en la zona media-alta.

- Prop opcional **`endCard`** que dibuja, en los últimos `frames` (default **1** = solo el último
  frame): la **imagen** a pantalla completa → una **capa negra translúcida** (`scrim.opacity` ≈0.35) →
  el **texto** con contorno.
  ```json
  "endCard": { "image": "<frame>.png", "frames": 1,
               "scrim": { "color": "#000000", "opacity": 0.35 },
               "text": { "lines": ["…","…"], "fontSize": 80, "centerY": 700,
                         "color": "#ffffff", "outlineColor": "#141414", "outlineWidth": 6 } }
  ```
- El frame base es un PNG extraído del montaje (en `public/`, gitignored); el `<OffthreadVideo>` se
  mantiene montado, así que **el audio no cambia**.
- **El PNG del frame ES la imagen del thumbnail** (el fondo de la portada): se guarda **también en el
  NAS**, junto al caso, como `<NN_nombre>_endcard_frame.png` — no basta con dejarlo en `public/`.
  **Registrar de qué cuadro salió:** en `01_squishy01` es el frame de **t=4.0 s** del montaje
  (`ffmpeg -ss 4.0 -i 01_squishy01_edit_matched.mp4 -frames:v 1 01_squishy01_endcard_frame.png`),
  elegido porque muestra la caja con los mini squishies y deja libre la zona del texto.
- **Antes de renderizar** hacen falta **dos archivos en `public/`** (los dos gitignored, no se
  commitean): el **video base** (copia del montaje del NAS) y el **PNG del frame**. El nombre del PNG
  debe coincidir con `endCard.image` de los props (en `01_squishy01`: `squishy01_endcard_frame.png`).
- **Cómo elegir ese frame:** uno donde el **producto se lea claro** y quede **espacio libre** para el
  texto (en `01_squishy01`: la caja con los mini squishies, t=4.0 s). Se extrae con
  `ffmpeg -ss <t> -i <montaje>.mp4 -frames:v 1 frame.png`, se revisa a ojo y se copia a `public/`.
  Sacar 5–6 candidatos en una hoja de contacto y elegir es más rápido que probar uno por uno.
- Para sacar la portada suelta: extraer el último frame del render a PNG
  (`ffmpeg -i final.mp4 -vf "select='eq(n,833)'" -frames:v 1 cover.png`).

### Alternativa one-off: PIL + ffmpeg

Stickers PNG generados con PIL (caja redondeada + texto oscuro) y superpuestos con
`overlay=x:y:enable='between(t,a,b)'`. Conserva el audio original **intacto**, pero no queda
versionado.

- Pitfall: **no** intentar la caja redondeada con dibujo vectorial ASS (`\p1`) — quedó
  desalineada; y con `BorderStyle=3` la caja usa el color de *outline*, no el de fondo.
- Fuente CJK disponible en vps-tools: `Noto Sans CJK JP`
  (`/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc`).

## 8. Hacer una VARIACIÓN de un video ya entregado

Un caso entregado se puede volver a editar (mismo material propio, guion/voz/edición nuevos) porque
**todo queda en su carpeta del NAS**. Cada caso entregado lleva un **`<caso>_MANIFEST.md`** en la raíz
de su carpeta con: la referencia, el material propio, **la tabla plano→clip de la receta** (con
`trimStart`/`trimEnd`), la voz, el guion, los captions con sus tiempos, los entregables y **la cadena de
comandos exacta** para rehacerlo. Empezar por leerlo: es el índice del caso.

- **Ubicación (los 3 casos recreados se movieron el 2026-11-05):** viven en
  **`tiktok/hamaca/edits/<NN>_<caso>/`** → **`10_squishy01`**, **`11_blanket`** y **`12_suitcase`**
  (antes en `creators_research/edits/`). Los **archivos internos conservan su prefijo viejo**
  (`01_squishy01_*`, `02_blanket_*`, `03_suitcase_*`), así que el manifiesto de cada uno avisa de su
  número nuevo. **Las recetas se reescribieron a la ruta nueva** (`/mnt/polaris/tiktok/hamaca/edits/…`)
  y sus rutas se verificaron una por una; si algún caso se vuelve a mover, reescribir
  `ffmpegRecipe.clips[].src` y `audio.src` de la receta y volver a verificar antes de montar.

Piezas y dónde viven:

| Pieza | Archivo | Para qué sirve en una variación |
|---|---|---|
| Referencia | `input/snaptik_*.mp4` (+ transcripción) | rehacer el guion o los tiempos |
| **Receta** | `<caso>_recipe*.json` | **el mapeo plano→clip y los recortes** (pieza crítica) |
| Material propio | `recordings/` o `assets/video/` | los clips; no se tocan |
| Voz | `assets/audio/` (por línea + unida) | reemplazarla si cambia el guion |
| Guion | `input/<caso>_script.md` o `script_*.json` | variar el diálogo |
| Captions | `props*.json` (o el `.fcproj` de FilmCraft) | rehacer los subtítulos |
| Entregables | `<caso>_final.mp4`, `*_endcard.png`, `*_cover.png` | comparar y como portada |

Pasos (detalle en el manifiesto del caso):

1. **Guion** → JSON de líneas → voz con el helper versionado
   `ttchop-server/scripts/creators/tts/tts_lines.mjs` (PumaVoice01), unir con `atempo` + pausas y medir
   (§4).
2. **Edición** → editar `clips[]` de la receta (orden, `trimStart`/`trimEnd`, `src`) y cambiar
   `meta.outputPath` para no pisar el render anterior.
3. **Montaje** → `python3 scripts/collage_builder.py <receta.json>` en vps-projects, en background
   (~18 min por corrida).
4. **Captions** → copiar el montaje a `public/` de `ttchop-post_templates`, actualizar el `props.json` y
   `npx remotion render index.ts caption-overlay … --props=… --crf=18` (§7).
5. **Audio final** → remux de la voz **en AAC y sin `-shortest`** (si no, se pierde el `endCard`).
6. **QA** → `ffprobe` + `volumedetect` + hoja de contacto + el último frame.

- **No** volver a correr `build_recipe_from_plan.py` si solo se ajusta un clip: recalcula los cortes por
  defecto y deshace el ajuste.
- **`01_squishy01` es el caso frágil:** sus clips conservan el **nombre de cámara**
  (`20261031_234928.mp4`…), así que **la única copia del mapeo plano→clip es la receta** (está en el NAS
  y su SHA-256 quedó anotado en el manifiesto). No borrar ni mover ese archivo.
- Los casos con **varios productos** (`03_suitcase`: `cicilife/` y `other/`) llevan un subdirectorio por
  producto; el guion y los captions se ajustan a las funciones de cada uno.

## Caso verificado — `10_squishy01` (archivos `01_squishy01_*`)

- Referencia: `input/snaptik_7685601865454587154_v3.mp4` — 25.83 s, 720×1280, 30 fps, audio ja.
- Transcripción ASR (12 segmentos) → `snaptik_…_v3.transcript.txt`.
- Desgloses → `01_squishy01_script.md` (offer-led) y `01_squishy01_recordings-editing.md`
  (16 cortes candidatos → 17 intervalos).
- Audios: `line_01..12.mp3` (defaults), `…_1p4x_joined` (26.31 s), `…_1p5x_joined` (24.56 s) y
  `…_1p5x_spaced` (27.85 s, con pausas de 0.3 s).
- Montajes: `01_squishy01_edit.mp4` (17 clips en orden de archivo, duraciones escaladas ×1.078)
  y `01_squishy01_edit_matched.mp4` (17 clips **empatados por contenido**, planos 1–16 con la
  duración exacta del original y el 17º absorbiendo los 2.01 s del audio). 27.81 s, 1080×1920.
- 33 clips propios en `assets/video/`; el **mapeo plano↔clip** queda en
  `01_squishy01_recipe_matched.json` (raíz de la carpeta del caso) y los **props completos** de la
  composición en `01_squishy01_props.json` — ya no solo en el chat de la sesión.
- **Subtítulos/overlays:** `01_squishy01_subs.ass` (versión one-off) y
  `01_squishy01_edit_matched_subs.mp4` (ffmpeg + stickers PNG, audio intacto). Versión **elegida
  por Arturo: Remotion** → `01_squishy01_remotion.mp4` (composición `caption-overlay`, audio
  remuxeado bit-exacto).
- **Portada final:** `01_squishy01_cover.png` (último frame del video: frame del producto +
  capa negra translúcida + texto blanco con contorno «1個買ったらおまけ7個 / 人気スクイーズ再入荷»),
  generado con el prop `endCard` de la composición.
- **Frame del thumbnail:** `01_squishy01_endcard_frame.png` — es el **fondo** de esa portada (frame de
  t=4.0 s del montaje, **sin** texto ni capa oscura: eso lo añade la composición). Es el archivo que
  hay que copiar a `public/` para re-renderizar.

## Caso verificado — `11_blanket` (archivos `02_blanket_*`, 2026-11-02/03)

- Referencia: `input/snaptik_7703402548501187847_v3.mp4` — 26.63 s, **720×1280 (vertical)**, audio ja.
- Transcripción: **11 líneas**. Guion variado aprobado por Arturo: 11 líneas / 207 caracteres, sin
  nombrar el color (la referencia decía “rosa”), sin nombre de marca y **sin ningún % de descuento**
  (la oferta quedó genérica).
- Voz: PumaVoice01, una toma por línea (`line_01..11.mp3`). Natural 33.41 s → **1.4× + pausas de
  0.3 s = 26.645 s** (referencia 26.633 s: +0.01 s). También se guardó la variante 1.5× (25.05 s).
- Lista de shots: **25 tomas · 6 grupos · GIFs 6 fps**, publicada en
  `https://lemonsushi.com/uploads/vps2/creators-research/02_blanket/02_blanket_shots.html`
- Grabación propia: **27 clips** en `recordings/`, **1920×1080 horizontales** a 30 fps (≈3.8 min de
  material). Arturo los **renombró por número de shot** (`1A`, `1B`, `2A`… `25A`).
- Montaje: `02_blanket_recipe.json` (shot N → `<N>A.mp4`; los shots **12 y 13** no tienen archivo y
  reutilizan `10A`/`11A` en otro tramo) → `02_blanket_edit.mp4`: **26.615 s, 1080×1920, 30 fps**,
  audio mono, pico −1.5 dB.
- **Lección de formato:** la referencia es vertical y el material propio se grabó horizontal; al
  recortar el centro a 9:16 solo se conservan 607×1080 y se amplían a 1080×1920 (**1.8×**). Por eso
  el builder pasó a usar **lanczos**. Grabar en vertical (o en 4K horizontal, que sí aguanta el
  recorte) evita esa pérdida.
- Continuación (cerrada el 2026-11-03): los captions/overlays y la portada del último frame se hicieron
  **dentro de FilmCraft** sobre este montaje, y el proyecto se migró al **layout escalonado en 3 pistas**.
  Todo el detalle —API de gráficos, trampa de `background_color`, relink a `P:` del paquete portable—
  está en [[ttchop-filmcraft-video-tests]].

## Caso verificado — `12_suitcase` (archivos `03_suitcase_*`, 2026-11-03/04)

- **Dos productos en un mismo caso:** `recordings/cicilife/` y `recordings/other/` (ambas maletas; el
  `cicilife` es la H1 de la ficha de TikTok Shop). Arturo confirmó a mitad del trabajo que el cicilife
  **tampoco** tiene soporte de móvil en la manija ni freno en las ruedas — de ahí la corrección del guion.
- Referencia: `snaptik_7690535153034202369_v3.mp4` — 31.767 s, 720×1280, 30 fps. ASR: 9 segmentos / 240
  caracteres (con errores esperables: 「超のメラカー」→「超滑らか」, 「クック」→「フック」, 「トッパー」→
  「ストッパー」, 「サイズでも」→「Sサイズでも」).
- **Cortes:** 28 intervalos (umbral 0.27) → **1 falso de 0.133 s (el 11)** → **27 tomas**.
- **Lista de shots (HTML en inglés, pedido explícito de Arturo):** 27 tomas · 6 grupos · GIFs 6 fps.
  El toolkit trae los textos de interfaz **fijos en español**: para entregarlo en inglés se traduce
  `shotlist.json` (grupos, `hint`, `enc`, `act`) y luego se sustituyen las cadenas de la UI al generar
  (título, `Grouped` / `By edit order`, `shots`, `No group`…). Comprobar que no quede ninguna en español.
- **Voz:** PumaVoice01, una toma por línea; natural 39.52 s → **`atempo 1.353` + pausas de 0.34 s =
  31.765 s** (referencia 31.743 s). Subida a `assets/audio/`.
- **Montaje:** `build_recipe_from_plan.py` (duraciones de la referencia) → `collage_builder.py`; 27 clips,
  31.76 s, ~18 min por corrida (lanczos leyendo por CIFS).
- **Captions:** 10 (uno por línea), tiempos de `silencedetect` sobre el audio final y **encadenados**;
  etiqueta + flecha + disclaimer + `endCard` (que es el thumbnail: el último frame).
- **Guion entregado (v3):** 10 líneas **reordenadas para que cada una caiga sobre la toma que le
  corresponde** (ver pitfalls), sin precio ni descuento, y sin las afirmaciones no verificables de la
  referencia («日本ブランド», «アルミ合金»).
- **Entregado:** `03_suitcase_cicilife_final.mp4` (953 frames, 1080×1920 a 30 fps, AAC mono 44.1 kHz,
  31.77 s, −17.7/−1.3 dB) + `03_suitcase_cicilife_endcard.png` (el thumbnail) + guion, plan, props y
  receta finales. Sin publicar.

## Pitfalls

- `pumassh` (wrapper Windows `P:`) hoy falla por memoria; no es la ruta.
- `P:` no existe en la sesión SSH de Windows: usar SMB con credenciales por stdin.
- En la PC, el venv de transcripción falla si las credenciales se leen con `readline()`.
- `ffprobe` por CIFS es lento: medir duraciones una vez y reutilizarlas en el recetario.
- Al añadir subtítulos, **medir el estilo en el original** (posición/tamaño/caja); es fácil asumir
  “blanco con contorno” cuando en realidad es caja blanca con texto oscuro.
- En FilmCraft la caja de fondo de un texto sale **negra por defecto**: si se usa `background: true` sin
  fijar `background_color`, el caption queda ilegible (letras oscuras sobre caja negra). Detalle en
  [[ttchop-filmcraft-video-tests]].
- **El builder recorta el CENTRO de los clips horizontales** (de 1920×1080 toma los 607 px centrales y los
  escala a 1080×1920): un sujeto en el borde **desaparece**. Revisar cada clip **con el recorte del
  builder** (`scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920`), no el
  clip completo. Si el sujeto queda fuera de cuadro, **ningún `trimStart` lo arregla**: hay que **cambiar
  el clip** (Arturo autoriza repetir una toma en otro punto, con un `trimStart` distinto al ya usado).
- **Los captions van por LÍNEA de voz, no por plano.** Si las tomas propias no siguen el orden de la
  referencia, el texto acaba contradiciendo la imagen (caso real: 「仕切り付き」 sobre el candado). El
  arreglo es **reescribir/reordenar el guion** para que cada línea corresponda a lo que se ve en su ventana
  de tiempo — no retocar los tiempos a mano.
- **No usar `-shortest` al remuxear el audio del render de Remotion:** recorta el último frame, que es
  justo donde va el `endCard` (el thumbnail del video). Entregar el audio en **AAC** (si se muxea el `.mp3`
  de la voz tal cual, el MP4 queda con pista mp3).
- **La duración de `caption-overlay` ya sale de los props** (`props.duration` o el máximo `end`; commit
  `81d0a04`). Antes estaba fija en 834 frames (27.8 s) y **cortaba cualquier video más largo**.
- Para tareas de código en `ttchop-post_templates`, el perfil `developer` puede estar
  **rate-limited**; en ese caso `developer_ds` sí corrió. Verificar siempre el commit en `origin/main`.
- No dejar credenciales en el wiki, en commits ni en el chat.
