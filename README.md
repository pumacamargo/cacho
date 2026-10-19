# Cacho — Wiki central de IA de Arturo

> **Fuente de verdad compartida** para todos los sistemas de IA de Arturo:
> Claude, todos los agentes de Hermes, y LLMs vía OpenRouter.
> Si una IA necesita contexto, lo busca aquí primero.

## Qué es esto

Un repositorio de documentación en markdown plano, interconectado, que
centraliza el contexto que antes estaba disperso en chats y docs sueltos.
Toda IA con acceso a este repo (o que le inyecten su contenido) ve la
**misma información actualizada**.

## Cómo leerlo (para cualquier IA)

1. Lee **`SCHEMA.md`** — las reglas. Obligatorio, no lo saltes.
2. Lee **`index.md`** — catálogo de todas las páginas por sección.
3. Revisa el final de **`log.md`** — actividad reciente.
4. Para tu consulta, abre la página relevante de `entities/`, `concepts/`,
   `comparisons/`, `queries/` o `operations/`.

## Estructura

- `raw/` — fuentes inmutables (logs, capturas, exportaciones)
- `entities/` — empresas, sistemas, agentes, personas
- `concepts/` — flujos, procesos, decisiones
- `comparisons/` — comparativas
- `queries/` — respuestas valiosas reutilizables
- `operations/` — runbooks operativos

## Reglas básicas (detalle en SCHEMA.md)

- Markdown plano, nombres lowercase-con-guiones.
- Toda página lleva frontmatter YAML y enlaza a ≥2 otras páginas.
- NUNCA se commitean secretos — solo referencias por nombre.
- No se crean ramas de trabajo ni PRs: todos los cambios finales van directamente a `main`.
- Antes de editar, comprobar que `main` está limpia y sincronizada; si está ocupada o sucia, parar y preservar el estado, sin crear ramas laterales. Tras revisión del mantenedor, commit y push directos a `main`.
- Actualiza `index.md` y `log.md` en cada cambio.

## Estado

Iniciado: 2026-10-10. Repositorio reutilizado de "cacho"
(asistente personal N8N de notas — contenido obsoleto eliminado).
