---
title: Vías para hacer un video (punto de entrada)
created: 2026-11-05
updated: 2026-11-06
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

## Las 3 herramientas (y cómo se combinan)

Lo que cambia entre vías es de dónde vienes y cuántos pasos previos haces; las **herramientas** que
hacen el video son tres (más una de efectos):

| Herramienta | Qué aporta | Dónde vive |
|---|---|---|
| **`ttchop-server` (FFmpeg)** | el **montaje**: une los clips según la receta (`scripts/collage_builder.py`); además orquesta el Producer | repo `ttchop-server` (vps-projects) |
| **Remotion** | los **captions/overlays, carruseles y clips de personaje**: composiciones React (`caption-overlay`, `CarouselSlide`, `CharacterClip`, `AutoOverlay`…) que se renderizan con `npx remotion` o a través del overlay-server | repo **`ttchop-post_templates`** (composiciones) + repo **`ttchop-post`** (`overlay-server`, :3001 — expone `/render`, `/character/render`, carruseles) |
| **FilmCraft** | **editar a mano** en la PC: timeline, overlays nativos, paquete portable (hace de los dos anteriores) | app local en PumaDeskAsus (no es repo) |
| *(`ttchop-effects`)* | *efectos*: blur de rostros/ojos, disclaimer (*Python, repo `ttchop-effects`*) | repo `ttchop-effects` |

**El camino por defecto usa dos de ellas en secuencia:** montaje con **ttchop-server/FFmpeg** →
captions/overlays con **Remotion**. **FilmCraft** reemplaza a las dos cuando la edición se hace a mano
(casos MAGINA Tagiras, Ellis if01, 02_blanket) — está documentado que *«el Producer actual sigue usando
`ttchop-server`/FFmpeg; no usa FilmCraft»*.

Y la diferencia entre vías son los **pasos previos al montaje**:

| Vía | Pasos previos | Automatización |
|---|---|---|
| 1 · Automática | ninguno: los crons recorren scout→producer y renderizan | total |
| 2 / 3b · Manuales | resolver producto y clips → diálogo/canción o voz → receta | media |
| 3 · Recrear un creador | transcripción → **lista de shots** → **grabar** → plan → receta → tiempos de captions | la cadena más larga |
| 4 · FilmCraft | lo mismo que 2/3, pero la edición final se hace en la PC a mano | manual |

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

## Clips generados con IA (opcional, para planos sin producto)

Existe una vía de **generación con IA** (kie.ai) ya integrada en `ttchop-server`, útil para los planos
**sin producto ni manos** (agua, espuma, vapor, texturas, ambientes). Dos reglas fijas: el clip debe
**coincidir con el encuadre del shot** (se logra dando el **fotograma de la referencia como primer cuadro**)
y la persona debe ir **siempre con ropa**. Detalle, precios y trampas en el skill `ttchop-content-ops`
(`references/ai-video-generation-kie.md`) y en la bitácora del 2026-11-05.

**Flujo verificado de punta a punta (caso 13, `13_NachoShampoo01`):** los planos de persona se generan
**primero como imagen** (`google/nano-banana-edit`, cada una recreando **fielmente** el fotograma de su
propio plano — ver los pitfalls del runbook) → Arturo las aprueba → **solo entonces** se animan
(`wan/2-6-flash-image-to-video`, 720p o 1080p, 5 s, usando la imagen aprobada como primer cuadro) → montaje
normal. Documentado paso a paso en [[recrear-video-creadores-edits]] → «Caso verificado —
13_NachoShampoo01».

## Animación programada con libro pop-up (flujo manual adicional)

Para un comercial ilustrado, en lugar de montar clips: **[[ttchop-popup-book-commercial]]** documenta el caso Enchenal `14_shaverAfter`, con Lemo-Opuscar / Paper Pop-up Book, Three.js + Canvas2D, poses aprobadas, voz japonesa, storyboard, cámara y entrega reproducible. Es un flujo manual adicional, **fuera de EffectCraft/FilmCraft y no integrado al Producer**; no cambia las herramientas ni el camino por defecto descritos arriba. El runbook identifica el MP4 final `enchenal_book_camera_v3_fixed.mp4` y su paquete fuente en el NAS.

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
