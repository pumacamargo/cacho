---
title: Hooks: cómo usarlos al inicio de un video
created: 2026-11-23
updated: 2026-11-23
type: runbook
tags: [runbook, hooks, guion, ttchop, referencia]
status: active
confidence: medium
owners: [arturo, ttchop_robot]
related: [recrear-video-creadores-edits, planes-de-video-nuevos, estandar-thumbnail-video, ttchop-video-paths]
---

# Hooks: cómo usarlos al inicio de un video

Runbook para **usar un clip de hook al inicio** de un video de producto (TikTok Shop / orgánico) y para
**grabar un banco de hooks propios**. Nace de la biblioteca de 12 hooks de referencia que Arturo dejó en
`P:\Tiktok\hamaca\assets\hooks\origen_creadores\2026-11-23_lote01\` (2026-11-23).

> **Regla de oro:** el hook no es el clip. Es **visual + texto en pantalla + línea hablada**, y los tres
> tienen que apuntar a **la misma idea**. Si compiten, el espectador se va.

## 1. Qué es el hook y por qué manda

- **Ventana:** los primeros **1.5–3 s**. El promedio decide en **1.7 s** en TikTok (1.4 s Reels, 2.3 s Shorts).
- **Umbral:** con **≥65–70 % de retención a los 3 s** el algoritmo amplifica; por debajo de ~50 % entra a
  supresión. 63 % de los videos con mejor CTR enganchan dentro de los primeros 3 s.
- **El hook es lo único que ve TODO el mundo**: incluso quien scrollea, alcanza a ver el primer texto.
- **Shop:** el producto debe estar **en cuadro desde el segundo 1** y el hook atado al producto
  (las guías de Shop hablan de ventana de hook de 3–6 s).
- **CTA antes del segundo ~22**, no al final.

Fuentes: [veonib](https://veonib.com/s/guides/cracking-the-2026-short-form-video-algorithm-65-retention-secrets-for-e-commerce-brands) ·
[hansencommerce](https://hansencommerce.com/insights-tiktok-hook-3-seconds) ·
[kometmedia](https://www.kometmedia.com/tutorials/hook-writing-framework-for-short-video) ·
[octomind](https://octomind.run/tap/skills/video-hooks) ·
[varg.ai](https://varg.ai/how-to/make-a-tiktok-shop-video) ·
[creativeanalytics](https://www.creativeanalytics.cc/blog/ad-hook-library)

## 2. El dato que decide cómo abrir

Codificaron la apertura de **43 videos de afiliado de TikTok Shop** (nov-2026):

| Apertura | ≥5M views | 1–5M | <1M |
|---|---|---|---|
| Una persona, un momento o una confesión | **12** | 0 | 0 |
| Un resultado concreto o un precio | **6** | 1 | 0 |
| Sin palabras, solo la imagen | 4 | 0 | 1 |
| El producto y sus cualidades | 1 | 3 | 4 |
| Le habla al espectador ("stop scrolling si…") | 0 | 2 | 6 |
| Saludo o texto fuera de tema | 0 | 0 | 3 |

**Lección:** abrir con **el mundo del espectador** (una persona, un momento, una confesión, un resultado),
no con el producto ni interpelando al que mira. Los que se quedaron abajo elogiaban el producto o
saludaban. Fuente: [ugc.live](https://ugc.live/blog/tiktok-shop-hooks)

## 3. Las tres capas (checklist antes de publicar)

- **Visual:** algo que **se mueva en el 1er segundo y medio**. No zoom lento, no logo, no "hola chicos".
  Rompe el patrón del feed.
- **Texto en pantalla:** 5–12 palabras, específico (número, momento, error concreto). Legible **con el
  sonido apagado**. **Nunca el mismo texto que la línea hablada.**
- **Línea hablada:** una sola idea, **sin el nombre del producto**, dentro de una respiración.
- **On-ramp (2–4 s):** el beat siguiente debe **extender el hook**, no saltar al pitch. Si el hook
  promete "por qué te pasa esto", lo siguiente explica la causa.

## 4. Trampas (las dos que más caro cuestan)

1. **Promesa que el producto no paga.** Un hook desconectado sube la retención de 3 s y **destruye la
   conversión**. El hook tiene que conectar con el dolor que el producto resuelve.
2. **Derechos.** Un clip de creador (disfraz, caída, gym, deportes) **no se publica** en un video de Shop:
   riesgo de strike o reclamo. La biblioteca de referencia es **mood/referencia**; para publicar se usa
   material propio o generado.

## 5. Plantilla de tiempos (para nuestros videos)

```
0.0–0.8   Interruptor visual: clip de hook (audio original MUDO; push-in leve ok)
0.8–2.0   Hook en pantalla (frase corta y específica) + VO línea 1 (distinta del rótulo)
2.0–3.0   Open loop: "y lo peor es…" / pregunta sin cerrar
2.5–3.0   Corte duro → PRODUCTO EN CUADRO
3.0–6.0   Problema, en palabras del comprador
6.0–15    Producto + demo (un solo número real de la ficha)
15–22     Prueba (dato verificado, no el del video original)
<22–25    CTA al carrito + tag/flecha + descargo
```

Total recomendado **18–30 s**. El clip de hook se usa **recortado a su mejor beat** (1.2–2.0 s), no completo.

## 6. Mapeo: qué ángulo pega con cada estilo de hook

| Hook de referencia | Estilo | Ángulo de venta que le queda |
|---|---|---|
| `hook01_pov_moto` | POV movimiento | producto "para llevar / afuera" |
| `hook02_gorila` | absurdo/comedia | "no vas a creer esto" |
| `hook03_demolicion` | antes/después | "rompe el problema" |
| `hook04_estructura_madera` | DIY/construcción | casa y herramientas |
| `hook05_gym_battle_rope` | esfuerzo/fitness | cuidado personal, energía |
| `hook06_drone_altura` | altura/panorámica | "grande/impresionante", oferta general |
| `hook07_ejercicio_casa` | rutina en casa | hogar y bienestar |
| `hook08_mansion_alberca` | aspiración/lujo | regalo, "cuida lo que ya tienes" |
| `hook09_talking_head_nieve` | testimonio | confianza (**cara → no publicable sin derechos**) |
| `hook10_caida_comedia` | fallo cómico | "¿te pasa esto?" (**cara → igual**) |
| `hook11_tobogan_agua` | alivio/agua | baño, limpieza, verano |
| `hook12_macro_impresion3d` | precisión/técnico | gadgets y herramientas |

**Recortes útiles (medidos en la biblioteca):** `hook11` → usar el **splash** (~4–5 s), no el arranque ni el
fundido a negro final; `hook12` (17 s) → un tramo de 1.5 s; `hook06` → el borde de la azotea o el aéreo,
no el parque.

## 7. Banco de hooks propios — shot list de 12 estilos

Objetivo: grabar en **una sola sesión** versiones propias de los 12 estilos, para no depender de clips de
terceros. Todas **verticales 1080×1920, 30 fps, 2–4 s**, **sin texto quemado** (el texto lo pone el montaje)
y con **audio ambiente limpio**.

Reglas de grabación: una toma por estilo (2–3 repeticiones), movimiento en el primer frame, mano/cuerpo
entrando a cuadro, y **nada de props inventados** (ver [[planes-de-video-nuevos]] — decoración de fondo sí,
componentes del producto no).

| # | Estilo | Encuadre y acción (2–4 s) | Texto sugerido (JP) | Props |
|---|---|---|---|---|
| 1 | POV movimiento | Cámara en mano/pecho saliendo de casa o caminando rápido; movimiento constante | もう限界… / これで解決 | ninguno |
| 2 | Absurdo | Entrar a cuadro y **dejar caer** algo cotidiano exagerando la reacción | え、まさか | objeto común |
| 3 | Antes/después | Dos tomas del mismo encuadre: estado "antes" y estado "después" | ビフォー / アフター | zona limpia y zona por limpiar |
| 4 | DIY/casa | Montaje rápido manos trabajando en una superficie (mesa, lavabo) | これだけでいい | herramientas básicas |
| 5 | Esfuerzo | 3–5 s de ejercicio real (sentadillas, saltos) con corte a media repetición | 毎日これだけ | ropa deportiva |
| 6 | Panorámica | Gesto de "mira esto" + paneo lento a un espacio amplio | 広い空間もこれ1つ | cuarto/patio |
| 7 | Rutina en casa | POV de rutina mañanera: despertar, lavabo, espejo | 朝の5分で | baño |
| 8 | Aspiración | Plano cuidado de un rincón bonito de la casa, movimiento lento | きれいを保つ | decoración de fondo sí |
| 9 | Testimonio | Hablar a cámara 3 s, una sola frase, **sin leer** | 正直、半信半疑でした | ninguno |
| 10 | Fallo cómico | Tropezar/dejar caer algo y reír; **sin burla a terceros** | またやった… | objeto común |
| 11 | Agua/alivio | Agua corriendo, mano bajo el chorro, vapor | お風呂上がりに | baño |
| 12 | Macro técnico | Primer plano extremo del producto girando o de un detalle | ここがポイント | producto |

Cada clip se guarda en `assets\hooks\propios\<fecha>_loteNN\` con el mismo `indice.json` (campos
`estilo`, `angulo`, `producto`, `duracion_s`, `sha256`) y su hoja de contacto.

## 8. Matriz de 3 variantes (misma pieza, tres hooks)

Se producen **tres variantes del mismo video** cambiando **solo el arranque** (0–3 s). Así se aísla el
efecto del hook. Se llenan las columnas por producto y se corren como A/B.

| | **A · Dolor** | **B · Curiosidad** | **C · Resultado/precio** |
|---|---|---|---|
| **Visual** | Gesto de frustración o "antes" del problema | Detalle raro del producto funcionando (macro/lado B) | El "después" ya resuelto o el producto en mano |
| **Texto en pantalla** | El problema en palabras del comprador | Pregunta que abre un loop | Resultado concreto (dato verificado) |
| **VO línea 1** | Nombra el dolor en 5–12 palabras | "Nadie te dice esto de…" | Qué logras y en cuánto |
| **On-ramp (2–4 s)** | Explica **por qué** pasa | Entrega la primera pista | Empieza la demo |
| **Cuerpo** | **idéntico** | **idéntico** | **idéntico** |
| **Mide** | hook rate 3 s · hold rate | hook rate 3 s · hold rate | hook rate 3 s · hold rate |

Ejemplo llenado con dadawoca ナノグラス ムダ毛ケア (producto JP; solo como muestra):

| | A · Dolor | B · Curiosidad | C · Resultado |
|---|---|---|---|
| Visual | Manos pasando la rasuradora y gesto de molestia | Primer plano macro de la placa con rejilla | Mano deslizando la placa sobre la piel, sin esfuerzo |
| Texto | カミソリ負けしてない？ | これ、本当に塗らないの？ | 数十秒でお手入れ完了 |
| VO | 剃るたびに肌が荒れる…そんな悩みありませんか。 | 電源も刃もいらないケア、知ってますか。 | 肌を滑らせるだけ。数十秒で終わります。 |
| On-ramp | 原因は肌に直接触れる刃にあるんです。 | これはナノガラスのプレートです。 | まずは目立たない場所から試して。 |

## 9. Medición y A/B

- **Hook rate** = vistas de 3 s ÷ impresiones. **Por debajo de 25–30 %, el hook está mal** — no el cuerpo.
- **Hold rate** = % que llega al final del bloque de producto.
- Probar **3–5 hooks sobre el MISMO cuerpo**. Si gana uno, **no se reescribe el video**: se cambia el
  cuerpo o la oferta y se deja el hook ganador.
- Con la biblioteca y esta matriz, la producción se ordena como: 1 producto → 3 aperturas → 1 cuerpo.

## Changelog

- **2026-11-23 — creación.** Guía + mapeo de los 12 hooks de referencia + shot list de 12 estilos propios
  + matriz de 3 variantes. Fuentes citadas en §1 y §2; los 12 clips quedaron en
  `assets\hooks\origen_creadores\2026-11-23_lote01\` (referencia/mood, **no publicables**).
