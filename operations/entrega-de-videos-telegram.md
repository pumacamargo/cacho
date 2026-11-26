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

- **Formato del archivo:** para que Telegram lo acepte sin problemas, el video va en
  `720×1280 · H.264 baseline/level 3.1 · AAC mono` (≈2 MB). Los másters de 1080×1920 se guardan igual,
  pero al chat se manda la versión ligera.
- **Los archivos se crean antes de responder:** si el `ffmpeg` que produce el video todavía está
  corriendo en segundo plano cuando se escribe la respuesta, el archivo puede no existir aún.
- **Los logs son la fuente de verdad:** ante cualquier «no llegó», revisar
  `profiles/ttchop_robot/logs/gateway.log` buscando `Delivering` / `Skipping` / `Sending video`.

## Changelog

- **2026-11-26 — creación.** Diagnóstico con evidencia (logs por perfil) y solución: envío directo por
  `sendVideo` con verificación `ok`/`message_id`.
