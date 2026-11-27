---
title: Carruseles de frases para hamaca azul (desmenuzar + recrear)
created: 2026-11-26
updated: 2026-11-26
type: runbook
tags: [runbook, proceso, negocio]
status: active
confidence: high
related: [cuentas-tiktok-shop-affiliate, nicho-cabello-tiktok, ttchop-carousel-creation, dashboards-hosting]
---

# Carruseles de frases para hamaca azul (desmenuzar + recrear)

Runbook para **desmenuzar un carrusel de imágenes** de otra cuenta y **recrearlo con
una variación** (contenido propio) para publicarlo. Es el formato con el que
**arranca [[cuentas-tiktok-shop-affiliate]] (hamaca azul)**: primero crecer
seguidores con carruseles, después vender. **Se van a hacer más** — este documento
es el método reutilizable, no el registro de un caso suelto.

> **Regla de Arturo (2026-11-26): el desmenuzado de un CARRUSEL NO se mezcla con el
> desmenuzado de un VIDEO.** Son procedimientos y artefactos distintos: el de video
> mide script + recordings + video editing con audio y tiempos (ver
> [[recrear-video-creadores-edits]] y [[estudio-creadores-fuentes-datos]]); el de
> carrusel es slide por slide, sin audio ni edición de video. Van en carpetas e
> índices separados para que no se revuelvan.

## Dónde se guarda (separado del video)

- **Artefacto local:** `/root/desmenuzados-carrusel/<caso>/` (hermana de
  `/root/desmenuzados`, **no** dentro). Un caso contiene:
  - `desmenuzado.md` — el análisis (Fase 1) + la entrega (Fase 2).
  - `slides/01.jpg…NN.jpg` — los slides de la referencia, en orden.
  - `fondos/` — las imágenes de fondo usables (elegida + alternativas) + `README.md`
    con el comando para re-montar con otra.
  - `ai/` — generación de fondos con IA (`gen_backgrounds.py`) + `manifest.json`.
  - `final_<letra>/01.png…` — la salida montada (una carpeta por fondo).
  - `perfil/` — avatar/bio propuestos (si se hicieron).
  - `build_slides.py` (renderizador) y `build_carrusel.py` (CLI).
- **Copia de los slides:** imprescindible, porque los adjuntos entrantes viven en la
  caché del gateway (se autolimpia). El nombre de carpeta que asigna el gateway es el
  **SHA-256 del archivo** — no da orden ni nombre original.
- **Herramientas compartidas (reusar, no reescribir):** `/root/desmenuzados-carrusel/_tools/`
  → `build_slides.py` (renderizador), `build_carrusel.py` (CLI) y `gen_backgrounds.py`
  (fondos con IA). Se **copian** a cada caso nuevo; ver `_tools/README.md`.
- **Conocimiento:** esta página de Cacho.
- **Publicación del artefacto (opcional, solo si Arturo lo pide):** en su propia
  carpeta/índice del hosting (p. ej. `uploads/vps2/carruseles/`), **nunca** dentro de
  `creators-research` (índice de desmenuzados de video). Ver [[dashboards-hosting]].

## Fase 1 — desmenuzar (slide por slide)

Nada de script/recordings/video-editing: eso es del video.

1. **Inventario de entrada:** cuántos slides llegan y cuál(es) se ignoran (suele haber
   un slide final de anuncio/CTA de la cuenta ajena). Confirmarlo con Arturo.
2. **Ficha técnica del formato** (medida, no estimada):
   - nº de slides de contenido, px reales, si el **fondo se repite** o cambia por slide
     (comparar regiones sin texto por diferencia de píxeles),
   - color/estilo del texto, con caja o sin caja, sombra, familia tipográfica,
   - **cuerpo e interlineado** por detección de bandas de texto (filas con píxeles
     claros) y **centro vertical del bloque** (no siempre anclado arriba),
   - extras: números, flechas, stickers, contador, atribución fija.
3. **Por cada slide:** nº, **rol narrativo** (hook / definición / mecanismo / tesis /
   juicio / consecuencia / consejo / mandato / reencuadre / cierre-CTA), descripción de
   la imagen y el **texto original (JP) + traducción ES de revisión**.
4. **Arco narrativo:** cómo encadenan (a veces las frases continúan de un slide al
   siguiente) y dónde está el gancho y el cierre.

## Fase 2 — recrear con variación

- Misma **estructura, ritmo y arco**; **contenido propio**: frases **reescritas** y
  **fondo propio** (no reciclar texto ni foto ajena).
- Fijar antes de generar: **tema** de las frases, **fondo** (generado vs. reutilizado) y
  **título/hashtags**.
