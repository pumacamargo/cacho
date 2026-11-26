---
title: Research de nicho TikTok — cabello (para hamaca azul)
created: 2026-11-26
updated: 2026-11-26
type: runbook
tags: [tiktok, nicho, research, hamaca-azul, affiliate]
status: active
confidence: medium
related: [cuentas-tiktok-shop-affiliate, hooks-para-inicio-de-video, ttchop-video-paths]
---

# Research de nicho: cabello → accesorios y herramientas (para **hamaca azul**)

Objetivo de la cuenta nueva: **subir seguidores primero**, y con base de seguidores vender TikTok Shop affiliate (ver [[cuentas-tiktok-shop-affiliate]]). Este research busca el nicho con más potencial de crecimiento para esa fase.

**Formato del contenido: carruseles de imágenes** (no video). Encaja con el dato de origen, que sale de la pestaña **Photo posts** de la herramienta — o sea, la demanda medida es de carruseles.

## De dónde salen los datos

- **Fuente**: video de 23.5 s (596×1280) grabado desplazándose por **Creator Search Insights** de TikTok, pestaña **Photo posts**. Enviado por Arturo el **2026-11-26**.
- **Método**: extracción de 23 cuadros (1 fps), OCR con `tesseract` (jpn+eng) y **lectura cuadro por cuadro** de 15 fotogramas clave. Los cuadros se solapan, así que la lista se reconstruyó por orden de aparición.
- **Límite de la fuente**: es **una sola captura**, de una cuenta, en una pestaña concreta. Los temas vienen **mezclados en japonés (40) e inglés (16)** tal como los muestra la herramienta. La primera y la última fila quedaron cortadas por el desplazamiento.
- **Datos crudos guardados**: `raw/creator-search-insights-2026-11-26.csv` (tabla) y `raw/creator-search-insights-2026-11-26.md` (lista legible con traducciones).

## Agrupación de los 56 temas

| Grupo | Temas | Con >1K vistas | Vistas sumadas | % del total |
| --- | ---: | ---: | ---: | ---: |
| **Cabello (cuidado y estilizado)** | 27 | 17 | 6,182,492 | **87.0 %** |
| Estilo de vida / narrativa | 5 | 2 | 359,899 | 5.1 % |
| Moda y accesorios | 6 | 4 | 350,498 | 4.9 % |
| Hogar y organización | 3 | 1 | 199,299 | 2.8 % |
| Belleza / skincare | 4 | 1 | 12,799 | 0.2 % |
| Tecnología y gadgets | 11 | 1 | 4,393 | 0.1 % |

**Dato que decide:** de los **15 temas con más vistas, 12 son de cabello**; solo se cuelan bolsos (7º), artículos de guardado (12º) e historia personal (13º).

**El salto grande está entre el puesto 15 y el 16**: 168K → 30.7K (**5.5× menos**). Del 1 al 15 son temas de 168 mil vistas o más; del 16 en adelante, de 30 mil o menos. Otros escalones: 20→21 (12.3K → 5.7K) y 41→42 (199 → 100).

## Top 20 (ordenado por vistas)

| # | Original | Español | Vistas | Crec. |
| ---: | --- | --- | ---: | ---: |
| 1 | Best styles for long hair | Los mejores estilos para cabello largo | 1.33M | — |
| 2 | My go-to hair products | Mis productos de cabello de siempre | 1.03M | — |
| 3 | スタメンヘアケアアイテムをご紹介 | Presenta tus productos de cuidado del cabello imprescindibles | 1.03M | — |
| 4 | My favorite hair straighteners | Mis planchas de cabello favoritas | 615K | — |
| 5 | お気に入りのヘアケアアイテムを紹介 | Presenta tus productos de cuidado del cabello favoritos | 516K | ▲157.9 % |
| 6 | ヘアスタイリングにおすすめのアイテム | Artículos recomendados para estilizar el cabello | 344K | ▲85.4 % |
| 7 | お気に入りの普段使いバッグは？ | ¿Cuál es tu bolso favorito para el día a día? | 319K | ▲41.5 % |
| 8 | Show your favorite soft hair clips | Muestra tus pinzas de cabello suaves favoritas | 293K | ▲1,000 %+ |
| 9 | Tips for curling short hair | Consejos para rizar cabello corto | 277K | — |
| 10 | おすすめ！爽やかヘアアレンジ | ¡Recomendado! Peinados frescos y ligeros | 274K | — |
| 11 | くせ毛さんに◎おすすめのヘアケアルーティン | Rutina recomendada para cabello con onda/rizado | 221K | ▲1,000 %+ |
| 12 | あなたの持っている収納アイテムのお気に入り | Tus artículos de organización/guardado favoritos | 199K | — |
| 13 | あなたの人生から物語を語ろう | Cuenta una historia de tu propia vida | 191K | — |
| 14 | おすすめのヘアトリミングツールを見せて | Muestra tus herramientas de corte de cabello recomendadas | 190K | — |
| 15 | 愛用のワークアウトグッズをシェアして | Comparte tus artículos de entrenamiento de siempre | 168K | — |
| 16 | Discuss your favorite hair clippers | Habla de tus máquinas de cortar cabello favoritas | 30.7K | ▲102 % |
| 17 | クリエイティブなネックレスのギフトアイデアを見せて | Muestra ideas creativas de collares para regalar | 17.1K | — |
| 18 | 使っているヘアケア商品を公開 | Muestra los productos de cuidado del cabello que usas | 14.2K | ▲1,000 %+ |
| 19 | おすすめのスキンケアコンボを紹介して | Presenta tu combinación de cuidado de piel recomendada | 12.5K | ▲525 % |
| 20 | お気に入りのスマホケースを見せて | Muestra tu funda de celular favorita | 12.3K | — |

