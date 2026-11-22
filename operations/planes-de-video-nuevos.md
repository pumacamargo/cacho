---
title: Planes de video nuevo (shot list HTML + animatic) para productos futuros
created: 2026-11-22
updated: 2026-11-22
type: runbook
tags: [runbook, pipeline, automatizacion, producto]
status: active
confidence: high
related: [recrear-video-creadores-edits, estudio-creadores-fuentes-datos, ttchop-video-generation, ttchop-video-paths]
---

> **Vía / punto de entrada:** [[ttchop-video-paths]] — cuál de las vías usar y qué comparten.
> Este runbook es la vía **"plan nuevo"**: todavía no hay video de referencia del producto,
> así que se arma un plan de rodaje desde cero. Cuando ya existe el video, la vía es
> [[recrear-video-creadores-edits]].

# Planes de video nuevo (shot list HTML + animatic)

Cómo se construye un **plan de video** para un producto que todavía no se ha filmado:
una shot list en HTML con el mismo formato que los desmenuzados, con imágenes de
referencia generadas por IA y un animatic para revisar el guion. El plan es una guía
de rodaje, no material filmado.

**Caso verificado de punta a punta:** `dadawoca ナノガラス ムダ毛ケア` (`prod_c2xwdrb`),
plan de 27 tomas / 31.77 s publicado en
`https://lemonsushi.com/uploads/vps2/creators-research/nanoglass-plan27/index.html`
(2026-11-22). Todo lo de abajo sale de ese caso; el documento crece con cada plan nuevo.

## 1. Regla de oro: qué se copia y qué no

| Pieza | De dónde sale | Qué se transfiere |
|---|---|---|
| **Estructura, tiempos y tipos de plano** | Un **desmenuzado** pasado (molde) | Número de tomas, `dur` por toma, orden de bloques, encuadres. Nada más. |
| **Guion (la voz)** | La **documentación de ASU** | Los 4 movimientos y la familia de apertura. |
| **Contenido, acciones y claims** | La **ficha real del producto** | Solo lo que la ficha autoriza. |

Los desmenuzados **no traen guion**: sus `SHOTS` no tienen una sola línea de voz
(verificable: 0 caracteres CJK en el array). Si alguien dice "el script se basó en los
3 videos", es falso: del video se copia el ritmo, el guion es propio. Esta es la
corrección más cara de deshacer, así que se dice desde el principio.

## 2. Fuentes de verdad

### 2.1 Documentación de ASU (primaria para el guion)

- **Guía publicada** (resumen navegable): `https://lemonsushi.com/uploads/vps2/creators-research/asu_kurashi/index.html`
- **Reporte completo por guion** (~50 KB, ~20 guiones analizados):
  `/root/.hermes/profiles/developer/workspace/creator-script-language/inputs/asu_kurashi/script-structure-report.md`
  (no está publicado; se lee desde ahí. También hay copia en
  `.../inputs/sora_no_kurashi3/script-structure-report.md`).
- **Resumen operativo** ya destilado para producir: skill `ttchop-shotlist-storyboard`,
  `references/asu-script-formula.md`.
- Página de wiki que apunta al estudio: [[estudio-creadores-fuentes-datos]].

**Los 4 movimientos** (base de todo guion):

1. **Dar una razón para escuchar** — el hook hablado: la oferta, la preocupación del
   oyente o una reserva honesta.
2. **Detalles útiles** — función y su consecuencia (qué hace y qué cambia para quien lo usa).
3. **Ubicarlo en la vida real** — la situación cotidiana donde encaja.
4. **Siguiente paso** — qué hace el oyente ahora (CTA).

**Familias de apertura** (sobre 20 guiones): offer-led **11**, problem-led **5**,
discovery-led **4**. Elegir **una sola** apertura honesta por guion; no mezclar tres
hooks compitiendo. Si la ficha prohíbe precio y promesas, **offer-led no aplica**:
usar problem-led o discovery-led y explicarlo en la entrega.

