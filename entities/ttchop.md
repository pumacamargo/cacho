---
title: ttchop (empresa y pipeline)
created: 2026-10-10
updated: 2026-10-16
type: entity
tags: [empresa, proceso, pipeline, cron]
status: active
confidence: high
---

# ttchop

Empresa con pipelines diarios de automatización (scout → producer).

## Pipeline diario

- Fase **scout** → fase **producer**.
- Cron (JST): 06:00 / 09:00 / 19:00 / 21:00.
- Automatización gestionada también vía n8n (en el mismo VPS).

## Infra relacionada

- Comparte VPS y herramientas con [[hermes-agent]] y sus perfiles de [[hermes-agentes]].
- Documentación central en [[cacho]].

## Convención operativa

Arturo prefiere revisar cada función automatizada en vivo antes de darla por
buena; para desarrollo delega mediante Hermes a cualquiera de sus agentes adecuados (Research, Developer, jr_developer o ttchop_robot). Quiere cambios commiteados y pusheados (regla TTC-41).