## Nicho elegido: **cabello → accesorios y herramientas de peinado**

No “cuidado del cabello” en general (dominado por marcas y con productos difíciles de demostrar), sino el tramo de **herramientas y accesorios**:

**Temas con volumen *y* crecimiento (los que valen):**
- **Pinzas de cabello suaves** — 293K con **▲1,000 %+**
- **Rutina para cabello ondulado/rizado** (くせ毛) — 221K con **▲1,000 %+**
- **Artículos para estilizar** — 344K con ▲85.4 %
- **Rizar cabello corto** — 277K
- **Herramientas de corte de cabello** — 190K

**Por qué este y no otro:**
1. **Demanda alta y creciente** — son los únicos temas con volumen grande *y* crecimiento marcado.
2. **Encaja con el pipeline** — un accesorio se demuestra solo (antes/después en 15 s); no hace falta actor ni estudio.
3. **Variantes infinitas** — pinzas, cepillos, planchas, rizadores, tijeras, gorros de satén, ligas, espumas; cada uno con 4–5 ángulos.

**Ángulo de contenido:** no “cabello”, sino **“cabello difícil, arreglado rápido”** — el dolor de quien tiene onda o rizo y no tiene tiempo.

**Formatos que funcionan ahí:** antes/después, comparativa de precios y reseña de una herramienta.

**Plan B con datos reales:** **bolsos y accesorios de uso diario** (319K, 4 de 6 temas por encima del piso) — menos demanda, mucha menos competencia, igual de comprable. Y **organización del hogar** (199K, solo 3 temas en esta vista).

**Descartado con estos datos:** tecnología (11 temas, todos en el piso 99–400) y belleza/skincare (4 temas, todos en el piso salvo uno).

## Los 3 temas a trabajar (con el japonés para buscar)

Los tres que sostienen el nicho. **Ojo con el idioma original de cada uno**: dos aparecieron **en japonés** en la herramienta y uno **en inglés** — por eso este último lleva traducción al japonés para buscarlo.

### 1. Pinzas de cabello suaves — vistas 293K · crecimiento **▲1,000 %+**

- **Apareció en inglés** en la herramienta: `Show your favorite soft hair clips`
- **Japonés (traducción, para buscar):** お気に入りのやわらかいヘアクリップを見せて
- **Términos de búsqueda:** `ヘアクリップ` · `柔らかいヘアクリップ` · `痛くないヘアクリップ` · `跡がつかないヘアクリップ`
- **Por qué vale:** es el tema de mayor crecimiento de la lista y el producto es barato, fotografiable y de afiliado directo.

### 2. Rutina para cabello ondulado/rizado — vistas 221K · crecimiento **▲1,000 %+**

- **Apareció en japonés** (original de la herramienta): `くせ毛さんに◎おすすめのヘアケアルーティン`
- **Términos de búsqueda:** `くせ毛` · `くせ毛 ヘアアレンジ` · `くせ毛 ヘアケア` · `くせ毛 ルーティン` · `くせ毛 縮毛矯正`
- **Nota de traducción:** `くせ毛` es cabello **con onda o rizado natural** (no “rizado con plancha”); `◎` marca “muy recomendado”.

### 3. Artículos para estilizar — vistas 344K · crecimiento **▲85.4 %**

- **Apareció en japonés** (original de la herramienta): `ヘアスタイリングにおすすめのアイテム`
- **Términos de búsqueda:** `ヘアスタイリング` · `スタイリング剤` · `ヘアアレンジ アイテム` · `ヘアアイテム`
- **Por qué vale:** es el de más vistas de los tres, y el más amplio — da para muchas variantes de carrusel (planchas, cepillos, rizadores, ceras, espumas).

**Cómo usarlos al buscar los posts:** en TikTok, pegar el término japonés en la búsqueda y mirar **cuántos resultados y de qué fecha** salen. Eso es la competencia, que es el dato que este research **no** trae.

## Advertencias (leer antes de comprometerse)

- Este research mide **volumen de búsqueda**, **no competencia ni ingresos**. Demanda alta con muchos creadores encima no sirve; hay que contar cuántos videos ya existen por tema.
- La mitad baja de la lista son **valores de piso** (99/100/199/200 repetidos) que probablemente no son mediciones reales. Lo aprovechable es el top 20.
- Es **una captura de una cuenta**: conviene repetir la extracción con más categorías y fechas antes de fijar el nicho.

## Pendiente

- Validar competencia por tema (cuántos videos existen).
- Confirmar que existan productos de afiliado para los accesorios elegidos.
- Armar el plan de contenido de los primeros 10 videos (tema, gancho, formato, producto).