**Reglas de honestidad:** no prometer resultados, no inventar escasez ni descuentos,
no inventar una oferta para completar el modelo, no forzar la objeción en todos los
guiones. La guía **no analiza lo visual ni los tiempos**: el flujo numerado es un
modelo editorial, no un storyboard cronometrado. Los tiempos salen del molde.

### 2.2 Desmenuzados pasados (molde estructural)

- **Dashboard publicado:** `https://lemonsushi.com/uploads/vps2/creators-research/`
  (pestañas *Por fecha*, *Por idioma* y *Planes*).
- **Copias locales + generador:** `/root/desmenuzados/` (`build_dashboard.py`,
  `dashboard_data.json`, `creators-research__*__index.html`).
- Cada HTML trae `const SHOTS = [...]` con `n`, `fr`, `dur`, `enc`, `act` e `img` en
  base64. **Filtrar `img` antes de imprimir** o el output se llena de base64.

**Cómo elegir el molde:** por estructura, no por producto.
- `17_carpet` — bloques claros (gancho → textura → cuidado → prueba → cierre).
- `03_suitcase` — features en secuencia + CTA (usado en el plan 27).
- `02_blanket` — comparación + uso cotidiano.

**Ritmo por toma** (mantener la densidad del molde que se calca):
carpet ≈1.28 s/toma (24 tomas / 30.6 s) · suitcase ≈1.18 s (27 / 31.8) ·
blanket ≈1.06 s (25 / 26.6).

**Solo se usan los moldes que Arturo nombró.** Si dice "usa 1, 5 y 6", no se agregan
otros, ni el del mismo SKU, ni variantes "por si acaso".

### 2.3 Ficha del producto

Sin ficha real no se escriben claims. Si el link es de ttchop2
(`ttchop2.web.app/producto/...`), abrirlo con browser y leer título, precio, vendidos y
descripción. Anotar en la entrega las **restricciones de la ficha** (zonas prohibidas,
qué no se puede prometer, si prohíbe precio).

## 3. Procedimiento (8 pasos)

Todo vive en una carpeta de trabajo bajo `/root/`; en el caso 27 fue
`/root/nanoglass-shotlist/`.