- **Publicación en TikTok:** ttchop_robot **nunca** publica; Arturo publica a mano.

## Pipeline reproducible — hacer el siguiente (paso a paso)

```bash
mkdir -p /root/desmenuzados-carrusel/<caso> && cd /root/desmenuzados-carrusel/<caso>
cp /root/desmenuzados-carrusel/_tools/build_slides.py \
   /root/desmenuzados-carrusel/_tools/build_carrusel.py .
mkdir -p ai && cp /root/desmenuzados-carrusel/_tools/gen_backgrounds.py ai/

# 0) Guardar los slides de referencia FUERA de la caché (ver Pitfalls) y analizarlos
#    -> desmenuzado.md
#    Editar SLIDES / SLIDES_REESCRITO en build_slides.py con el texto del caso.

# 1) (Opcional) Generar fondos con IA. Editar CONCEPTS en ai/gen_backgrounds.py.
export KIEAI_API_KEY=$(ssh root@100.68.238.117 \
  'grep -m1 "^KIEAI_API_KEY=" /root/projects/ttchop/ttchop-server/.env | cut -d= -f2-' \
  | tr -d '"'"'"'\r\n')          # nunca imprimir la clave
python3 ai/gen_backgrounds.py     # crea manifiesto ANTES de poll-ear (no re-cobra timeouts)

# 2) Montar el set completo (10 slides) con el fondo elegido y el texto reescrito
python3 build_carrusel.py --fondo fondos/A_retrato.jpg --texto reescrito --out final_A
#    --texto: reescrito | original     --out: carpeta nueva (no pisar entregas)
#    Para publicar el mismo post con otra foto:
#    python3 build_carrusel.py --fondo fondos/B_ventana.jpg --texto reescrito --out final_B

# 3) QA antes de entregar
#    - hoja de contacto 5x2 y revisión con visión
#    - medir márgenes: ninguna línea puede salirse del ancho (a 64 px, ≤16 caracteres/línea)
# 4) Entregar los PNG individuales en orden por Telegram (no ZIP). Nunca publica el bot.
```

**Especificación de diseño vigente** (la del caso 01, reutilizable):

| Pieza | Valor |
| --- | --- |
| Lienzo | **1080×1440** (3:4) |
| Fondo | imagen B/N recortada a 3:4 + viñeta/oscurecido para legibilidad |
| Tipografía | **`Noto Sans CJK JP` Bold 64 px**, interlineado 98 px |
| Texto | blanco **#ffffff** centrado, **sin caja**, sombra suave |
| Bloque | centrado vertical a **≈53 %** de la altura |
| Atribución | 「アドラー心理学」 (o la que corresponda al tema) debajo |
| Número de orden | **«N / 10»** abajo al centro |
| Salida | PNG individuales, 1080×1440 |

**Fuentes japonesas disponibles** (son las únicas 3 familias reales en los hosts; DejaVu/
Liberation no traen japonés):
`KeinannMaruPOPjp` (redondeada, estándar de portadas ttchop, `/root/dualshaver-announcer/`),
`Noto Sans CJK JP`, `Noto Serif CJK JP` (+ `Noto Sans Mono CJK JP`, monoespaciada).

**Avatar y bio de la cuenta** (propuestas del 2026-11-26, en `perfil/` del caso 01):
avatar **tipográfico** — un kanji fijo (p. ej. 「心」) blanco sobre fondo oscuro: se lee a
tamaño diminuto y mantiene la identidad B/N + texto blanco. Bio propuesta:
「心を軽くする言葉を、ひとつずつ。／人間関係やマインドセットのヒントを発信しています🌿／
フォローしてもらえると嬉しいです。」

**Costos:** generar fondos = **5 créditos por imagen** (kie.ai, `bytedance/seedream-v4-text-to-image`).
Los fallos del proveedor **no se cobran**. Pedir autorización de gasto antes de generar.

## Caso 01 — Frases de psicología (Adler) · 2026-11-26

Primer caso. Cuenta japonesa de frases con retrato vintage en B/N.

- **Entrada:** 11 imágenes (960×1280). **10 de contenido** + **1 final de anuncio de la app
  Motto**, que Arturo pidió **ignorar** (guardado solo como referencia).
- **Formato medido:** fondo **idéntico en los 10 slides** (retrato B/N con viñeta); texto
  blanco **#ffffff** centrado sin caja con sombra; gothic/rounded sans; cuerpo ≈48 px de
  tinta e interlineado ≈83 px (a 960 de ancho); atribución 「アドラー心理学」; bloque centrado
  vertical a **≈53 %**.
