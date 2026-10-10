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

## [2026-10-10] create | Categorías y proyectos
- Creada [[categorias-proyectos]] (mapa de 6 categorías).
- Creadas 6 páginas de categoría: backpack, macanishi, tts, moon, cliff, sandbox.
- Creadas 12 páginas de proyecto: japanese, drums, draw, singing, travel, farmers,
  lemon-sushi, moon-sto, moon-fut, app/game/shortfilm-development.

## [2026-10-10] create | Categorías y proyectos (taxonomía)
- Creada [[categorias-proyectos]]: mapa de las 6 categorías.
- Creadas 6 páginas de categoría: backpack, macanishi, tts, moon, cliff, sandbox.
- Creadas 13 páginas de proyecto + index reconstruido (30 páginas total).

## [2026-10-10] create | ttchop proyecto + automatizaciones
- Creada [[proyecto-ttchop]]: proyecto software (web app ttchop/ttchop2, editor
  ttchop-server/post, bot ttchop-bot).
- Creada [[ttchop-automatizaciones]]: scheduler (06/09/19/21/23:30 JST) y pipeline
  scout→producer (daily-tasks, request-samples, needs-content, find-bestsellers, producer).

## [2026-10-10] update | ttchop-automatizaciones detallada
- Expandida [[ttchop-automatizaciones]]: explicación individual de TODAS las
  automatizaciones (scout: daily-tasks, request-samples, needs-content,
  find-bestsellers, competitors; producer; intel + next-day-plan; risk anti-ban;
  delivery; adb/open/close/navigate/vision/png-crop/product-name-filter).
- Criterios reales tomados de los comentarios de cabecera de cada módulo.

## [2026-10-10] update | ttchop-automatizaciones — objetivos pipeline
- Añadida sección "Objetivos del pipeline": objetivo de negocio para cada una de
  las 5 fases (daily-tasks, request-samples, needs-content, find-bestsellers, producer).

## [2026-10-10] update | ttchop-automatizaciones — escalabilidad multi-cuenta
- Añadido requisito de diseño: los procesos deben generalizarse/escalar a varias
  cuentas; señalar hardcode de ACCOUNT en intel/index.js, y la base correcta
  (scout ya itera por cuenta activa). Consideraciones Firestore/risk/cooldowns.
