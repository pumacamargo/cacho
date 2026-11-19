---
title: Montar videos en la PC (collage_builder en PumaDeskAsus)
created: 2026-11-19
updated: 2026-11-19
type: runbook
tags: [infra, video, runbook, nas, rendimiento]
status: active
confidence: high
---

# Montar videos en la PC (PumaDeskAsus)

Camino para ejecutar `collage_builder.py` **en la PC de escritorio** en lugar del VPS, cuando el
montaje es el cuello de botella. Medido y verificado el **2026-11-19**. Complementa
[[recrear-video-creadores-edits]] §5 (montaje) y [[ttchop-video-paths]]; el acceso Windows está en
[[acceso-remoto-pumadeskasus]] y el NAS en [[acceso-nas-polaris]].

## Por qué (causa real, medida)

El VPS **no** es lento por CPU: es lento **leyendo el NAS**.

- `vps-projects` (4 vCPU AMD EPYC, 7 GB, **sin GPU**) tiene Polaris montado por CIFS en
  `/mnt/polaris` (solo lectura). La conexión Tailscale al NAS es *directa* pero con
  **~243 ms de latencia** (IPv6), y SMB con esa latencia se arrastra.
- Lectura real medida: **un clip de 23 MB tardó 197 s (~0,12 MB/s)** con `cat`/`dd` desde
  `/mnt/polaris`. La extracción de un solo fotograma podía tardar más de un minuto.
- La PC está en la misma red que el NAS: **el mismo material se lee en segundos**.

## Comparación medida (mismo montador, misma receta)

Receta de prueba: los mismos 4 segmentos (01A, 02A, 3A, 4A de `20_dualshaver`) con la voz real
del caso, 10.4 s de video; `collage_builder.py` sin modificar su lógica en los dos lados.

| | PC (PumaDeskAsus) | VPS (`vps-projects`) |
|---|---|---|
| Tiempo total | **10.4 s** | **213 s** (3 min 33 s) |
| Peso de la salida | 4.96 MB | 4.98 MB |

**≈20× más rápido en la PC.** Salidas equivalentes: misma duración (10.4 s) y diferencia
imperceptible al comparar los dos archivos (SSIM 0.987, PSNR 44.5 dB) — del mismo orden que la
variación normal de codificar dos veces con x264.

Desglose en la PC: 6.0 s los cuatro recortes · 4.2 s la unión + audio.

**Prueba aparte (grafos ffmpeg crudos, mismo tramo):** x264 5.2 s / 5.34 MB · **NVENC 2.2 s /
12.48 MB** (`-cq 23`). NVENC es más rápido pero con ese ajuste pesa más del doble; su calidad,
comparada contra x264, dio SSIM 0.987 / PSNR 45.2 dB. Para adoptarlo habría que subir `-cq` y
volver a medir. En el camino de la PC **no** se usa NVENC: se mantiene x264 con los valores del
pipeline para no cambiar la calidad entregada.

## Requisitos en la PC (ya presentes, no hubo que instalar nada)

- **Python real 3.11.9**: `D:\staging\hermes-transcription\venv\Scripts\python.exe`. El
  `python.exe` que responde por defecto es el alias de la Microsoft Store, que no sirve.
- **ffmpeg/ffprobe**: `D:\staging\creator-av-audit\bin\ffmpeg.exe` (con NVENC disponible;
  máquina: Ryzen 5 3600X, 16 GB RAM, RTX 2060 SUPER).
- **NAS**: se monta dentro de la misma sesión SSH
  (`net use Z: \\100.91.254.118\Projects /user:… … /persistent:no`). Las credenciales se leen de
  `/root/.config/pumassh/polaris.json` y **nunca se imprimen**; el runner
  `/root/clipmap-20-dualshaver_tools/psrun.py` sustituye `__USER__`/`__PW__`, envía el script
  codificado en base64 y borra el secreto de la salida.
- La sesión **no interactiva** por SSH no hereda las unidades mapeadas del usuario (aparecen
  `P:`/`Z:` como *Unavailable*), así que el montaje se hace en la misma sesión.

## Montador adaptado (qué cambia)

Copia de `ttchop-server/scripts/collage_builder.py` con **cuatro cambios, ninguno en la lógica de
montaje**:

1. `FFMPEG`/`FFPROBE` por variable de entorno (`COLLAGE_FFMPEG`, `COLLAGE_FFPROBE`), con
   `ffmpeg`/`ffprobe` como valor por defecto. **Todas** las invocaciones las usan, incluida la
   unión final.
2. `LOG_DIR` (`COLLAGE_LOG_DIR`) y `temp_dir` (`COLLAGE_TEMP_DIR`) por entorno, con valores
   Windows por defecto.
3. Medición de tiempos (`TIMING total=… marks={…}` en el log y `timing_seconds` en el JSON de
   salida).
4. `COLLAGE_KEEP_TEMP=1` conserva los temporales para QA en vez de borrarlos.

Se conservan los filtros del original (`scale=1080:1920:force_original_aspect_ratio=increase:
flags=lanczos,crop=1080:1920,setpts=PTS-STARTPTS`), el recorte por `-ss/-t` clip a clip, la unión
por `concat` y el encode final `-c:v libx264 -pix_fmt yuv420p -c:a aac -shortest`.

Ubicación: **PC** `D:\staging\ttchop-montaje\collage_builder_win.py` · copia en `vps-tools`
`/root/pc-montaje/collage_builder_win.py`. No se tocó el script compartido del repo ni el pipeline.

## Procedimiento

1. Escribir la receta `recipe.json` con rutas **de la PC** (`Z:\Tiktok\…` para los clips, ruta
   local para el audio, `meta.outputPath` local).
2. Enviar por SSH un script de PowerShell que: monte `Z:`, asegure el directorio de trabajo,
   exporte `COLLAGE_FFMPEG`/`COLLAGE_FFPROBE`, **añada el bin de ffmpeg al `PATH`** y ejecute
   `python.exe collage_builder_win.py recipe.json` con la salida a un archivo de log.
3. Leer del log `TIMING …` y el JSON de salida; comprobar `duration`/`size` con `ffprobe`.
4. Subir el MP4 al NAS (desde la propia PC, que lo ve rápido) y verificar con lectura de vuelta
   (SHA-256) si aplica.

## Trampas encontradas

- **`$ErrorActionPreference='Stop'` aborta con stderr de un comando nativo.** Python escribe los
  logs a stderr, así que el script moría en la primera línea de log. Solución: `'Continue'` y
  redirigir todo a un archivo (`*> run.log`) y leerlo después.
- **ffmpeg tiene que estar en el `PATH` o absoluto en TODAS las llamadas.** Si solo se pasa el
  ejecutable de los recortes, la unión final falla con `'ffmpeg' is not recognized`.
- **`/mnt/polaris` en el VPS es de solo lectura**: la salida producida en el VPS se sube al NAS
  desde `vps-tools` por SMB (con lectura de vuelta), no copiando dentro de `/mnt/polaris`.
- **No hace falta instalar Python ni mapear el NAS de forma permanente** en la PC.

## Estado y alcance

- Verificado: montaje completo (recortes + unión + audio) en la PC con salida válida y copiada al
  NAS en `20_dualshaver\_ab_test\`.
- El pipeline **no** cambió: el VPS sigue haciendo voz, rótulos (Remotion), portada, QA y entrega.
- Pendiente de decisión: versionar el wrapper Windows en `ttchop-server/scripts/` (hoy vive solo
  en la PC y en `vps-tools`) y, si se adopta NVENC, reajustar `-cq` y volver a medir peso/calidad.
