---
title: ttchop (empresa y pipeline)
created: 2026-10-10
updated: 2026-10-10
type: entity
tags: [empresa, proceso, pipeline, cron]
status: active
confidence: high
---

# ttchop

Empresa registrada en [[paperclip]] (id `f3009db4-1c63-4894-a00d-c568409b890b`)
y pipelines diarios de automatización (scout → producer).

## Agentes (en Paperclip)

- CEO (Sonnet 5)
- Developer
- Auditor
- Supervisor
- Peon (Haiku 4.5, solo tareas sencillas)

Presupuestos mensual/lifetime sin tope; **no** hay ventana diaria.

## Pipeline diario

- Fase **scout** → fase **producer**.
- Cron (JST): 06:00 / 09:00 / 19:00 / 21:00.
- Automatización gestionada también vía n8n (en el mismo VPS).

## Infra relacionada

- Corre sobre [[paperclip]] (orquestación) y comparte VPS con
  [[hermes-agent]].
- Documentación central en [[cacho]].

## Convención operativa

Arturo prefiere revisar cada función automatizada en vivo antes de darla por
buena; para fixes abre tasks de Paperclip al agente Developer, y quiere cambios
commiteados y pusheados (regla de commit TTC-41).
