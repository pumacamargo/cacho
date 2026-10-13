---
title: ttchop automatizaciones
created: 2026-10-10
updated: 2026-10-11
type: concept
tags: [proceso, pipeline, cron, automatizacion]
status: active
confidence: high
---

# ttchop — Automatizaciones

Detalle de las automatizaciones internas de `ttchop-bot` (ver [[proyecto-ttchop]]).
La webapp que consume estas capacidades es [[ttchop-webapps]].
El scheduler central (`ttchop-bot/scheduler/index.js`, node-cron en Asia/Tokyo)
es mantenido vivo por PM2 y dispara cada job.

## Horario diario (JST)

| Hora | Automatización |
|---|---|
| 06:00 | **Pipeline Scout completo** (secuencial, con control de pantalla del celular) |
| 09:00 | Intel matutina (reporte vía Telegram) + plan de grabación |
| 19:00 | Plan de grabación del día siguiente (Telegram) |
| 21:00 | Intel vespertina (reporte vía Telegram) |
| 23:30 | Red de seguridad: apagar pantalla del celular |

## Pipeline de las 06:00 (secuencial, 5 fases)

1. **`daily-tasks`** — tareas del afiliado en TikTok Shop (~15 min).
2. **`request-samples`** — pedir samples gratuitos (~5 min).
3. **`needs-content`** — detectar samples que necesitan contenido (~5 min).
4. **`find-bestsellers`** — productos top con comisión ≥8% (~2 min).
5. **Producer** — generar 3 videos collage (~10 min c/u).

Cada fase es tolerante a errores: una falla no aborta el resto. Resultado guardado
en Firestore `bot_daily_runs/{date}` (per-fase: `tasks`, `requestSamples`,
`needsContent`, `findBestsellers`, `producer`).

## Objetivos del pipeline (qué busca lograr cada fase)

1. **`daily-tasks`** — revisar los tasks que TikTok Shop da al afiliado para
   detectar los importantes que pasen nuestros filtros, y ver qué productos de
   ese task tenemos disponibles para hacer el video, completar el task y cobrar
   la recompensa (dinero o cupones).
2. **`request-samples`** — agregar los productos de mejor calidad al showcase,
   para que Arturo los revise y pida muestras gratuitas de los mejores.
3. **`needs-content`** — cuando las muestras gratuitas llegan a casa aparecen en
   TikTok Shop como productos que necesitan contenido; generar una lista para
   crear ese contenido lo antes posible (evitar penalizaciones).
