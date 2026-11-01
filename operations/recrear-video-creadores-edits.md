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

## Pitfalls

- `pumassh` (wrapper Windows `P:`) hoy falla por memoria; no es la ruta.
- `P:` no existe en la sesión SSH de Windows: usar SMB con credenciales por stdin.
- En la PC, el venv de transcripción falla si las credenciales se leen con `readline()`.
- `ffprobe` por CIFS es lento: medir duraciones una vez y reutilizarlas en el recetario.
- No dejar credenciales en el wiki, en commits ni en el chat.
