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

## [2026-10-10] update | ttchop-automatizaciones — find-bestsellers uso data esposa
- Complementado objetivo de find-bestsellers: se usa la data de la cuenta de la
  esposa (Momo's Choice) porque vende mucho y los productos ya están en casa.
  Coincide con sales_reference_data en el código (data subida de otras cuentas).

## [2026-10-10] create | ttchop webapps (ttchop2 detalle)
- Creada [[ttchop-webapps]]: relación ttchop/ttchop2 (fork, Firebase propio, server
  compartido), secciones, stack, arquitectura (contenedores, imports, databaseService),
  Firestore (colecciones) y funciones. Fuente: README.md + CLAUDE.md del repo.

## [2026-10-10] update | paperclip/ttchop — agentes en evaluación
- Quitadas menciones específicas a los agentes de Paperclip ([[paperclip]], [[ttchop]]).
  Arturo no está convencido de ellos y puede dejar de usarlos; se dejó nota de
  "en evaluación" en vez de documentar el detalle.

## [2026-10-10] lint | Auditoría completa — todo OK
- Revisión integral: frontmatter OK, sin links rotos, sin huérfanas, todas
  indexadas, sin secretos.
- Corregido durante lint: ttchop-webapps quedó huérfana → añadidos enlaces desde
  proyecto-ttchop y ttchop-automatizaciones; 3 páginas de hardware tenían 1 solo
  enlace de salida → añadido enlace a arturo.

## [2026-10-10] create | Runbook abrir task en Paperclip
- Creada [[runbook-abrir-task-paperclip]] (operations/): pasos para abrir un issue
  en Paperclip con el CLI board (agent list → issue create → verificar), con la
  convención de asignar al Developer y la regla de commit de [[ttchop]].
- Aplicado en vivo: issue TTC-52 creado y asignado a Developer (prioridad high)
  — daily-tasks solo extrae showcaseProducts al crear la task, no al actualizarla.

## [2026-10-11] update | Voz en Hermes + fixes del bot ttchop
- Documentada la config de voz de [[hermes-agent]]: STT=Vosk es vía
  `HERMES_LOCAL_STT_COMMAND`, TTS=Edge es-MX-JorgeNeural, modos `/voice`.
- Documentados fixes de [[ttchop-automatizaciones]]:
  - request-samples: robustez ADB (TTC-53) — timeout ya no tumba la fase.
  - producer: fallback de emergencia (TTC-54) — si el fallback aleatorio da
    0 candidatos por cooldown, produce igual 3 videos (source=random_emergency).
- Operación verificada en vivo: request-samples 3/3, producer 3/3 con emergencia
  (sin sesiones libres, red rescata el día).

## [2026-10-14] create/update | Agentes persistentes de Hermes + carruseles image_carousel
- Creada [[hermes-agentes]]: roster de los 3 bots persistentes de [[hermes-agent]]
  (Research → investiga, modelo gpt-6-luna; Developer → desarrolla código, gpt-6-sol;
  ttchop_robot → asiste [[ttchop]], gpt-6-luna, conectado a Telegram como @Puma_gym_bot).
  Modelos vía suscripción ChatGPT de Arturo (openai-codex). Actualizada [[hermes-agent]] con la sección.
- Actualizada [[ttchop-webapps]]: feature **image_carousel** implementada y desplegada.
  Plan TTC-55 (aprobado), implementación TTC-56 (fases 0–4, deploy en vivo), Fase 5 → TTC-57.
  Detalle: generación photo-only con kie.ai (seedream-v4 default), texto en overlay (Remotion),
  idioma es/en/ja, UI Carousels en webapp2, reglas no negociables. Smoke test real pasó (40 créd).
