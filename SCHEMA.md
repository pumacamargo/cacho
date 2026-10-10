# Wiki Schema — Cacho

> Este archivo es la **constitución** del wiki. Toda IA que opere sobre este repo
> DEBE leer `SCHEMA.md` + `index.md` (y el final de `log.md`) antes de tocar nada.
> Reglas no ambiguas para que agentes distintos produzcan resultados consistentes.

## Domain (¿qué cubre este wiki?)

Todo lo que Arturo necesita que sus sistemas de IA tengan como contexto compartido:

- **Empresas y proyectos** que gestiona (negocios, videojuegos, automatizaciones).
- **Infraestructura de IA**: Paperclip, Hermes, n8n, Affine, OpenRouter, agentes multi-agente.
- **Pipelines y automatizaciones** (ej. pipeline diario ttchop).
- **Procedimientos operativos** (runbooks) y decisiones.

La realidad operativa de los sistemas de IA NO vive en el chat de cada herramienta;
vive aquí. El objetivo es que **todas las IAs vean la misma información actualizada**.

## Conventions (convenciones obligatorias)

1. **Nombres de archivo**: lowercase, con guiones, sin espacios.
   Ej. `pipeline-ttchop.md`, `hermes-setup.md`.
2. **Frontmatter YAML obligatorio** en toda página (ver plantilla abajo).
3. **Wikilinks**: cada página enlaza al menos a 2 otras páginas con `[[wikilink]]`.
   Las páginas aisladas no existen — son invisibles.
4. Al actualizar una página, **bump `updated`** con la fecha de hoy.
5. Cada página nueva debe **añadirse a `index.md`** bajo su sección correcta.
6. Cada acción debe **registrarse en `log.md`** (append-only).
7. **Idioma**: el wiki es bilingüe tolerante pero el contenido de trabajo se escribe
   en español (como lo habla Arturo). Los nombres propios y técnicos van en su idioma
   original (Paperclip, n8n, Docker).
8. **Sin secretos jamás**: NUNCA commitear tokens, claves, contraseñas, API keys.
   Van en `.env` / vaults / variables, referenciados por nombre en el wiki.
9. **Escritura**: los agentes NO reescriben `entities/`, `concepts/` o `operations/`
   a la carrera. Proponen cambios (issue/PR/branch) y Arturo (o un mantenedor)
   los mergea. Solo el mantenedor toca `main` directamente para consolidar.

## Frontmatter (plantilla de página)

```yaml
---
title: Nombre de la Página
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | runbook
tags: [desde la taxonomía]
status: active | draft | superseded
confidence: high | medium | low   # opcional, para claims débiles
owners: [agente-rol o persona]     # opcional
related: [otra-pagina]            # opcional, sin [[ ]]
---
```

### Frontmatter raw/ (fuentes inmutables)

```yaml
---
source_url: https://...        # si aplica
ingested: YYYY-MM-DD
sha256: <hex del cuerpo>       # detecta drift al re-ingestar
owner: persona | claude | hermes | paperclip | openrouter
---
```

## Tag Taxonomy (añadir aquí ANTES de usarlos)

- **tipo-de-activo**: empresa, proyecto, producto, videojuego
- **sistema**: paperclip, hermes, n8n, affine, rustdesk, openrouter
- **rol-agente**: c-level, developer, auditor, supervisor, task-runner
- **infra**: docker, vps, tailscale, red, almacen
- **proceso**: pipeline, cron, automatizacion, runbook
- **integracion**: github, api, webhook, cli, sync

Regla: todo tag usado en una página debe estar en esta lista. Si falta uno,
añadirlo aquí PRIMERO y luego usarlo. Evita tag sprawl.

## Estructura del Repositorio

```
cacho/
├── README.md          # PUNTO DE ENTRADA: orientación rápidapara CUALQUIER agente
├── SCHEMA.md          # reglas (este archivo)
├── index.md           # catálogo de contenido (leer para navegar)
├── log.md             # bitácora cronológica (append-only, rotar anual)
├── raw/               # capa 1: fuentes inmutables (nunca editar)
│   └── ...            #   capturas de refs, logs, exportaciones
├── entities/          # capa 2: páginas de entidades (empresas, sistemas, personas)
├── concepts/          # capa 2: conceptos / flujos / decisiones
├── comparisons/       # capa 2: análisis comparativos lado a lado
├── queries/           # capa 2: respuestas valiosas que valen la pena reutilizar
└── operations/        # capa 2: runbooks operativos (paso a paso)
```

- **raw/** es inmutable: se lee, nunca se modifica. Las correcciones van en páginas.
- Todo lo demás es el wiki vivo, mantenido por los agentes.

## Capa 1 — raw/ (fuentes)

Contenido capturado de origen: capturas de pantalla de decisiones, exportaciones,
logs, specs. Se guardan aquí tal cual, con frontmatter `raw/`.

## Capa 2 — páginas del wiki

### Entities (`entities/`) · type: entity
Una página por entidad notable: empresa, sistema, agente, persona.
Incluye: overview, datos clave, relaciones (`[[wikilinks]]`), referencias.

### Concepts (`concepts/`) · type: concept
Uno por concepto/flujo/proceso: cómo funciona algo, estado actual, decisiones.

### Comparisons (`comparisons/`) · type: comparison
Comparativa lado a lado (tablas preferidas): dimensión, veredicto, fuentes.

### Queries (`queries/`) · type: query
Respuestas sustanciales que serían dolorosas de re-derivar. No archivar trivialidades.

### Operations (`operations/`) · type: runbook
Procedimientos operativos paso a paso (cómo ejecutar cosas, cómo arreglar X).

## Umbrales de página

- **Crear página** cuando una entidad/concepto aparezca en 2+ fuentes O sea central en una.
- **Añadir a página existente** cuando una fuente solo mencione algo ya cubierto.
- **NO crear** páginas para menciones pasajeras o detalles fuera del dominio.
- **Partir** una página que exceda ~200 líneas en subtemas con cross-links.
- **Archivar** (mover a `_archive/`, fuera de `index.md`) cuando esté superada.

## Update Policy (qué pasa cuando hay conflicto)

1. Checa fechas — fuentes más nuevas superseden a las viejas.
2. Si hay contradicción real, anota **ambas** posiciones con fechas y fuentes.
3. Marca en frontmatter: `status: draft` o nota la contradicción.
4. Nunca sobrescribas en silencio: deja rastro en `log.md` y flágalo a Arturo.
5. Los agentes proponen cambios; no mutan `entities/concepts/operations` directamente.

## Escritura y control de versiones

- `main` es la fuente de verdad estable.
- Los agentes trabajan en branch → abren PR/issue → Arturo aprueba y mergea.
- Commits: mensajes claros en español o inglés técnico, formato convencional
  (`feat:`, `fix:`, `docs:`, `wiki:`). Ej: `wiki: add entity for paperclip-agent`.
- `log.md`: formato `## [YYYY-MM-DD] accion | asunto`. Rotar cuando >500 entradas.

## Comandos de orientación (para agentes Hermes)

```bash
WIKI="/root/cacho"
read_file "$WIKI/SCHEMA.md"
read_file "$WIKI/index.md"
read_file "$WIKI/README.md"
read_file "$WIKI/log.md"   # últimas 30 líneas
```
