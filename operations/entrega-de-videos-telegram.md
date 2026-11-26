---
title: Entrega de videos por Telegram (por qué a veces no llegan)
created: 2026-11-26
updated: 2026-11-26
type: runbook
tags: [runbook, telegram, entrega, videos, ttchop, gateway]
status: active
confidence: high
owners: [arturo, ttchop_robot]
related: [hooks-para-inicio-de-video, estandar-thumbnail-video, tareas-diarias-ttchop]
---

# Entrega de videos por Telegram (por qué a veces no llegan)

Runbook de la falla recurrente «**no me mandaste el video**»: el agente respondía con el tag
`MEDIA:<ruta>` y el video nunca aparecía en el chat.

## Síntoma

- El agente escribe `MEDIA:/root/.hermes/profiles/ttchop_robot/media/<archivo>.mp4` en la respuesta.
- El archivo **existe** en disco, es un MP4 válido y pesa pocos MB.
- En el chat **no llega nada** (ni el video ni un error).

## Cómo se diagnosticó (con evidencia)

Los logs del gateway **son por perfil**: `/root/.hermes/profiles/ttchop_robot/logs/gateway.log`
(el `/root/.hermes/logs/gateway.log` global no registra los turnos del perfil).

Ahí, una entrega normal se ve así:

```
INFO gateway.platforms.base: [Telegram] Delivering 1 non-image MEDIA attachment(s)
INFO gateway.platforms.base: [Telegram] Sending video attachment (.mp4) to 6407630145
```

Y cuando el tag se escribe pero el archivo no está, avisa:

```
WARNING gateway.platforms.base: Skipping MEDIA directive path (not found on this host): <ruta>
```

**El caso que falla no deja NINGUNA de las dos líneas**: el turno termina con
`Sending response (N chars)` y nada más — o sea, el tag `MEDIA:` **no llegó al texto final** que se
despacha, y el gateway no tiene nada que entregar. (El código sí tiene un respaldo —`_append_auto_media_tags`
en `gateway/run_turn_runner.py`— que añade tags `MEDIA:` que aparezcan en resultados de herramientas del
turno, pero no cubre un tag que sólo venía en el texto del modelo.)

## Solución adoptada (verificable)

Mandar el video **directo por la Bot API de Telegram** (`sendVideo`) con el token del perfil
(`TELEGRAM_BOT_TOKEN` en `/root/.hermes/profiles/ttchop_robot/.env`, **nunca** imprimirlo) y el chat
`6407630145`, y **verificar la respuesta**: `ok: true` + `message_id` es la única prueba real de entrega.

Script: `scripts/tg_send_video.py` (copia de trabajo en
`~/.hermes/profiles/ttchop_robot/cache/scratch/tg_send_video.py`).

```
python3 tg_send_video.py <ruta.mp4> "caption"
# -> ok: True | message_id: 5223 | size: 2007076
```

Con eso la entrega queda **comprobada**, no supuesta. El tag `MEDIA:` se puede seguir usando (cuando
funciona, evita duplicar), pero **no** es garantía: si el video importa, se manda por el script.

## Detalles que importan

- **Manda el máster (1080×1920) por defecto.** La Bot API acepta hasta 50 MB, así que no hace falta
  degradar: la versión ligera (720×1280) es **sólo un respaldo** si el máster falla o si se pidió algo
  muy liviano. Mandar la ligera sin avisar se percibe como «se ve más cuadrado / peor», aunque el
  aspecto (9:16) sea idéntico.
- **Verifica el aspecto antes de culpar al archivo:** `ffprobe -select_streams v:0 -show_entries
  stream=width,height,sample_aspect_ratio,display_aspect_ratio` → un vertical correcto da `9:16` con
  `SAR 1:1`. Un `N/A` en SAR/DAR es normal (se deduce del ancho/alto).
- **Formato del respaldo ligero:** `scale=720:1280`, `libx264 -profile:v baseline -level 3.1 -crf 30`,
  `-pix_fmt yuv420p`, `aac -b:a 96k -ac 1`, `-movflags +faststart` (≈2 MB para ~15 s).
- **Los archivos se crean antes de responder:** si el `ffmpeg` que produce el video todavía está
  corriendo en segundo plano cuando se escribe la respuesta, el archivo puede no existir aún.
- **Los logs son la fuente de verdad:** ante cualquier «no llegó», revisar
  `profiles/ttchop_robot/logs/gateway.log` buscando `Delivering` / `Skipping` / `Sending video`.

## Changelog

- **2026-11-26 — resolución.** Por defecto se manda el máster 1080×1920; la ligera 720×1280 es respaldo.
  Se documenta cómo verificar el aspecto (9:16, SAR 1:1) antes de atribuir un problema al archivo.
- **2026-11-26 — creación.** Diagnóstico con evidencia (logs por perfil) y solución: envío directo por
  `sendVideo` con verificación `ok`/`message_id`.
