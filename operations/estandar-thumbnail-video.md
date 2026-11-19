---
title: Estándar de portada/thumbnail de video
created: 2026-11-18
updated: 2026-11-18
type: runbook
tags: [runbook, decision, arte]
status: active
confidence: high
owners: [arturo, developer]
related: [ttchop-video-paths, recrear-video-creadores-edits, ttchop-carousel-creation]
---

# Estándar de portada/thumbnail de video

Regla fija para la **portada (thumbnail) de un video ttchop**. Existe porque los dos primeros videos
entregados salieron con portadas **distintas entre sí**: distinta **posición vertical** del texto,
distinto **centrado horizontal** y distinto **mecanismo** (una prop-driven, la otra un PNG horneado).
Arturo pidió definirlo, estandarizarlo y dejarlo guardado aquí.

Aplica a **todas las vías** de video (ver [[ttchop-video-paths]]) y al paso de captions/overlays de
[[recrear-video-creadores-edits]] §7.

## Regla

**Portada = 1 solo fotograma, el ÚLTIMO del video; imagen real del propio material con el producto
protagonista; texto japonés corto (≤2 líneas) SIEMPRE en la misma posición: bloque centrado
horizontalmente con su centro vertical en `y = 378 px` (19.7 % del alto).**

La posición del texto **nunca se mueve** entre videos: es lo que hace que todas las portadas
coincidan. Si el texto choca con el producto o la cara, se ajusta el **encuadre/imagen** o el
**scrim**, jamás la posición del texto.

Se probaron las dos posiciones reales sobre los dos materiales: la de `y ≈ 378` (arriba) **funciona
en los dos**; la de `y = 650` **tapa el producto del shaver**. Por eso la posición válida es
**FIJA ARRIBA (`y = 378`)**.

**Regla del fondo:** la **imagen de fondo de la portada SIEMPRE debe incluir el producto**. El
fotograma elegido tiene que mostrar el **producto protagonista visible y reconocible** — no una
escena sin producto, ni solo habitación/textura/persona. Si el último fotograma del video no lo
muestra bien, se elige el fotograma final que **sí** lo muestre o se recompone la portada con el
producto visible, **manteniendo intacta la posición del texto** (`y = 378`, `x = 540`). Esto
complementa la regla existente de «producto protagonista»: ahora es explícito que aplica al **fondo
de la portada** y no solo al encuadre.

## Valores exactos

| # | Campo | Valor | Notas |
|---|---|---|---|
| 1 | Composición | **1080×1920**, un solo fotograma (el **último** del video) | imagen real del propio material, producto protagonista; oscurecido **opcional** negro `0.22`–`0.35` solo para contraste |
| 2 | Texto | **máximo 2 líneas** japonesas cortas | |
| 3 | Tipografía | familia **`KeinannMaruPOPjp`** (fallback `Noto Sans CJK JP`) | peso **Regular 400 real**; **nunca** negrita sintética / faux bold (Keinann solo tiene Regular) |
| 4 | `fontSize` | **80 px** | |
| 4 | `lineHeight` | **1.15** | |
| 4 | `color` | **`#ffffff`** | relleno del texto |
| 4 | `outlineColor` | **`#101010`** | contorno oscuro |
| 4 | `outlineWidth` | **6** | |
| 5 | Posición | centro horizontal del bloque **x = 540 px (50 % del ancho)**; centro vertical del bloque **y = 378 px (19.7 % del alto)** | equivale al bbox medido `y 262–494` |
| 6 | `scrim` (si se usa) | `color #000000`, `opacity` **0.22–0.35** | solo para contraste |
| 7 | `frames` del `endCard` | **1** (solo el último fotograma) | |
| 8 | Fondo | **el fotograma de fondo SIEMPRE incluye el producto** visible y reconocible | no escena sin producto (ni solo habitación/textura/persona); si el último frame no lo muestra, usar otro fotograma final que sí o recomponer, **sin mover el texto** |

**Prohibido en la portada (punto 6 del estándar):** flecha, botón/etiqueta CTA, precio,
%/descuento numérico, escasez/inventario, claims no verificados, marca redundante si el frame ya la
muestra.

## Mecanismo

- **Preferido (prop-driven):** el prop `endCard` de la composición Remotion **`caption-overlay`**
  en `ttchop-post_templates` (repo `ttchop-post`), con `frames: 1` (último fotograma), y exportar el
  PNG del **frame final exacto** como `cover.png`.
  ```json
  "endCard": { "frames": 1, "image": "<frame>.jpg",
               "scrim": { "color": "#000000", "opacity": 0.22 },
               "text": { "lines": ["…","…"], "fontSize": 80, "fontWeight": 400,
                         "centerY": 378, "lineHeight": 1.15, "outlineWidth": 6,
                         "color": "#ffffff", "outlineColor": "#101010" } }
  ```
- **Evitar el PNG horneado ad-hoc** salvo caso justificado; si se usa, **debe respetar los puntos
  1–8** (misma posición, tipografía, tamaño y colores).
- Extracción de la portada suelta del render (último fotograma):
  `ffmpeg -sseof -1 -i final.mp4 -update 1 -frames:v 1 cover.png`
  (o por número de cuadro: `ffmpeg -i final.mp4 -vf "select='eq(n,1832)'" -frames:v 1 cover.png`).
- Detalle del prop, fuentes y pitfalls: [[recrear-video-creadores-edits]] §7.

## Tabla de comprobación (antes de entregar)