- **Arco:** hook (el mal humor es el mayor pecado) → definición (inmaduro) → mecanismo
  (busca atención) → tesis (controla al otro) → juicio (niño de 3 años) → consecuencia
  (tratarles en serio hace perder) → consejo (ignorar) → mandato (no gastar tu tiempo) →
  compasión (pobre persona) → cierre (concéntrate en lo tuyo).
- **Entrega final:** texto **reescrito** (propio, mismo arco) + fondo **A** (retrato de
  época generado con IA, B/N) → `final_A/01..10.png` (1080×1440).
- **Fondos guardados** en `fondos/`: `A_retrato` (elegido), `B_ventana`, `C_textura`,
  `D_adler_dominio-publico` (la foto original de Adler) + `README.md`.
  Generación: `ai/gen_backgrounds.py`; gastado **15 créditos** (A, B y C — el C falló en el
  primer intento sin cobro y se reintentó). El texto de referencia se conserva también: para
  volver a él, `--texto original`.
- **Título/hashtags entregados:** 不機嫌で周りを振り回す人には、関わらなくていい。 +
  `#名言 #心理学 #人間関係 #マインドセット #人生 #アドラー心理学 #気づき`. **No** se copia el CTA
  de la app de la cuenta de referencia (es de ellos y no tenemos esa app).
- **Nota de coherencia:** el [[nicho-cabello-tiktok|research de nicho]] había elegido
  *accesorios y herramientas de peinado*; el contenido que se está produciendo para hamaca
  azul es **carruseles de frases**. Encaja con «crecer seguidores primero» (las frases crecen
  rápido), pero **queda pendiente confirmar** si el nicho de producto sigue siendo cabello o
  cambió.

## Segundo formato: texto vertical (tategaki) — casos 02 y 03

La misma cuenta de referencia (Motto) publica **otro diseño**: **frases sueltas en texto vertical**
sobre fondo crema. Es el formato de los casos 02 y 03 (ver `desmenuzado.md` de cada uno).

| Pieza | Valor |
| --- | --- |
| Lienzo | **1180×1574** o **1080×1440** (3:4) |
| Fondo | **crema liso `#F4EDDB`** |
| Texto | **vertical (tategaki)**, columnas **de derecha a izquierda**, tinta `#2C231A` |
| Cuerpo | ≈**66–72 px** (ancho de columna ≈63–79 px) |
| Intercolumnas | paso ≈78 px |
| Etiqueta / atribución | vertical, ≈**35 px**, al pie **a la izquierda**, en dos columnas |
| Marca | wordmark del dueño abajo al centro (**su marca: no se reutiliza**) |
| Número de orden | **«N / 10» arriba a la derecha** (lo pide Arturo; el molde no lo trae) |
| Extras | sin flechas ni contador (el molde no numera) |

- **Qué lleva cada cuenta como "etiqueta"**: el caso 02 atribuye cada frase a **personas reales**
  (nombre + rol) — y varias son **misatribuciones conocidas**; el caso 03 usa una **etiqueta de
  categoría** (「ムカついた時に読みたい言葉»). Para lo nuestro: **frases propias** con etiqueta de
  categoría, o citas **verificadas** si se quiere atribuir.
- **La portada es el punto delicado**: el caso 02 abría con una **obra con copyright** (Magritte);
  el 03 **no tiene portada** (10 frases + CTA). Si un molde trae una imagen ajena, **hay que
  hacer una propia**.
- **El renderizador de este formato es nuevo**: PIL no trae maquetación vertical; hay que
  **dibujar carácter por carácter**, por columna, de derecha a izquierda (ojo con 、。「」 y con el
  centrado del bloque).
- **La fuente la define Arturo, no el molde**: aunque la referencia use **mincho**, para lo
  nuestro va **la fuente definida del proyecto** (`Noto Sans CJK JP`, **gothic**). Dijo
  explícitamente que la mincho "no es la fuente que definimos" (2026-11-26).
- **El fondo puede ser una FOTO propia** (no solo el crema): el renderizador acepta foto y
  entonces el texto va **en claro con sombra**. El C03 usó el **papel arrugado en B/N** que mandó
  Arturo (`fondos/fondo-papel-negro.jpg`), recortado a 1180×1574 y oscurecido ×0.86.
- **Casos:** **C02** (`C02_motto-meigen`) — 12 de contenido + CTA; traía la portada de Magritte y
  atribuciones a personas. **C03** (`C03_motto-mukatsuita`) — el **molde más limpio** (10 frases +
  CTA, etiqueta de categoría, sin portada ni duplicados) y **el primer formato ENTREGADO**: 10
  frases propias, fondo de papel propio, pie «Hamaca Azul», etiqueta 「自分を守る言葉» →
  `final_foto/01..10.png`, scripts `build_tategaki.py` + `build_c03.py` (copia en `_tools/`).

