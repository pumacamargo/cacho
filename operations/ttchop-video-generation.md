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

# Generación de videos en TTChop2

Guía breve para preparar, generar y comprobar un render de video. Generar un
render **no lo publica en TikTok**; la publicación es un paso separado que
requiere autorización explícita. Ver también [[ttchop-webapps]] y
[[ttchop-automatizaciones]].

## Antes de generar

- Inicia sesión en TTChop2 y selecciona el contenedor/cuenta correcto.
- Elige un producto existente y clips/sesión utilizables asociados a ese
  producto. Para el flujo Producer, la sesión debe incluir el ID del producto
  y cada clip necesita `downloadUrl` HTTPS y duración positiva; no basta con
  tener IDs de clips.
- Revisa cooldowns del Producer: 3 días por producto y 20 días por clips/sesión.
  Si el único material útil sigue en cooldown, no lo reutilices sin autorización.
- Confirma guion/datos del producto, idioma y plantilla de collage. El Producer
  usa `temp_y3w17i3` (25 sec), PumaVoice (`ve7BOdejheJbgrBriBx4`), proyecto
  `ttchop`, japonés (`ja`) para región JP y español (`es`) en otro caso; overlay
  está desactivado por defecto. No sustituyas estos defaults por una plantilla
  de voz distinta.
- Para un video manual con diálogo específico del producto, genera el diálogo
  con el producto completo, la plantilla y el idioma; muestra el guion a Arturo
  y espera su aprobación antes de consumir recursos de TTS/render.

## Generar y comprobar

1. En TTChop2, abre **Create Video**, selecciona producto, material y plantilla,
   y revisa los datos/guion antes de iniciar la generación. No inventes datos de
   producto ni promociones desactualizadas.
2. Espera a que el trabajo asíncrono termine; enviar la solicitud no significa
   que el video esté listo.
3. En la app, abre **Products → producto → Renders** para comprobar el render.
   Verifica además en el mismo proyecto de Firebase que `renders/{renderId}`
   alcance `status: done` y tenga `videoUrl`. Descarga el MP4 y comprueba que
   abre/reproduce; si se hace una revisión técnica, valida streams, dimensiones
   y duración con `ffprobe` y mira fotogramas representativos.
4. El render persistido pertenece a la colección `renders` del proyecto
   seleccionado; el MP4 se conserva en el almacenamiento asociado y se enlaza
   mediante `videoUrl`. No lo confundas con una publicación: solo una acción
   posterior autorizada publica en TikTok.

La generación no concede permiso para publicar. No publiques ni programes el
video sin autorización explícita de Arturo.