4. **`find-bestsellers`** — encontrar los productos que mejor hemos vendido para
   hacer más videos de ellos. **Se apoya en la data de la cuenta de la esposa
   (Momo's Choice)**: está vendiendo bastantes productos, así que su data sirve y
   los productos ya están en casa.
5. **Producer** — generar los 3 videos que se publican en TikTok (3 diarios).

### Scout (módulos que controlan el celular vía ADB + visión)

- **`daily-tasks.js`** — escaneo diario de tareas en TikTok Shop Growth.
  Estrategia "barato→preciso": la lista de tareas la lee del XML de
  uiautomator (texto exacto del árbol de accesibilidad); el detalle de cada tarea
  y producto lo interpreta visión Haiku (captura todos los pasos aunque digan
  "yen" o "views"). Guarda en `scout_tasks`.
- **`request-samples.js`** — añade al showcase hasta `MAX_SAMPLES_PER_RUN`
  productos free-sample que cumplan TODO: badge "Free sample" + badge
  "Top selling" + ≥1000 unidades vendidas.
  **Robustez ADB (TTC-53, 2026-10-11)**: un timeout transitorio en
  `adb pull`/`screencap` (canal VPS→Pi→ADB→teléfono) ya no tumba la fase
  entera — hay reintentos/backoff, y se guardan conteos parciales aunque el
  proceso salga con código ≠ 0.
- **`needs-content.js`** — navega a goShopToolkit → Manage samples → Free sample
  (Pending criteria); extrae nombre del producto y días restantes para publicar
  contenido; guarda en `sample_content_needed`. **Alerta** si quedan ≤4 días.
  Ojo: `detected:0` en el resultado es normal (limpieza), no un fallo.
- **`find-bestsellers.js`** — analiza datos Excel REALES de ventas de todas las
  cuentas (propias + referencia de otras cuentas) y escribe top-5 con comisión
  8–50% y ventas ≥5. Excluye productos producidos en los últimos 3 días (solo
  los que se produjeron bien).
- **`competitors.js`** — scraping de productos promovidos por competidores:
  abre perfil por deeplink, captura la grilla, visión identifica los 3 primeros
  videos no fijados, entra a cada uno y al card del producto.

### Producer (`modules/producer/index.js`)

- Genera **3 videos collage diarios**. Lógica: lee el plan de grabación de hoy
  (`recording_plans/{date}`, guardado el día anterior a las 19:00); por cada
  producto del plan busca producto Firestore + sesiones disponibles; los que
  coinciden y no están en cooldown se producen; los huecos se rellenan con
  fallback aleatorio. Cooldown: `bot_productions` a 3 días. Registra `fromPlan`
  vs `fromRandomFallback` (para que el Auditor confíe en el ROI).
- **Fallback de emergencia (TTC-54, 2026-10-11)** — regla de Arturo "no quedarse
  sin videos diarios": si el fallback aleatorio encuentra **0 candidatos**
  (todas las sesiones en cooldown de 20d → `0 candidates`), el producer **igual
  produce los 3 videos** saltándose el cooldown de sesión y de producto,
  eligiendo los **menos usados** (least-recently-used) y marcando el slot como
  `random_emergency` (caption 🚨 en Telegram). Fuera de ese caso se respeta el
  cooldown. **Dependencia**: si no hay NINGÚN clip grabado (no "en cooldown"),
  ni esto produce — hace falta grabar clips nuevos.

### Intel (`modules/intel/*`)

- **`index.js`** — analítica y decisiones de producción: lee renders +
  `tiktok_videos` + `analytics_orders` de Firestore, calcula **ROI por video,
  producto y plantilla**, decide qué productos rinden mejor y alimenta al
  producer. Genera el reporte diario y lo manda por Telegram.
- **`next-day-plan.js`** — plan de grabación: qué grabar HOY para que el bot
  produzca mañana. Combina `sample_content_needed` (samples que ya tiene,
  ordenados por urgencia) y `scout_tasks` (productos de tareas activas, por
  recompensa). Guarda en `recording_plans/{date}`.

### Risk (`modules/risk/index.js`) — anti-ban

- Protege las cuentas TikTok de bans/restricciones. Filosofía: TikTok detecta
  bots por **patrones**, no por páginas visitadas. Añade **variación** de tiempos,
  orden de acciones y cantidad diaria; si detecta una advertencia → **detiene todo
  y alerta a Arturo** (pausa la cuenta ese día). Utilidades: `trackAction` (tope
  diario por cuenta), `humanDelay`/`readingDelay` (retrasos aleatorios),
  `reportWarning`/`hasActiveWarning`/`detectWarningInText` (detección de warnings).

### Delivery (`modules/delivery/index.js`) — Telegram

- Filosofía **NO spam**: solo un reporte diario consolidado; alertas solo si
  requieren acción de Arturo; el resto va en silencio a Firestore. Envía texto y
  capturas con caption a Telegram.

### Celular / ADB (`modules/scout/`)

- **`adb.js`** — control remoto del celular: VPS → Pi (socat:5038) → ADB server
  → teléfono.
- **`open-phone.js` / `close-phone.js`** — encender/desbloquear y cerrar
  TikTok/apagar pantalla, al inicio/fin del flujo diario.
- **`navigate.js`** — secuencias de navegación dentro de TikTok; usa visión para
  tocar elementos.
- **`vision.js`** — todas las llamadas de visión vía OpenRouter (Claude Haiku).
- **`png-crop.js`** — recorta el screenshot a una banda vertical para que la
  visión acierte mejor las coordenadas.
- **`product-name-filter.js`** — filtra etiquetas de UI que la visión confunde
  con nombres de producto (evita que "3 days left" o "Sample product" entren al
  plan de grabación y el Producer renderice nada real).
- **`debug-logger.js`** — logger visual para depurar el scout.

## Infra / datos

- Firestore: 2 proyectos (ttchop y ttchop2) con colecciones distintas.
  Ver referencia de layout en el skill `ttchop-bot-ops`.
- Repos: `ttchop-bot` (scout+scheduler+producer) y `ttchop-server` (render/TTS),
  en [[hardware-vps-projects]].

## Retos

- A TikTok no le gustan los bots → automatizar es complicado; la parte física
  (grabar, pedir samples, subir) es de Arturo.

## Escalabilidad multi-cuenta (REQUISITO de diseño)

Actualmente se opera **1 cuenta** de TikTok, pero la idea es escalar a **varias
cuentas** una vez el proceso esté 100% automatizado. **Los procesos deben estar
diseñados generalizados/escalables a más cuentas desde ahora** — no hardcodear a
una sola cuenta.

Consideraciones:
- No asumir una única cuenta en rutas ni constantes (ej. `ACCOUNT = 'arts.choice'`
  aparece fijo en `intel/index.js` — debe volverse configurable/por-cuenta).
- Los módulos de scout ya iteran "por cuenta activa" (`modules/scout/index.js`
  corre para cada cuenta activa), lo cual es la base correcta.
- Al añadir una cuenta nueva, verificar: colecciones Firestore por cuenta, límites
  de riesgo anti-ban por cuenta, y cooldowns independientes.

## Relaciones

- Proyecto: [[proyecto-ttchop]] · empresa/pipeline: [[ttchop]]
- Categoría [[categoria-tts]] · sistemas [[paperclip]], [[hermes-agent]]