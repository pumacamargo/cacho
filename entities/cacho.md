---
title: Cacho (repositorio)
created: 2026-10-10
updated: 2026-10-16
type: entity
tags: [empresa, proyecto, integracion]
status: active
confidence: high
---

# Cacho

Repositorio central de documentación de Arturo, en GitHub
(`github.com/pumacamargo/cacho`). Originalmente era un asistente personal de
notas basado en N8N (gym, meditación, nutrición, options trading, inversiones,
excel) con utilidades en JS; ese contenido quedó obsoleto y fue eliminado.

## Estado actual

Reconvertido en **wiki central de IA** (patrón LLM Wiki): fuente de verdad
compartida para [[hermes-agent]], sus agentes persistentes ([[hermes-agentes]]) y Claude.
Estructura y reglas definidas en `SCHEMA.md`; catálogo en `index.md`.

## Relaciones

- Repositorio consumido por [[hermes-agent]] (clon en `/root/cacho`).
- Contenido mantenido por los agentes de Hermes y Claude.
- Empresa principal documentada: [[ttchop]].

## Convención

Nunca commitear secretos. Commit messages en formato convencional
(`wiki:`, `docs:`, `feat:`). Ver SCHEMA.md para la política completa.
