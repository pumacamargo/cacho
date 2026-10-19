---
title: Cacho (repositorio)
created: 2026-10-10
updated: 2026-10-19
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

No crear ramas de tema ni PRs: todos los cambios finales van directamente a
`main`, tras revisión del mantenedor. Antes de editar, verificar que `main` esté
limpia y sincronizada; si está ocupada o sucia, parar y preservar el estado sin
crear ramas laterales. Commit messages convencionales (`wiki:`, `docs:`, `feat:`).
Nunca commitear secretos. Ver SCHEMA.md para la política completa.
