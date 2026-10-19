---
title: Generación de videos en TTChop2
created: 2026-10-19
updated: 2026-10-19
type: runbook
tags: [sistema, runbook, pipeline]
status: active
confidence: high
related: [ttchop-webapps, ttchop-automatizaciones]
---

# Flujos de creación y render de video

Esta página separa dos procesos distintos: la creación iniciada desde la UI de
TTChop2 y la producción automatizada/manual tipo Producer basada en catálogo y
clips grabados. Crear o renderizar un video **no lo publica en TikTok**. Ver
[[ttchop-webapps]] y [[ttchop-automatizaciones]].

## A. Crear video desde la UI de TTChop2

Usa esta sección solo para lo que está confirmado de la UI: **Create Video** es
el flujo guion → voz → render. No mezcles aquí los prerrequisitos, cooldowns ni
parámetros del Producer.

1. En TTChop2, abre **Create Video** y sigue el flujo de guion, voz y render que
   ofrece la interfaz. Revisa el resultado en la UI antes de darlo por terminado.
2. La sección **Products → producto → Renders** permite consultar renders del
   producto, según la UI documentada en [[ttchop-webapps]].
3. No asumas que todos los archivos renderizados desde la UI se guardan en una
   ruta de almacenamiento específica. La documentación confirma la colección
   `renders` como parte del modelo de datos, pero no establece una ubicación
   universal para los archivos de la UI.

Esta sección no especifica defaults de Producer, almacenamiento de archivos ni
pasos de publicación.

## B. Producer automatizado o collage manual

Este flujo requiere un producto de catálogo y material de sesiones/clips; no es
la secuencia de **Create Video** descrita arriba.

### Prerrequisitos y revisión

- Resuelve el producto, su `userId` y las sesiones correspondientes en el
  proyecto Firebase correcto. Confirma que `session.productIds` incluye el ID
  del producto y que cada clip seleccionado tiene `downloadUrl` HTTPS y
  duración positiva. No envíes solo IDs de clips.
- Comprueba los cooldowns del Producer: 3 días por producto y 20 días por
  clips/sesión. Si la única sesión utilizable sigue en cooldown, informa a
  Arturo antes de reutilizarla; un override manual requiere su aprobación
  explícita y no debe registrarse silenciosamente en `bot_productions`.
- Para mantener los valores del Producer en un collage manual, usa la plantilla
  `temp_y3w17i3` ("25 sec"), voz `ve7BOdejheJbgrBriBx4`, proyecto `ttchop`, y
  `ja` para región `jp` / `es` en otro caso. El Producer no solicita overlay;
  queda apagado por defecto. No sustituyas la voz por una plantilla distinta.
- Para diálogo específico del producto, solicita primero el texto con
  `POST /collage/dialogue`, enviando el objeto completo del producto, la
  plantilla de collage y el idioma. Usa solo datos de producto respaldados y
  evita precios/ofertas que puedan estar desactualizados. Presenta el diálogo a
  Arturo y espera su aprobación **antes de TTS o render**.

### Generar y verificar el collage

1. Solo después de aprobar el diálogo, inicia `POST /collage/create` con un
   `renderId` explícito, `projectId`, `voiceId`, diálogo aprobado, idioma,
   plantilla de collage, datos completos del producto y videos de sesión con
   `downloadUrl` y duración. Añade `userId` únicamente si hace falta asociar un
   render manual a la biblioteca del usuario. `needsOverlay` es false por
   defecto; encadena overlay solo si se solicita y los datos actuales de precio
   u oferta son fiables.
2. La solicitud inicia un trabajo asíncrono; no equivale a un render terminado.
   En el mismo proyecto, verifica `renders/{renderId}` hasta que tenga
   `status: done` y `videoUrl`.
3. Descarga el MP4 enlazado y valida streams, dimensiones y duración con
   `ffprobe`; inspecciona fotogramas representativos y confirma que el archivo
   reproduce correctamente.

La verificación del render cierra el paso de generación, no autoriza a publicar.
Publicar en TikTok es un paso separado y requiere aprobación explícita de Arturo;
no publiques ni programes el video sin ella.
