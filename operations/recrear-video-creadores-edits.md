---
title: Recrear un video de creador (creators_research/edits)
created: 2026-11-01
updated: 2026-11-01
type: runbook
tags: [runbook, almacen, red, tailscale, pipeline]
status: active
confidence: high
related: [estudio-creadores-fuentes-datos, acceso-nas-polaris, ttchop-raw-asset-manual-edit, ttchop-video-generation]
---

# Recrear un video de creador (creators_research/edits)

Procedimiento repetible para **recrear un video de Asu/Sora**: partir del video de
referencia, sacar su guion y su desglose audiovisual, escribir una variación del guion,
generar los audios y montar el video con el pipeline de `ttchop-server`.
Caso verificado de punta a punta: `01_squishy01` (2026-11-01). Ver también
[[estudio-creadores-fuentes-datos]], [[acceso-nas-polaris]] y
[[ttchop-raw-asset-manual-edit]].

## Estructura de carpetas en el NAS

`\\Polaris\Projects\Tiktok\hamaca\creators_research\edits\<NN_nombre>\`

- `input/` — el video de referencia (p. ej. `snaptik_<id>_v3.mp4`) **y** los entregables del
  análisis (transcript + desgloses).
- `assets/audio/` — los audios generados (TTS), por línea y unidos.
- `assets/video/` — el material propio (clips grabados por Arturo).
- Raíz de la carpeta — el montaje final (`<NN_nombre>_edit*.mp4`).

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
Es **lento** cuando lee por CIFS (~25 s por clip); lanzarlo en segundo plano.

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

### Alternativa one-off: PIL + ffmpeg

Stickers PNG generados con PIL (caja redondeada + texto oscuro) y superpuestos con
`overlay=x:y:enable='between(t,a,b)'`. Conserva el audio original **intacto**, pero no queda
versionado.

- Pitfall: **no** intentar la caja redondeada con dibujo vectorial ASS (`\p1`) — quedó
  desalineada; y con `BorderStyle=3` la caja usa el color de *outline*, no el de fondo.
- Fuente CJK disponible en vps-tools: `Noto Sans CJK JP`
  (`/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc`).

## Caso verificado — `01_squishy01`

- Referencia: `input/snaptik_7685601865454587154_v3.mp4` — 25.83 s, 720×1280, 30 fps, audio ja.
- Transcripción ASR (12 segmentos) → `snaptik_…_v3.transcript.txt`.
- Desgloses → `01_squishy01_script.md` (offer-led) y `01_squishy01_recordings-editing.md`
  (16 cortes candidatos → 17 intervalos).
- Audios: `line_01..12.mp3` (defaults), `…_1p4x_joined` (26.31 s), `…_1p5x_joined` (24.56 s) y
  `…_1p5x_spaced` (27.85 s, con pausas de 0.3 s).
- Montajes: `01_squishy01_edit.mp4` (17 clips en orden de archivo, duraciones escaladas ×1.078)
  y `01_squishy01_edit_matched.mp4` (17 clips **empatados por contenido**, planos 1–16 con la
  duración exacta del original y el 17º absorbiendo los 2.01 s del audio). 27.81 s, 1080×1920.
- 33 clips propios en `assets/video/`; mapeo usado documentado en el chat de la sesión.
- **Subtítulos/overlays:** `01_squishy01_subs.ass` (versión one-off) y
  `01_squishy01_edit_matched_subs.mp4` (ffmpeg + stickers PNG, audio intacto). Versión **elegida
  por Arturo: Remotion** → `01_squishy01_remotion.mp4` (composición `caption-overlay`), con el
  pendiente de audio estéreo/‑3 dB anotado arriba.

## Pitfalls

- `pumassh` (wrapper Windows `P:`) hoy falla por memoria; no es la ruta.
- `P:` no existe en la sesión SSH de Windows: usar SMB con credenciales por stdin.
- En la PC, el venv de transcripción falla si las credenciales se leen con `readline()`.
- `ffprobe` por CIFS es lento: medir duraciones una vez y reutilizarlas en el recetario.
- Al añadir subtítulos, **medir el estilo en el original** (posición/tamaño/caja); es fácil asumir
  “blanco con contorno” cuando en realidad es caja blanca con texto oscuro.
- Para tareas de código en `ttchop-post_templates`, el perfil `developer` puede estar
  **rate-limited**; en ese caso `developer_ds` sí corrió. Verificar siempre el commit en `origin/main`.
- No dejar credenciales en el wiki, en commits ni en el chat.
