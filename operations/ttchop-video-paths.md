---
title: Vías para hacer un video (punto de entrada)
created: 2026-11-05
updated: 2026-11-05
type: runbook
tags: [sistema, runbook, video, indice]
status: active
confidence: high
related: [ttchop-video-generation, recrear-video-creadores-edits, ttchop-raw-asset-manual-edit, ttchop-filmcraft-video-tests, traduccion-video-pumasvoice-sincronizada, ttchop-music-generation, ttchop-carousel-creation]
---

# Vías para hacer un video (punto de entrada)

**Empezar por aquí.** Hay **3 vías distintas** para producir un video (más 1 sub-caso y 1 entorno
alternativo), y todas comparten piezas. Esta página dice **cuál usar, qué necesitas y dónde está el
paso a paso**; cada vía sigue teniendo su runbook propio.

## Las vías

| # | Vía | Para qué | Qué necesitas | Paso a paso |
|---|---|---|---|---|
| **1** | **Automática (Producer / pipeline + UI)** | producción diaria de catálogo: scout→producer, o crear un video desde la UI de TTChop2 | producto con ficha, sesión de clips, plantilla y diálogo aprobado | [[ttchop-video-generation]] §A · skills `ttchop-producer-ops`, `ttchop-pipeline-status` |
| **2** | **Manual con clips y trims de TTChop2** | cuando ya tienes los clips en el sistema y quieres montar collage + canción sin pasar por el Producer | producto, proyecto, clips resueltos y una canción ya generada | [[ttchop-video-generation]] §B |
| **3** | **Recrear el video de un creador** | partir del video de un creador (ASU/Sora) y hacer tu propia versión: transcripción → **lista de shots** → tus grabaciones → montaje → captions | el video de referencia + tus grabaciones (y la lista de shots para grabar) | [[recrear-video-creadores-edits]] (incluye **§8 variaciones** de un video ya entregado) |
| **3b** | *(sub-caso de 2)* **Manual Producer-style sin catálogo** | cuando **no hay catálogo/ficha**, solo audio y videos (casos Juice Discount, ELLISS, Ellis if01) | audio aprobado + clips, sin producto en sistema | [[ttchop-raw-asset-manual-edit]] |
| **4** | *(entorno alternativo)* **FilmCraft en la PC** | editar el timeline/overlays **a mano** en FilmCraft en vez del CLI (layout de pistas, texto nativo, paquete portable) | el material y el montaje de la vía 2 o 3 | [[ttchop-filmcraft-video-tests]] |

## Cómo elegir

- ¿Es la **producción de siempre** del pipeline (catálogo, crons, renders)? → **1**
- ¿Tienes ya los clips y una canción, y quieres el montaje tú? → **2**
- ¿**No hay catálogo**, solo el audio y los videos? → **3b** (sub-caso de 2)
- ¿Partes del **video de un creador** que quieres recrear? → **3**; si ya existe y quieres **cambiarle guion/voz/edición**, su **§8** (y su manifiesto en el NAS)
- ¿Quieres **tocar el timeline o los overlays a mano** (o el paquete portable)? → **4**, sobre el material de la 2 o la 3

## Piezas compartidas (no reinventarlas)

- **El montaje:** `ttchop-server/scripts/collage_builder.py` — recibe una **receta** (`ffmpegRecipe`) con los clips y sus recortes. Para armarla desde un plan de duraciones: `scripts/creators/build_recipe_from_plan.py`.
- **Subtítulos/overlays:** la composición Remotion **`caption-overlay`** en `ttchop-post_templates` (prop-driven: captions, tag, flecha, disclaimer, endCard). Detalle en [[recrear-video-creadores-edits]] §7.
- **La voz:** **PumaVoice01** (`ve7BOdejheJbgrBriBx4`) con el helper ya versionado `ttchop-server/scripts/creators/tts/tts_lines.mjs`; se ajusta el ritmo con `atempo` + pausas ([[recrear-video-creadores-edits]] §4).
- **Para variar un video ya entregado:** el **manifiesto** de su carpeta en el NAS (`<caso>_MANIFEST.md`) tiene el mapeo plano→clip, la voz, los captions y los comandos ([[recrear-video-creadores-edits]] §8).

## Pasos de apoyo (se usan dentro de las vías)

- **Voz / traducción de un video ya hecho** (ES→JA, alinear inicio/fin): [[traduccion-video-pumasvoice-sincronizada]]
- **Música** (canto con ElevenLabs Music): [[ttchop-music-generation]]
- **Carruseles** (imágenes, no video): [[ttchop-carousel-creation]]
- **Segmentar** un video del NAS por cortes: [[separar-videos-nas-por-cortes]]

## Reglas que aplican a todas las vías

- **No se publica nada en TikTok sin el OK de Arturo.** Los videos de creadores no se modifican ni se publican.
- **Sin precio, sin % inventado** y sin afirmaciones que la ficha del producto no respalde (los claims del habla del creador no están verificados).
- **Verificar en vivo** lo entregado (`ffprobe`/`volumedetect`/decode + hoja de contacto + el último frame) y reportar lo que falte.
- Los cambios de código en repos van **committeados y pusheados** (regla TTC-41) y verificados por cuenta propia.
