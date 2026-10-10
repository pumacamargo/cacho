---
title: ttchop automatizaciones
created: 2026-10-10
updated: 2026-10-10
type: concept
tags: [proceso, pipeline, cron, automatizacion]
status: active
confidence: high
---

# ttchop — Automatizaciones

Detalle de las automatizaciones internas de `ttchop-bot` (ver [[proyecto-ttchop]]).
El scheduler central vive en `ttchop-bot/scheduler/index.js` (node-cron, Asia/Tokyo)
y es mantenido vivo por PM2.

## Horario diario (JST)

| Hora | Automatización |
|---|---|
| 06:00 | **Pipeline Scout completo** (secuencial, encendiendo el celular) |
| 09:00 | Inteligencia matutina + plan de grabación (Telegram) |
| 19:00 | Plan de grabación del día siguiente (Telegram) |
| 21:00 | Inteligencia vespertina (Telegram) |
| 23:30 | Red de seguridad: apagar pantalla del celular |

## Pipeline de las 06:00 (secuencial)

1. **`daily-tasks`** — tareas del afiliado en TikTok Shop (~15 min).
2. **`request-samples`** — pedir samples gratuitos (~5 min).
3. **`needs-content`** — detectar samples que necesitan contenido (~5 min).
4. **`find-bestsellers`** — encontrar productos top con comisión ≥8% (~2 min).
5. **Producer** — generar 3 videos collage (~10 min c/u).

Resultado guardado en Firestore `bot_daily_runs/{date}`.
Control de pantalla del celular: el 06:00 enciende la pantalla al inicio y la apaga
al final (garantizado incluso en fallo, con red de seguridad a las 23:30).

## Componentes de automatización

- **Scout** (`modules/scout/*`): daily-tasks, request-samples, needs-content,
  find-bestsellers, competitors — controla el celular vía ADB y visión.
- **Producer** (`modules/producer/`): genera 3 videos de convenio; lee
  `recording_plans`, enfría por `bot_productions` (3 días) y rellena con fallback
  aleatorio si no hay plan.
- **Intel** (`modules/intel/*`): reportes y plan del día siguiente (Telegram).
- **Delivery** (`modules/delivery/`): entrega/despliegue.
- **Risk** (`modules/risk/`): gestión de riesgo.

## Infra / datos

- Firestore: 2 proyectos (ttchop y ttchop2) con colecciones distintas.
  Ver referencia de layout en el skill `ttchop-bot-ops`.
- Repos: `ttchop-bot` (scout+scheduler+producer) y `ttchop-server` (render/TTS),
  en [[hardware-vps-projects]].

## Retos

- A TikTok no le gustan los bots → automatizar es complicado; la parte física
  (grabar, pedir samples, subir) es de Arturo.

## Relaciones

- Proyecto: [[proyecto-ttchop]] · empresa/pipeline: [[ttchop]]
- Categoría [[categoria-tts]] · sistemas [[paperclip]], [[hermes-agent]]