### Paso 0 — Confirmar antes de generar
En **una sola** llamada de `clarify`: idioma de la voz, duración (o "igual que las
referencias"), si el material es nuevo o reutilizado, y formato del storyboard.
Preguntarlo antes evita rehacer el entregable completo.

### Paso 1 — Extraer los SHOTS del molde
Regex `const SHOTS\s*=\s*(\[.*?\]);` + `json.loads`, e imprimir `n, dur, enc, act`
(sin `img`).

### Paso 2 — Fusionar la shot list
~20–27 tomas / ~30 s, anotando de qué molde sale cada toma. Verificar la suma real
contra la duración objetivo.

### Paso 3 — Escribir el guion con la fórmula de Asu
Un solo archivo de datos (`planXX.py`) con:
- `PRODUCT` — descripción exacta del producto para los prompts.
- `STYLE` — estilo visual + restricciones de imagen (qué no puede aparecer).
- `SHOTS` — lista de tuplas `(n, dur, grupo, encuadre, acción ES, prompt EN, línea JP)`.
- `LINES` — `(n de la toma donde entra, texto JP, movimiento de Asu)`.
- `LINES_ES` — traducción para el animatic.
- `BLOQUES` — los bloques del molde.
- `timeline()` — acumula `t0/t1` y asigna la línea JP a su toma.

Comentar en el archivo **qué apertura se eligió y por qué** (en el caso 27:
problem-led, "la cuchilla irrita", sin oferta ni precio).

### Paso 4 — Generar las imágenes IA
`genXX.py` recorre `plan27.timeline()`, compone `PRODUCT + prompt + STYLE` y llama a
kie.ai (`kie_gen.py`), con reintentos y caché (`if os.path.exists(p) and size>20000`).
Receta completa y pitfalls: skill `ttchop-shotlist-storyboard`,
`references/ai-images-kie.md`.

**Revisar las imágenes una por una** (hoja de contacto + zoom en las dudosas) antes de
publicar. En el caso 27 salieron 4 discrepancias que se marcaron en el HTML.

### Paso 5 — Construir el HTML
`build_htmlXX.py` incrusta las imágenes en base64 y arma el mismo formato que un
desmenuzado. Tres vistas:

1. **Agrupado por similitud** — grupos que comparten encuadre, fondo y luz.
2. **Por orden de edición** — 1 → N tal como se monta.
3. **Por orden de rodaje** — los mismos grupos ordenados de menos a más complicación
   de set; cada grupo se graba de corrido.

Cada tarjeta lleva: número rojo de posición, `inicio–fin · duración`, tipo de plano,
la acción, una línea **「Cómo se graba」** (encuadre, si la cámara se mueve, qué hace la
mano) y la línea de voz en japonés debajo. Etiqueta **PLAN** en el título y aviso
"aún no filmado".

### Paso 6 — Agrupar por similitud **mirando las imágenes**
Este es el paso que se corrigió en el caso 27: la primera agrupación se hizo por guion
y Arturo la rechazó ("los agrupaste por similitud y no son muy similares"). La regla:

> **Agrupar por lo que se ve en la imagen** (encuadre, fondo, luz, si hay manos, si hay
> estuche), no por lo que dice el guion. Si una toma quedó fuera de su grupo por cómo
> se ve, se mueve.

En el caso 27 quedaron 8 grupos: G1 producto solo sin manos · G2 manos junto a la
ventana/lavabo · G3 manos con producto y estuche sobre mesa · G4 uso en antebrazo ·
G5 uso en pierna · G6 agua en el grifo · G7 persona de cuerpo entero · G8 cenital.

Y donde la imagen no coincide con la acción, se marca un **aviso rojo** en la tarjeta
(`MISMATCH` en el builder): "en el rodaje manda la acción, no la imagen".

### Paso 7 — Animatic (cuando Arturo quiere "confirmar si entiende")
MP4 con las imágenes en el orden del shot list, el guion en español y voz TTS.
Receta, cadena de filtros y pitfalls: skill `ttchop-shotlist-storyboard`,
`references/animatic-desde-imagenes.md`. Se entrega como archivo por Telegram (no como
página) y se dice la duración real y qué líneas se tocaron.

### Paso 8 — Publicar y verificar
Subir a `uploads/vps2/creators-research/<carpeta>/index.html` con
`/root/publish_ftp.py put <local> <remoto>`, y **verificar en vivo**: código 200,
tamaño y **MD5 idéntico** entre el archivo servido y el local. Después, si el plan
debe aparecer en el dashboard, agregar su carpeta al diccionario `PLANES` de
`/root/desmenuzados/build_dashboard.py` y volver a correr el generador.

## 4. Artefactos y dónde quedan

| Archivo | Qué es |
|---|---|
| `planXX.py` | Datos: producto, estilo, SHOTS, LINES, LINES_ES, BLOQUES, `timeline()`. |
| `genXX.py` | Genera las imágenes IA con caché y reintentos. |
| `build_htmlXX.py` | Genera el HTML con las 3 vistas e incrusta las imágenes. |
| `indexXX.html` | El entregable publicado. |
| `animaticXX/build_animaticXX.py` | Arma el MP4 con imágenes + voz ES. |
| `aiXX/shotNN.png` | Una imagen por toma. |

Plantillas reutilizables ya instaladas en la skill `ttchop-shotlist-storyboard`:
`templates/sketch_storyboard.py`, `scripts/build_shotlist_html.py`,
`scripts/gen_ai_images.py`.

## 5. Puertas de calidad (verificar antes de entregar)

- [ ] Suma de duraciones = objetivo, calculada, no estimada.
- [ ] Tomas: ninguna duplicada, ninguna faltante, ninguna fuera de su grupo.
- [ ] Cada toma tiene acción + 「Cómo se graba」 + línea de voz (si le toca).
- [ ] Las 3 vistas cambian de contenido al pulsar (comprobado en el navegador).
- [ ] Imágenes revisadas una por una; discrepancias marcadas en rojo.
- [ ] Restricciones de la ficha respetadas en imágenes **y** en la voz.
- [ ] Etiqueta PLAN + "aún no filmado" + aviso de que las imágenes son referencias.
- [ ] Publicado: 200, tamaño y MD5 iguales al local.
- [ ] Dashboard actualizado si se pidió (carpeta en `PLANES`).

## 6. Pitfalls aprendidos

- **No mezclar referencias**: meter el desmenuzado propio del producto o moldes extra
  cambia la estructura pedida y el usuario lo rechaza.
- **`publish_ftp.py put` conserva el nombre del archivo LOCAL**: para publicar como
  `index.html` hay que copiar antes a un directorio temporal con ese nombre; si no,
  queda `…/carpeta/index-ia.html/index_ai.html` y el dashboard no lo encuentra.
- **Las imágenes IA no salen en 9:16** aunque se pida `portrait_16_9`: vuelven ~1024×1024.
  Recortar con PIL o usar `aspect-ratio` + `object-fit:cover`.
- **El producto IA se parece pero no es idéntico** (color, logo grabado, proporciones).
  Decirlo en la entrega; para el rodaje se usa el producto físico.
- **La voz traducida no cabe en la misma duración**: el TTS en español tarda más que el
  japonés. No acelerar por defecto: estirar los tiempos de imagen y entregar la
  duración real.
- **Al traducir no se cuelan promesas**: コスパ ("buena relación calidad-precio") no se
  convierte en "rinde mucho" ni en precio si la ficha no lo autoriza.
- **Cada molde trae su propia prueba y no son intercambiables**: carpet prueba con
  líquido derramado, blanket con un libro encima (grosor), suitcase con gráfico de
  colores/tallas. Se reutiliza la prueba del molde que se calca.
- **Título o rótulos en japonés con PIL**: DejaVuSans no trae CJK y salen cuadros
  vacíos; usar `/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc`.
- **Si dice "no se parece mucho"**: comprobar qué se copió de verdad y decirlo con
  evidencia (bloques, segundos por toma, pruebas de cada molde) antes de rehacer.
- **Si dice "no entendí los shots"**: explicar en palabras llanas antes de rehacer nada
  (general = espacio/cuerpo, medio = torso y brazos, detalle/macro = solo producto o
  piel; la flecha es el movimiento del producto, no de la cámara).

## 7. Cómo crece este documento

Este runbook es **vivo**. Reglas para que siga creciendo sin degradarse:

1. **Un plan nuevo = una fila en el changelog** (abajo) y, si aplica, un caso verificado
   en §1 con su URL.
2. **Solo se apunta lo verificado.** Cada lección nueva entra en §6 con el porqué; si
   una regla resultó falsa, se corrige en su sitio (no se añade otra contradictoria).
3. **Si un paso cambia de herramienta o ruta**, se actualiza el paso, no se agrega una
   nota al final.
4. **Bump `updated`** en el frontmatter y registrar la acción en `log.md`.
5. **Nada de secretos**: claves y tokens por nombre (kie.ai, FTPS), nunca el valor.
6. Cuando el patrón se repita en 2–3 productos, mover las piezas estables a la skill
   `ttchop-shotlist-storyboard` (plantillas y scripts) y dejar aquí el criterio.

### Changelog

| Fecha | Plan | Producto | Tomas / s | Qué se aprendió |
|---|---|---|---|---|
| 2026-11-22 | `nanoglass-plan27` | dadawoca ナノガラス ムダ毛ケア | 27 / 31.77 | Agrupar por similitud **mirando las imágenes**, no por guion; marcar discrepancias en rojo; el guion sale de Asu, no del desmenuzado. |

## 8. Referencias

- [[recrear-video-creadores-edits]] — la vía cuando ya existe el video de referencia.
- [[estudio-creadores-fuentes-datos]] — de dónde salen los transcript y el reporte de Asu.
- [[ttchop-video-generation]] — qué hace el Producer y qué no.
- Skill `ttchop-shotlist-storyboard` (+ `references/asu-script-formula.md`,
  `references/ai-images-kie.md`, `references/animatic-desde-imagenes.md`).
