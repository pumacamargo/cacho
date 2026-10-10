---
title: Runbook — Abrir un task en Paperclip
created: 2026-10-10
updated: 2026-10-10
type: runbook
tags: [proceso, integracion, sistema]
status: active
confidence: high
related: paperclip, ttchop
---

# Abrir un task en Paperclip (CLI board)

Procedimiento verificado para que un agente (p.ej. Hermes) abra un issue/task en
Paperclip y lo asigne a un agente (Developer, Auditor…) que lo resuelva.
Válido pera el flujo de [[ttchop]]: cuando se detecta un bug o mejora en el
pipeline, Arturo abre un task al Developer, que commitea y pushea el fix
(regla de commit [[ttchop]]).

## Prerrequisitos

- CLI instalado: `npm install -g paperclipai` (paquete `paperclipai`, no `@paperclipai/cli`).
- Auth de board guardada en `/root/.paperclip/auth.json` (token `pcp_board_...`).
  Si falta, ver `paperclipai auth whoami --api-base http://172.17.0.1:3100 --json`
  para confirmar (board = admin de todas las empresas del instance).
- Servidor alcanzable en `172.17.0.1:3100` (docker bridge gateway, no localhost).

## 1. Obtener el id del agente asignable (Developer)

`agent list` da nombre, adapter y `reportsTo`, pero **no** el modelo. Basta para
sacar el id del destinatario:

```bash
export PATH="$PATH:$(npm prefix -g 2>/dev/null)/bin"
API=http://172.17.0.1:3100
COMP=f3009db4-1c63-4894-a00d-c568409b890b   # empresa ttchop
paperclipai agent list --api-base "$API" --company-id "$COMP" --json \
  | python3 -c "import sys,json;[print(a['id'],'->',a['name']) for a in json.load(sys.stdin)]"
```

Anotar el id del agente al que se asignará (p.ej. Developer).

## 2. Crear el issue

Verbo del grupo de tareas = `issue` (no `task` ni `issue create --help` para ver flags).

```bash
paperclipai issue create \
  --api-base "$API" \
  --company-id "$COMP" \
  --assignee-agent-id <id-del-developer> \
  --title "Frase corta: qué arreglar" \
  --description "$DESC" \
  --priority high \
  --json
```

- `--description`: incluir contexto, evidencia (runs, IDs, colecciones de Firestore),
  el comportamiento observado vs el esperado, y los cambios propuestos. Escrito en
  español, nombres técnicos en su idioma.
- `--priority`: low / medium / high. A juicio del impacto.
- Flags opcionales: `--project-id`, `--goal-id`, `--parent-id`, `--status`.

Salida (con `--json`): `id` (uuid) e `identifier` (número de issue, p.ej. **TTC-52**).
Usar ese identificador para referenciar el follow-up.

## 3. Verificar

```bash
paperclipai issue list --api-base "$API" --company-id "$COMP" --json   # o
paperclipai issue get <id-or-identifier> --api-base "$API" --json
```

Confirmar que el issue quedó creado, asignado al agente correcto y con el
`identifier` esperado.

## Notas

- Sin secretos: nunca pasar tokens/keys en la descripción del issue.
- Un issue nuevo cae en la cola del agente asignado; con `runtimeConfig.heartbeat`
  desactivado, se ejecuta vía `wakeOnDemand` cuando el agente/board lo despierta.
- Referencia de operación completa del CLI: skill `paperclip` del agente Hermes.

## Relaciones

- Sistema: [[paperclip]] · empresa/pipeline: [[ttchop]] · automatizaciones: [[ttchop-automatizaciones]]
- Wiki: [[cacho]]
