---
title: Generación de videos en TTChop2
created: 2026-10-19
updated: 2026-10-20
type: runbook
tags: [sistema, runbook, pipeline]
status: active
confidence: high
related: [ttchop-webapps, ttchop-automatizaciones]
---

# Flujos de creación y render de video

Esta página separa dos procesos distintos: la creación iniciada desde la UI de
TTChop2 y la producción manual tipo Producer basada en un producto de catálogo y
clips grabados. Crear o renderizar un video **no lo publica en TikTok**. Ver
[[ttchop-webapps]] y [[ttchop-automatizaciones]]. Para generación manual de
canciones con ElevenLabs Music, sin integración de servidor, consulta
[[ttchop-music-generation]].

## A. Crear video desde la UI de TTChop2

Usa esta sección solo para lo que está confirmado de la UI: **Create Video** es
el flujo guion → voz → render. No mezcles aquí los prerrequisitos ni parámetros
del Producer/collage.

1. En TTChop2, abre **Create Video** y sigue el flujo de guion, voz y render que
   ofrece la interfaz. Revisa el resultado en la UI antes de darlo por terminado.
2. **Products → producto → Renders** permite consultar renders del producto,
   según la UI documentada en [[ttchop-webapps]].
3. No asumas una ubicación universal para los archivos renderizados desde la UI.
   La documentación confirma la colección `renders`, pero no una ruta universal
   para los archivos de la UI.

Esta sección no especifica defaults de Producer, almacenamiento de archivos ni
pasos de publicación.

## B. Video manual de producto con clips y trims guardados en TTChop2

Para un pedido manual de un solo producto, usa `POST /collage/create` en
`ttchop-server`. **No ejecutes `runProducer`**: Producer es un proceso por lotes
que puede generar tres slots y seleccionar productos o sesiones distintos de los
pedidos. El collage manual no ejecuta el scheduler ni aplica sus cooldowns. En
este flujo, resuelve producto, sesiones, plantilla y render en TTChop2; no
reutilices allí IDs ni datos del proyecto original `ttchop`.

### 1. Resolver producto, proyecto y clips

1. Confirma que el pedido corresponde a un único producto y determina el Firebase
   project correcto de TTChop2. Resuelve allí el producto completo, su `userId`,
   las sesiones asociadas y los clips. No reutilices IDs ni datos de otro proyecto.
2. Comprueba que cada sesión seleccionada incluye el ID del producto en
   `session.productIds`. Confirma las URLs de video HTTPS y la duración real de
   cada archivo.
3. Conserva los `trimStart` y `trimEnd` guardados por la app para cada video y
   envíalos en el payload; no los sustituyas por el rango completo. Valida
   `0 <= trimStart < trimEnd <= duración real`. Si la duración guardada en
   Firestore o la app falta o es 0, mide el archivo fuente con `ffprobe` para
   este trabajo. No alteres el registro fuente solo para corregir el dato de
   trabajo.
4. Los cooldowns pertenecen al Producer automatizado: bloquea un producto
   producido en los últimos 3 días; para sesiones prefiere las nunca usadas y,
   cuando todas ya se usaron, permite reutilizar las que no se produjeron en los
   últimos 20 días. `/collage/create` manual no ejecuta esos filtros ni escribe
   `bot_productions`; no consultes el proyecto original `ttchop` solo para
   simularlos durante un trabajo manual de TTChop2. Mantén los trims como
   instrucciones de este job; no alteres el registro fuente ni la plantilla
   guardada. Una solicitud explícita de un rerender tras cambiar trims se limita
   a ese único render y no borra ni crea registros de cooldown.

### 2. Defaults: distinguir proyectos

Los IDs de plantillas y proyectos son propios de cada Firebase project:

- `temp_y3w17i3` (plantilla llamada “25 sec”) y `projectId=ttchop` son del
  Producer/proyecto original. No asumas que aplican a TTChop2.
- En TTChop2, localiza de nuevo dentro del proyecto correcto la plantilla
  equivalente del usuario y revisa su contenido, no solo el título. En un render
  reciente se usó la plantilla local `temp_s6m3u02`; es solo una referencia de
  ese render, no un ID universal.
- Envía explícitamente `projectId=ttchop2` para este flujo TTChop2: si omites el
  campo, `ttchop-server` usa `ttchop` como proyecto predeterminado.
- Defaults orientativos del Producer: voz PumaVoice01, ID
  `ve7BOdejheJbgrBriBx4`; idioma `ja` para `region=jp` y `es` en otros casos;
  overlay apagado (`needsOverlay:false`) salvo pedido explícito.

“25 sec” es el nombre de una plantilla; **no fuerza** un video de 25 segundos.
El audio y el guion pueden producir un video más corto.

### 3. Preparar y aprobar el diálogo

Para diálogo nuevo, usa hechos respaldados del producto. No inventes testimonios,
efectos ni precios. Si solicitas un borrador con `POST /collage/dialogue`, envía
el producto completo, la plantilla del proyecto y el idioma; trátalo como
borrador, no como texto aprobado. Presenta el guion y espera aprobación antes de
TTS o render.
Si Arturo pide explícitamente repetir un render con un guion ya aprobado,
reutiliza literalmente ese mismo guion: no lo regeneres ni pidas otra aprobación
del texto.

### 4. Enviar y seguir el trabajo

Envía `POST /collage/create` con un `renderId` único y payload explícito que
incluya `projectId`, voz, diálogo aprobado, idioma, plantilla correcta del
proyecto, objeto completo del producto y clips con URL, duración, `trimStart` y
`trimEnd`. Establece `needsOverlay:false`, salvo que se haya pedido overlay
explícitamente. Añade `userId` solo si hace falta asociar el render a la
biblioteca del usuario.

El endpoint encola internamente el trabajo y devuelve estado pendiente y
`jobId`; la respuesta no significa que terminó. No hay callback separado de
collage: no esperes `/collage/callback` ni lo confundas con `/ai/callback`.
Consulta `renders/{renderId}` en el proyecto correcto hasta verificar
`status=done` y `videoUrl`.

### 5. QA y entrega

1. Compara en los logs los IDs de clips realmente usados y sus límites de trim
   contra la selección de la app. Si se omitió algún clip, identifica cuál. Si
   Arturo pidió usar todos, no declares éxito mientras falte alguno.
2. Descarga el MP4 y revisa audio, video, dimensiones y duración con `ffprobe`;
   inspecciona fotogramas representativos y reproduce el archivo.
3. Compara el empaque y la marca visibles con la ficha del catálogo; señala
   cualquier discrepancia en vez de darla por correcta.
4. Entrega el MP4 como adjunto e indica que no se publicó. Publicar en TikTok es
   una acción separada y requiere autorización explícita de Arturo.
