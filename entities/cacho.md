---
title: Cacho (repositorio)
created: 2026-10-10
updated: 2026-10-21
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

Cuando Arturo pide documentación, editarla directamente en el wiki: el historial
de Git conserva las versiones y no se requiere propuesta/revisión separada. Cuando
pide código, proceder dentro del alcance solicitado sin confirmación redundante.
No crear ramas de tema ni PRs; trabajar directamente en `main`, pero solo si está
limpia y sincronizada con `origin/main`. Si está ocupada o sucia, preservar el estado
y detenerse. Commitear y pushear los cambios pedidos después de validar. Pedir
autorización aparte para escrituras/migraciones de producción, despliegues/reinicios,
gastos/créditos o cambios de credenciales, seguridad o red. Nunca commitear secretos.
Ver SCHEMA.md para la política completa.