## Tercer formato: carrusel en ESPAÑOL con fondo IA — C04 (cuenta Totocha)

Cuenta nueva **Totocha** (en español, contenido cristiano/bíblico), a partir del molde «Davi».
Molde: **2 slides** (collage B/N + «La biblia dice:» y una foto de Biblia con cita + mensaje).

Lo que quedó como formato propio:

| Pieza | Valor |
| --- | --- |
| Lienzo | **1080×1440** (3:4) |
| Fondo | **UNA imagen generada con IA** reutilizada en todos los slides + degradado oscuro arriba para el texto. Elegido: **paisaje al amanecer sin cruz**; se generaron 5 opciones (Biblia, iglesia, amanecer con cruz, manos, paisaje sin cruz) y Arturo eligió |
| Tipografía | **profesional (fuentes variables OFL)**: `Playfair Display` (referencia y gancho), `Lora` (versículo y reflexión), `Inter` (rótulo). **Sombra suave en capas**, nunca contorno duro (`stroke_width`) |
| Texto | blanco cálido, alineado a la izquierda (salvo el gancho, centrado); `Lora` a 0.2 pt de interletrado natural; márgenes x=96 |
| Slides | **3**: gancho (“Es solo un verso de la biblia…”) → **cita bíblica real** (texto RVR1960; el C04 terminó con **Isaías 41:10**) → **reflexión propia** (el C04 la llevó **sin rótulo**, por pedido de Arturo) |
| Cuenta | **totocha** = cuenta **cristiana en español (México)**, de la mamá de Arturo ⇒ versículos en **RVR1960** (versión cristiana/evangélica usada en México) |
| Marca | **sin marca** en los slides (el nombre de la cuenta va en el perfil) |

- **Contenido religioso:** la cita debe ser **bíblica y real**; si se añade una reflexión, **rotularla**
  como reflexión y no atribuirle frases inventadas a la Biblia.
- **Idioma español** ⇒ tipografías latinas (las JP de los otros formatos no aplican).
- Coste: **5 créditos por imagen IA**. Ojo: ofrecer **varias opciones de fondo** es lo que Arturo
  espera (pidió «otras imágenes como opciones» y luego descartar la cruz de una); el C04 gastó
  **25 créditos** en 5 fondos. Artefacto: `/root/desmenuzados-carrusel/C04_davi-biblia/`
  (`final/01..03.png`, `ai/`, `build_c04.py`).

## Pitfalls

- **No mezclar** con el desmenuzado de video ni con su índice (`creators-research`).
- **Bajo «Libro capítulo:versículo» va el TEXTO REAL del versículo**, no una paráfrasis
  inspiracional. El molde de Davi ponía «Lo que Dios tiene para ti no necesitará que lo persigas
  desesperadamente» bajo **Romanos 8:28**, que **no es** ese versículo: se detectó y se sustituyó por
  el texto real (RVR1960). Verificar el versículo antes de montarlo.
- **Copiar los slides fuera de la caché** antes de 24 h: los adjuntos entrantes se
  autolimpian y con ellos se pierde la fuente.
- El nombre de carpeta que da el gateway a cada adjunto es su **SHA-256**: no contiene el
  orden ni el nombre original.
- El **fondo puede ser una sola imagen** repetida en todos los slides: comprobarlo por
  diferencia de píxeles, no a ojo (el zoom aparente engaña).
- **Dos líneas largas se salen del ancho:** a 64 px, cada carácter CJK mide 64 px, así que
  ninguna línea puede pasar de ~16 caracteres. Medir los márgenes antes de entregar.
- Al centrar texto en PIL, **no** usar `anchor="mm"` y restar `ancho/2` a la vez: se
  desplaza a la izquierda. Con `anchor="mm"`, la x es el centro del lienzo.
- La **traducción es de revisión**, no un hecho verificado: marcar matices (p. ej. 不機嫌 =
  mal humor/estar de mal genio; 「幼稚」 = inmaduro/infantil).
- **La cuenta ajena puede promocionar su propia app**: ese CTA no se copia.
- Los fondos generados salen **1600×2848** (9:16); al montar se recorta el centro a **3:4**.

## Relacionado

- [[cuentas-tiktok-shop-affiliate]] — las cuentas (hamaca shop / hamaca azul).
- [[nicho-cabello-tiktok]] — research de nicho para hamaca azul.
- [[ttchop-carousel-creation]] — creación de carruseles (Kie.ai/local, QA).
- [[dashboards-hosting]] — dónde viven los dashboards publicados (video).
- [[recrear-video-creadores-edits]] — el equivalente para VIDEO (no mezclar).