| Comprobación | Requerido | Cómo se verifica |
|---|---|---|
| Dimensiones | 1080×1920 | `PIL` / `ffprobe` del PNG |
| Fotograma | es el **último** del video | comparar con `-frames:v 1` del final del MP4 |
| Fondo con producto visible | el producto protagonista se ve claro y reconocible en el fondo | revisión visual del PNG de portada |
| Nº de líneas | ≤ 2 | inspección / props |
| Familia y peso | `KeinannMaruPOPjp`, `fontWeight 400` | props; **sin faux bold** |
| `fontSize` / `lineHeight` | 80 / 1.15 | props |
| Colores | `#ffffff` + `#101010`, `outlineWidth 6` | props |
| Centro horizontal del bloque | **x = 540 px (50 %)** | bbox de texto medida en píxeles |
| Centro vertical del bloque | **y = 378 px (19.7 %)** | bbox de texto medida en píxeles |
| Mecanismo | `endCard` prop-driven `frames:1` | props.json del caso; PNG horneado solo si está justificado |
| Prohibidos | ninguno presente | revisión visual |

Medición del bbox del texto (re-verificable, sobre el PNG real 1080×1920): contar los píxeles
**casi blancos** (`R,G,B > 230`) y tomar su `min/max` de `x` e `y`; el centro del bloque es el punto
medio del bbox. En la portada del shaver hay que **restringir la zona del texto** (`y < 600`), porque
el material tiene otros blancos (producto/flecha) que contaminan la cuenta.

## Desviaciones reales de los dos casos entregados (números medidos)

Medición hecha sobre las **portadas reales** a 1080×1920 (PIL, píxeles) y re-verificada el
2026-11-18. Ninguno de los dos cumple todavía el estándar completo.

| Dimensión | **17_carpet** (final v1) | **18_shaver** (v7) | Estándar |
|---|---|---|---|
| Archivo | `carpet17-final-v1/cover.png` | `shaver18-overlays-v7/assets/cover_design.png` | PNG del último frame → `cover.png` |
| Composición | 1080×1920 | 1080×1920 | 1080×1920 |
| bbox texto (medido) | **x 250–833, y 574–729** | **x 133–843, y 262–494** | — |
| Centro horizontal | **50.1 %** ✅ | **45.2 %** ❌ (no centrado) | **50 %** (x = 540) |
| Centro vertical del bloque | **≈651 px = 33.9 %** ❌ (abajo) | **≈378 px = 19.7 %** ✅ | **378 px (19.7 %)** |
| Líneas | 2 | 2 | ≤ 2 |
| Fondo con producto | **✅** muestra la alfombra (producto) en el suelo de la habitación | **✅** muestra la afeitadora (producto) en estudio | fondo siempre con el producto visible |
| Tipografía / peso | `fontSize 80`, `fontWeight 400` ✅ | horneada en el PNG | 80 px / Regular 400 |
| `lineHeight` / contorno | 1.15 / `#101010`, ancho 6 ✅ | horneada | 1.15 / `#101010`, 6 |
| Color de texto | `#ffffff` ✅ | horneada | `#ffffff` |
| Scrim | `#000000`, opacity **0.22** ✅ (dentro de 0.22–0.35) | horneada | 0.22–0.35 |
| Mecanismo | **`endCard` prop-driven** (`props.json`, `frames:1`, `image hero.jpg`) ✅ | **PNG horneado ad-hoc** ❌ | prop-driven `frames:1` |
| Cumple el estándar | **No** — solo falla la posición vertical (`y=650` → 33.9 %; el estándar es `y=378`) | **No** — la posición vertical ya es la correcta, pero falta el centrado horizontal (45.2 %) y el mecanismo prop-driven | — |

Diferencia real de origen, en una frase: **`18_shaver` tenía el texto arriba y centrado a ojo
(45.2 %), `17_carpet` lo tenía más abajo (33.9 %) y prop-driven a 50 %**; el estándar se queda con
**la posición de arriba del shaver, pero centrada al 50 % del carpet y con el mecanismo prop-driven
del carpet**.

## Trampa al extraer el último fotograma (verificada 2026-11-19)

Con `endCard` de **un solo cuadro**, el comando `ffmpeg -sseof -1 … -frames:v 1` que se usaba como
atajo devuelve un fotograma **~0.5 s antes del final** y **pierde la portada** (sale el video sin el
texto). En `20_dualshaver` la portada se extrajo por **número de cuadro**
(`-vf "select=eq(n,1066)"`, último cuadro real del render) y se verificó con PIL que el bloque de
texto queda centrado en `x=540` / `y=380`.

## Registro por caso

Anotar en el **manifiesto del caso** en el NAS (`<caso>_MANIFEST.md`, ver
[[recrear-video-creadores-edits]] §8) los valores de `centerY` / `centerX` usados en el `endCard` y
que cumplen este estándar, para que la próxima reconstrucción salga idéntica.

## Estado

**PENDIENTE de OK de Arturo:** aplicar el estándar a los dos videos ya entregados (`18_shaver` v7 y
`17_carpet` final v1) **no está hecho**. Este documento solo fija y guarda la especificación; no se
regeneraron portadas, no se tocó código de la app/Remotion, colas, medios ni el NAS. La decisión de
rehacer/mantener las portadas entregadas la toma Arturo después.

## Ver también

- [[ttchop-video-paths]] — punto de entrada de las vías de video y sus piezas compartidas.
- [[recrear-video-creadores-edits]] — §7 subtítulos/overlays y el prop `endCard`; §8 variaciones.
- [[ttchop-carousel-creation]] — portadas de carrusel (misma familia tipográfica, otro formato).
