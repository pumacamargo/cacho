---
title: Paperclip
created: 2026-10-10
updated: 2026-10-10
type: entity
tags: [sistema, infra, integracion]
status: active
confidence: high
---

# Paperclip

Orquestador multi-agente auto-alojado usado por Arturo para gestionar varias
empresas de agentes IA y automatizaciones. Trae adapter nativo para
[[hermes-agent]] (`hermes_local` / `hermes_gateway`).

## Infraestructura

- **Servidor**: Docker, `172.17.0.1:3100` (compose en `/root/paperclip`).
- **UI pública**: https://paperclip.lemonsushi.com (modo authenticated).
- **Versión**: 2026.1005.0. Contenedor `paperclip-server-1`, comparte netns
  con el sidecar de Tailscale.
- **CLI**: `paperclipai`. Auth de board en `/root/.paperclip/auth.json`.

## Uso

- Una empresa registrada: **ttchop** ([[ttchop]]).
- Conexión OpenRouter "My OpenRouter API" (variables de entorno, sin secretos
  en el repo).
- 5 agentes: CEO, Developer, Auditor, Supervisor, Peon. Ver detalle en
  la página de [[ttchop]].

## Relaciones

- Orquesta a [[hermes-agent]] y a agentes propios.
- Empresa principal: [[ttchop]].
- Documentación centralizada en [[cacho]].
