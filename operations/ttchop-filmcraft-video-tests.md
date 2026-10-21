---
title: Pruebas de edición de video con FilmCraft para TTChop2
created: 2026-10-21
updated: 2026-10-21
type: runbook
tags: [runbook, pipeline, cli]
status: draft
confidence: high
related: [ttchop-video-generation, ttchop-automatizaciones, ttchop-webapps]
---

# FilmCraft: muestras locales, no pipeline integrado

Esta página distingue la implementación vigente del Producer, las pruebas locales de FilmCraft del 2026-10-21 y una posible integración futura. Para el flujo manual de collage/UI, consulta [[ttchop-video-generation]]; para scheduler y cooldowns, [[ttchop-automatizaciones]]. TTChop2 y `ttchop` son proyectos Firebase distintos: [[ttchop-webapps]]. Las muestras aquí descritas no se publicaron, no se guardaron como renders en Firebase ni se enviaron por Telegram.

## 1. Producer vigente (referencia; no ejecutar para un pedido manual)

Código inspeccionado en `vps-projects:/root/projects/ttchop`: `ttchop-bot` commit `706529b` (`modules/producer/index.js`, `modules/delivery/index.js`) y `ttchop-server` commit `d45332a` (`routes/collage.js`, `scripts/collage_builder.py`). Confirma los commits antes de reutilizar estos detalles. Esta ruta no llama a FilmCraft: usa generación de receta y FFmpeg/Python.

1. `runProducer()` prepara hasta tres slots. Lee `ttchop2/recording_plans/{fecha JST}`, busca productos en `ttchop2/products` primero por `sourceId` y luego por coincidencia de palabras, y busca `ttchop2/sessions` que incluyan el producto y clips con `videos[].downloadUrl`.
2. El bot consulta `ttchop/bot_productions` para los cooldowns de producto (3 días) y sesión (20 días). Completa slots con productos JP aleatorios de `ttchop` cuando el plan no alcanza; el fallback de emergencia puede ignorar cooldowns si el fallback normal no encuentra candidatos. El proyecto `ttchop` y `ttchop2` no deben confundirse.
3. Por slot, pide diálogo a `POST /collage/dialogue` y envía `POST /collage/create` con el producto, plantilla, voz y sesiones completas. El Producer no selecciona cortes individuales ni trims. El servidor pide al LLM una receta de montaje (hook de 3–5 cortes breves, cuerpo acelerado típicamente 1.5–4×), corrige algunos límites y huecos, y entrega la receta al builder.
4. `scripts/collage_builder.py` descarga los clips seleccionados, aplica trims y velocidad con FFmpeg, escala/recorta a 1080×1920, concatena y agrega audio; el servidor sube el MP4 a Storage y actualiza `renders`.
5. El Producer consulta el estado del render cada 8 s, hasta 5 min. Cuando está listo, descarga el MP4, lo manda con `sendVideo` del bot de Telegram y registra `bot_productions`. Esto no es la publicación en TikTok ni prueba la entrega del perfil Hermes `ttchop_robot`.

Para pedidos manuales no ejecutes `runProducer()`: puede escoger hasta tres productos/slots distintos. El procedimiento manual de `/collage/create` está en [[ttchop-video-generation]].

## 2. Prueba local con FilmCraft 0.9.0

FilmCraft está instalado en PumaDeskAsus. Por SSH documentado en [[acceso-remoto-pumadeskasus]], `C:\Program Files\FilmCraft\filmcraft-cli.exe --version` devolvió `filmcraft-cli 0.9.0`. El MCP local por stdio respondió a `initialize`, `notifications/initialized` y `tools/list`; se observaron herramientas como `command_run`, `command_batch`, `project_inspect`, `sequence_inspect` y `media_import`. Esto prueba el servidor MCP de la aplicación, no que Hermes en el VPS ya lo pueda controlar de forma remota.

La viabilidad de edición se probó con clips reales existentes en Firestore/Storage de `ttchop2` (`ttchop2.firebasestorage.app`), en modo lectura. Se usaron planes históricos; `recording_plans/2026-10-21` no existía al momento de la consulta. No se comprobó cooldown ni selección efectiva del Producer porque estos datos viven en el proyecto `ttchop`.

| Muestra | Plan → producto → sesión | Clips | Edición local | Exportación verificada |
| --- | --- | --- | --- | --- |
| ELLISS | `recording_plans/2026-10-09` → `products/prod_dvjf4oy` → `sessions/sess_oaslrwm` | `vid_l216dsr`, `vid_i63nf5r`, `vid_rr0ryje`, `vid_rufls9o` | Cuatro cortes de hook de 0.75 s a 1×; cuatro de cuerpo de 2 s a 2×; `clip.fillFrame` en ocho clips para llenar el encuadre. | `elliss-final.mp4`: H.264, 1080×1920, 24 fps, 11.0 s, sin audio. Proyecto: `elliss-fill.fcproj`. |
| MAGINA | `recording_plans/2026-10-15` → `products/prod_9q8wzve` → `sessions/sess_awpv63q` | `vid_a8r3vu1`, `vid_3uy8jvn`, `vid_qcn1zf9`, `vid_odz256y` | Cuatro cortes de hook de 0.75 s a 1×; cuerpo de 2, 2, 2 y 1.5 s a 2×; encuadre por defecto. | `magina-final.mp4`: H.264, 1080×1920, 24 fps, 10.5 s, sin audio. Proyecto: `magina.fcproj`. |

