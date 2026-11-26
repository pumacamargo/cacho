---
title: Desmenuzar un carrusel de imágenes (método y casos)
created: 2026-11-26
updated: 2026-11-26
type: runbook
tags: [runbook, proceso, negocio]
status: active
confidence: high
related: [cuentas-tiktok-shop-affiliate, nicho-cabello-tiktok, ttchop-carousel-creation, dashboards-hosting]
---

# Desmenuzar un carrusel de imágenes

Runbook para **desmenuzar un carrusel** de otra cuenta y luego **recrearlo con una
variación** para hacer contenido único. Nace para la cuenta nueva
[[cuentas-tiktok-shop-affiliate]] (hamaca azul), que arranca con carruseles de
imágenes en vez de video.

> **Regla de Arturo (2026-11-26): el desmenuzado de un CARRUSEL NO se mezcla con el
> desmenuzado de un VIDEO.** Son procedimientos y artefactos distintos: el de video
> mide script + recordings + video editing con audio y tiempos (ver
> [[recrear-video-creadores-edits]] y [[estudio-creadores-fuentes-datos]]); el de
> carrusel es slide por slide, sin audio ni edición de video. Van en índices y
> carpetas separados para que no se revuelvan.

## Dónde se guarda (separado del video)

- **Artefacto local:** `/root/desmenuzados-carrusel/<caso>/` (hermana de
  `/root/desmenuzados`, **no** dentro). Cada caso: `desmenuzado.md` + `slides/`
  con los PNG/JPG en orden, renombrados `01.jpg`…`NN.jpg`.
- **Copia de los slides:** imprescindible, porque los adjuntos entrantes viven en la
  caché del gateway (se autolimpia). El nombre de carpeta que asigna el gateway es
  el **SHA-256 del archivo** (no sirve para ordenar: el orden lo da el carrusel).
- **Conocimiento:** esta página de Cacho.
- **Publicación (opcional, solo si Arturo lo pide):** en su propia carpeta/índice
  del hosting (p. ej. `uploads/vps2/carruseles/`), **nunca** dentro de
  `creators-research` (el índice de desmenuzados de video). Ver [[dashboards-hosting]].

## Método (Fase 1 — desmenuzar)

Slide por slide, y **nada** de script/recordings/video-editing (eso es del video):

1. **Inventario de entrada:** cuántos slides llegan y cuál(es) se ignoran (p. ej. el
   slide final de anuncio/CTA de la cuenta). Confirmarlo con Arturo.
2. **Ficha técnica del formato** (medida, no estimada):
   - nº de slides de contenido, aspecto (px reales), si el **fondo se repite** o
     cambia por slide (comparar regiones sin texto por diferencia de píxeles),
   - color/estilo del texto, presencia de caja o no, sombra, familia tipográfica,
   - **cuerpo e interlineado** por detección de bandas de texto (filas con píxeles
     claros), **centro vertical del bloque** (no siempre está anclado arriba),
   - extras: números, flechas, stickers, contador, atribución fija.
3. **Por cada slide:** nº, **rol narrativo** (hook / definición / mecanismo / tesis /
   juicio / consecuencia / consejo / mandato / reencuadre / cierre-CTA), descripción
   de la imagen, y el **texto original (JP) + traducción de revisión (ES)**.
4. **Arco narrativo:** cómo encadenan los slides (frases que continúan de uno al
   siguiente, gancho → cierre).

## Método (Fase 2 — recrear con variación)

- Misma **estructura y ritmo**; **contenido propio**: texto reescrito y composición
  propia (no reciclar el fondo ni el texto del original) para que sea único.
- Fijar antes de generar: **tema/temática** de las frases, **imagen de fondo**
  (propia vs. reutilizada) e **imágenes** (Kie.ai si son generadas → ver
  [[ttchop-carousel-creation]]: créditos y autorización de gasto aparte), y
  **título/hashtags**.
- **Publicación en TikTok:** ttchop_robot **nunca** publica; Arturo publica a mano.

## Caso 01 — Frases de psicología (Adler) · 2026-11-26

Primer caso. Cuenta japonesa de frases con retrato vintage en B/N.

- **Entrada:** 11 imágenes (960×1280, 3:4). **10 de contenido** + **1 final de
  anuncio de la app Motto**, que Arturo pidió **ignorar** (guardado solo como
  referencia).
- **Formato medido:** fondo **idéntico en los 10 slides** (retrato B/N con viñeta);
  texto blanco **#ffffff** centrado sin caja, con sombra; gothic/rounded sans;
  cuerpo ≈48 px de tinta e interlineado ≈83 px (a 960 de ancho); atribución fija
  「アドラー心理学」; bloque de texto **centrado verticalmente a ≈53 %** de la altura.
- **Arco:** hook («el mal humor es el mayor pecado») → definición (inmaduro) →
  mecanismo (buscan atención) → tesis (controlar al otro) → juicio (niño de 3 años)
  → consecuencia (tratarles en serio hace perder) → consejo (ignorar) → mandato (no
  gastar tu tiempo) → compasión (pobre persona) → cierre (concéntrate en lo tuyo).
- **Artefacto:** `/root/desmenuzados-carrusel/C01_adler-psicologia/` (`desmenuzado.md`
  + `slides/01..10.jpg` y `11_CTA_Motto_IGNORADO.jpg`), verificado por SHA-256.
- **Pendiente:** Fase 2 (tema, fondo propio, título/hashtags) — sin arrancar.

## Pitfalls

- **No mezclar** con el desmenuzado de video ni con su índice (`creators-research`).
- **Copiar los slides fuera de la caché** antes de 24 h: los adjuntos entrantes se
  autolimpian y con ellos se pierde la fuente.
- El nombre de carpeta que da el gateway a cada adjunto es su **SHA-256**: no
  contiene el orden ni el nombre original.
- El **fondo puede ser una sola imagen** repetida en todos los slides: comprobarlo
  por diferencia de píxeles, no a ojo (el zoom aparente engaña).
- La **traducción es de revisión**, no un hecho verificado: marcar los matices
  (p. ej. 不機嫌 = mal humor/estar de mal genio; 「幼稚」 = inmaduro/infantil).

## Relacionado

- [[cuentas-tiktok-shop-affiliate]] — las cuentas (hamaca shop / hamaca azul).
- [[nicho-cabello-tiktok]] — research de nicho para hamaca azul (carruseles).
- [[ttchop-carousel-creation]] — creación de carruseles (Kie.ai/local, QA).
- [[dashboards-hosting]] — dónde viven los dashboards publicados (video).
