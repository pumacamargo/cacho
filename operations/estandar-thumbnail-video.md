---
title: Estándar de portada/thumbnail de video
created: 2026-11-18
updated: 2026-11-24
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

## Recomponer la portada a mano (cuando el último cuadro no sirve)

Si el último cuadro sale **negro** o no muestra el producto, el estándar manda tomar **otro fotograma
final que sí lo muestre** —un tramo con el producto en primer plano y **sin flecha ni etiqueta CTA**— y
mantener **intacta** la posición del texto.

- **Fuente: `KeinannMaruPOPjp`, NO el *fallback*.** El `Noto Sans CJK JP` del punto 3 vale como reserva
  si la familia no está instalada, pero **no para recomponer una portada que tiene que convivir con las
  horneadas por FilmCraft**: sale recto y delgado y el formato deja de coincidir — Arturo lo rechazó el
  2026-11-23 con «no siguen el mismo formato». El `.ttf` está en
  `vps-projects:/root/blanket-announcer-variation-v1/filmcraft/KeinannMaruPOPjp.ttf` (copia también en
  `blanket-announcer-15/assets/` y en `blanket-announcer-variation-v1/filmcraft/assets/`); `fc-query` lo
  reporta como familia `KeinannMaruPOPjp, けいなん丸ポップ体JP`, estilo **Regular**. Peso Regular real,
  **sin negrita sintética**, igual que la horneada.
- **Receta de 2 líneas (ffmpeg):**
  ```
  -vf "drawbox=x=0:y=0:w=iw:h=ih:color=black@0.22:t=fill,
       drawtext=fontfile=<KeinannMaruPOPjp.ttf>:text='<línea1>':fontsize=80:fontcolor=white:
         borderw=6:bordercolor=0x101010:x=(w-text_w)/2+5:y=<Y1>,
       drawtext=…:text='<línea2>':…:y=<Y2>"
  ```
  Arranca en `Y1=286`, `Y2=378` (interlineado 92 = 80×1.15); el `y` de `drawtext` es el **borde
  superior** de la línea y el `+5` en `x` compensa el centrado asimétrico de los glifos japoneses.
- **Medir y corregir, no entregar «a ojo»:** cuenta los píxeles casi blancos (`R,G,B>230`) con **PIL**
  restringidos a `y<600` (así el producto, la flecha y el rótulo quemado no contaminan la cuenta) y
  **desplaza las dos líneas** por la diferencia hasta que el centro del bloque dé `(540, 378)` ±4 px.
  Es una iteración, no un cálculo único. Con Keinann a 80 px el alto del bloque queda en **≈158–160 px**,
  igual que el horneado de referencia.
- Entrega las portadas como **PNG individuales** en el chat (no solo un ZIP) y en el NAS junto al video,
  con un `*_cover.json` que registre mecanismo, fotograma usado, texto, posición y la medición del bbox.

Verificado el 2026-11-23: `19_dualshaver` (fotograma t=35,5 s; bloque en x=540,0 · y=377,5) y
`20_dualshaver` (fotograma t=11,0 s; x=540,0 · y=378,0).

## Portada de una VARIACIÓN

**Regla general (Arturo, 2026-11-24): TODO video y TODA variación llevan una portada NUEVA — nunca se
reutiliza la de otro video ni la de la versión anterior.** Aunque el resto del material se derive del
mismo caso, la portada se rehace (otro cuadro y otro texto).

**La portada de una variación tiene que ser una variación: otro cuadro y otro texto.** Repetir el
fotograma que ya trae la portada horneada —o su mismo texto— **repite la original**; Arturo lo rechazó el
2026-11-23: «debería ser una variación, no el mismo, diferente imagen diferente texto».

- Elige **otro** fotograma final con el producto visible y sin flecha ni CTA, y **otro** texto de ≤2
  líneas que no repita el de la original. El formato y la posición **no cambian** (eso es lo que las hace
  coherentes entre sí).
- Referencia: las portadas originales del 19 y del 20 llevaban las dos `1台2役で全身ケア / 顔・ワキ・腕・脚・VIO`;
  las variaciones llevan `本物はどれ？ / 3つのポイントで見分ける` (19) y `剃るたび肌が荒れる人へ / 電動1台で全身お手入れ` (20).
- El **video** de la variación puede seguir terminando en el cuadro horneado original (eso viene del
  render de Arturo y no se toca): la portada de publicación es un **PNG aparte**.

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

**El último cuadro puede venir EN NEGRO** (verificado 2026-11-23 en `19_dualshaver`): si el `endCard`
del proyecto quedó vacío, ese fotograma sale negro **también en el render original de Arturo** — no es
un fallo de tu derivada. Pista barata: extrae el último cuadro de cada versión y **compara tamaños**;
un cuadro uniforme pesa unos **cientos de bytes** frente a **~10 KB** de uno con contenido. Cuando
pasa, la portada se **recompone** con otro fotograma (siguiente sección) — nunca moviendo el texto.

## Registro por caso

Anotar en el **manifiesto del caso** en el NAS (`<caso>_MANIFEST.md`, ver
[[recrear-video-creadores-edits]] §8) los valores de `centerY` / `centerX` usados en el `endCard` y
que cumplen este estándar, para que la próxima reconstrucción salga idéntica.

## Estado

**Resuelto (2026-11-19).** Arturo decidió que los dos videos ya entregados (`17_carpet` final v1 y
`18_shaver` v7) **se quedan como están**: **no** se regeneran sus portadas. Este documento solo fija y
guarda la especificación; no se regeneraron portadas, no se tocó código de la app/Remotion, colas, medios
ni el NAS.

El estándar **aplica a las entregas nuevas**, y las dos más recientes lo **cumplen** (medido con PIL sobre
las portadas reales a 1080×1920 y revisado visualmente el 2026-11-19):

| Caso | Archivo | bbox de texto (medido) | Centro del bloque | ¿Cumple? |
|---|---|---|---|---|
| **19_dualshaver** v1 | `dualshaver19-final-v1/19_dualshaver_ja_v1_cover.png` | x 207–873, y 301–459 | **x 540.0 · y 380.0** | **Sí** (`x=540`, `y≈378`; fondo con el producto visible) |
| **20_dualshaver** v1 / v2 | `dualshaver20-final-v2/20_dualshaver_ja_v2_cover.png` | x 207–873, y 301–459 | **x 540.0 · y 380.0** | **Sí** (`x=540`, `y≈378`; fondo con el producto visible) |

En ambos el `endCard` prop-driven usa `centerY 378`; el centro medido cae en `y≈380`, dentro de la
tolerancia ±4 px. El producto (la afeitadora blanca sostenida en mano) se ve claro en el fondo de las dos
portadas, y ninguna lleva flecha, CTA ni precio.

**Actualización (2026-11-23):** se añadieron la **trampa del último cuadro en negro**, el método para
**recomponer** una portada a mano (con **`KeinannMaruPOPjp`**, no el *fallback* Noto) y la regla de **la
portada de una variación** (otro cuadro y otro texto). Verificado en las variaciones del `19_dualshaver` y
del `20_dualshaver`.

## Ver también

- [[ttchop-video-paths]] — punto de entrada de las vías de video y sus piezas compartidas.
- [[recrear-video-creadores-edits]] — §7 subtítulos/overlays y el prop `endCard`; §8 variaciones.
- [[ttchop-carousel-creation]] — portadas de carrusel (misma familia tipográfica, otro formato).