Los artefactos de prueba están en `/root/.hermes/cache/scratch/filmcraft-demo-ttchop2-20261021/`: `manifest.json` (parámetros, probe y hashes), `sources.json` (documentos, rutas de Storage sin tokens, nombres, tamaños y hashes), `assets/`, recetas JSONL, proyectos y exportaciones. Los proyectos referencian clips en `C:\Users\puma_\AppData\Local\Temp\FilmCraftTTChop2Demo_20261021\assets`; si se mueven, hay que reubicar/reimportar los medios. Son copias temporales, no almacenamiento permanente.

## 3. Repetir la prueba local de forma controlada

1. Confirma autorización para usar los clips y consulta solo datos de `ttchop2`. Trabaja en un directorio temporal nuevo y aislado. No registres URLs con tokens ni credenciales. Para reproducir exactamente las muestras, usa las copias `assets/` y verifica sus SHA-256 contra `sources.json`; no es necesario volver a descargar desde Firebase.
2. En PumaDeskAsus, verifica la versión con `"C:\Program Files\FilmCraft\filmcraft-cli.exe" --version`. Crea un proyecto/secuencia con `file.newProject` y `file.newSequence` en JSONL, con `width:1080`, `height:1920`, `fps:24`, pistas de video/audio y `--data-dir` aislado. Guarda una copia `.fcproj` en la misma carpeta de prueba.
3. Importa los clips y consulta `inspect project` para conocer los IDs de media de ese proyecto: los IDs cambian entre proyectos. Coloca cortes en `V1` con `timeline.place`, especificando `sourceIn` y `duration` en ticks (en estas pruebas: 254016000000 ticks/s). Aplica `clip.speedDuration` a segmentos de cuerpo con `speed:200`, `ripple:true`, `interpolation:"frameSampling"`. En ELLISS se usó `exec clip.fillFrame clips=[...]` para llenar el encuadre; inspecciona visualmente el crop, ya que puede quitar contenido relevante.
4. Reabre el proyecto, exporta con `export <archivo.mp4> --format h264 --gpu-rendering off --no-audio`, comprueba que no haya media offline y valida el resultado con `ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,avg_frame_rate,nb_frames:format=duration -of json <archivo.mp4>`. Revisa también la reproducción y el encuadre. Las recetas `elliss-edit.jsonl` y `magina-edit.jsonl` son evidencia de esta prueba, no plantillas universales ni la receta del Producer.

## 4. Límites y posible integración futura

No se ha integrado Producer→FilmCraft. Siguen sin probarse con FilmCraft: receta LLM, TTS/voz sincronizada, música, duración de ~25 s, overlays/personajes, polling, escritura a Storage/Firestore, cooldowns, reintentos/idempotencia y entrega por `ttchop_robot`. Tampoco se demostró un cliente Hermes remoto que invoque el MCP de Windows. Las muestras reales son video-only; no reutilizaron audio ni generaron voz.

Si Arturo autoriza desarrollo posterior, separar el pedido manual del Producer diario: resolver assets autorizados, transportar clips a un worker temporal de PumaDeskAsus, traducir una receta aprobada a una secuencia FilmCraft, crear el `.fcproj`, exportar y validar MP4/proyecto, devolver archivos y enviarlos al chat de origen. Diseñar estado durable, reintentos e idempotencia antes de conectar producción. Probar en sandbox y obtener aprobación antes de tocar el Producer, desplegar, reiniciar servicios o gastar créditos. La cola en memoria de `ttchop-server` y el `sendVideo` del bot no prueban por sí solos una entrega confiable de Hermes.

No ejecutes `runProducer()` para una petición manual. No publiques en TikTok ni escribas a Firebase/Storage sin autorización específica. Nunca copies al wiki URLs de Storage que incluyan tokens.

## Procedencia

- Código leído en `vps-projects:/root/projects/ttchop/ttchop-bot` (`706529b`) y `ttchop-server` (`d45332a`); los repos no se modificaron.
- Evidencias FilmCraft y artefactos locales del 2026-10-21: `/root/.hermes/cache/scratch/filmcraft-demo-ttchop2-20261021/{manifest.json,sources.json,elliss-edit.jsonl,magina-edit.jsonl}`.
- Pruebas CLI/MCP previas: sesiones Hermes Developer `20261021_030813_be6d71` y `20261021_032003_e55bd2`.
