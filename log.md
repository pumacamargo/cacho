# Wiki Log

> Registro cronológico de todas las acciones sobre el wiki. Append-only.
> Formato: `## [YYYY-MM-DD] accion | asunto`
> Acciones: create, ingest, update, query, lint, archive, delete
> Rotar a log-YYYY.md cuando supere 500 entradas.

## [2026-10-10] create | Wiki inicializado
- Repositorio "cacho" reutilizado: eliminados 26 archivos del asistente personal
  N8N obsoleto (data/ gym,meditacion,nutricion,options,inversiones,excel; utils/; CLAUDE.md).
- Creados: SCHEMA.md, README.md, index.md, log.md.
- Entidades iniciales: [[cacho]], [[hermes-agent]], [[paperclip]], [[ttchop]].

## [2026-10-10] create | Entidades iniciales
- Creadas 4 páginas de entidades: [[cacho]], [[hermes-agent]], [[paperclip]], [[ttchop]].
- Estructura completa: raw/, entities/, concepts/, comparisons/, queries/, operations/, _archive/.

## [2026-10-10] create | Perfil de Arturo
- Creada entidad [[arturo]]: biografía, carrera (rigger 3D), ubicación (Osaka, Japón),
  motivos (proyectos con capital, nada de rigging) y preferencias de trabajo.
- SCHEMA: añadidos tags tipo-de-pagina, personal, negocio.

## [2026-10-10] create | Inventario de hardware
- Creada [[hardware-inventario]] con el mapa de la red Tailscale.
- Creadas páginas por dispositivo: vps-tools, vps-projects, raspberry-pi5,
  desktop-puma, celular-android.
- Verificado el inventario contra `tailscale status` (5 nodos linux/windows).
