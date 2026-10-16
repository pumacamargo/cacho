# Wiki Log

> Registro cronológico de todas las acciones sobre el wiki. Append-only.
> Formato: `## [YYYY-MM-DD] accion | asunto`
> Acciones: create, ingest, update, query, lint, archive, delete
> Rotar a log-YYYY.md cuando supere 500 entradas.

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

## [2026-10-10] lint | Auditoría completa — todo OK
- Revisión integral: frontmatter OK, sin links rotos, sin huérfanas, todas
  indexadas, sin secretos.
- Corregido durante lint: ttchop-webapps quedó huérfana → añadidos enlaces desde
  proyecto-ttchop y ttchop-automatizaciones; 3 páginas de hardware tenían 1 solo
  enlace de salida → añadido enlace a arturo.

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

## [2026-10-15] update | Carruseles — templates y modelo nano-banana-2-lite
- Actualizada [[ttchop-webapps]] con los 3 templates `carousel_script`, los 5 estilos `carousel_style`
  y `nano-banana-2-lite`; se documentó que el precio/disponibilidad del modelo y el deploy de
  estos cambios todavía no están confirmados.
- Siembra Firestore de ttchop2 verificada de vuelta para Arturo: 5 estilos + 3 guiones seed
  (seedVersion 1); se conservaron templates ajenos al carrusel. Commits de código pusheados a
  master: webapp2 `d9b450b`, ttchop-server `32b4212`; build reportado por jr_developer como exitoso.

## [2026-10-15] update | Producer defaults + aislamiento de Vosk STT
- Documentados en [[ttchop-automatizaciones]] los defaults del Producer verificados en código:
  template `temp_y3w17i3`, voz PumaVoice01, proyecto `ttchop`, idioma `ja`/`es` y overlay/personaje desactivados por default.
- Aislado Vosk en Python 3.10 y actualizado su wrapper para no mezclar paquetes con Python 3.14;
  config de Hermes y proveedor STT alternativo quedaron intactos. Transcripción end-to-end verificada.

## [2026-10-16] update | Enrutamiento de trabajo y roster Hermes
- Alineada la documentación para delegar trabajo exclusivamente mediante los agentes Hermes: Research, Developer, jr_developer y ttchop_robot.
- Retirados procedimientos y páginas de gestión externa obsoletos; actualizado el índice, schema y contexto de ttchop.
- Actualizado el roster de [[hermes-agentes]] para incluir jr_developer.

## [2026-10-16] deploy | Template de confesión/revancha en TTChop2
- El PR #1 de `ttchop2` se integró a `master` en `6fa2ee0`; se desplegó solo Firebase Hosting del proyecto `ttchop2` (sin tocar `/root/ttchop`, reglas de Firestore ni `ttchop-server`).
- Verificación in vivo final: `https://ttchop2.web.app` respondió HTTP 200, el login se renderizó sin errores de Firebase y `index-4FlHiNuC.js` contiene el título y `seedKey` del template. Build y 5 tests de backfill pasan.
- La primera build desde un worktree limpio omitió `.env` (ignorado por Git) y causó `auth/invalid-api-key`; se corrigió con el entorno de `ttchop2`, permisos 600, rebuild y redeploy. La copia temporal de `.env` se eliminó; no se escribieron documentos manualmente a Firestore.

## [2026-10-16] fix | 403 en backfill de seed
- Confirmada la causa: el get transaccional del documento estable ausente chocaba con la regla de ownership basada en `resource.data.userId`.
- En `ttchop2` PR #2, commit `3b203e0`, la regla permite solo el get del ID de seed propio cuando falta el documento; autenticación y ownership de otros documentos se conservan. `firebase deploy --only firestore:rules --project ttchop2` compiló y publicó las reglas.
- Sin pruebas del Emulator por falta de Java en VPS; pendiente que el usuario recargue la app y abra Templates para confirmar el backfill autenticado.
