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
- En `ttchop2` PR #2, commit `3b203e0`, la regla permite solo el get de seed propio cuando falta el documento; autenticación y ownership de otros documentos se conservan. `firebase deploy --only firestore:rules --project ttchop2` compiló y publicó las reglas.
- Sin pruebas del Emulator por falta de Java en VPS; pendiente que el usuario recargue la app y abra Templates para confirmar el backfill autenticado.

## [2026-10-16] update | flujo editorial y recreación de carrusel Reddit
- Ampliada [[ttchop-webapps]]: para este formato, primero se busca y registra internamente un post público; luego se resume y adapta como historia original de siete slides, sin presentar el post anónimo como verificado.
- Documentados la referencia de r/ProRevenge usada, los beats de la adaptación japonesa, la dirección visual, composición local 1080×1920, QA y forma de entrega. Se aclara que el modelo exacto de Kie.ai no quedó registrado y que no se publicó.
- Actualizado el índice de Cacho.

## [2026-10-16] update | descubrimiento seguro de credenciales de TTChop2
- Documentadas en [[ttchop-webapps]] las referencias `GOOGLE_APPLICATION_CREDENTIALS` (ttchop-bot) y `FIREBASE_SERVICE_ACCOUNT_PATH_TTCHOP2` (ttchop-server), verificando solo existencia y `project_id=ttchop2`; no se registran rutas resueltas ni valores secretos.
- Añadidos el flujo actual de `sales_reference_data` frente a `analytics_orders` y los límites de alcance: sesión autenticada para uso normal; acceso administrativo solo ante autorización explícita, lectura mínima y sin suplantar usuarios.
- Actualizado el índice de Cacho.

## [2026-10-17] create/update | runbook de creación de carruseles editoriales
- Creado [[ttchop-carousel-creation]] para diferenciar TTChop2 autenticado (Firestore) del flujo local Kie.ai + composición PNG (sin login de TTChop2, escrituras a Firebase ni publicación).
- Documentados el gate de créditos, Seedream v4, batch 6+1, persistencia previa de `taskId`/slots/coste para sobrevivir timeouts, composición 1080×1920 con overlay CJK y QA visual. El coste real del ejemplo del 17 de octubre no pudo recuperarse; 35 créditos es solo estimación.
- Registrada como procedencia editorial interna la historia anónima recopilada en r/BestofRedditorUpdates: post original fechado 2026-01-16 y actualización 2026-01-17; no se conservan nombres/handles ni van en el arte. Actualizados `ttchop-webapps.md` e `index.md`.

## [2026-10-17] update | Incorporación de decisión visual de carrusel
- Incorporada a [[ttchop-webapps]] la decisión aprobada originalmente el 2026-10-15: sombra negra sin recuadro, exclusiva de `image_carousel`; sigue sin persistir ni desplegarse.
- Conservado el runbook [[ttchop-carousel-creation]] y sus entradas existentes en el índice y este historial.

## [2026-10-19] update | ventas y flujos de contenido TTChop2
- Aclarado en [[ttchop-webapps]] que TTChop2 conserva filas parseadas y metadatos, no el workbook original; se distinguieron `sales_file` y `sales_reference` y se señaló que `label`/`accountId` no prueban procedencia.
- Mejorada la navegación al runbook existente [[ttchop-carousel-creation]] desde la página de webapps y el índice, sin duplicar el procedimiento.
- Creado [[ttchop-video-generation]] con prerrequisitos Producer, verificación del render persistido y separación explícita entre render y publicación; actualizado `index.md`.

## [2026-10-19] update | separación UI Create Video y Producer/collage
- Aclarado [[ttchop-video-generation]] como dos flujos distintos: UI Create Video (solo hechos verificados, sin afirmar una ubicación de almacenamiento universal) y Producer/collage manual (prerrequisitos, cooldown, aprobación de diálogo, render explícito y validación MP4).
- Separada generación/render de publicación; actualizado [[ttchop-webapps]] para enlazar la distinción.

## [2026-10-19] update | Política Git de Cacho: solo main
- Documentada la política de no crear ramas de tema ni PRs: cambios finales
  directamente a `main` tras revisión del mantenedor; comprobar `main` limpia y
  sincronizada antes de editar y detenerse preservando cualquier estado ocupado/sucio.

## [2026-10-20] update | runbook video manual de producto TTChop2
- Ampliado [[ttchop-video-generation]] para elegir entre Create Video y collage manual; resolver clips y trims en TTChop2, distinguir defaults por proyecto, aprobar guion, enviar y seguir el job, verificar todos los clips solicitados y hacer QA/entrega sin publicar.
- Actualizados resumen y fecha del runbook en `index.md`.

## [2026-10-20] create/update | generación manual de canción con ElevenLabs Music
- Creado [[ttchop-music-generation]] con el procedimiento reutilizable y guardrails; registra la prueba manual (200, audio/mpeg, variaciones verificadas) sin secretos ni assets.
- Aclarada la diferencia entre TTS y canto, y que `audioBase64` en collage no es integración Music end-to-end validada; enlazado desde [[ttchop-video-generation]] y añadido al índice (36 páginas).

## [2026-10-20] update | collage manual con canción preexistente
- Documentada en [[ttchop-video-generation]] la prueba única de `audioBase64`
  en `/collage/create`, incluida la verificación de duración con `ffprobe` y la
  regla de extender/rellenar video, nunca recortar la canción.
- Actualizada [[ttchop-music-generation]] para reemplazar la afirmación obsoleta
  de que el hook no se había probado; actualizado el resumen en `index.md`.
- El render de referencia quedó `done` y no se publicó.

## [2026-10-20] create/update | acceso remoto SSH a PumaDeskAsus
- Creado [[acceso-remoto-pumadeskasus]] con el endpoint Tailscale, autenticación
  SSH verificada, huella de host, alcance del firewall, comandos y límites de
  control remoto; no se guardaron claves ni secretos.
- Actualizados [[hardware-desktop-puma]], [[hardware-inventario]] e `index.md`
  para reflejar el nodo actual `PumaDeskAsus` y distinguir la última prueba SSH
  exitosa de la comprobación posterior que agotó el tiempo.

## [2026-10-20] update | MAC Ethernet de PumaDeskAsus
- Consultada por SSH la interfaz física: MAC Ethernet `F0:2F:74:00:8D:3B`;
  registrada en [[hardware-desktop-puma]] y [[acceso-remoto-pumadeskasus]] para
  identificar el equipo en una futura prueba Wake-on-LAN.

## [2026-10-21] update | encendido y apagado remoto de PumaDeskAsus
- Ampliado [[acceso-remoto-pumadeskasus]] con comandos Wake-on-LAN desde
  `pi5puma01` y apagado por SSH; ambos ciclos se probaron y la última
  comprobación dejó la PC fuera de línea.

## [2026-10-21] create/update | pruebas FilmCraft de videos TTChop2
- Creado [[ttchop-filmcraft-video-tests]] como runbook draft: separa Producer
  vigente (`ttchop-bot`/`ttchop-server`/FFmpeg), pruebas locales FilmCraft 0.9.0
  con clips reales ELLISS y MAGINA de `ttchop2`, y el flujo futuro aún no integrado.
  Las muestras son MP4 verticales sin audio; no se ejecutó Producer, no hubo
  escritura a Firebase ni publicación.
- Enlazado desde [[ttchop-video-generation]] y añadido a `index.md` (38 páginas).
  Evidencias de prueba en `/root/.hermes/cache/scratch/filmcraft-demo-ttchop2-20261021/`.

## [2026-10-21] update | edición solicitada directamente en wiki y código
- Actualizados `README.md`, `SCHEMA.md` y [[cacho]]: los cambios documentales
  solicitados se aplican directamente y quedan versionados en Git, sin requerir
  propuesta/revisión adicional. El código pedido también se implementa dentro del
  alcance explícito, sin confirmación redundante.
- Conservada autorización separada para escrituras/migraciones de producción,
  despliegues/reinicios, gastos/créditos y cambios de credenciales, seguridad o red.

## [2026-10-21] update | acceso a Polaris/P: por SSH con credenciales en el VPS
- Ampliado [[acceso-remoto-pumadeskasus]] con el wrapper `pumassh`, rutas y
  permisos de su archivo privado, transporte por stdin cifrado de SSH, comandos
  de uso y diagnóstico sin exponer credenciales. No se incorporó ningún secreto.
- Documentadas dos conexiones SSH nuevas con autenticación y lectura del NAS
  exitosas; diferenciados PSDrive por proceso, mapeo global y acceso nativo.
  Escritura y recuperación tras reinicio permanecen sin probar.
- Actualizados [[hardware-desktop-puma]], [[hardware-inventario]] e `index.md`
  para reflejar el acceso actual en vez del timeout anterior.

## [2026-10-21] update | flujo manual de video FilmCraft con música y narración
- Ampliados [[ttchop-filmcraft-video-tests]] y [[ttchop-video-generation]] con
  el procedimiento local de montaje, mezcla en pistas separadas, export H.264,
  QA, entrega en Polaris y límites de no integración con Producer.
- Actualizado [[acceso-remoto-pumadeskasus]]: la escritura mediante `pumassh` y
  la verificación SHA-256 de cinco archivos quedaron probadas; acceso de FilmCraft
  nativo a `P:` y reapertura interactiva del `.fcproj` siguen sin verificar.
- Actualizado `index.md`. Sin cambios en código, Firebase, publicación ni secretos.

## [2026-10-22] update | traspaso manual ttchop-server → FilmCraft
- Documentado en [[ttchop-filmcraft-video-tests]] el flujo de crear un render vía `ttchop-server`, recuperar el `editManifest` y reconstruirlo en FilmCraft; se separa explícitamente del Producer integrado.
- Añadido el caso verificado del masajeador: 10 segmentos, 492 frames, H.264 1080×1920/24 fps + AAC 48 kHz; render final verificado en Polaris y sin publicación. Se dejó constancia de cuantización de duración y de que el audio es un master mezclado, no stems separados confirmados.
- Enlazado desde [[ttchop-video-generation]] y actualizado `index.md`. No se modificaron código, Firestore ni configuración del servidor.

## [2026-10-22] update | layout predeterminado de tres pistas en FilmCraft
- Documentado en [[ttchop-filmcraft-video-tests]] el reparto cíclico V1→V2→V3 para segmentos secuenciales y la verificación de que no haya clips contiguos ni solapados en una misma pista.
- Registrada la variante verificada de 10 clips en Polaris (4/3/3), abierta en FilmCraft; conserva audio y medios. No se hizo un render nuevo ni se publicó.
- Actualizados [[ttchop-video-generation]] e `index.md` para indicar que tres pistas es el default al traducir un render a FilmCraft.

## [2026-10-26] create/update | edición manual desde audio y clips originales
- Creado [[ttchop-raw-asset-manual-edit]] con el flujo raw-assets sin catálogo/sesiones y el caso Juice Discount: inspección de NAS, metadata derivada, reglas Producer, fallback al `collage_builder.py` y mezcla de instrumental a 0,6×.
- Se documentó que `/collage/create` falló con OpenRouter 404 (`o4-mini-2025-04-16`); el builder directo produjo y entregó el MP4, pero `-shortest` acortó el último segmento visual. Se registra ese límite y se evita afirmar que todos los cortes finales cumplen el mínimo de body.
- Actualizados el enlace y fecha de [[ttchop-video-generation]] y el catálogo. El documento fallido `renders/render_manual_juice_20261026_001` permanece en `ttchop`; no hubo render exitoso en Firestore/Storage, cambios de código, deploy ni publicación. Los temporales se limpiaron; salida solo en scratch.

## [2026-10-26] update | mezcla final Juice Discount y flip bajo pedido
- Actualizada [[ttchop-raw-asset-manual-edit]] con las revisiones de música: final `volume=0.2` desde la pista original para evitar atenuación acumulativa; la voz queda sin ganancia. Se registraron streams, niveles medidos y QA de la salida final.
- El flip horizontal se aplicó porque Arturo lo pidió explícitamente y se dejó como operación opt-in, nunca default; se señala que espeja también el texto del empaque. Actualizado el resumen en `index.md`; sin cambios en código, Firebase, deploy ni publicación.

## [2026-10-26] create/update | bitácora de tres videos ELLISS Shining Shot
- Producto según el diálogo de Arturo: **ELLISS Shining Shot**. Fuentes NAS: `P:\Tiktok\hamaca\edits\03_ellisWhiteDiscount\`; `EllisWhite_corte_01.mp4`, `EllisWhite_corte_02.mp4` y `EllisWhite_corte_04.mp4`.
- Voz: `ttchop-server/pipeline/elevenlabs.js` (`textToSpeech`, PumaVoice01, `eleven_v3`); aceleración con FFmpeg `atempo=1.5` → `elliss-shining-shot-producer-voice-1.5x.mp3`.
- Videos entregados: (1) `elliss-white-discount-producer-edit.mp4`, clips 01/02/04, sin música ni flip; (2) `elliss-white-discount-02-04-hflip.mp4`, solo clips 02/04, flip pedido y sin música; (3) `elliss-white-discount-02-04-hflip-with-music-0.2x.mp4`, clips 02/04, flip y el instrumental de celebración `audio_3dae2d554059.mp3` a `volume=0.2`, manteniendo la voz.
- Montaje de los tres: `ttchop-server/scripts/collage_builder.py` con receta JSON temporal; FFmpeg para el mux/padding, `hflip` solo en versiones 2–3 y `amix` en versión 3. Sin `runProducer()`, `/collage/create`, escrituras a Firestore, cambios de código ni publicación. Inputs temporales limpiados; bitácora detallada en [[ttchop-raw-asset-manual-edit]].

## [2026-10-27] create/update | transcripción NAS del curso Gerardo Santiago
- Creado [[transcripcion-curso-gerardo-santiago]]: inventario de los ocho MP4 originales y TXT homónimos, entorno Python 3.10 aislado con faster-whisper, transferencia serial por PSDrive/FileStream, publicación, reanudación segura y límites de STT automático.
- Contrastados de nuevo en Polaris los ocho TXT: tamaño y SHA-256 coinciden con `progress.json` (8/8). El log cerró el 2026-10-26 17:59:32 +0100 con `processed=5 verified=8/8`. El noveno MP4 posterior queda fuera del manifiesto; no se transcribió ahora ni se modificaron originales o servicios.
- Enlazado el runbook de [[acceso-remoto-pumadeskasus]] y actualizado `index.md` (40 páginas). Ni medios ni transcripciones se incorporaron al repositorio.

## [2026-10-27] create/update | separación de videos NAS por cortes visuales
- Creado [[separar-videos-nas-por-cortes]] con el procedimiento ejecutado el 2026-10-26: staging por pumassh/scp, métricas scene y revisión visual, recorte por frames/timestamps, H.264/AAC y verificación de decodificación, cobertura y hashes al devolver a Polaris.
- Conservados inventario y límites históricos de cinco clips Juice, cuatro partes de 5.702 s de su clip final y cuatro clips EllisWhite. Se distingue la recodificación de una copia sin pérdidas y se documenta que cambios de tracking facial no prueban cortes editoriales; los límites históricos de Juice ligados a máscara requieren revalidación si se exigen solo cortes reales.
- Enlazado [[ttchop-raw-asset-manual-edit]] y actualizado índice. Documentación solamente: no se volvieron a procesar ni modificar videos del NAS.

## [2026-10-27] deliver | cortes de Tagilas y Shampoo en Polaris
- A petición de Arturo se localizaron y segmentaron los videos de `P:\Tiktok\hamaca\edits\04_tagilas\` y `P:\Tiktok\hamaca\edits\05_Shampoo\`, siguiendo la detección de candidatos y revisión visual de [[separar-videos-nas-por-cortes]], con acceso por [[acceso-remoto-pumadeskasus]]. No se confundieron cambios de filtro facial con cortes editoriales.
- **Tagilas:** fuente `2026-10-26-233700590.mp4`, 59 806 685 bytes, 1765 frames; dos cortes en frames 356 y 1252 (11.608893 y 41.455273 s). Entregados en esa misma carpeta `Tagilas_corte_01.mp4` (11.609 s), `Tagilas_corte_02.mp4` (29.847 s) y `Tagilas_corte_03.mp4` (17.292 s).
- **Shampoo:** fuente `2026-10-26-233822582.mp4`, 57 721 619 bytes, 1680 frames; un corte en frame 788 (26.056157 s). Entregados en esa misma carpeta `Shampoo_corte_01.mp4` (26.057 s) y `Shampoo_corte_02.mp4` (29.928 s).
- Ambos mantienen 1080×1920 y audio, recodificados H.264 CRF 18/AAC 256k. Los originales tenían timestamps irregulares con retrocesos: se distribuyeron monótonamente los frames de cada toma sobre su intervalo temporal, conservando todos los frames y el audio correspondiente; no es preservación exacta del VFR fuente. Para el intervalo final se incluyó el offset del stream y la duración del contenedor, evitando truncar la cola.
- **QA:** decodificación completa; cobertura de 1765/1765 y 1680/1680 frames; timestamps de salida crecientes; lectura de tamaño/SHA-256 en NAS coincidente con los cinco archivos locales. Los hashes fuente permanecieron iguales: Tagilas `B2A03557BAD7A7D0D29A5831A0B587D2E01287456B48F578CA2FA68F5AE65A34`; Shampoo `8C103F520DBD998A0DC0A6094BB22A6A5872EF020643F47352DCA1F2E8CF0D49`. No se alteraron originales ni se publicó contenido.
- Evidencia temporal: `/root/.hermes/cache/scratch/cuts-04-05/manifest.json` (sujeta a limpieza). La copia directa NAS→staging falló por red; se completó con FileStream por bloques de 1 MiB y reintentos, scp y verificación. La escritura final al NAS se hizo con FileStream/CreateNew sin sobrescribir destinos.
- En paralelo se encargó a `jr_developer` transcribir los nuevos videos sin TXT de `P:\Tiktok\Learning\gerardoSantiago_course\videos`, reutilizando [[transcripcion-curso-gerardo-santiago]] y preservando los ocho resultados previos. Encargo despachado; esta entrada no declara ese nuevo lote terminado.

## [2026-10-27] update | MAGINA FilmCraft: assets finales en Polaris
- Actualizado [[ttchop-filmcraft-video-tests]]: `C:\staging` queda documentado como staging temporal; el paquete portable debe incluir todos los medios bajo `P:\TikTok\Hamaca\edits\<producto>\assets`, con rutas del `.fcproj` actualizadas y verificación de rutas/hash. Se aclara que `pumassh` no valida el estado online dentro de FilmCraft; para eso hace falta reabrir en la sesión interactiva de Windows.
- Reubicados los tres `Tagilas_corte_*.mp4`, la voz `magina-tagirasa-producer-voice-1.5x.mp3`, `audio_3dae2d554059.mp3` y `magina-filmcraft-last-frame-7e2af133ba.png` a `P:\Tiktok\hamaca\edits\04_tagilas\assets`; los seis tamaños/SHA-256 se verificaron y se eliminó la copia temporal `C:\staging\filmcraft-magina-tagirasa-7e2af133ba\assets`.
- Actualizado el `.fcproj` portable para que sus seis medios apunten a `P:`: 15,112 bytes, SHA-256 `80596fef803fdb78f5d754c28b232907f484a5be242ab8ad0de81654aadbcb79`. El MP4 se mantuvo sin cambios: 29,149,165 bytes, SHA-256 `0f70656dac2fe86c8853638dd29e36fd1ed2b92da85e6d420fbb27dbeede4cbb`. Los paths y hashes se leyeron de vuelta por `pumassh`; la reapertura interactiva del `.fcproj` sigue pendiente.
- Actualizado el resumen de [[ttchop-filmcraft-video-tests]] en `index.md`; sin publicación, Firebase/Firestore ni cambios de código del pipeline.

## [2026-10-27] verify | reapertura GUI del proyecto MAGINA FilmCraft
- A petición de Arturo se activó FilmCraft en la sesión interactiva de Windows 1 y se verificó visualmente el proyecto `MAGINA-Tagiras-FilmCraft-verified`: nombre esperado en la ventana, miniaturas del media bin, preview y timeline poblado con video, voz y música. No apareció aviso de medios offline ni diálogo de error; esto cierra la verificación GUI que había quedado pendiente en la entrada anterior.
- Se capturó el escritorio a 1920×1080 y se envió por Telegram un recorte de 1540×1080 para excluir una notificación superpuesta sin retocar la imagen; SHA-256 del PNG enviado: `7faa87616fc10bafc61a3c9caea59e4b3d66a8fad906e883be8613654875bd33`. La captura está en scratch local, no en el repo.
- No se modificó ni reexportó el proyecto o sus medios; sin cambios de código, Firebase/Firestore, despliegue ni publicación.

## [2026-10-27] update | flip horizontal del video MAGINA Tagiras
- A petición de Arturo se creó una variante de la última exportación FilmCraft verificada (`magina-tagirasa-filmcraft-verified-7e2af133ba.mp4`); no se modificó el `.fcproj`. `hflip` se aplicó solo al video y el audio AAC se copió intacto.
- Salida local `magina-tagirasa-filmcraft-verified-7e2af133ba-hflip.mp4`: 15 755 225 bytes, SHA-256 `4037cd4ea7543f9bb8e95ce1fda39b7e52d9e4858e8cc1dd9989a86da44c12f4`. H.264, 1080×1920/24 fps, video 11,375 s; AAC estéreo 48 kHz, audio 11,392 s. El hash del stream de audio coincide antes/después (`53b608cd15e9f85205aa6da61518ba08d6fbbe443c7b37f684c06e6cfd9687c6`), con pico −3,7 dB.
- Decodificación completa y QA visual correctas; envases/texto legibles tras el flip. Entregado por Telegram, no publicado; sin cambios en Polaris, Firebase/Firestore, código ni despliegue.

## [2026-10-27] update | montaje Ellis if01 con tres cortes, imágenes y música
- Añadido a [[ttchop-raw-asset-manual-edit]] el procedimiento manual: voz pregunta/pausa/respuesta, video 2× y `hflip`, imágenes 540×540 en `x=48,y=120`, concatenación 01→02→03 y música `audio_3dae2d554059.mp3` a `volume=0.2` sin atenuar la voz.
- Registradas las tres variantes individuales y el composite final `ellis-if01-pointing-01-02-03-with-music-0.2.mp4` en Polaris, con tamaños, SHA-256, streams y QA (14,985 s; pico −0,9 dB; decodificación completa). Los adjuntos de imagen quedaron en caché local, no en Polaris; no se creó `.fcproj`.
- Los originales de `06_Pointing` permanecen intactos. Sin Producer, `/collage/create`, escrituras a Firestore, cambios de código ni publicación; actualizado el resumen del índice.

## [2026-10-27] update | desambiguación de proyectos FilmCraft
- Añadido a [[ttchop-filmcraft-video-tests]] un inventario explícito por caso y ruta: MAGINA Tagiras tiene un `.fcproj` propio, verificado en la interfaz; Ellis if01 tenía MP4 final pero aún no `.fcproj`, y el solicitado debía separar videos, voces, música e imágenes.
- Documentado el flujo local-first autorizado: trabajar/guardar en `C:\staging` si Polaris no está disponible, marcar NAS pendiente, conservar los medios hasta verificar la copia y relink. Aclarado que FileStream solo aplica después de preparar `P:`; añadido el último error observado de `pumassh` sin atribuirlo a RAM física.
- Aclarado en [[ttchop-raw-asset-manual-edit]] que el proyecto MAGINA de `04_tagilas` no es el de Ellis if01 de `07_ellis_if01`; las imágenes fuente de Ellis siguen en caché local. Se actualizó el resumen del índice para advertir que no se mezclen proyectos entre productos.
- Documentación solamente: sin cambios a FilmCraft, medios, NAS, código, Firestore, despliegue ni publicación.

## [2026-10-27] update | ruta local de staging FilmCraft
- A petición de Arturo, se fija `D:\staging` como raíz preferida para staging local en nuevos trabajos FilmCraft y se actualizan las recetas de `[[ttchop-filmcraft-video-tests]]`, `[[ttchop-video-generation]]`, `[[acceso-remoto-pumadeskasus]]` y `[[separar-videos-nas-por-cortes]]`.
- Se conservan en log y casos verificados las rutas `C:\staging` realmente usadas en trabajos anteriores; no se reescribió el historial operativo.
- Documentación solamente; no se creó la carpeta ni se modificaron medios, FilmCraft o Polaris.

## [2026-10-27] create/verify | proyecto FilmCraft Ellis if01 local
- Creado `D:\staging\filmcraft-ellis-if01-20261027\Ellis-IF01-Layered.fcproj` en FilmCraft CLI 0.9.0: V1 con tres videos, V2 con tres overlays, A1 con preguntas/respuestas separadas y A2 con música a volumen 0,2 (−13,9794 dB). Los 14 medios de `assets/` se verificaron por hash.
- Export `Ellis-IF01-Layered-preview.mp4`: H.264 1080×1920/30 fps, 449 frames; AAC estéreo 48 kHz. `offlineMedia:[]`, decodificación correcta, pico −0,7 dB sin clipping y QA visual de los tres overlays. Hashes: `.fcproj` `90369D3F98F03758A72E8BFC54AA224228DAB2E68941924CDAEA75DE8E86B6B9`; preview `988b1329685f8725bf1bc2581b207fd1f4735e8c151e194e16bfc023f8bad502`.
- Local-only y no publicado. No se transfirió a Polaris: la lectura del destino Ellis falló con `pumassh: Not enough memory resources are available to process this command`. Relink y apertura en la GUI interactiva quedan pendientes; conservar `D:\staging` hasta verificar la copia NAS.
- Actualizados el estado de [[ttchop-filmcraft-video-tests]], [[ttchop-raw-asset-manual-edit]] y el resumen de `index.md`; sin cambios a Producer, Firestore, código ni servicios.

## [2026-10-28] create/update | priorizar SMB directo VPS a Polaris sin borrar alternativas
- A petición de Arturo se añadió [[acceso-nas-polaris]] con el orden: 1) SMB directo desde vps-tools por Tailscale con las mismas credenciales protegidas; 2) Windows por SSH e IP/FQDN cuando haga falta; 3) wrapper histórico por nombre corto Polaris, conservado para compatibilidad/diagnóstico y actualmente fallido.
- Prueba real directa con `smbprotocol`/`smbclient` en venv Python 3.10 aislado de scratch, cifrado SMB requerido: autenticación/listado correctos y lectura de `01TiktokShop.md` (21277 bytes), SHA-256 `f7b2908fdbd602633d329999027620b9570f6eb09936e89c120f8fe5d4738f47`. No se probó escritura ni se instaló herramienta global o montaje persistente; no necesita la PC encendida para acceder a archivos del share.
- Conservado el diagnóstico de Developer: fallo nativo Windows 8 en `New-PSDrive` por nombre corto; IP Tailscale, LAN y FQDN leyeron correctamente. Causa raíz no confirmada; no atribuirlo a DNS o RAM física ni afirmar que se reparó `P:`.
- Actualizados enlaces/prioridades en [[acceso-remoto-pumadeskasus]], [[hardware-desktop-puma]], [[transcripcion-curso-gerardo-santiago]], [[separar-videos-nas-por-cortes]], [[ttchop-raw-asset-manual-edit]], [[ttchop-filmcraft-video-tests]], [[ttchop-video-generation]] e índice (42 páginas). Se conservan los comandos, casos y estados anteriores; los pipelines no se migraron automáticamente y ningún entregable pendiente se declara copiado.
- Documentación solamente: sin modificar credenciales, mappings, servicios, medios o reportes del NAS. No se copió ningún secreto al repositorio.

## [2026-10-28] verify | entrega FilmCraft Ellis if01 en Polaris
- Verificado el paquete `P:\Tiktok\hamaca\edits\07_ellis_if01\filmcraft-ellis-if01-20261027\`: `.fcproj` `Ellis-IF01-Layered.fcproj` SHA-256 `41fb0eb7386e3aa8c520385d826bc9e63aee3c82381d7e6d6a8eb8538f31713a`; preview `Ellis-IF01-Layered-preview.mp4` SHA-256 `988b1329685f8725bf1bc2581b207fd1f4735e8c151e194e16bfc023f8bad502`; manifest y 14 medios presentes, cada tamaño/SHA-256 coincide.
- El proyecto portable contiene 14 referencias `P:\Tiktok\hamaca\edits\07_ellis_if01\assets\` y cero rutas `D:\staging`. El staging continúa disponible con el `.fcproj` original (SHA-256 `90369d3f98f03758a72e8bfc54aa224228dab2e68941924cdaea75de8e86b6b9`), la variante portable, el preview y 14 medios.
- La transferencia se hizo por la ruta Windows/SSH temporal con IP Tailscale documentada en [[acceso-nas-polaris]], reutilizando el wrapper seguro; no cambió credenciales ni reparó el mapeo histórico por nombre corto. Esto verifica este paquete, no escritura SMB directa.
- La reapertura del proyecto final en FilmCraft GUI sigue pendiente; `offlineMedia:[]` corresponde al export/inspección CLI local y no sustituye esa comprobación. No publicado ni cambios a código, Producer o Firestore.
- Actualizados [[ttchop-filmcraft-video-tests]], [[ttchop-raw-asset-manual-edit]], [[acceso-nas-polaris]] e índice para reflejar el estado actual y separar el resultado de CLI de la validación GUI.

## [2026-10-28] update | recorte y nuevo montaje Ellis if01
- A petición de Arturo se retiró 1 s de movimiento (30 frames) al final de cada corte Ellis if01 01–03, congelando el último cuadro y conservando el audio completo. Los tres archivos individuales nuevos y sus hashes/tamaños quedan registrados en [[ttchop-raw-asset-manual-edit]]; quedaron en scratch local y no se copiaron a Polaris (la lectura de retorno confirmó que esos nombres no estaban allí).
- Se re-unieron los cortes nuevos en orden 01→02→03 con el instrumental aprobado continuo a volumen 0,2. Nuevo archivo en `P:\Tiktok\hamaca\edits\07_ellis_if01\ellis-if01-pointing-01-02-03-minus-1s-motion-with-music-0.2.mp4`, 12 340 702 bytes, SHA-256 `b1293e9ca54cf1d8398af8b208447e7eb7837b1b066f14b76062d485cb338f45`; se verificó lectura de retorno exacta en Polaris. El montaje previo con otro nombre se conservó.
- QA: H.264 1080×1920/30 fps, 449 frames; AAC estéreo 44,1 kHz; streams difieren menos de un frame; decodificación completa, orden/cortes/overlays/cuadros finales y música en pausas revisados; pico −1,1 dB, sin clipping. El proyecto FilmCraft no se modificó y su reapertura GUI sigue pendiente; el nuevo MP4 es un render aplanado, no un proyecto editable. No publicado; sin Producer, Firestore ni cambios de código.
- Actualizados [[ttchop-raw-asset-manual-edit]] e índice. De las salidas de esta actualización, los tres cortes individuales recortados siguen en scratch local; solo el montaje concatenado nuevo se verificó en Polaris.

## [2026-10-28] preference | recorte solo por solicitud explícita
- Arturo indicó que quitar el último segundo de movimiento debe ocurrir solo cuando él lo pida expresamente. No asumir por defecto duración ni ubicación del recorte; si pide recortar sin especificarlos, preguntar antes de editar.
- Actualizados [[ttchop-raw-asset-manual-edit]], su resumen en índice y la skill local `ttchop-content-ops` para aplicar esa preferencia. No se modificó ningún video ni se publicó nada por esta actualización.

## [2026-10-28] update | Ellis hair: parámetros y clips 01–02
- Documentados en [[ttchop-raw-asset-manual-edit]] los parámetros que faltaban del nuevo test: video 2×, voz por locución a 1,5×, pausa fija de 0,3 s, `hflip` del video antes del overlay sin espejar la imagen y recorte explícito de 1 s/30 frames de movimiento. Sin música ni publicación; originales de `06_Pointing` intactos.
- Clip 01 final: `pointing-hair-frizz-01-hflip-minus-1s-motion-voice-1.5x.mp4`, 3 298 106 bytes, SHA-256 `37bd72cd15a826104ca205be386787fb7fee8f5b3369fc738290a5a4505843d3`; H.264 1080×1920/30 fps, AAC mono 44,1 kHz; voz completa y QA correcto.
- Clip 02: `pointing-hair-silky-02-hflip-minus-1s-motion-voice-1.5x.mp4`, 4 087 716 bytes, SHA-256 `ebeeb113091b75309d1957f57f7df019d054d98f62398aafa84af3bf58ff49eb`; 3,5 s, H.264 1080×1920/30 fps + AAC mono 44,1 kHz. Tras la voz (3,136122 s) se añadió 0,363878 s de silencio, dentro del umbral de cola breve; pico −0,9 dB, decodificación/contact sheet correctos.
- Clip 03 no se exportó: a 2× y tras quitar 30 frames queda 5,233333 s de movimiento frente a 3,070385 s de voz, diferencia 2,162948 s. Queda pendiente la decisión de Arturo sobre conservar la cola silenciosa o retirar movimiento adicional. Clips 01–02 permanecen en scratch local, no Polaris; no se actualizaron servicios ni se publicó.
- Actualizados `index.md` y [[ttchop-raw-asset-manual-edit]].

## [2026-10-28] deliver | Ellis hair clip 03 con cola silenciosa aprobada
- Arturo eligió conservar el recorte de 1 s solicitado y dejar que el video 03 continúe en movimiento sin voz durante 2,162948 s; no se hizo recorte adicional.
- Render `pointing-hair-dry-ends-03-hflip-minus-1s-motion-voice-1.5x-silence-tail.mp4`: 6 089 148 bytes, SHA-256 `02fd6a6db962edc03d3bc37c0b7a3e675fcd2dc88ae634ca9aff44ab41c6f8a0`; H.264 1080×1920/30 fps, 157 frames/5,233333 s, AAC mono 44,1 kHz/5,233333 s. La voz 1,5× con pausa fija de 0,3 s dura 3,070385 s y la cola final silenciosa 2,162948 s. Pico −0,9 dB; cola, decodificación y revisión visual correctas.
- Actualizados [[ttchop-raw-asset-manual-edit]] e `index.md`. Los tres videos siguen en scratch local; no se copiaron a Polaris ni se publicaron; sin escrituras a Firestore o cambios de código.

## [2026-10-28] deliver | Ellis hair 01–03 con música continua
- A petición de Arturo se concatenaron los tres clips nuevos en orden 01→02→03, con cortes directos y sin reiniciar la música. Se reutilizó el instrumental previamente aprobado `audio_3dae2d554059.mp3` (30,024 s, estéreo 48 kHz, SHA-256 `c8f235579823e11227250bfb7512f2db982dfc3fdae19dc27cf07eef6932ab85`) a ganancia lineal 0,2; la voz no se atenuó ni normalizó. Solo se añadió 0,008866 s de silencio tras el audio completo del clip 01 para alinear la duración visual.
- Montaje `ellis-hair-pointing-01-02-03-with-music-0.2-20261028.mp4`: 9 589 479 bytes; SHA-256 `8a347e9b290db0429a2392434979232e2b3754f12152f51e750d5a660a5e469b`. H.264 1080×1920/30 fps, 359 frames/11,966667 s; AAC estéreo 44,1 kHz/11,966667 s. QA: full decode y contact sheet correctos, cortes/overlays limpios, música continua también bajo las colas silenciosas; pico PCM −0,66 dBFS, cero muestras saturadas.
- Copiado a `P:\Tiktok\hamaca\edits\07_ellis_if01\ellis-hair-pointing-01-02-03-with-music-0.2-20261028.mp4`; tamaño y SHA-256 leídos de vuelta y coincidentes. El staging temporal se eliminó después de la verificación; el render aplanado local permanece. No se publicó ni se modificó FilmCraft, Producer, Firestore o código.
- Actualizados [[ttchop-raw-asset-manual-edit]] e `index.md`.

## [2026-10-28] deliver/update | Ellis IF01 — primer hook de belleza interior
- A petición de Arturo se preparó y entregó solo el clip 01 del nuevo guion: `[curious] 内側からキレイになりたい？` → `[excited] オレンジのカートをチェック！`. Se reutilizó el video 01 de `06_Pointing` con los ajustes aprobados del lote anterior: 2×, `hflip` antes del overlay, recorte de 1 s de movimiento, overlay 540×540 en `x=48,y=120`, voz 1,5×, pausa 0,3 s y sin música/audio de cámara. El original se conservó.
- MP4 `pointing-inner-beauty-01-hflip-minus-1s-motion-voice-1.5x.mp4`: 3 303 002 bytes, SHA-256 `f12252f30fbf8d52a627a883519563c61e7b2a7aebc2198e0fb541c3ca0e03b1`; H.264 1080×1920/30 fps, 97 frames/3,233333 s; AAC mono/44,1 kHz. Voz 3,181270 s; silencio final 0,052063 s. Pico −0,90 dBFS, cero muestras saturadas, frames iguales a la versión visual aprobada y full decode/contact sheet correctos.
- Copiado a `P:\Tiktok\hamaca\edits\07_ellis_if01\pointing-inner-beauty-01-hflip-minus-1s-motion-voice-1.5x.mp4`; escritura y lectura de vuelta por SMB directo verificadas con tamaño/hash coincidentes. La evidencia puntual actualiza [[acceso-nas-polaris]]; no implica prueba de rendimiento con archivos grandes. No se publicó ni se creó proyecto editable.

## [2026-10-28] deliver/update | Ellis IF01 — imágenes nuevas y clip 01 corregido
- Arturo proporcionó tres prompts para overlays cuadrados: mujer en cocina con agua, retrato curioso sobre ingrediente de belleza y uvas Shine Muscat con mujer en fondo. Kie.ai Seedream v4, `square_hd`/1K, 3 tareas; gasto real verificado: 5 créditos por imagen, 15 total. Se inspeccionaron sin texto/logos/packaging/collage.
- PNGs 540×540 entregados individualmente: `ellis-if01-inner-beauty-01-540x540.png` (604 732 B, SHA `eaee1ded1c2a2aa23c97651a68d9f86cdcb604762040ab5233cc29dedd4ad14f`); `ellis-if01-l-cystine-02-540x540.png` (714 116 B, SHA `b0653455ca793a7abd8ee2325ea74b1615259d6baf12f7026e7bce947bd4a957`); `ellis-if01-muscat-03-540x540.png` (662 274 B, SHA `c8d24573269b924033a3077e303e2ec91111a379ea975fcea414ea396b01eb1e`).
- Se actualizó solo el clip 01 con el overlay 01 nuevo (540×540, `x=48,y=120`, sin espejo), manteniendo los ajustes y el audio ya aprobados. MP4: `pointing-inner-beauty-01-hflip-minus-1s-motion-voice-1.5x-new-square-image-corrected.mp4`, 3 440 492 B, SHA `769243dd46cd0a346a52f617978490a6282c8d07fba59d8738ff9d9f1a1f6958`; H.264 1080×1920/30 fps, 97 frames/3,233333 s; AAC mono/44,1 kHz/3,232993 s. Hash de audio AAC idéntico a la primera versión (`db765645d3f170ec792767df32af7199783448896c70cbe9698fd74ae7cf9439`); full decode y contacto visual correctos, pico −0,90 dBFS, cero clipping.
- Tres PNGs y MP4 actual copiados a `P:\Tiktok\hamaca\edits\07_ellis_if01\`; SMB leyó de vuelta todos los destinos con tamaño/SHA coincidentes. La versión previa permanece como histórica; no se publicó ni se creó proyecto FilmCraft.

## [2026-10-28] deliver/preflight | Ellis IF01 — clip 02 listo; cola del 03
- Se actualizó y entregó clip 02 con la imagen correspondiente de L-シスチン. MP4 `pointing-l-cystine-02-hflip-minus-1s-motion-voice-1.5x-with-image.mp4`: 3 801 605 B, SHA `b6aadc2ad5709f6f903485d1f52de1027bc667fdc65e4e4a46e31ad93f0dbe1b`; H.264 1080×1920/30 fps, 105 frames/3,5 s; AAC mono/44,1 kHz. Audio packet hash sin cambios (`ca569f1748151d9f6ad7ffb81e164a36b14d905b5b01d732708432ec5f860b17`), pico −0,9 dBFS, full decode y contacto visual correctos.
- Copia Polaris `P:\Tiktok\hamaca\edits\07_ellis_if01\pointing-l-cystine-02-hflip-minus-1s-motion-voice-1.5x-with-image.mp4` con lectura/hash de vuelta verificados.
- El preflight del clip 03 detecta unos 2,54 s de silencio al final de la voz mientras continúa el video. La imagen 03 existe, pero el video nuevo no se renderizó ni entregó; queda pendiente la decisión de conservar esa cola o recortar el movimiento. No publicado.

## [2026-10-28] deliver | Ellis IF01 — clip 03 con overlay Shine Muscat
- Arturo indicó aplicar el mismo tratamiento de los videos recientes; se conservó la cola de movimiento y silencio (~2,54 s). MP4 `pointing-muscat-03-hflip-minus-1s-motion-voice-1.5x-silence-tail-with-image.mp4`: 5 586 550 B, SHA `98fbd43d800ddbf0599baec8c3f7f083103626276d6fcc63f6bf95dc2e835d62`; H.264 1080×1920/30 fps, 157 frames/5,233333 s; AAC mono/44,1 kHz/5,232993 s.
- Audio aprobado remuxeado sin recodificar; hash de paquetes idéntico (`f36a7b32632a3ce80166b0a3ebbd72c4a1175b6ff242d1810db1c7174097db36`), pico −0,9 dBFS, cero clipping y full decode correcto. Contact sheet visual QA correcto.
- Polaris `P:\Tiktok\hamaca\edits\07_ellis_if01\pointing-muscat-03-hflip-minus-1s-motion-voice-1.5x-silence-tail-with-image.mp4`; lectura/hash de vuelta verificados. No publicado.

## [2026-10-28] deliver | Ellis IF01 — montaje belleza interior con música
- Se unieron los tres MP4s finales en orden 01→02→03 con una pista continua del instrumental aprobado. `audio_3dae2d554059.mp3` (30,024 s, estéreo 48 kHz; SHA `c8f235579823e11227250bfb7512f2db982dfc3fdae19dc27cf07eef6932ab85`) coincide byte por byte con `ellis-if01-music-approved.mp3`; música a volumen lineal 0,2, limitada al montaje, sin loop. No se aplicó ganancia a las voces.
- Salida `ellis-if01-inner-beauty-l-cystine-muscat-01-02-03-with-music-0.2-20261028.mp4`: 11 859 136 B, SHA `6738e829df71577bbdf9b1950849fd9042a2d221c3006b209906d3ee46d5c7f0`; H.264 1080×1920/30 fps, 359 frames/11,966667 s; AAC estéreo 44,1 kHz/11,966009 s. Full decode y contact sheet correctos; mezcla media −17,6 dB, pico −0,4 dBFS y sin clipping; la música continúa durante la cola de voz silenciosa del clip 03.
- Polaris `P:\Tiktok\hamaca\edits\07_ellis_if01\ellis-if01-inner-beauty-l-cystine-muscat-01-02-03-with-music-0.2-20261028.mp4`; tamaño/hash de vuelta verificados. MP4 aplanado, sin proyecto FilmCraft actualizado ni publicación.

## [2026-10-29] create/update | traducción japonesa con PumaVoice y voz alineada al original
- A petición de Arturo se documentó en [[traduccion-video-pumasvoice-sincronizada]] la prueba del 2026-10-28: transcripción local del clip de ~9,176 s, traducción propia, una generación TTS `eleven_v3` con PumaVoice01 y sustitución de audio sin recodificar imagen.
- Después de la entrega inicial, Arturo pidió igualar inicio/fin de habla: se midieron silencios, se recortó solo entrada/silencio sobrante, se ajustó `atempo=1.0048475497832565`, se añadió delay por muestras y silencio final; no hubo nueva generación pagada. Voz ES detectada 1.58048–7.28501 s; JA final 1.58447–7.34109 s (~4 ms y ~56 ms de diferencia). Arturo aprobó el resultado. Es alineación del intervalo de habla, no labios por fonema.
- Salida aprobada `video_ja_sincronizado.mp4`: 4 977 530 bytes, SHA-256 `a780fda4eefdcd0661ad13f0fc28c58399c83543fc8d500f06081fbc21278ebf`, H.264 720×1280/AAC japonés; full decode correcto y bitstream de imagen igual al original. Entregada por Telegram; no publicada ni copiada al NAS en esta tarea.
- Consumo TTS confirmado por header/historial: 14 créditos incluidos; sin overage reportado. La prueba Dubbing anterior registró aumento de cuenta de 1682 créditos: comparación puntual, no precio universal. Se guardaron receta, parámetros finales, límites y verificación; scratch/evidencias no se incorporaron al repo.
- Actualizado [[ttchop-video-generation]] e índice (43 páginas). Documentación solamente: sin gasto adicional, cambios de servicios, credenciales o código de producción.

## [2026-10-30] create/update | FTPS Lemon Sushi, raíz organizada y URL pública
- A petición de Arturo se creó [[acceso-ftps-lemon-sushi]] con el endpoint probado `server310.web-hosting.com:21`, FTPS explícito con TLS/certificado y conexión de datos cifrada, autenticación y listado verificados. El alias `ftp.lemonsushi.com` falla la coincidencia de certificado; no se desactiva su validación.
- Guardada en `/root/.config/ftp/config.json` la equivalencia `/public_html/uploads/vps2/` → `https://lemonsushi.com/uploads/vps2/`, condicionada a que `public_html` sea el document root del dominio; comprobación HTTP pendiente. Se conservaron las reglas de subcarpetas por proyecto/tarea, sin archivos sueltos en la raíz ni escrituras fuera de ella.
- Documentadas la ubicación protegida de credenciales y la advertencia de accesibilidad pública: no subir secretos ni información privada. El repositorio no contiene la contraseña ni el archivo de credenciales. Actualizado el índice (44 páginas).
- Esta actualización solo modifica configuración local y documentación; sin subidas FTP, cambios de hosting, despliegues ni pruebas de escritura remota.

## [2026-10-31] create | diagnóstico de espacio en disco en vps-tools
- Arturo recibió una alerta de poco espacio y pidió un reporte de qué lo consumía; se creó [[diagnostico-espacio-disco-vps]] a partir de una auditoría de **solo lectura** del disco de [[hardware-vps-tools]].
- Estado real: `/dev/sda3` 96 GB, 87 GB usados, **4.4 GB libres (96 %)**. Se descartó la hipótesis de copias de video del NAS: todo el material audiovisual del VPS suma menos de 1 GB (del curso solo 49 MB de staging y ~1.5 GB de entornos/modelos de transcripción en el scratch de `jr_developer`).
- Causas medidas: Docker ~48 GB (capas 49 GB con 11.6 GB recuperables y 13 imágenes huérfanas, build cache 5.9 GB, volúmenes 7.5 GB con Paperclip 3.6 GB, logs de contenedores 4.0 GB, imagen Paperclip 5.1 GB), `/root/.npm` 11 GB, respaldo n8n de mayo 2025 2.0 GB, `.codex` 1.6 GB, `/var/cache/apt` 1.9 GB.
- Hallazgo de causa raíz: ningún contenedor tiene rotación de logs salvo `affine_app`; `postiz-postgres` acumuló 3.1 GB de log desde el 18 de octubre, así que hay que revisar por qué registra errores, no solo truncar.
- **Sin limpieza ejecutada**: 35–45 GB liberables quedaron como propuesta; las acciones sobre Paperclip y el respaldo de n8n requieren autorización explícita aparte. Evidencia cruda en scratch, no incorporada al repositorio.
- Actualizado [[index.md|índice]] (45 páginas). Documentación solamente: sin borrados, cambios de servicios, reinicios ni despliegues.

## [2026-10-31] update | limpieza de disco autorizada en vps-tools (~29.6 GB liberados)
- Arturo autorizó las acciones seguras del diagnóstico [[diagnostico-espacio-disco-vps]] y se ejecutaron: caché de npm (11 GB → 1.5 GB), imágenes huérfanas de Docker (33 → 20 imágenes, 0 colgantes), caché de compilación (5.9 GB → 0), truncado de logs de contenedores (4.0 GB → 864 KB) y `apt-get clean` (1.9 GB → 48 KB).
- Resultado medido: `/dev/sda3` pasó de **87 GB usados / 4.4 GB libres (96 %)** a **58 GB usados / 34 GB libres (64 %)**. Verificación posterior: n8n y Affine responden HTTP 200; los 10 contenedores activos siguen en pie; ninguna imagen en uso se eliminó.
- Se mantienen **sin ejecutar y pendientes de autorización aparte** (~14 GB): Paperclip completo, respaldo de n8n de mayo 2025, Tradenote, releases viejas de Codex, modelos de transcripción duplicados y la caché `_npx` restante.
- Sigue pendiente de decisión la rotación de logs en `/etc/docker/daemon.json` (requiere reiniciar Docker) y revisar por qué `postiz` lleva desde julio en espera del puerto 4200. Documentación operativa: sin cambios de credenciales, red, despliegues ni datos de producción.

## [2026-10-31] update | segunda limpieza de disco autorizada en vps-tools (~14 GB más; 43 GB totales)
- Arturo autorizó el resto de las acciones del diagnóstico [[diagnostico-espacio-disco-vps]]: Paperclip (compose `down`, imagen 5.1 GB, volúmenes `paperclip_paperclip-data`/`paperclip_pgdata`/`paperclip_tailscale-state` y red), respaldo de n8n de mayo 2025 (2.2 GB, no montado por ningún contenedor), Tradenote (2 contenedores detenidos 3 meses + 2 volúmenes), releases de Codex 0.163.0 y 0.165.0 (conservando 0.166.0 en uso), dos copias duplicadas del modelo de transcripción en `jr_developer` (se preservó `models/`) y caché `_npx`.
- Estado final: **44 GB usados / 48 GB libres (48 %)** frente a 87 GB / 4.4 GB (96 %) al inicio → **43 GB liberados** en la sesión. Verificado después: n8n y Affine responden HTTP 200, el daemon de Codex 0.166.0 sigue activo y los 8 contenedores restantes no se detuvieron (13 → 8 por los proyectos eliminados).
- Quedan ~7.4 GB de imágenes Docker sin uso (Tradenote, `mongo:6`, `mysql:8`, `php:8.2-cli`, `n8nio/n8n:latest-debian`, `n8n-custom:latest`) que no se borraron por implicar re-descarga; se liberan con `docker image prune -a` si Arturo lo pide.
- Pendiente de decisión, sin ejecutar: rotación de logs en `/etc/docker/daemon.json` (requiere reiniciar Docker) e investigar por qué `postiz` no responde (sigue en espera del puerto 4200 desde julio). Sin cambios de credenciales, red, despliegues ni datos de producción.

## [2026-10-31] update | tercera limpieza de disco en vps-tools (~14 GB más; 57 GB totales)
- Arturo autorizó las dos acciones restantes del diagnóstico [[diagnostico-espacio-disco-vps]]. `docker image prune -af` liberó **10.64 GB** de imágenes sin uso; `n8n-custom:latest` no se tocó por estar en uso.
- **Postiz**: se comprobó que la app llevaba atascada desde julio (esperando el puerto 4200, sin responder en `localhost:5000`) y se apagó el proyecto con `docker compose down`: 3 contenedores y la red eliminados. Los volúmenes de datos (`postiz_postiz-config`, `postiz_postiz-uploads`, `postiz_postiz-postgres-data`, ~540 MB) **se conservaron** por contener material de Arturo; borrarlos requiere confirmación aparte.
- Estado final del disco: **30 GB usados / 62 GB libres (32 %)**, frente a 87 GB / 4.4 GB (96 %) al inicio → **57 GB liberados** en la sesión. Verificado: n8n y Affine responden HTTP 200, el daemon de Codex 0.166.0 sigue activo y quedan 5 contenedores (Affine 3 + n8n 2) todos en marcha.
- Pendiente de decisión, sin ejecutar: borrar los volúmenes de Postiz y quitar/comentar el bloque `postiz.lemonsushi.com` del Caddyfile de `n8n-server` (hoy apunta a un backend inexistente). Sin cambios de credenciales, red, despliegues ni datos de producción.

## [2026-10-31] update | cierre de pendientes del diagnóstico de disco: Caddyfile y rotación de logs
- Tras la limpieza de [[diagnostico-espacio-disco-vps]] (30 GB usados / 62 GB libres, 57 GB liberados), Arturo aceptó la recomendación de no borrar más y cerrar los dos pendientes de fondo.
- **Caddyfile de `n8n-server`:** retirados los bloques `postiz`, `tradenote` y `paperclip` (`lemonsushi.com`), todos apuntando a servicios ya eliminados. Backup `Caddyfile.bak3-20261031`, `caddy validate` correcto y `caddy reload` en caliente. Verificado: `notes` 200, `flows` 200, `hermes` 302; `postiz` deja de responder. `rd.lemonsushi.com` sigue en 502 por el RustDesk eliminado y se dejó intacto.
- **Rotación de logs de Docker:** `/etc/docker/daemon.json` con `json-file`/`max-size 10m`/`max-file 3` (DNS conservado, backup en scratch). Reinicio de Docker y recreación de los contenedores de `n8n-server` y `affine` para heredar la configuración. Verificado: n8n 200, Affine 200, sitios de Caddy OK, 4 workflows de n8n reactivados y `max-size:10m max-file:3` en los 5 contenedores; logs totales en 140 KB.
- Sin cambios de credenciales ni datos de producción. Queda pendiente de decisión borrar los ~540 MB de volúmenes de Postiz.

## [2026-10-31] create | inventario del estudio de creadores (videos, transcripciones y reportes)
- Arturo pidió dejar en el repo de Cacho la información del material que sustenta la guía de los dos creadores, para poder revisar la data ante cualquier duda. Se creó [[estudio-creadores-fuentes-datos]].
- Registrado: 43 videos fuente (20 Asu + 23 Sora) y 43 transcripciones TXT en japonés en `Projects\Tiktok\hamaca\creators_research\<creador>\{videos,transcripts}`; los análisis largos de guion y las auditorías audiovisuales en el mismo NAS (50 KB y 75 KB los `.md`; 9.4 MB y 10.2 MB los HTML); y los **13 enlaces públicos verificados con HTTP 200** (guías de estructura, auditorías y versiones del estudio).
- Documentado el historial de versiones, incluida la **activa `study-standard-63f35614c4fc`** (SHA-256 `63f35614c4fc…`, 16 306 232 B: 5 secciones estandarizadas, todo desplegado por defecto, sin Hybrid) y la retirada `study-sources-d3e378514b07`, de la que Arturo pidió quitar el bloque de fuentes que se había añadido en el pie de la guía.
- Registrado también dónde viven las mediciones: 43 objetivos automáticos y las 6 revisiones visuales (3 por creador) en `creator-av-audit`, y el proyecto de construcción `creator-standardize`. Límite vigente: interpretación visual con IA sólo en 3 videos por creador.
- Actualizado [[index.md|índice]] (46 páginas). Documentación solamente: sin cambios de código, publicación, credenciales ni datos de producción.

## [2026-10-31] update | limpieza del hosting: solo la última versión del estudio de creadores
- Arturo pidió limpiar las versiones viejas del creator research **en el FTP**. Se borraron **16 carpetas** de `/public_html/uploads/vps2/creators-research/` (~146 MB): `study` (primera), `study-97a276b8cae6`, `study-stitch-01aad09306bf`, `study-complete-f49ae44b9303`, `study-evidence-2f685f21a16b`, `asu-script-pilot-93c58ce1deec`, `study-script-layout-1eb2e94a3542`, `study-script-three-82ca7d46c1b1`, `study-script-language-c9ed0947f474`, `study-av-collapse-b58470cb13b0`, `study-sources-d3e378514b07`, las dos `study-production-preview-*`, las dos `study-recording-editing-*` y `study-standard-4ab186c1e022`.
- Conservadas: la versión activa `study-standard-63f35614c4fc` (SHA-256 `63f35614c4fc…`, 16 306 232 B) y los dos reportes por creador (`asu_kurashi`, `sora_no_kurashi3`: guía de estructura + auditoría audiovisual, 47 494 / 9 408 129 / 42 268 / 10 192 783 B), verificados por lectura exacta **antes y después** del borrado.
- Comprobación: listado FTP final con solo esas tres carpetas, hash correcto de la guía activa y los 4 archivos de reportes, y las 16 URLs antiguas ya sin responder.
- Aprendido y documentado: el hosting **devuelve 404 intermitentes en archivos que sí existen**; la prueba de existencia o borrado debe hacerse por lectura y listado FTP. Además, tras `RMD` la sesión FTP queda dentro de la carpeta eliminada y el siguiente `MLSD` falla con `421` hasta volver a la raíz.
- Actualizado [[estudio-creadores-fuentes-datos]] (tabla de versiones con estado y sección de limpieza). Documentación y hosting solamente: sin cambios en el NAS, el VPS ni el código de la guía.

## [2026-10-31] update | curso Gerardo Santiago: confirmado transcrito al 100% (20 de 20)
- Arturo preguntó si ya estaban todos los videos del curso transcritos. Verificación por SMB directo al NAS: **20 MP4 en `videos\` y 20 TXT en `transcripts\`**, emparejados uno a uno por nombre base, sin faltantes ni sobrantes y sin procesos activos.
- Los 20 TXT se releyeron y hashearon: **los 20 coinciden** con el hash registrado en la corrida que los produjo (16 en `progress.json` de los lotes, 3 en `verification.json` del lote del Manual del Creador, 1 en el `pipeline.log` del video de Fitness). Copia local: `/root/.hermes/cache/scratch/curso-estado/estado-curso.private.json`.
- Corregido en [[transcripcion-curso-gerardo-santiago]]: la página decía ocho videos y ubicaba los TXT en `videos\`. Ahora documenta el estado final de 20/20, la tabla completa de pares con bytes y SHA-256, el historial de lotes (original 8 + new_batch + queued_batch + mentalidad_batch + mentalidad04_queue + fitness05_batch + Manual del Creador) y que la carpeta final de los TXT es `transcripts\`.
- Recordado en la página: los TXT son transcripción automática (no revisión humana) y para lecturas nuevas del NAS se usa SMB directo, no el wrapper `pumassh` (que sigue fallando por nombre corto). Solo lectura: no se relanzó ni modificó ninguna transcripción.

## [2026-11-01] create/update | recreación del primer video de creador (edits/01_squishy01)
- Arturo pidió recrear un video de Asu y aprender el proceso; se documentó como runbook reutilizable [[recrear-video-creadores-edits]] (estructura de carpetas, transcripción en la PC, desglose script/recordings/editing, variación de guion, TTS, montaje con `ttchop-server`, QA y pitfalls).
- **Transcripción** del original (`snaptik_7685601865454587154_v3.mp4`, 25.83 s, 720×1280, audio ja) en PumaDeskAsus con el entorno del estudio (faster-whisper `small`, CUDA, `ja`, beam 5, VAD), leyendo el NAS por SMB con credenciales por stdin cifrado. 12 segmentos.
- **Desglose** entregado a `input/`: transcript, `01_squishy01_script.md` (familia **offer-led**) y `01_squishy01_recordings-editing.md` (16 cortes candidatos → 17 intervalos, campos del estudio).
- **Guion variación** (mismo esqueleto y cifras, palabras cambiadas) quitando el testimonio no verificable (“lo compré 4 veces”) y sin inventar el % de descuento.
- **Audios** con PumaVoice01 y defaults del server: 12 tomas por línea en `assets/audio/`, más unidos a 1.4× (26.31 s), 1.5× (24.56 s) y 1.5× con pausas de 0.3 s (27.85 s). El audio de referencia no tiene pausas entre líneas (medido con silencedetect).
- **Montajes con `ttchop-server`**: `01_squishy01_edit.mp4` (17 clips en orden de archivo, duraciones escaladas ×1.078) y `01_squishy01_edit_matched.mp4` (17 clips **empatados por contenido** con los planos del original, planos 1–16 con su duración exacta y el 17º absorbiendo los 2.01 s del audio). 1080×1920, 27.81 s, QA con ffprobe/volumedetect/decode y hash verificado en el NAS.
- **Infra nueva autorizada (opción A):** para que `ttchop-server` lea el NAS sin descargar se instaló `cifs-utils` en vps-projects y se montó `//100.91.254.118/Projects` en `/mnt/polaris` **read-only** (vers 3.0 + seal), con las credenciales en `/root/.smb-polaris.cred` (modo 600). Aprendido: **no pasar `iocharset=utf8`** (falta `nls_utf8` → error 79 / “needed shared library”).
- Límites: artefacto del builder directo (no render de Firestore); no se publicó nada; los originales del NAS no se modificaron. Actualizado [[index.md|índice]] (47 páginas).

## [2026-11-01] update | subtítulos y overlays de la recreación (Remotion `caption-overlay`)
- Se completó la recreación de `01_squishy01` con **subtítulos y overlays**. El estilo real del original se midió píxel a píxel en 8 fotogramas: **caja blanca redondeada con texto oscuro** (no blanco con contorno), **un solo renglón** con texto corto (4–10 caracteres) y centro vertical al **26.3 %** del alto; al final, etiqueta «ここからチェック», **flecha roja con contorno blanco** y disclaimer al pie.
- **Dos implementaciones:** (a) one-off con stickers PNG (PIL) superpuestos por ffmpeg — conserva el audio intacto, no versionada; (b) **Remotion**: se añadió la composición genérica **`caption-overlay`** en `ttchop-post_templates` (`src/CaptionOverlay.jsx` + registro en `Root.jsx`), props-driven y reutilizable, con el video base en `public/` (gitignored). Commit `232a694` en `main` (verificado en `origin/main`).
- **Arturo eligió la versión de Remotion.** Queda anotado el **pendiente de audio**: ese render entregó el audio en estéreo y ~3 dB más bajo que el base (mean −21.2 dB / pico −4.8 dB vs −18.2/−1.8); corregir o remuxear el audio original antes de darlo por final.
- Delegación: el perfil `developer` y `jr_developer` estaban **rate-limited** (~68 h) por su proveedor; el trabajo lo ejecutó `developer_ds` y se verificó el commit y el MP4 de forma independiente.
- Entregables en el NAS (carpeta del caso): `01_squishy01_edit_matched_subs.mp4` (ffmpeg), `01_squishy01_subs.ass`, `01_squishy01_remotion.mp4` (Remotion). Actualizado [[recrear-video-creadores-edits]] y el índice. Sin publicación.

## [2026-11-01] update | fixes de subtítulos/overlays: audio y flecha
- A petición de Arturo se aplicaron dos correcciones a la composición `caption-overlay` de `ttchop-post_templates`, en `main` (commit `30edb5e`, verificado en `origin/main`):
  - **Audio:** el render salía en estéreo y ~3 dB más bajo que el video base; ahora el MP4 final es **mono** y coincide con el base (mean −18.2 dB / pico −1.8 dB).
  - **Flecha del tag:** se ancla **por construcción** al bloque de texto (`ここから / チェック`) — centro horizontal = centro del texto y borde superior ~18 px por debajo — con `arrow.dx/dy` opcionales. Antes usaba `x/y` fija y quedaba desalineada.
- Verificado de forma independiente: commit en `origin/main`, `ffprobe` (1080×1920, mono) y `volumedetect` idénticos al base, y revisión visual de la flecha centrada bajo el texto.
- `01_squishy01_remotion.mp4` reemplazado en la carpeta del caso del NAS (hash de vuelta verificado). Actualizado [[recrear-video-creadores-edits]]. Sin publicación.

## [2026-11-01] update | tipografía del caption: peso natural (sin faux bold)
- Arturo preguntó si el texto de Remotion estaba en negrita. Sí: caption y tag usaban `fontWeight: 700`, pero la primera fuente de la pila (`KeinannMaruPOPjp`, redondeada y la más parecida a Asu) **solo existe en peso Regular**, así que el navegador **sintetizaba** la negrita y engrosaba los trazos artificialmente.
- Se cambió a **`fontWeight: 400`** (expuesto como prop con default 400) conservando la familia redondeada. Commit `06d4173` en `main` (verificado en `origin/main`).
- Re-render con remux bit-exacto del audio: 1080×1920, **mono**, mean −18.2 dB / pico −1.8 dB (idéntico al base). Comparación visual original vs 700 vs 400: el 400 se ve más natural y más cercano al original. `01_squishy01_remotion.mp4` reemplazado en el NAS (hash de vuelta verificado) y runbook actualizado. Sin publicación.

## [2026-11-01] feat | thumbnail de portada al final (`endCard`) en la recreación
- Arturo pidió una **portada estilo Asu** (frame del producto + texto) visible **en el último frame** del video, con una **capa negra translúcida** entre el frame y el texto. Dejó de referencia su grid de portadas.
- Se añadió el prop opcional **`endCard`** a la composición `caption-overlay` (`ttchop-post_templates`): dibuja la imagen del frame a pantalla completa → scrim negro (~0.35) → texto blanco con contorno; default **solo el último frame**. El `<OffthreadVideo>` se mantiene montado, así que el audio no cambia. Commit `1299621` en `main` (verificado en `origin/main`).
- Texto de la portada: 「1個買ったらおまけ7個 / 人気スクイーズ再入荷」 (adaptado del cover real de Asu para este producto). Frame elegido: la caja con los mini squishies.
- Verificado de forma independiente: último frame inspeccionado visualmente (frame + capa oscura + texto), `ffprobe` mono y `volumedetect` −18.2/−1.8 dB idéntico al base, y solo el frame 833 contiene el endCard.
- NAS: `01_squishy01_remotion.mp4` reemplazado + **`01_squishy01_cover.png`** (portada suelta, 1080×1920) añadida. Runbook actualizado. Sin publicación.

## [2026-11-01] audit | el runbook, ¿basta para que otro agente lo repita?
- Arturo preguntó si otro agente podría recrear el siguiente video con esta documentación. Auditoría: el **procedimiento** estaba bien, pero faltaban **artefactos reproducibles**.
- Huecos encontrados: (1) el `props.json` real solo existía en `/root/squishy_edit/` (scratch); (2) el mapeo plano↔clip se remitía a “el chat de la sesión”, no durable; (3) los scripts auxiliares vivían en el scratch efímero del perfil; (4) no estaba escrita la **regla de captions** ni cómo elegir el frame de la portada; (5) el skill `ttchop-content-ops` seguía recomendando los stickers PIL en vez de Remotion.
- Cerrado todo:
  - **NAS:** `01_squishy01_props.json` y `01_squishy01_recipe_matched.json` subidos a la carpeta del caso (hash verificado) como plantillas reales.
  - **Toolkit versionado:** `ttchop-server/scripts/creators/` (rama `master`, la default del repo) con `build_recipe_from_plan.py`, `measure_caption_style.py`, `extract_clip_frames.sh`, `nas/{put,get,list_dir}.py`, `plan.example.json` y README (commit `13572b5`, + fix del README `830a484`). **Prueba de aceptación verificada por mí:** el builder regenera el recetario del caso con delta **0.00**.
  - **Runbook:** se añadió la sección «Herramienta y artefactos de referencia», la **regla de captions** (un caption por LÍNEA del guion, no por plano; tiempos encadenados desde el audio) y cómo elegir el frame de la portada.
  - **Skill:** Remotion como ruta preferida; PIL/`.ass` quedan como alternativas one-off.
- Nota de infra: el venv con `smbclient` para los helpers SMB se dejó durable en `/root/.venvs/nas-smb` (antes solo en un venv del cache, que se poda). Probados **en vivo** contra el NAS con ese venv: `nas/list_dir.py` y `nas/get.py` (hash del archivo bajado coincide con el local).

## [2026-11-01] fix | el frame del thumbnail faltaba en el NAS
- Arturo preguntó si, para **variar la edición** en unos días, está todo guardado. Auditoría: el material (33 clips), los audios, el montaje, los props y el recetario ya eran durables, pero el **PNG del frame del thumbnail no estaba en el NAS**: vivía solo en `public/` (gitignored) y en un scratch de vps-projects, y los props guardan únicamente el **nombre** del archivo, no de dónde salió.
- Subido a la carpeta del caso como **`01_squishy01_endcard_frame.png`** (hash de vuelta verificado, `482f5997…`, idéntico al que está en `public/`).
- Runbook: se explicita que **ese PNG es la imagen del thumbnail** (el fondo de la portada, sin texto ni capa oscura — eso lo añade la composición), que sale del frame de **t=4.0 s** del montaje (con el comando para regenerarlo si hiciera falta) y que antes de renderizar hacen falta **dos archivos en `public/`**: el video base y ese PNG (con el nombre que pida `endCard.image`). Actualizada también la estructura de carpetas y el caso verificado.

## [2026-11-02] create | lista de shots para grabar con GIFs (segundo video: `02_blanket`)
- Arturo arrancó el video siguiente y dejó la referencia en `creators_research/edits/02_blanket/input/` (`snaptik_7703402548501187847_v3.mp4`, 26.63 s). Transcripción (11 líneas) con el script ya generalizado `transcribe_creator_ref.py <caso>` y desglose automático (26 cortes → uno falso de 0.03 s → **25 tomas**).
- Pidió una **lista HTML de los shots a grabar** con ejemplo visual de cada uno. Iteraciones: agrupar por tipo de toma; imágenes más chicas y menos texto; selector **Agrupado / Por orden**; corregir que el objeto era un **libro** (no un celular) en **3** tomas; mover las 3 tomas de los grupos G/H a **B**; y finalmente **GIF animados de 6 fps** en vez de imágenes fijas.
- Resultado: 25 tomas · 26.6 s · 6 grupos · GIFs 6 fps/180 px/64 colores (~4 MB) · HTML con selector de modo y miniatura embebida de respaldo.
- Publicado por FTPS con lectura de vuelta y verificado por HTTP (200 + tamaño + abierto en navegador): `https://lemonsushi.com/uploads/vps2/creators-research/02_blanket/02_blanket_shots.html`. Copia en el NAS: `input/02_blanket_shots.html` + `input/shots/`.
- Comprobado que los frames salen del **punto medio** de cada shot (diff medio contra el inicio >10 y ~1 contra la mitad).
- Documentado: runbook **§3b** (procedimiento completo + pitfalls) y toolkit versionado en `ttchop-server/scripts/creators/shotlist/`; skill `ttchop-content-ops` actualizado con el criterio.

## [2026-11-03] update | 02_blanket: voz, montaje y asignación por número de shot
- Arturo aprobó el guion variado (11 líneas, 207 caracteres) y pidió la voz con PumaVoice01: 11 tomas por línea, natural 33.41 s → **1.4× + pausas de 0.3 s = 26.645 s** (referencia 26.633 s). Subido a `02_blanket/assets/audio/` (35 archivos).
- **Primera asignación rechazada:** monté emparejando por contenido con nombres originales (`20261102_*`), pero Arturo ya había **renombrado los clips por número de shot** (`1A`, `1B`, `2A`… `25A`). Rehecho el recetario con shot N → `<N>A.mp4`; los shots 12 y 13 (sin archivo) reutilizan `10A`/`11A`.
- Montaje final: `02_blanket_edit.mp4` — 25 tomas, 26.615 s, 1080×1920, 30 fps, audio mono pico −1.5 dB. Comparación shot por shot contra la referencia: 24/25 pares correctos (el shot 16 es el único flojo: quedó un plano de persona donde la referencia tiene un detalle de mano).
- **Cambio en el builder:** `collage_builder.py` pasó a usar escalado **lanczos** en el ajuste a 1080×1920 (commit `370d022`), porque el material propio es horizontal y el recorte a vertical implica 1.8× de ampliación. Coste: ~40 s por clip (25 tomas ≈ 16–18 min).
- Documentado en el runbook: bloque «Caso verificado — 02_blanket» + la convención de nombres de clips propios; `02_blanket_recipe.json` subido al NAS como artefacto del caso. Sin publicación.

## [2026-11-03] create | 02_blanket reconstruido en FilmCraft (desde el recetario, sin Firestore)
- Arturo pidió recrear el video en FilmCraft en la PC. Variante nueva del flujo de FilmCraft: en vez del `editManifest` de un render de Firestore, se tradujo **el recetario JSON de `collage_builder`** a una secuencia.
- Medios: 23 clips + la voz (**430 MB**) copiados del NAS a `D:\staging\filmcraft-blanket02\assets` por SMB con tamaño verificado y `source-media-manifest.json`.
- Proyecto FilmCraft 0.9.0 por CLI: `file.newProject` + `file.newSequence` (1080×1920, **30 fps**, 48 kHz estéreo), import de 24 medios, `inspect project` para los IDs, `timeline.place` de los 25 clips en V1 (ticks: 8467200000 por frame) + la voz en A1, y `clip.fillFrame` sobre los 25 (material horizontal en secuencia vertical).
- Export H.264 sin GPU: **799 frames = 26.632 s**, 1080×1920 a 30 fps, AAC estéreo, `offlineMedia: []`, render 56 s. Audio −17.9 dB / pico −1.5 dB **idéntico** al montaje del servidor; decode completo OK y comparación de secuencia sin diferencias.
- Paquete en el NAS: `creators_research\edits\02_blanket\filmcraft-20261103\` (MP4 67 480 633 B + `.fcproj` 43 832 B + manifest), hashes verificados.
- **Limitación declarada:** el `.fcproj` apunta a `D:\staging` (24 rutas locales) y **no se relinkeó a `P:`** (no hay unidad `P:` verificable desde SSH) → es un proyecto **local**, no portable; la reapertura en la GUI interactiva no se validó.
- Documentado en [[ttchop-filmcraft-video-tests]] (nuevo «Ejemplo verificado: 02_blanket»), con las dos trampas del CLI (JSON por `exec` pierde comillas → usar JSONL con `run`; el script de `run` necesita ruta absoluta). Sin publicación.

## [2026-11-03] feat | overlays de texto hechos DENTRO de FilmCraft (02_blanket)
- Arturo pidió los overlays dentro de FilmCraft. Se hicieron con la API de gráficos del CLI, sin hornear texto en PNG (salvo la flecha y la portada).
- **11 captions** (uno por línea del guion, encadenados con los tiempos medidos del audio): caja blanca redondeada con texto oscuro, `size 48`, `y=505` — el estilo medido de la referencia. Se consiguió con `graphics.newText` + `graphics.set` (`background`, `background_radius: 24`, `background_size: 1.25`, `background_opacity: 100`, `fill_color: #141414`).
- **Etiqueta** 「ここから/チェック» y **disclaimer** al pie: texto blanco con contorno oscuro (`stroke`, `stroke_width`, `stroke_color`), sin caja.
- **Flecha roja:** los clips de imagen no se posicionan con `graphics.set` (no hay transformación), así que se horneó en un PNG 1080×1920 transparente ya alineado y se insertó con `graphics.newFromFile`.
- **Portada:** PNG compuesto (frame + capa negra 35 % + «ふわふわで暖かい / 人気の毛布») insertado en el último frame y **recortado a 1 frame** (`timeline.trim`), porque `newFromFile` coloca 5 s por defecto.
- **Descubrimiento útil:** el CLI **rechaza props inexistentes** (`no property …`), así que se pueden encontrar los nombres válidos probando candidatos con `--keep-going`.
- Export final: **799 frames** exactos, 1080×1920 a 30 fps, AAC estéreo, `offlineMedia: []`, audio −17.9/−1.5 dB sin cambios. Subido al NAS: `filmcraft-20261103\blanket02-filmcraft-overlays.mp4` (67 711 946 B) + `.fcproj` + `arrow_full.png` + `cover.png`. Documentado en [[ttchop-filmcraft-video-tests]]. Sin publicación.

## [2026-11-03] docs + chore | relink del proyecto FilmCraft al NAS y aclaración del layout de pistas
- Arturo pidió mover el proyecto a la carpeta del proyecto y asegurar que funcione. Se generó **`blanket02-filmcraft-portable.fcproj`**: 27 rutas reescritas a `P:\tiktok\hamaca\creators_research\edits\02_blanket\…` y **cero** a `D:\staging`; los 27 archivos se verificaron presentes en el NAS por SMB y el `.fcproj` abre en FilmCraft (29 items). Subido a `filmcraft-20261103\`.
- **Bloqueo honesto:** desde la sesión SSH los 27 medios salen `missing` (ahí no existe `P:`). En la PC el mapeo persistente está `Unavailable` (`P:` → `\\Polaris\Projects`, nombre corto con fallo histórico) y Windows no tiene credenciales para `100.91.254.118`; mapear la unidad requiere prompt interactivo, no automatizable sin dejar una credencial del NAS en la PC (algo que Arturo evita). Queda como validación pendiente en la GUI.
- **Corrección de documentación:** el runbook §5.4 decía «por defecto, distribuye los segmentos en tres pistas cíclicamente», pero el caso `02_blanket` puso los 25 clips en **una sola pista V1** y el render salió idéntico. Se reescribió como **layout de pistas: no cambia el render** (V1 o escalonado en 3 pistas), con la verificación real que sí importa (orden, sin huecos ni solapes). Sin publicación.

## [2026-11-03] feat | 02_blanket migrado al layout escalonado en 3 pistas + fix de captions en caja negra
- Arturo eligió **estandarizar el escalonado en 3 pistas**. Se migró el proyecto FilmCraft de `02_blanket`: `sequence.addTracks {video:2, videoAfter:"first"}` para crear las pistas de clips **debajo** de los overlays y `timeline.move` para repartir los 25 clips cíclicamente → **9 en Video 1, 8 en Video 2, 8 en Video 3**, huecos mínimos de 32 frames (sin solapes ni adyacencias), overlays intactos en Video 4–8 y duración igual: **799 frames**.
- **Bug detectado y corregido:** al ampliar un caption del render se vio que la caja salía **NEGRA** (texto oscuro sobre caja negra, ilegible). Causa: el estilo se aplicó con `background: true` pero **sin `background_color`**, que por defecto es negro — mi verificación anterior se hizo sobre hojas de contacto a escala y no lo detectó. Corregido con `graphics.set {props:{background_color:"#ffffff"}}` en los 11 captions y verificado con zoom (caja blanca, texto oscuro) en t=8 s y t=25 s. **Lección: revisar un caption ampliado, no la hoja de contacto.**
- Export escalonado + corregido: **799 frames**, H.264 1080×1920 a 30 fps, AAC estéreo 48 kHz, `offlineMedia: []`, decodificación completa OK, audio −17.9/−1.5 dB sin cambios. **67 714 660 B**, SHA-256 `759c592b…`. Subido al NAS reemplazando la entrega anterior, junto con el `.fcproj` escalonado y el portable relinkeado a `P:` (27/27 rutas verificadas). Sin publicación.
- **Paquete portable validado en vivo:** Arturo abrió `blanket02-filmcraft-portable.fcproj` en FilmCraft desde su escritorio y **los medios se ven online** (el relink a `P:` es correcto; desde la sesión SSH seguirán apareciendo `missing`, que es esperado).
- **Limpieza autorizada:** con el OK de Arturo se borró del NAS `blanket02-filmcraft-overlays.fcproj` (el viejo: pista única y captions en caja negra). La carpeta del proyecto quedó: MP4 sin overlays, MP4 final con overlays, `.fcproj` escalonado, portable, `arrow.png`, `arrow_full.png`, `cover.png` y `source-media-manifest.json`.

## [2026-11-03] docs | cierre de huecos de documentación tras el caso 02_blanket
- Arturo pidió confirmar que quedara todo documentado. Auditoría (leyendo archivos, no de memoria) → el runbook de FilmCraft estaba completo; faltaban 3 huecos, que se cerraron con su OK:
- **(a) `index.md` desactualizado:** la entrada de `ttchop-filmcraft-video-tests` decía que 02_blanket tenía «el `.fcproj` local sin relinkear a `P:`». Corregido a: overlays de texto nativos **dentro de FilmCraft**, **layout escalonado en 3 pistas** y **portable relinkeado a `P:` y validado en la GUI**. También se añadió el enlace cruzado desde la entrada de `recrear-video-creadores-edits`.
- **(b) El skill era el hueco más grave:** `ttchop-content-ops` → `references/filmcraft-local-video.md` afirmaba «la caja sale blanca por defecto… no hace falta prop de color de fondo» — exactamente la creencia que produjo el bug de los captions en caja negra, y sin mención del escalonado. Corregido: **la caja sale NEGRA por defecto**, hay que fijar `background_color: "#ffffff"` y **verificar un caption ampliado** (nunca la hoja de contacto). Añadidas dos secciones: «Captions y overlays dentro de FilmCraft» (receta + flecha + portada) y «Layout de pistas: escalonado en 3 pistas (estándar)» con `sequence.addTracks`/`timeline.move` y la advertencia de dejar los clips debajo del texto; más la nota de que la validación de medios online la hace Arturo en la GUI.
- **(c) `operations/recrear-video-creadores-edits.md`:** su caso 02_blanket terminaba en el montaje con ffmpeg sin decir que siguió en FilmCraft. Se cerró con la continuación y enlace a [[ttchop-filmcraft-video-tests]], y se agregó el pitfall del `background_color` a su lista.
- Sin cambios de código ni de contenido publicado. Sin publicación en TikTok.

## [2026-11-04] feat | caso `03_suitcase`: video de cicilife (ttchop-server + captions Remotion)
- Caso nuevo con **dos productos**: `recordings/cicilife/` y `recordings/other/`. Referencia `snaptik_7690535153034202369_v3.mp4` (31.767 s, 720×1280, 30 fps): 28 cortes con umbral 0.27 → **1 falso (0.133 s)** → **27 tomas**.
- **Lista de shots en inglés** (pedido explícito de Arturo): 27 tomas · 6 grupos · GIFs 6 fps, publicada por FTPS y copiada al NAS (`03_suitcase/input/`). El toolkit trae la interfaz **fija en español** → se tradujo el `shotlist.json` y se post-procesaron las cadenas de la UI (verificado: sin restos en español).
- **Transcripción ASR** en la PC (faster-whisper, ja): 9 segmentos / 240 caracteres. **Guion propio y único** de 10 líneas (PumaVoice01, `atempo 1.353` + pausas de 0.34 s = **31.765 s** vs 31.743 de la referencia). Fuera precio/urgencia y lo no verificable de la referencia (「日本ブランド」, 「アルミ合金」).
- **Corrección por producto:** Arturo confirmó que el cicilife **no tiene soporte de móvil en la manija ni freno en las ruedas** → reescritas las líneas 3 y 5 y **guion reordenado** para que cada línea caiga sobre la toma que le toca (antes el texto contradecía la imagen en 3 momentos: 「仕切り付き」 sobre el candado).
- **Dos defectos encontrados y corregidos:**
  1. **Penúltimo plano sin producto** (~1 s de habitación vacía): el corte por defecto cayó donde ya había salido de cuadro y, además, el **recorte central** del builder (607 px de 1920) deja fuera al sujeto pegado al borde → se cambió ese plano al clip `9A` en una ventana distinta (probado con el mismo recorte del builder **antes** de remontar).
  2. **El `endCard` (thumbnail) desaparecía** al remuxear con `-shortest` (recorta el último frame) → remux **sin** `-shortest` y audio a **AAC** (el `.mp3` de la voz dentro del MP4 no lo aceptan las plataformas).
- **Fix de código** (delegado a `developer_ds`; `developer` estaba rate-limited): la composición `caption-overlay` de `ttchop-post_templates` tenía la duración **fija en 834 frames (27.8 s)** → ahora la calcula de los props (`calculateMetadata`), commit **`81d0a04`** en `origin/main`, con retrocompatibilidad verificada (834 con los props del caso anterior, 954 con `duration: 31.79`).
- **Entregado:** `03_suitcase_cicilife_final.mp4` (953 frames, 1080×1920 a 30 fps, AAC mono 44.1 kHz, 31.77 s, decode OK, −17.7/−1.3 dB) + `03_suitcase_cicilife_endcard.png` (el thumbnail = último frame) + guion, plan, props y receta finales. Título y hashtags entregados listos para copiar. **Sin publicar.**
- **Pendiente:** el segundo producto de la carpeta `other/`.

## [2026-11-04] docs + chore | dejar los 3 casos listos para variaciones futuras
- Arturo preguntó si en el futuro se podrán hacer **variaciones** de los 3 videos recreados (mismo material propio, guion/voz/edición nuevos) y si está toda la información. Auditoría del NAS por caso → sí, con 3 huecos que se cerraron:
- **Manifiestos nuevos** (`<caso>_MANIFEST.md` en la raíz de cada carpeta del NAS): referencia, material propio, **tabla plano→clip de la receta** con `trimStart`/`trimEnd` y SHA-256 de la receta, voz (unida + por línea), guion, **captions con sus tiempos** (los de `02_blanket` se extrajeron del `.fcproj` de FilmCraft, que es donde vivían), entregables y la **cadena de comandos exacta** para rehacerlo. Subidos a `01_squishy01/`, `02_blanket/` y `03_suitcase/`.
- **`01_squishy01` era el caso frágil:** sus 33 clips conservan el **nombre de cámara** (`20261031_…`), así que el mapeo plano→clip existía **solo** en la receta; ahora está además tabulado en el manifiesto y su hash anotado.
- **Helper de TTS versionado** (delegado a `developer_ds`; `developer` sigue rate-limited): `ttchop-server/scripts/creators/tts/tts_lines.mjs` + su README, antes vivía suelto en `/root` de vps-projects y se perdía en cada caso.
- **Runbook §8 «Hacer una VARIACIÓN de un video ya entregado»** en [[recrear-video-creadores-edits]]: tabla de piezas (referencia, receta, material, voz, guion, captions, entregables), los 6 pasos y los dos avisos (no re-correr `build_recipe_from_plan.py` para un ajuste puntual; no borrar la receta de `01_squishy01`).
- Sin publicar. Nada del material propio se modificó.

## [2026-11-04] feat | caso `03_suitcase`: segundo producto (`other`, 京の小町屋)
- Arturo pasó la ficha: **京の小町屋** — maleta blanca, **4 colores (黒・白・ピンク・銀色)**, tallas **S/M/L**, y de su descripción **超軽量** y **静音設計** (usables: son de su propia ficha). Sin soporte de móvil ni freno (confirmado antes).
- **Verificación previa de sus 29 tomas CON el recorte del builder** (la lección del plano 26 de cicilife): ninguna cae en tramo vacío y la maleta se ve en las 27 ✓. Confirmado además que **se ve el candado** (5A/14A/15A/18A), **los bolsillos interiores** (21A/23A), **el portavasos con botellas** (13A/16A) y **las ruedas** (17A).
- **Guion nuevo y distinto** (10 líneas, para que no se lea como copia del cicilife ni de la referencia): abre por **peso y ruido** («lo más importante es el peso y lo silenciosa que sea»), y **reordenado según las tomas** (candado ~14 s → ロック付き; ruedas ~17 s → 静音キャスター; interior 20–23 s → ポケット付き / 1〜2泊ちょうどいい; colores al final). Captions distintos a los de cicilife (静音キャスター, 黒・白・ピンク・シルバー…). Fuera precio/cupones.
- **Voz:** PumaVoice01 por línea con el **helper ya versionado** (`scripts/creators/tts/tts_lines.mjs` — estreno en producción ✓), `atempo 1.436` + pausas de 0.34 s → **31.739 s** (video 31.756).
- **Montaje** con la misma receta/plan (misma referencia) → **953 frames**, 1080×1920 a 30 fps, AAC mono 44.1 kHz, 31.77 s, decode OK, **−17.6/−1.5 dB**; etiqueta + flecha + disclaimer + **tarjeta final** (「超軽量スーツケース / カラー4色・S/M/L」). QA de la hoja de contacto: caption ↔ toma alineados en 9 de 10 (la de ドリンクホルダー cae sobre la maleta con la bolsa, medio segundo antes de las botellas).
- **Entregado:** `03_suitcase_other_final.mp4` + `03_suitcase_other_endcard.png` + guion, plan, props y receta finales. El **manifiesto de `03_suitcase`** se actualizó con la sección del segundo producto (piezas, hashes y notas). Título y hashtags listos para copiar. **Sin publicar.**
- **Con esto quedan los 4 productos con video** (squishy, cobija, cicilife, other).
- **Corrección posterior (misma fecha):** Arturo detectó que el audio decía 「ドリンクホルダー」 cuando la imagen mostraba la bolsa. Causa: esa línea caía en la ventana 9.9–12.5 s y **las botellas aparecen a los 12.2 s**. Arreglo aplicado: **línea 4 = 持ち運びがラク** (cae sobre el plano de llevarla/arrastrarla) y **línea 5 = 「ドリンクホルダーもロックも付いてる…」** (cae sobre las botellas **y** el candado, que sí están en esa ventana). Captions: **持ち運びラク** y **ドリンクとロック**. Voz regenerada (`atempo 1.456` + pausas → 31.791 s) y captions re-renderizados; verificado frame a frame que la ventana 12.5–15.5 s muestra el portavasos con la botella y el candado. **Lección:** cuando una queja de este tipo llegue, revisar la **ventana de tiempo** de esa línea contra la cronología de tomas y **fusionar o reasignar líneas** — no retocar los captions a mano.

## [2026-11-05] chore | los 3 casos recreados se movieron de carpeta en el NAS
- Arturo reubicó los 3 videos de recreación (ASU) de `tiktok/hamaca/creators_research/edits/` a **`tiktok/hamaca/edits/`**, **renumerándolos** dentro de la serie general: `01_squishy01` → **`10_squishy01`**, `02_blanket` → **`11_blanket`**, `03_suitcase` → **`12_suitcase`** (los archivos internos conservan el prefijo viejo). `creators_research/edits/` quedó **vacía**.
- **Lo funcional:** las 4 recetas apuntaban a la ruta vieja → se reescribieron a `/mnt/polaris/tiktok/hamaca/edits/…` y se **verificó ruta por ruta** que cada archivo existe (18/18, 26/26, 28/28 y 28/28). Sin eso, cualquier variación futura habría fallado al montar.
- **Manifiestos actualizados:** cada uno ahora dice su número nuevo, avisa de dónde vive y lleva el **SHA-256 nuevo de la receta** (cambió al reescribir las rutas). Los nombres de archivo de los manifiestos se dejaron como estaban (renombrarlos implicaría borrar los viejos).
- **Docs actualizadas** a la ruta nueva: runbook de recrear (§8 + encabezados de los 3 casos), runbook de FilmCraft (la ruta del caso 02_blanket→11_blanket), el skill `ttchop-content-ops` (SKILL.md + su reference) y esta bitácora (las entradas anteriores quedan como registro histórico, con la ruta que tenían entonces).
- Sin publicar; nada del material propio se tocó.

## [2026-11-05] docs | punto de entrada «Vías para hacer un video»
- Arturo preguntó cuántas maneras tiene de hacer videos y si están bien documentadas y organizadas. **Auditoría:** hay **3 vías reales** — (1) automática (Producer/pipeline + UI de TTChop2), (2) manual con clips y trims de TTChop2, (3) recrear el video de un creador (incluye §8 variaciones) — más **1 sub-caso** (edición manual Producer-style sin catálogo, cuando no hay ficha) y **1 entorno alternativo** (FilmCraft en la PC). Cada vía ya tenía su runbook con `status: active` y su skill, pero **la organización fallaba**: dos hubs que se solapan (`ttchop-video-generation` A/B/C y el runbook de creadores) y **ningún punto de entrada** que dijera cuál usar ni qué comparten.
- Creado **`operations/ttchop-video-paths.md`**: tabla de las vías (para qué / qué necesitas / paso a paso / skill), guía de elección, **piezas compartidas** (`collage_builder`, composición `caption-overlay`, PumaVoice + el helper de TTS ya versionado, manifiestos por caso), pasos de apoyo (voz/traducción, música, carruseles, segmentar) y las reglas que aplican a todas.
- Enlazado desde el **índice** y con una línea de cabecera en los **7 runbooks** relacionados; añadido también un puntero en el skill `ttchop-content-ops`.
- **No se tocó el contenido** de los runbooks existentes (solo el enlace de entrada). Sin publicar.

## [2026-11-05] docs | mapas publicados en el FTP (video y ecosistema completo)
- Arturo pidió poder **visualizar la documentación** cómodamente: un diagrama de flujo de la parte de video y, después, un **mapa completo interactivo de todo** (no solo ttchop), como documento aparte.
- Creado **`web/ttchop-mapa-documentacion.html`** (el de video): las 3 herramientas con el camino por defecto (ttchop-server → Remotion, FilmCraft como reemplazo manual), las vías con sus pasos previos, cómo está organizado el wiki y una tabla «si quieres X → esto hago».
- Creado **`web/mapa-ecosistema.html`** + **`web/build-mapa.py`**: el mapa **completo**. **Se genera desde las fichas reales** del wiki (títulos, descripciones y tags leídos de `entities/` y `operations/`), así que no se desincroniza y cubre las **48 fichas** (persona, 6 categorías con sus proyectos —incluida Cliff, que sigue «en veremos»—, hardware, sistemas y los 15 runbooks). Trae **buscador**, filtros por área y fichas desplegables, y **cada ficha enlaza a su página en GitHub** (el repo es público).
- Ambos publicados en el FTP (`/uploads/vps2/docs/`), verificados por HTTP 200 y probados en el navegador en viewport de celular (sin scroll horizontal; filtros y desplegables funcionando).
- **Para saberlo:** al añadir fichas nuevas al wiki hay que volver a correr `web/build-mapa.py` y, si son proyectos o runbooks, añadir su id a las listas del generador. El de video, en cambio, es de edición manual (es un resumen curado).
- Sin publicar nada en TikTok.

## [2026-11-05] docs | la pecera 3D: el wiki navegable en tres dimensiones
- Arturo pidió una versión **visual en 3D** («una pecera gigante en medio de un cuarto, moverte alrededor, ver dentro en 360, zoom in/out»). Se hizo tal cual: un **cilindro de cristal** en un cuarto oscuro con el contenido del wiki flotando en capas — **Arturo arriba**, luego **categorías** (con líneas a sus proyectos), **proyectos**, **runbooks** y **plataforma** al fondo, en espiral para que se lean.
- **`web/mapa-pecera.html`** generado por **`web/build-pecera.py`** desde las fichas reales (51 nodos: 13 proyectos + los 4 de Cliff sin ficha + 15 runbooks + 12 de plataforma + 6 categorías + la persona). Se **gira alrededor** con arrastre, se hace **zoom** con pellizco/rueda y hay un botón **«Entrar a la pecera»** con animación de cámara hasta dentro. Al tocar un nombre se abre su ficha con el enlace a GitHub.
- **Librería vendorizada** en `web/lib/` (three.js 0.160.0 + OrbitControls + CSS2DRenderer): la página es **autónoma, sin CDN**. Al publicar hay que subir la página **y** los 3 archivos (`docs/` + `docs/lib/`).
- **Dos lecciones técnicas** (documentadas en `web/README.md`): (1) **`CSS2DRenderer` reescribe `element.style.display` en cada frame**, así que las etiquetas se ocultan con una clase de opacidad, no con `display` — con `display` parece funcionar y no funciona; (2) **una pestaña en segundo plano pausa `requestAnimationFrame`**, así que al probar animaciones en un navegador automatizado hay que forzar la visibilidad o se concluye un bug que no existe (perdí un rato con eso).
- Los tres mapas quedan enlazados entre sí: la pecera (3D), el mapa del ecosistema (plano) y el de video. Verificado en navegador: WebGL 2.0, las etiquetas por nivel (5 → 29 → 51 al acercarse), la ficha al tocar, la animación de entrada y la vuelta a girar.
- Sin publicar nada en TikTok.

## [2026-11-05] docs | pecera 3D: corrección de controles y color coding por categoría
- **Queja de Arturo:** «el movimiento solo funciona cuando hay un botón» y faltaba agrupar por categorías con color. Tenía razón en las dos.
- **Causa raíz del movimiento:** los `OrbitControls` estaban enganchados a la **capa de etiquetas**, que tiene `pointer-events:none` → solo respondían los botones. Ahora van enganchados al **canvas**: se **rota arrastrando en cualquier parte de la página**, se **panea** con botón derecho (escritorio) o **dos dedos** (celular) y el zoom con rueda/pellizco. `enablePan` y `screenSpacePanning` explícitos.
- **Color coding:** cada una de las **6 categorías tiene su color** (🎒 backpack verde, 🎬 cliff rosa, 👨‍👩‍👧 macanishi ámbar, 📈 moon violeta, 🛠️ sandbox celeste, 🛒 tts amarillo) y **sus proyectos usan el mismo color**, igual que las **líneas categoría→proyecto**; los runbooks y la plataforma quedan en neutro para que la agrupación se lea de un golpe. La leyenda se genera del mismo mapa de colores.
- **Verificado con eventos reales del navegador** (no simulados): el arrastre con botón izquierdo **rota** ✓ (los nodos se desplazan distinto) y la rueda **hace zoom** ✓; el clic en una etiqueta abre la ficha ✓. El **pan** quedó habilitado con el mapeo estándar de la librería (botón derecho / dos dedos) pero **no lo pude verificar concluyentemente** en el navegador automatizado (con cámara en perspectiva un pan también desplaza distinto a cada profundidad, así que mi criterio de prueba no servía) — se confirma en 2 segundos usándolo.
- **Otra lección de laboratorio:** los eventos de puntero **sintéticos** (dispatchEvent) pelean con el `setPointerCapture` de los controles y dan falsos negativos; hay que usar `Input.dispatchMouseEvent`/`dispatchTouchEvent` del navegador. Y una sesión con emulación de móvil + WebGL pesado puede **atorar** el harness: conviene cerrarla y abrir una limpia.

## [2026-11-05] docs | prueba de video con IA (kie.ai) para los planos sin producto
- Arturo preguntó si se podía **recrear el video con IA** (caso `13_NachoShampoo01`, referencia de 10.9 s con 15 tomas). Se verificó que la capacidad **ya está integrada** en `ttchop-server` (`/ai/prompt` → `/ai/generate` → `/ai/callback`; el scheduler ya encola videos de IA) y se corrió una **prueba real** con sus reglas: **el encuadre debe coincidir con el shot** y **la persona siempre con ropa**.
- **Modelos probados y precios reales** (kie.ai, 1 crédito ≈ $0.005): `kling-4.0/reference-to-video` ($0.1425/s), `kling-4.0/keyframe-to-video` (idem), `wan/2-6-flash-image-to-video` (~$0.03/s), `google/nano-banana-edit` (~$0.04), `nano-banana-2` (8 cr). Ranking de realismo consultado (Genativity oct-2026): FLUX 3 (no está como video en kie), Kling 4.0, Wan 3.0.
- **Resultados:** el **primer cuadro es lo que fija el encuadre** (con composición libre el clip se va — uno pasó de plano general a primer plano; otro salió con **espalda descubierta** y se descartó). El mejor de la prueba fue **Wan 2.6 flash con primer cuadro** (con ropa ✓, encuadre casi fijo ✓, sin manos deformes ✓). **Kling keyframe** respetó la ropa pero **deformó las manos** y el pelo salió plástico → confirma que **las tomas con manos/producto las graba Arturo**. La limpieza de la insignia/texto quemados con `nano-banana-edit` funcionó perfecto.
- **Costo real: 373 créditos ≈ $1.87** (saldo 733.46 → 360.46). Todo guardado y verificado en el NAS (`13_NachoShampoo01\ai-test\`, 12 archivos, con README). Método en el skill `ttchop-content-ops` → `references/ai-video-kie.md`.
- Nada publicado en TikTok.

## [2026-11-05] docs | prueba con IA, segunda parte: shot por shot y preview multicorte
- Tras el primer spike, Arturo pidió el multicorte con un solo prompt; se probó `multi_shots: true` de Wan 2.6 flash con un prompt numerando 4 planos: **no produjo cortes** (0 cambios a umbrales 0.3/0.15/0.08; 10 fotogramas revisados = un plano continuo) y además **empeoró** el material frente a un clip de 5 s con prompt simple. Conclusión registrada: **el multicorte se hace en la edición**.
- Se generó **shot por shot por grupos** con `wan/2-6-flash-image-to-video` (30 créditos / 5 s a 1080p, cargos medidos) usando el **fotograma de la referencia como primer cuadro** (regla del encuadre) y `nsfw_checker: true` (regla de la ropa). Resultados: el clip de **pelo mojado** salió **usable** (ropa ✓, encuadre clavado ✓, mojado creíble ✓); el de pelo seco necesitó un **reintento** (el primero salió **de frente con la cara** por un prompt ambiguo ✗) y aun así trae un **texto borroso arriba** que hubo que **recortar** (no se evita por prompt, verificado).
- Se armó un **preview de 10.9 s** cortando los clips de IA con las **duraciones reales de la referencia** y poniendo **tarjetas oscuras** en los 4 planos que graba Arturo (producto, espuma, secadora, botella) → se ve el ritmo real y qué falta. Guardado en el NAS (`13_NachoShampoo01\ai-test\`).
- **Aprendizaje de proceso:** para fijar encuadre hay que escribir en el prompt «de espaldas, la cara nunca se ve, cámara fija» (un «gira la cabeza» la volteó a cámara) y **siempre validar la sintaxis** (`node --check`) antes de lanzar un script de generación. Un clip de 5–10 s cubre **varias tomas cortas** variando el punto de entrada: no hace falta generar un clip por toma. Método completo en el skill `ttchop-content-ops` → `references/ai-video-generation-kie.md`.
- Gasto total de la prueba: **~$2.80**. Sin publicar nada en TikTok.

## [2026-11-05] docs | caso 13 `13_NachoShampoo01` — recreación completa con planos generados por IA

- **Encargo:** recrear una referencia de 10.9 s (15 tomas) donde **los planos sin producto los genera la
  IA** y los de producto/manos los graba Arturo. La referencia es 720×1280 a 30 fps y el ASR en ja detectó
  **una sola frase de 13 caracteres** → es música con un gancho hablado al inicio, así que el guion se
  escribió libre y la música se generó nueva (instrumental ~132 BPM, al estilo de la original).
- **Proceso completo** (documentado paso a paso en [[recrear-video-creadores-edits]] → «Caso verificado —
  13_NachoShampoo01»): transcripción → **shotlist HTML con GIFs** → **8 imágenes** con `nano-banana-edit`
  (cada una recreando fielmente el fotograma de su plano) → **8 clips** con `wan/2-6-flash-image-to-video`
  a **720p** usando la imagen aprobada como primer cuadro → **montaje** con `build_recipe_from_plan.py` +
  `collage_builder.py` (15 piezas a 1080×1920, SAR 1:1, 30 fps) → **`caption-overlay`** para el cierre y la
  portada → **emojis e insignias ①②③ quemados con ffmpeg** → **portada** = último fotograma.
- **Lo que más costó** (y quedó en los pitfalls del runbook): las imágenes necesitaron **6 rondas** porque
  al principio se le pedía a la IA «otra mujer» (inventaba una distinta por plano y el pelo cambiaba de
  tono) y «pelo largo a la cintura» (abría el plano y rompía el recorte). Y los overlays de la referencia
  hubo que **medirlos por color, píxel a píxel, sobre 55 fotogramas**: así se descubrió que los **emojis
  alternan en cada corte** (impares 😢 / pares 😊), que van **centrados al 50%** y que miden **9.2% del
  ancho** — estimarlos a ojo desde hojas reducidas provocó dos rechazos seguidos. También: **el plano 15
  (toma horizontal de Arturo) se rota a vertical** en vez de recortarla, y así las botellas quedan paradas
  y las etiquetas legibles.
- **Entregado:** `13_NachoShampoo01_FINAL_v8_musica.mp4` y `_FINAL_v8_SIN_MUSICA.mp4` (11.13 s, 1080×1920,
  audio bit-exacto −13.3 dB) + el thumbnail PNG + la música + la toma rotada, todo en el NAS y verificado
  por hash. La versión con el **audio original** de la creadora se guardó aparte **solo para comparar**
  (`_comparacion_interna_no_publicar/`) — no es publicable.
- **Gasto: 321.5 créditos ≈ $1.61** (las imágenes y los 8 clips; el único video que falló por error del
  servidor se relanzó **sin costo**). El método quedó copiado al skill `ttchop-content-ops`
  (`references/ai-video-generation-kie.md`) y el expediente del caso en `CASE_NOTES.md`, en el NAS.
- Sin publicar nada en TikTok (falta el OK explícito de Arturo).
- **Cierre del caso (misma fecha):** carpeta del NAS **reorganizada** al estilo de las anteriores — la
  entrega y los documentos clave quedan en la raíz, el material en subcarpetas (`input/`+`shots/`,
  `recordings/{arturo,ia,piezas_v1}/`, `final_pieces/`, `assets/audio/`, `shotlist/`, `thumbnails/`,
  `_revision/`, `_versiones_anteriores/`, `_comparacion_interna_no_publicar/`, `ai-test/`) y **sin borrar
  nada**: las versiones previas del montaje pasaron a `_versiones_anteriores/`. Se escribió el
  **`13_NachoShampoo01_MANIFEST.md`** (tabla plano→clip con la duración real de cada toma, overlays con
  tiempos, SHA-256 de las entregas y el título/hashtags del post) y las entregas se renombraron a
  `13_NachoShampoo01_final_musica.mp4` / `_final_sin_musica.mp4`. Todo verificado por hash tras mover.
  La receta conserva un detalle a vigilar: registra el `s15` con 4.657 s por el absorbedor del builder,
  pero **la duración montada real es 0.733 s**.

## [2026-11-06] docs | caso 14 Enchenal — comercial de libro pop-up y entrega v3 fixed

- A petición de Arturo, creado [[ttchop-popup-book-commercial]]: flujo manual Lemo-Opuscar / Paper Pop-up Book con Three.js + Canvas2D, Chromium y FFmpeg; separado de EffectCraft/FilmCraft y del Producer.
- Documentados referencia/fotos de TTChop2, guion japonés/PumaVoice01 y 1.5×, eliminación de las dos escenas técnicas y su audio, continuidad del viejito/montaña, seis páginas, jerarquía foreground/background, storyboard aprobado v5, cámaras suaves y barrido de barba final.
- Registrada la única generación de poses Kie (`nano-banana-2`, 18 créditos, task ID y limitaciones reales), sin confundir ese cargo con TTS ni uso del modelo Hermes.
- Identificada la entrega canónica **`enchenal_book_camera_v3_fixed.mp4`**: 34.5 s, 1080×1920/30 fps, 1035 frames; SHA-256 verificado contra NAS. El v3 sin fixed conserva el rótulo defectuoso y no es el final. Incluidos paquete `sourcepackage_fixed.tar.gz`, comandos de reconstrucción, QA, recibos y respaldo persistente.
- Enlace añadido al hub [[ttchop-video-paths]] y al índice; inventario contado: 49 páginas. Solo documentación; sin nueva generación, cambios de aplicaciones, despliegues o publicación en TikTok.

## [2026-11-09] docs | build VOX Enchenal con Announcer e imágenes distintas

- Añadido [[ttchop-vox-collage-commercial]], separado del Book: kit Vox Collage/HyperFrames, referencia original de ocho escenas, guion propio japonés, voz Announcer a 1.5× y 45 estados de caption.
- Registrado el archivo final **`vox_shaver_full_announcer_images_v2.mp4`** (47.4 s, 1080×1920/30 fps, 1422 frames), SHA-256, respaldo persistente, destino NAS y `sourcepackage.tar.gz` con comando `sh reproduce_images_v2.sh` leído del paquete real.
- Documentada una generación de ocho piezas con `nano-banana-2` (task `43434461cc8c7dcfaaab397c60299f33`, 18 créditos), aprobación de Arturo, extracción alfa, mapa de activos realmente sustituidos y límites. El audio/animación no cambiaron al integrar imágenes; no confundir ese cargo con las poses del Book, TTS o uso del modelo Hermes.
- Índice y hub de vías actualizados; 50 páginas contadas. Documentación y fuentes verificadas; sin generar/renderizar medios nuevos ni cambiar aplicaciones/servicios.

## [2026-11-17] create/update | transcripción del curso: 2 pendientes, ruta GPU en la PC y documentación de las trampas
- Arturo subió más videos al curso: hay **24 MP4 y 22 TXT**; los pendientes son `06ElCreadorTop_01ConvierteteEnUnCreadorTop.mp4` (1,93 GB) y `06ElCreadorTop_02Masterclass.mp4` (1,01 GB).
- **El VPS no sirve para esto**: el lote del 2026-11-16 publicó los dos TXT del Manual del Creador y luego murió por OOM (`Killed process (python) anon-rss: 1891760kB`) al cargar 70 minutos de audio en una máquina de 3,9 GB. Arturo pidió expresamente no correrlo en el VPS.
- El trabajo se movió a **PumaDeskAsus con `device='cuda'`** (RTX 2060 SUPER), reutilizando el runner del curso que ya estaba en la PC. Verificado: modelo cargado en GPU, 22 TXT preexistentes revalidados por SHA-256 antes y después, descarga con hash, publicación con temporal + lectura de vuelta + renombrado sin sobrescribir.
- **Documentado para no volver a investigarlo** en [[transcripcion-gpu-pumadeskasus]]: (1) en Windows la autenticación SMB falla aunque las credenciales sean correctas, y se arregla desactivando el cliente nativo (`spnego.client` + `use_ntlm`), no solo con `auth_protocol='ntlm'`; (2) las credenciales van por stdin y se leen con `read()`, porque el JSON es multilínea y `readline()` falla; (3) mapear `Z:`/`P:` no funciona por SSH (*“logon session does not exist”*); (4) hacen falta las DLL de cuBLAS/cuDNN en el PATH para la GPU.
- Actualizados [[acceso-nas-polaris]] (el venv de SMB ahora vive en `/root/.hermes/tools/course-stt-venv`, fuera de `scratch`, porque la limpieza automática lo borró) y [[transcripcion-curso-gerardo-santiago]] (estado real 24/22 y regla de audio largo). Solo documentación y el trabajo de transcripción en la PC.

## [2026-11-17] update | curso Gerardo Santiago transcrito por completo (24 de 24) en la PC con GPU
- Los dos pendientes (`06ElCreadorTop_01ConvierteteEnUnCreadorTop.mp4` y `06ElCreadorTop_02Masterclass.mp4`) se transcribieron en **PumaDeskAsus con `device='cuda'`**, no en el VPS: 239,5 s y 111,0 s de cómputo.
- Verificado por lectura directa del NAS: **24 MP4 y 24 TXT**, cero faltantes. Los dos nuevos coinciden en bytes y SHA-256 con lo publicado (`…01` 54 177 B / `d98e0fa7…`, `…02` 40 345 B / `2150f133…`) y su contenido es texto real en español. Los 22 TXT preexistentes se revalidaron antes y después (sin cambios).
- Rendimiento medido y documentado en [[transcripcion-gpu-pumadeskasus]]: **~13× el tiempo real** en GPU y **~37 MB/s** de descarga NAS→PC.
- Averiguado y documentado en el camino: `net use` muestra **P: como *Unavailable*** porque apunta a `\\Polaris\Projects` y el **nombre corto no resuelve** (el FQDN `polaris.tail639785.ts.net` sí → 100.91.254.118); y el proceso lanzado con `Start-Process` **muere al cerrarse la sesión SSH**, así que el trabajo hay que lanzarlo manteniendo la sesión abierta o con el Programador de tareas.
- Actualizada [[transcripcion-curso-gerardo-santiago]] (estado 24/24 e inventario con las dos filas nuevas).

## [2026-11-18] update | 18_shaver — entrega clon japonés v7
- Entrega v7 verificada en `P:\Tiktok\hamaca\edits\18_shaver\production\v7\`: `shaver18_ja_clone_final_v7.mp4`, 70 115 425 bytes, SHA-256 `aa708f5ec253d48a17d45c5e212eb9a9103b109f2630fc147ba077a35c51beff`; H.264 1080×1920, SAR 1:1, 30 fps, 1801 frames (60.033 s). Lectura de vuelta NAS verificada para 57 archivos; evidencia en `FINAL_DELIVERY_RECEIPT.json` y `NAS_RECEIPT.json` del scratch de ttchop_robot.
- Único cambio respecto a v6: inicio del primer rótulo 0.8→0.5 s (cuadro 15); final permanece en 2.0 s. Las tres tarjetas son estáticas; la tercera conserva `y=1390` y el cruce momentáneo de la mano aceptado. Flecha inferior izquierda conservada. Audio no regenerado: 2586 paquetes idénticos a v6; `cover.png` es idéntica a v6 y corresponde al último cuadro.
- También entregados `shaver18_ja_clone_final_v7_chat.mp4` (22 273 383 bytes) y `shaver18_overlays_v7_patch.zip` (SHA-256 `0c7e7e8193c0fbb4ddb21bf4523ca848e0056a2bb93c02feffac408d29d9a6a5`). README del parche documenta reconstrucción desde fuentes v3 + parche.
- Título de tienda:
  ```text
  買う前に確認したい、シェーバー選びの3つのポイント。
  #TikTokShopこれ買い #電動シェーバー #シェーバー #メンズケア #Enchenal
  ```
- Estadísticas en captura de origen: 5.5K ventas, 4.2/283 reseñas; no son verificación del listado actual. Afirmaciones heredadas de voz/texto sobre titanio, piel, falsificaciones y escasez no verificadas independientemente; no tratarlas como hechos clínicos o comprobados. Sin precio ni porcentaje de descuento.
- Guardado/entregado, no publicado; no consta aprobación explícita del MP4 como final. Sin cambios de apps, TTS, APIs pagadas ni Firebase.

## [2026-11-18] update | publicación TikTok exclusivamente manual por Arturo
- A petición explícita de Arturo, aclarada la regla en [[ttchop-video-paths]], [[recrear-video-creadores-edits]], [[ttchop-video-generation]], [[ttchop-filmcraft-video-tests]], [[ttchop-carousel-creation]] y [[ttchop-webapps]]: ttchop_robot nunca publica videos/carruseles en TikTok, aunque el contenido esté aprobado o exista autorización excepcional; Arturo publica manualmente.
- El agente cierra al crear, verificar y entregar archivos y título cuando corresponda. Registrar «entregado»/«guardado»; solo registrar «publicado» cuando Arturo confirme que él mismo publicó. Publicar HTML/GIFs de revisión por FTPS a solicitud sigue permitido y no equivale a publicar en TikTok. No se modificaron capacidades/API documentadas de la app ni estados históricos de trabajos.
- Corregido además el formato de ruta y bloque de título de la entrada previa de `18_shaver` para que la ruta Windows y el título/hashtags se lean literalmente. Solo documentación; sin cambios de apps, medios, NAS, Firestore ni publicación.

## [2026-11-18] create | estándar de portada/thumbnail de videos

- Arturo pidió estandarizar las portadas: los dos videos entregados salieron con thumbnails distintos (posición, centrado y mecanismo). Creada la página [[estandar-thumbnail-video]] con la regla fija y los valores exactos: **1080×1920, un solo fotograma (el último del video)**, ≤2 líneas japonesas, familia `KeinannMaruPOPjp` **Regular 400 real** (sin faux bold), `fontSize 80`, `lineHeight 1.15`, `#ffffff` con contorno `#101010` (`outlineWidth 6`), y **posición FIJA**: bloque centrado horizontal en `x = 540 px (50 %)` con el centro del bloque en `y = 378 px (19.7 %)`; `scrim` negro opcional `0.22–0.35`; prohibidos flecha/CTA/precio/%/escasez/claims no verificados. Mecanismo preferido: prop **`endCard`** de la composición Remotion `caption-overlay` (`frames: 1`) y exportar el PNG del último frame como `cover.png`.
- **Decisión y por qué:** se probaron las dos posiciones reales sobre los dos materiales; la de `y=650` **tapa el producto del shaver**, la de arriba (`y≈378`) funciona en ambos → posición fija ARRIBA.
- **Mediciones reales (1080×1920, PIL, píxeles; re-verificadas en este job):** `17_carpet` final v1 `cover.png` → bbox de texto **x 250–833, y 574–729** (centro X **50.1 %**, centro y **≈651 = 33.9 %**), 2 líneas, prop-driven (`props.json`: `fontSize 80`, `fontWeight 400`, `lineHeight 1.15`, `outlineWidth 6`, `#ffffff`/`#101010`, `scrim #000000` 0.22, `image hero.jpg`, `frames 1`). `18_shaver` v7 `assets/cover_design.png` → bbox de texto **x 133–843, y 262–494** (centro X **45.2 %**, centro y **≈378 = 19.7 %**), 2 líneas, **PNG horneado** (no prop-driven). Diferencia real: posición vertical (651 vs 378), centrado horizontal (50.1 % vs 45.2 %) y mecanismo.
- **Estado: aplicación PENDIENTE de OK de Arturo.** La página documenta el estándar y las desviaciones medidas; **no** se regeneraron portadas ni se modificó nada de los dos videos entregados. No se tocó código de la app, Remotion, colas, medios ni el NAS.
- Enlazada desde `index.md` (Operaciones), desde el hub [[ttchop-video-paths]] (piezas compartidas) y añadida una línea en [[recrear-video-creadores-edits]] §7 (`endCard`). Índice actualizado a **52 páginas**; verificador de integridad sin enlaces rotos ni páginas sin indexar. Solo documentación.

## [2026-11-18] update | estándar de portada: el fondo debe incluir el producto

- Arturo añadió una **regla fija** a [[estandar-thumbnail-video]]: la **imagen de fondo de la portada SIEMPRE debe incluir el producto**, con el producto protagonista **visible y reconocible** (no una escena sin producto, ni solo habitación/textura/persona). Si el último fotograma no lo muestra bien, se elige otro fotograma final que sí lo muestre o se recompone, **sin mover el texto** (`y = 378`, `x = 540`).
- Documentada como punto **8** de los valores exactos, en la sección de reglas y como fila **«fondo con producto visible»** en la tabla de comprobación. Complementa la regla previa de «producto protagonista»: ahora es explícito que aplica al **fondo de la portada**, no solo al encuadre.
- Las dos portadas reales **cumplen** esta regla: `17_carpet` muestra la alfombra (producto) en el suelo de la habitación y `18_shaver` v7 muestra la afeitadora (producto) en estudio (fila añadida a su tabla de desviaciones). Sin afirmar cambios nuevos en las portadas.
- Solo documentación (página + log + una palabra en el hub). Sigue **pendiente el OK de Arturo** para aplicar el estándar a los dos videos entregados; no se tocó código, medios, NAS ni Remotion.

## [2026-11-18] update | clonar o variar según el idioma del original

- Regla de Arturo añadida a [[recrear-video-creadores-edits]] §3a: **el idioma del original decide el tratamiento**.
  - **Original en español** (mercado de México): **se puede clonar** tal cual. No hay que forzar que quede más único.
  - **Original en japonés**: **hay que variar** (estructura igual, redacción y orden propios) para que no sea una copia literal.
- Motivo: en el mercado mexicano el material en español se trabaja como clon; el material japonés se traduce y se adapta para que el resultado no sea idéntico al original.
- No cambia el criterio de sostener lo verificable: cifras, reseñas y vendedor se toman del producto propio, no del original; se quitan claims no respaldados.
- Solo documentación. Sin cambios en videos, código, NAS ni medios.

## [2026-11-19] create | montar videos en la PC (≈20× más rápido que el VPS)

- Arturo pidió probar el montaje en la PC. Se midió el cuello de botella real: **no es la CPU del VPS, es la lectura del NAS** — el CIFS de `vps-projects` sobre `/mnt/polaris` rinde **~0,12 MB/s** (un clip de 23 MB tardó **197 s**) por los **243 ms de latencia** del enlace Tailscale, y el VPS (4 vCPU EPYC, 7 GB, **sin GPU**) está además limitado a x264 por software.
- **A/B con el mismo montador y la misma receta** (4 segmentos de `20_dualshaver` con la voz real del caso, 10.4 s): **PC 10.4 s** (6.0 s recortes + 4.2 s unión) vs **VPS 213 s**. Salidas equivalentes: misma duración, 4.96 vs 4.98 MB, SSIM 0.987 / PSNR 44.5 dB. Prueba aparte con grafos crudos: x264 5.2 s/5.34 MB vs **NVENC 2.2 s/12.48 MB** (`-cq 23`) con SSIM 0.987 / PSNR 45.2 dB.
- **Montador adaptado** (`collage_builder_win.py`): mismos filtros, recortes, unión y encode final; solo rutas/ejecutables por entorno, timing y `COLLAGE_KEEP_TEMP`. Ya no hay que instalar nada en la PC: tiene **Python 3.11.9** real (`D:\staging\hermes-transcription\venv`) y ffmpeg con NVENC en `D:\staging\creator-av-audit\bin`. El repo compartido y el pipeline **no** se tocaron.
- Creada la página [[montaje-video-en-pc]] (procedimiento, requisitos, trampas: `ErrorActionPreference='Stop'` que aborta con stderr nativo, ffmpeg en el `PATH` también para la unión final, `/mnt/polaris` de solo lectura) y enlazada desde `index.md` y desde [[recrear-video-creadores-edits]] §5. Pendiente: decidir si el wrapper Windows se versiona en `ttchop-server/scripts/`.
## [2026-11-19] entregas | casos `19_dualshaver` y `20_dualshaver` (clones en japonés, mismo producto)

**Producto (los dos videos):** `ttchop2/prod_5k79pno` — Enchenal Lab 電動シェーバー 男女兼用 多機能トリマー (2in1: red + recortadora), vendedor Enchenal Lab PersonalCare, https://shop.tiktok.com/jp/pdp/1735290027543529248 . Datos verificados usados en los videos: la ficha del 6-nov daba 4.3K vendidos · 3.8 ★ · 130 reseñas; **re-verificado en vivo el 19-nov: 3.8 ★ · 137 reseñas · 4.4K vendidos** (precio de lista 4,319 ¥ y 3,239 ¥ con −25 %; el video no usa cifras de precio).

### `20_dualshaver` — clon de un original mexicano (35.524 s, 7 tomas, audio español)
- **Entregado:** `P:\Tiktok\hamaca\edits\20_dualshaver\production\` — **v1** (12.96 MB), **v2** (con los 3 insertos de imagen, 28.4 MB) y **v3** (solo audio corregido, 28.95 MB). v3: 1067 frames, 35.571 s, 1080×1920 a 30 fps.
- **Guion:** 8 líneas en japonés, clon del original con los datos propios. Voz PumaVoice01 en una sola toma continua (`atempo` 1.16524). Rótulos japoneses 8 + tag CTA + flecha + descargo. Portada con el estándar (x=540 / y=380) y producto visible.
- **Insertos del primer bloque:** los 3 que tenía el original se generaron con **Kie.ai/seedream-v4 en una sola tarea (15 créditos)** — fotos de piel con irritación/granitos/vello — y se colocaron en los tiempos y cajas medidos en la referencia (1.100–1.967 / 3.200–4.033 / 5.467–6.867 s).
- **Fix v3 (solo audio):** la frase del baño se movió al tramo del **vaso de agua** (20.21–23.52 s) y se retiró la palabra 「防水」; el video quedó **idéntico byte por byte** (md5 del stream de video `5f295a13be218ce883d2f499db1d241a` en v2 y v3). Detalle en la sección de la auditoría del agua.
- **FilmCraft:** `filmcraft-20261119\` con proyecto local (medios en `D:\staging`) y **portable relinkeado a `P:`**, README y `source-media-manifest.json`. Arturo editó su propia versión (velocidades/duraciones/puntos de entrada); se exportó (1068 frames, 35.605 s). Después, **a petición suya**, se le reemplazó **la voz** por la corregida (mismo nombre de archivo → sin relink) y se **intercambiaron los dos rótulos** para que texto y voz coincidan; respaldos: `20_dualshaver_ja_v2_backup_20261119.fcproj` y `voice_final_backup_20261119.mp3`.

### `19_dualshaver` — clon de un original mexicano (44.467 s, 10 tomas, audio español)
- **Entregado:** `P:\Tiktok\hamaca\edits\19_dualshaver\production\v1\` — 18 archivos con lectura de vuelta SHA-256 OK. Video: 1334 frames, 44.478 s, 1080×1920, AAC 44.1 kHz mono, 17.31 MB.
- **Guion:** 10 líneas en japonés (clon) con **cifras propias verificadas** (más de 4,300 vendidos · 3.8 · más de 130 reseñas) en lugar de las del original (82.4K/4.6/7,569). Voz PumaVoice01, `atempo` 1.133538.
- **Overlays (los del original, adaptados):** banda roja 「偽物に注意」, **tres imágenes de producto** escalonadas (del propio listado: aparato, cabezal, caja), **panel de reseñas** (3.8 · 130件のレビュー), **panel del vendedor** (Enchenal Lab PersonalCare ・ 公式), tag CTA + flecha + descargo y portada estándar.
- **Montaje en la PC (primer video con el camino nuevo):** **58.8 s** de trabajo (36.3 s recortes + 22.5 s unión) y ~2 min 30 s el paso completo incluyendo subida al NAS ([[montaje-video-en-pc]]).
- **FilmCraft:** `filmcraft-20261119\` con proyecto local + portable. Después se le agregaron, sobre **su** proyecto (con respaldo previo), los overlays de los shots 3-5 que la referencia sí tiene y el proyecto no cubría: **tarjeta de producto** en T3 (★3.8 ・ 130件のレビュー ・ 4,300件販売), **panel de reseñas** en T4 y **panel del vendedor** en T5, con nota `NOTA_overlays_345.md` y 3 cuadros de verificación. Render de comprobación: 1335 frames, 44.501 s.
- **Entregados también los títulos y hashtags** de los dos videos, listos para copiar.

### Auditoría del agua (los dos casos) — NO se puede afirmar impermeabilidad
- La **descripción** del listado (PDP en vivo y el scrape de ttchop2) **no menciona agua ni 「防水」**; habla de 2in1, doble 3D flotante, 113 g/155 mm, Type-C (1.5 h → 90 min) y garantía de 1 año.
- Una **reseña de comprador verificado** (2026-06-28) pregunta si se puede mojar y señala que la información del producto dice **「水洗い不可」** mientras otros anuncios dicen lo contrario; sigue sin respuesta.
- La única mención de 「防水」 en el scrape corresponde a **otro producto** de la misma marca (shaver de hombre 3in1).
- El **título** del vendedor sí incluye **「お風呂剃り」**, en contradicción con su propia descripción.
- **Decisión aplicada:** se retiró 「防水」 del audio; la idea del baño se conserva solo apoyada en el título del vendedor. Las **fichas de caso** (`input\catalog\catalog_facts.json` en 19 y 20) quedaron actualizadas con la auditoría y los datos en vivo. Precedente ya documentado del mismo producto en [[ttchop-popup-book-commercial]] y [[ttchop-vox-collage-commercial]] («sin inmersión ni promesa de impermeabilidad»).

### Lecciones/pitfalls nuevos
- **Grabaciones verticales con `rotation=90` en metadata:** el contenedor dice 1920×1080 pero son 1080×1920; el mapa de clips las dio por horizontales y el montaje concluyó lo contrario. Comprobar `ffprobe` **y** un fotograma antes de recortar (ya anotado en [[recrear-video-creadores-edits]]).
- **El export de FilmCraft agrega un cuadro negro al final** (la portada queda como penúltimo); en las copias de chat se recorta ese cuadro.
- **Reemplazar un medio por otro con el mismo nombre de archivo evita el relink** en FilmCraft (así se aplicó la voz corregida, con respaldo previo).
- **Fix de solo audio:** muxear con `-c:v copy` y **verificar el md5 del stream de video** contra la versión anterior para demostrar que la imagen no cambió.

## [2026-11-19] docs | cierre de documentación de 17/18/19/20

Cierre de los 4 huecos de documentación aprobados por Arturo ("sí, a fondo"). **Solo wiki** (`/root/cacho`); no se tocó código, medios, el NAS ni Firestore.

- **Fichas de caso nuevas** en [[recrear-video-creadores-edits]]: `17_carpet`, `18_shaver` (v7), `19_dualshaver` y `20_dualshaver` (v1→v3), con referencia, material propio, mapeo toma→clip con ventanas, voz (atempo/duración), rótulos/overlays con tiempos, portada, entrega (rutas + hashes) y cadena de comandos; más la **auditoría del agua** del producto `prod_5k79pno` (sección propia, con cross-ref desde [[ttchop-popup-book-commercial]] y [[ttchop-vox-collage-commercial]]).
- **[[ttchop-filmcraft-video-tests]]:** reconstrucciones FilmCraft de `19_dualshaver` y `20_dualshaver` en `…\<caso>\filmcraft-20261119\` (proyecto local `D:\staging` + portable relinkeado a `P:`, README, `source-media-manifest.json` y MP4 de verificación) y **3 pitfalls nuevos**: (a) el export de FilmCraft añade un cuadro negro al final (la portada queda de penúltimo; se recorta con `-frames:v N-1 -c copy`); (b) reemplazar un medio con el **mismo nombre de archivo** evita el relink (así se aplicó la voz corregida del 20, con respaldos previos); (c) los **rótulos nativos se editan sin re-render** (intercambio de 2 textos en el 20; paneles/tarjeta añadidos en el 19 sobre una copia y luego al proyecto real con respaldo). La validación de "medios online" en la GUI la hace Arturo (desde SSH `P:` no existe).
- **[[ttchop-video-paths]]:** añadida la opción de **montar en la PC** (≈20× más rápido que el CIFS del VPS), enlazando [[montaje-video-en-pc]], tanto en el hub como en la lista de piezas compartidas.
- **[[estandar-thumbnail-video]]:** el estándar **aplica a las entregas nuevas**; se verificó con PIL sobre las portadas reales que **19 y 20 lo cumplen** (texto centrado en `x=540` / `y≈380` y producto visible).

**Decisiones de Arturo registradas explícitamente:**
1. Los dos videos (`17_carpet` y `18_shaver`) **quedan como entregados** — no consta publicación (Arturo publica manualmente); además se quedan con sus portadas actuales.
2. El **19 conserva la mención del agua del original** (audio y rótulo) — **desviación conocida y aceptada**; en el 20 sí se retiró 「防水」 del audio.


## [2026-11-21] fix | por qué se caía el SSH de PumaDeskAsus y corrección verificada
- Síntoma: `connection refused` en el 22 con la PC encendida y Tailscale activo. Causa: **el servicio `sshd` se caía**, no la red.
- Raíz: `ListenAddress` atado **solo a la IP de Tailscale** sin dependencia del servicio `Tailscale` (competían al arrancar, fallaba el bind) + **cero acciones de recuperación** (7034 sin reinicio) + la PC se reinicia sola por inactividad (Kernel-Power 578). Además `LogLevel DEBUG3` con un log de **330 MB**.
- Aplicado y verificado: `sc config sshd depend= Tailscale`, `sc failure sshd reset= 86400 actions= restart/5000/restart/10000/restart/30000`, `LogLevel DEBUG3 → INFO` (respaldo `sshd_config.bak-hermes`, validado con `sshd -t`, log rotado a `sshd.log.old-20261121-143956`).
- **Prueba real**: se mató el proceso del 22 y Windows lo reinició solo a los 10 s (evento 7031), reconectando sin intervención.
- Documentado en [[acceso-remoto-pumadeskasus]] con las causas, los comandos y cómo revisarlo si vuelve a pasar. Ojo: desde la LAN el 22 no aparece porque sshd escucha solo en la IP de Tailscale — falso negativo, no un fallo.

## [2026-11-21] create | Chromecast con Google TV: acceso por depuración inalámbrica y respaldo previo al debloat
- Arturo quiere probar [CleanYourTV](https://github.com/Gathin23/cleanyourtv) en su Chromecast y pidió poder **regresarla como estaba**. Investigado: el proyecto solo **desactiva** paquetes (`pm disable-user`, igual que Ajustes → Aplicaciones) y **escribe un registro de estado antes de tocar nada**; el regreso es un comando.
- Identificado el equipo: **Chromecast con Google TV 4K** (`sabrina`), Android 14, build `UTTC.250917.004` — coincide exacto con la lista curada del repo. En la red también hay un **Nest Hub** (`192.168.0.8`, no aplica) y un “Home group”. Ojo: un `.13` que parecía candidato resultó ser la **impresora Creality** (expone un login en el 5555).
- Aprendido y documentado: **“USB debugging” no abre el puerto de red**; hay que activar **Depuración inalámbrica** y emparejar con `adb pair <ip>:<puerto> <codigo>`. El código **caduca en minutos** y el puerto del diálogo de emparejar **no es** el de la pantalla principal (un intento falló por usar el puerto equivocado). Los puertos son aleatorios y cambian al reiniciar.
- Entorno montado **en el Pi** (no en la PC, para no instalar nada): repo en `/root/cleanyourtv`, venv con dependencias, y `TV_ADB_BINARY`/`TV_HOST` apuntando a la conexión emparejada.
- **Respaldo hecho, sin modificar la TV**: dos registros en `~/.cleanyourtv/` del Pi (lista que conserva casting = 14 paquetes; lista completa = 17), copia en `/root/.config/cleanyourtv/` del VPS. Todos los paquetes `enabled`; Home era `com.google.android.apps.tv.launcherx`. Documentado en [[chromecast-gtv-debloat]].
- Pendiente de decisión de Arturo: aplicar la lista que conserva casting (recomendada) o la completa con lanzador propio. Nada se ha desactivado todavía.

## [2026-11-21] apply | Chromecast: lista completa aplicada, lanzador propio como Home y hora corregida
- Se aplicó la **lista que conserva casting** (12 paquetes) y se verificó con `check.py`: *nothing drifted*, Home intacto, casting (8008/8009) abierto. Nota: aparecen 14 desactivados porque `cast2class` y `tvrecommendations` ya venían desactivados de fábrica y no están en la lista.
- Después, por decisión de Arturo (**“quiero el lanzador nuevo como default”**), se aplicó la **lista completa** (añade `dreamx`, `backdrop` y `tungsten.setupwraith`) y se instaló el **lanzador propio** `com.gathin.tvhome` como Home por defecto; el de fábrica quedó desactivado.
- **Trampa documentada**: con solo la lista de casting, el traspaso **falla y se revierte solo** porque `setupwraith` también reclama el Home (`…setupwraith/.RecoveryActivity`). Hay que aplicar la lista completa primero.
- **Compilar Android en ARM no se puede**: `aapt2` solo existe para x86-64; el build en el Pi muere con *Aapt2Daemon startup failed*. Se compiló en el **VPS** (JDK 17 + SDK 34) y el APK (575 KB) se pasó al Pi. Script de traspaso con `SKIP_BUILD=1`.
- **Hora**: la TV estaba en `America/Vancouver` (7 h atrasada). Corregida a `Asia/Tokyo` con `cmd alarm set-timezone` + `auto_time`/`auto_time_zone`; verificado `Sat Nov 21 18:56 JST`.
- Verificado el botón Inicio del control: `input keyevent KEYCODE_HOME` → `mCurrentFocus=com.gathin.tvhome/.MainActivity`.
- **Intercambios aceptados**: el casting desde el teléfono se rompe tras reiniciar la TV (credencial de fábrica dentro de `setupwraith`) y se pierde el salvapantallas ambiente (`dreamx`/`backdrop`). Antes de desactivar `setupwraith` se comprobó que la red Wi-Fi es de `android.uid.system:1000`, así que no se borra.
- Pendientes: reservar la IP en el router (MAC `DC:E5:5B:49:8F:1E` → `192.168.0.14`) y decidir si la revisión semanal del debloat queda automática (depuración encendida) o manual.
- Documentado en [[chromecast-gtv-debloat]].
- **Salvapantallas ambiente recuperado** a pedido de Arturo: se reactivaron `dreamx` y `backdrop` (la tarjeta de Spotify es parte del ambiente, no una app aparte). Verificado que la TV sigue apuntando al ambiente de Google (`screensaver_components=…dreamx/.service.Backdrop`, `screensaver_enabled=1`, `sleep_timeout=30 min`). No se puede forzar por adb (Android reserva `BIND_DREAM_SERVICE` al sistema): sale solo al quedar inactiva. `check.py` reportará esos 2 paquetes como *drift* contra la lista completa — es intencional.
- **Casting repuesto y verificado** (Arturo confirmó que funciona): al reiniciar la TV, la credencial de fábrica se pierde de memoria y YouTube responde *“Untrusted device — TV couldn't be verified”*. Se repone con el **parche de memoria**: encender `setupwraith` → esperar `ClientAuthSigner` en logcat → apagarlo → **volver a fijar** `set-home-activity` al lanzador nuevo. Automatizado en `/root/cleanyourtv/tools/reponer-cast.sh` del Pi (`TV_HOST=<ip>:<puerto> bash tools/reponer-cast.sh`). Dura hasta el próximo reinicio.
- **Medido**: reactivar `setupwraith` **roba el Home** aunque el lanzador ya esté declarado predeterminado (resolvió a `…setupwraith/.RecoveryActivity`), por eso el parche lo vuelve a fijar al final. En la ventana de ~1 min no reactivó `launcherx`.
- **Corregido el método para encontrar el puerto**: `adb mdns services` volvió **vacío** aunque la depuración estaba encendida. Lo que funciona es `nmap -Pn -p 30000-50000 --open 192.168.0.14` + `adb connect` a cada puerto, y elegir en `adb devices` el que dice `device` (los fallidos quedan como `offline` y aparecen primero en la lista). Puerto de esta sesión: `43567`.
- **La depuración inalámbrica se apaga sola en cada reinicio** (y el puerto cambia) → ninguna revisión automática puede funcionar sin que alguien la active en la TV. Por eso la revisión del debloat queda **manual**.
- Skill `android-tv-debloat` actualizada con ambas correcciones.

## [2026-11-21] create | Escritorio de la PC en la Chromecast: Moonlight + Sunshine (y por qué no el de Google)
- Arturo preguntó si se podía instalar el escritorio remoto de Google en la TV (no le aparecía en la tienda). Investigado y verificado **en su propia TV**:
  - **Chrome Remote Desktop**: Google no publica versión para Android TV; la app actual es un **envoltorio web (TWA)** que necesita Chrome (la TV no lo tiene) y es táctil → se puede instalar a mano pero probablemente no sirva. **Descartado.**
  - **Microsoft Windows App (RDP)**: la ficha existe pero la TV dice **“Your device isn't compatible with this version”**; además RDP exige **Windows Pro** y su PC es **Home** (`EditionID=Core`). **Descartado.**
  - **Moonlight**: está en la tienda de la TV con botón INSTALL (capturado) → **elegido**. Arturo dio luz verde.
- **Instalado y funcionando**: Moonlight 12.2 en la TV (se pulsó INSTALL por adb, buscando el botón con uiautomator) y **Sunshine v2026.914.233613** en la PC por MSI en silencio (servicio `SunshineService` Running). Emparejado con PIN: cliente “TV Moonlight”. Transmitiendo con **`hevc_nvenc`** (RTX 2060 SUPER), 1920x1080.
- Credenciales de la web de Sunshine: usuario `admin`, contraseña en `/root/.config/sunshine/sunshine.txt` del VPS (600).
- **Trampas**: `screencap` devuelve negro para la capa de video por hardware (las capturas negras NO significan fallo: se confirma con `dumpsys SurfaceFlinger` y con el log de Sunshine); el repo de Sunshine se mudó a **`SunshineStream/Sunshine`**; la API de GitHub sin `User-Agent` devuelve JSON de redirección.
- Documentado en [[moonlight-sunshine-tv]]. Pendiente: confirmar la imagen en la TV y, para el cursor, un mouse Bluetooth.

## [2026-11-22] create | Planes de video nuevo: runbook para productos futuros
- Arturo pidió documentar cómo se hacen planes nuevos para productos futuros, usando la información de los desmenuzados pasados pero **sobre todo la documentación de Asu**, y que el documento pueda seguir creciendo.
- Creado [[planes-de-video-nuevos]] (runbook): qué se copia de cada fuente (estructura y tiempos del desmenuzado; guion de Asu; contenido y claims de la ficha), las fuentes de verdad con rutas reales (guía publicada de Asu, reporte de ~50 KB en el workspace de developer, `references/asu-script-formula.md`), los 8 pasos con los artefactos del caso 27, las puertas de calidad y los pitfalls aprendidos.
- Caso verificado: `nanoglass-plan27` — 27 tomas / 31.77 s, publicado y verificado por MD5. La lección principal: **agrupar por similitud mirando las imágenes, no por el guion** (la primera agrupación se rechazó por eso).
- El runbook trae una sección «Cómo crece este documento» con reglas y un changelog: cada plan nuevo agrega una fila y solo se apunta lo verificado.

## [2026-11-22] create | Segundo plan de video nuevo: Derma:U シャンプー&トリートメント
- Arturo pidió otro plan para `prod_5obts4n` (Derma:U シャンプー&トリートメント セット) con el mismo estilo de Asu. Se aplicó el runbook [[planes-de-video-nuevos]] por segunda vez.
- Molde: `03_suitcase` (27 tomas / 31.77 s). Guion: fórmula de Asu, apertura **offer-led** (la ficha está en oferta), sin cifras en la voz para no dejar un precio obsoleto en un plan que se graba después.
- 27/27 imágenes IA generadas con kie.ai. Revisión una por una: 2 tomas con perfil de cara asomando (4 y 26) y 2 ángulos que no son cenital estricto (21 y 22); marcadas en el HTML.
- Publicado y verificado por MD5: `https://lemonsushi.com/uploads/vps2/creators-research/dermau-plan27/index.html` (200, 1.986.497 bytes). Dashboard actualizado con la segunda tarjeta en la pestaña Planes.
- Animatic ES: la voz no cabe en el molde (37.25 s contra 31.77 s) → se estiró la imagen ×1.204 y el MP4 quedó en 38.3 s. Lección añadida al changelog del runbook.

## [2026-11-22] update | Regla de props en los planes de video (retroalimentación de Arturo)
- Arturo corrigió el plan de dadawoca ナノガラス: usaba props que no existen (bolsa de papel, planta, taburete, paño, rastrillo, tubo de crema) y tuvo que sustituir cosas en plena grabación.
- Añadido al runbook [[planes-de-video-nuevos]] el **Paso 0b — Inventario de props: solo lo que existe**: listar props por toma, confirmar que existen, cambiar la acción si falta el prop y entregar la lista consolidada en el HTML. Lo garantizado por defecto es producto, persona y baño.
- Añadido a puertas de calidad y pitfalls, y a la skill `ttchop-shotlist-storyboard`.

## [2026-11-22] update | Componentes del producto vs decoración de fondo (2ª retroalimentación)
- Arturo aclaró el límite: **decoración de fondo sí se puede improvisar** (planta, toalla doblada, luz de ventana), pero **un componente del producto no se inventa**. En el plan de dadawoca había dos tomas imposibles: quitar un plástico protector que el producto no trae y meter el producto en un estuche que no existe. La ficha no menciona ninguno de los dos.
- Añadido al runbook [[planes-de-video-nuevos]] el bloque «Dos categorías que no se mezclan» y el pitfall correspondiente: antes de escribir una acción que toca el producto, confirmar qué incluye la caja (estuche, película, precinto, accesorios). Ojo con «新旧タイプ混在発送».
- Misma regla añadida a la skill `ttchop-shotlist-storyboard`.

## [2026-11-22] create | Carpeta de caso 21_nanoglass en el NAS
- Creada `\\Polaris\Projects\tiktok\hamaca\edits\21_nanoglass` con `input/`, `plan/` y `production/` para el video de dadawoca ナノガラス ムダ毛ケア.
- `plan/` lleva el plan publicado (`index27.html`), `plan27.py`, `build_html27.py`, las 27 imágenes IA (`ai27/`) y el animatic ES. En la raíz, `21_nanoglass_MANIFEST.md` con el estado (PLAN, no filmado), la agrupación, las restricciones de la ficha y el aviso de props.
- El montaje `/mnt/polaris` del VPS está en solo lectura; la escritura se hizo por SMB directo con `/root/.hermes/tools/course-stt-venv/bin/python` y lectura de vuelta SHA-256 de cada archivo.

## [2026-11-23] create | Runbook de hooks al inicio de video + biblioteca de 12 hooks
- Creada [[hooks-para-inicio-de-video]] con la investigación (ventanas 1.5–3 s, umbrales 65–70 % a los 3 s, dato de 43 videos de TikTok Shop), las dos trampas (promesa que el producto no paga; **derechos de clips de terceros**), la plantilla de tiempos 0–3 s, el mapeo de los 12 hooks de referencia, el **shot list de 12 estilos propios** y la **matriz de 3 variantes** (dolor / curiosidad / resultado).
- Biblioteca creada en `P:\Tiktok\hamaca\assets\hooks\` con subcarpetas `origen_creadores\` (lote `2026-11-23_lote01`: 12 clips 720×1280, `indice.json`, hoja de contacto y `SHA256SUMS.txt`, lectura de vuelta verificada), `propios\` e `ia\`. **Decisión de Arturo: los 12 clips de terceros son referencia/mood y NO se publican**; el índice los marca `producto=generico` y `uso=referencia_mood_NO_publicar`.
- Shot list para grabar los 12 estilos propios: pendiente de generar el HTML de apoyo (el contenido ya está en §7 del runbook). Matriz de 3 variantes: solo la matriz, **sin** aplicarla todavía al `21_nanoglass` v3 (elección de Arturo).
- Lección operativa: los videos entregados **no siempre viven en `production/`** (la variación Announcer del blanket está en `11_blanket\variations\announcer_v1\`), así que un barrido que solo mire `production|delivery|output|final` los pierde. Verificar por caso antes de afirmar que algo no se montó.

## [2026-11-23] update | 21_nanoglass: el video existe (v1 → v3) y el manifiesto quedó corregido
- El `21_nanoglass_MANIFEST.md` decía «**Estado: PLAN. Aún no filmado**» y `production/` «vacío»: quedó obsoleto el mismo 22 por la tarde, cuando el caso se filmó (32 clips propios en `input/recordings/`; el montaje usa **27**) y se montó. Manifiesto **reescrito** en el NAS con el estado real, las tres entregas y el título.
- **v1** `production\nanoglass_edit_jp.mp4` — 18 554 079 B · 27 tomas · 32.06 s (voz de prueba edge-tts).
- **v2** `production\v2_announcer15\nanoglass_edit_jp.mp4` — **voz Announcer JP** (`gU0LNdkMOQCOrPrwtbee`, modelo `eleven_v3`) con `tts_lines.mjs` (7 líneas) y **`atempo=1.5`** (crudo 22.88 s → 15.44 s): **952 cuadros · 31.86 s · 18 428 518 B**.
- **v3** `production\v3_overlays\nanoglass_announcer15_overlays.mp4` — **956 cuadros · 31.867 s · 30 287 640 B** (+ `_chat` 11 289 153 B): overlays de la composición Remotion `caption-overlay` (`props_nanoglass21.json`: 7 captions encadenados, tag 「詳細は/画面左下」 + flecha, disco 「※個人の感想です」, `endCard`) y audio remuxeado del base **sin recodificar**.
- Montaje **en la PC PumaDeskAsus** (`build_edit_win.py` leyendo `Z:\…`, ver [[montaje-video-en-pc]]). Verificación: `ffprobe` (dimensiones/cuadros/duración/canales), niveles de audio, hojas de contacto y fotogramas revisados con visión, `SHA256SUMS.txt` con lectura de vuelta en cada entrega.
- Título/hashtags entregados en `production\v3_overlays\publicacion.json` (título + 3 alternativas). **Pendiente confirmar con Arturo**: el título escribe ナノ**グ**ラス y el nombre del producto es ナノ**ガ**ラス (el hashtag sí va con ガ).
- Nace del plan [[planes-de-video-nuevos]] (27 tomas / 31.77 s molde `03_suitcase`). **Sin publicar**: publica Arturo.

## [2026-11-23] update | 19/20_dualshaver: variaciones sobre el render de FilmCraft (guion nuevo, reorden, hook y portadas)
- **Se descubrió que se estaba derivando sobre el archivo equivocado.** El paneo y las voces nuevas se habían construido sobre el render del **pipeline** (`production\vN\…`), y Arturo lo rechazó: «no coincide lo que apunta la mano con las imágenes». **Su video es el render de FilmCraft**: 19 → 1335 cuadros · 44,501 s · **48 kHz estéreo**; 20 → 1067 · 35,5667 s · **48 kHz estéreo**; los del pipeline son **44,1 kHz mono**. Regla nueva y cómo distinguirlos (mtime, audio, cortes por `scdet`, velocidades por clip 71,43 %/80 %, deriva ~6 cuadros): [[recrear-video-creadores-edits]] **§8a**.
- Entregado **sobre su render** (sin modificarlo): `…_paneo.mp4` con el **shot 1 intacto** (el paneo se comía el borde donde está el producto); **`…_var_orden.mp4`** con **guion reescrito + reorden de tomas** (§8b); **`…_var_orden_hook.mp4`** con hook de 1,800 s al inicio, **offset de audio 0 ms**; y **portadas nuevas** (§8d).
- **Portadas:** el último cuadro del 20 ya trae la portada horneada (`1台2役で全身ケア / 顔・ワキ・腕・脚・VIO`) — copiarlo **repetía la original** y Arturo lo rechazó («debería ser una variación… diferente imagen diferente texto»); el del 19 sale **negro, también en su render** (el `endCard` del proyecto quedó vacío). Rehechas con **`KeinannMaruPOPjp`** (no el *fallback* Noto, que sale recto y delgado y rompe el formato) y bloque de texto medido en **x=540 / y=378** ±4 px.
- Cada archivo derivado lleva su `SHA256SUMS.txt` y su nota junto al original (`_nota.json`, `_hook.json`, `_cover.json`). Detalle por caso en las secciones **`19_dualshaver`** y **`20_dualshaver`** de [[recrear-video-creadores-edits]].

## [2026-11-24] create | tercer creador en el estudio: `taku_takkun_`
- Arturo pidió extender el estudio de creadores con un creador nuevo. Se corrió el pipeline parametrizado sobre **19 videos** de `taku_takkun_` (NAS `Projects\Tiktok\hamaca\creators_research\taku_takkun_\videos`): **19/19** medidos por código, **19/19** transcritos en GPU, **3** revisados con IA (3 llamadas, 72 imágenes, 150 590 tokens).
- **Publicado** en el hosting (verificado HTTP 200 + hash exacto): `https://lemonsushi.com/uploads/vps2/creators-research/taku_takkun_/index.html` (18 771 B) y `…/audiovisual-audit.html` (10 276 121 B). Copia privada en el NAS `taku_takkun_\creator-av-audit-taku-v1\`.
- **Asu/Sora intactos** (20 completos / 468 candidatos y 23 / 705; 4 881 hashes legacy verificados en Windows; 551 archivos protegidos del coordinador sin cambios). Código del estudio parametrizado (conteos 20/23 por defecto); commits locales `71aa024` y `18e9c7b`.
- Creado el remoto **privado** `github.com/pumacamargo/creator-av-audit` y pusheado el repo del estudio (solo código/docs; `.gitignore` excluye medios, resultados y QA privada).
- Actualizado [[estudio-creadores-fuentes-datos]] con la sección del tercer creador, los enlaces publicados y los datos de medición.

## [2026-11-24] create | dashboards del hosting documentados en cacho
- Creada [[dashboards-hosting]]: índice de los tableros publicados en el hosting Lemon Sushi y sus generadores — **dashboard central** (`/uploads/vps2/central/`, 4 grupos), **desmenuzados** (`/creators-research/`), **dashboard integrado del estudio con los 3 creadores** (Asu/Sora/Taku, `study-standard-3c-281212a2a442`, 26 632 479 B, SHA-256 `281212a2…`), la versión previa Asu+Sora conservada (`study-standard-63f35614c4fc`, `63f35614c4fc…`), los estudios por creador y los mapas de `docs/`.
- **Taku entró al dashboard integrado** del estudio (nueva versión, sin tocar la anterior): selector por creador Asu/Sora/Taku, 5 secciones, sin Hybrid. Generador en `creator-standardize` del perfil `developer`; pipeline y datos versionados en el repo privado `github.com/pumacamargo/creator-av-audit` (commit `f62bcc5`). Asu/Sora preservados (hash de datos antes = después).
- El **dashboard central** vive ahora en `/root/central/build_central.py` (auto-descubre los HTML por FTP, agrupa por creador/producto/caso, verifica por SHA-256). Enlazada la página nueva desde [[acceso-ftps-lemon-sushi]].

## [2026-11-24] fix | index.md: listar moonlight-sunshine-tv y limpiar archivo basura
- `operations/moonlight-sunshine-tv.md` existía pero **no estaba listado en `index.md`** (página huérfana). Añadido bajo **Hardware** (junto a [[chromecast-gtv-debloat]], temáticamente afín) con su resumen de una línea; `Total pages` 55 → 56.
- Eliminado el archivo basura `/root/cacho/ | head -40` (44 B, contenido `=: command not found`), residuo de un comando mal redirigido.

## [2026-11-24] create | dashboard central: grupo «Tareas» con la página ttJapan
- Añadido al dashboard central un grupo **«Tareas»** (primer botón) con la página **ttJapan**: checklist de tareas diarias de Arturo — 1) Request Samples de Asu, Sora y Taku; 2) Record 3 videos diarios; 3) Editar 3 videos diarios; 4) 1 video para cuenta nueva. El estado de cada casilla se guarda en el navegador (localStorage) y **se reinicia cada día**; incluye botón «Reiniciar el día».
- Página en `https://lemonsushi.com/uploads/vps2/tareas/ttjapan.html` (subcarpeta `/tareas/`); generador nuevo `/root/central/build_ttjapan.py` (vps-tools), que publica por FTPS y verifica por lectura de vuelta + SHA-256.
- `build_central.py` actualizado: excluye la carpeta `tareas` de «Otros» y la muestra en su grupo propio. El central pasa de 4 a **5 grupos**; verificado HTTP 200 + hash y revisado en navegador. Documentado en [[dashboards-hosting]].

## [2026-11-24] create | Tareas diarias del proyecto TikTok Shop (ttchop)
- Creada [[tareas-diarias-ttchop]] con la rutina diaria de Arturo para el proyecto TikTok Shop: 1) Request Samples de Asu, Sora y Taku; 2) Record 3 videos diarios; 3) Editar 3 videos diarios; 4) 1 video para cuenta nueva. Enlaza al checklist publicado (grupo «Tareas» → ttJapan) y a los creadores de referencia.
- Añadida al `index.md` (Operaciones); `Total pages` 56 → 57.

## [2026-11-24] create | Variación de 18_shaver: producto nuevo (prod_c6ftp5t) + PumaVoice + portada nueva + hook
- Arturo pidió una **variación** del video `18_shaver` cambiando el producto por uno parecido de la misma marca: `prod_c6ftp5t` (Enchenal Lab ボディシェーバー メンズ). Mismo caso, **no** un caso nuevo; los originales v1–v7 no se tocan.
- **Voz:** PumaVoice01 (`ve7BOdejheJbgrBriBx4`), guion **v2 adaptado** al producto nuevo (datos reales de la ficha: **2.9K** ventas · **4.3★** · **124** reseñas; vendedor Enchenal Lab PersonalCare; características 極小ヘッド / 銀イオン抗菌メッシュ刃 / VIO). Natural 82.96 s → `atempo=1.3819` → **60.04 s**. (Antes se generó una toma de prueba con **Charon** —Gemini en kie— que Arturo descartó: 1.75 créditos; Charon sigue siendo la Opción 1 general, PumaVoice se usa cuando él lo especifica.)
- **Overlays nuevos:** `hook_card1/2/3` con fotos del producto **A8** (recortes de la ficha), `sales` → **2.9K** + nombre, `reviews` → **4.3 / 124**; el resto (headline, seller, claims, conditions, cta) se mantiene. Aplicados con FFmpeg PNG sobre el **base limpio** (`v3/inputs/clean_base_v2_audio.mp4`).
- **Portada NUEVA** (regla de Arturo: **cada video y cada variación llevan thumbnail nuevo**):「全身これ1台 / 電動ボディシェーバー」, **KeinannMaruPOPjp** 80 px, centrada `x=540 / y=377.5` (medida con PIL), ≤2 líneas, con el producto visible. Distinta cuadro y distinto texto de la original.
- **Hook visual al inicio:** `hook05_gym_battle_rope` (54 cuadros = 1.8 s) empalmado por **JOIN** (audio en una pasada, `adelay=1800` exacto, hook al 35 %). Total **1855 cuadros · 61.84 s**. Clip de **terceros** (referencia/mood, **no publicable**).
- **QA:** frames por visión en cada ventana; `ffprobe` (1855 frames / 1080×1920 / 44.1 kHz mono); `volumedetect` (hook −42 dB, comercial −18.5 dB).
- **Archivos (local, vps-tools):** `/root/shaver18-v3-prodc6ftp5t/` (máster, con-hook, audio, assets, guion, render, QA). SHA-256: máster `a769c4a1…8a8a87`, con hook `5bdc9e1a…d2edb7c0`. **No se sube al NAS** (regla de Arturo, 26-nov: publica a mano).
- Registrado el procedimiento en la skill `ttchop-content-ops` → `references/variacion-cambiar-producto.md`; actualizado [[estandar-thumbnail-video]] con la regla de portada nueva.

## [2026-11-24] create | Voz de personaje con Gemini TTS en kie: Charon elegida y lineamientos de emoción
- Arturo probó varias voces y se quedó con **Charon** (`google/gemini-3-8-flash-tts` en kie.ai), tras comparar Fenrir, Autonoe, Sadachbia y Charon con la misma frase y el mismo `style`.
- **Probado y descartado**: Puck, Zephyr, Riko, Achird (salían afeminadas con un prompt de tono agudo — error mío: pedir "high-pitched/squeaky" a voces masculinas las lleva al falsete). También se comparó **ElevenLabs V3** (Jessica) y Arturo prefirió Gemini.
- **Aprendido**: el campo `style` dirige la actuación pero **no cambia el timbre**; "amigable" y "exagerado" se suman, no se sustituyen; el contraste (una línea susurrada entre exclamaciones) es lo que hace sonar exagerado; la puntuación es dirección de actuación; y un prompt de diseño de ~1,100 caracteres en `style` funciona peor que una versión de actuación de ~450.
- **Costo medido**: ~0.03 créditos por segundo de audio (frase de 9 s ≈ 0.30). ElevenLabs vía kie ≈ 3× más caro. Regla confirmada: **no generar sin "sí" explícito de Arturo** (hubo un gasto de 0.97 por adelantarme; no se repite).
- **No se puede**: usar IDs tipo `voice_pl1zhbthxsj7` en kie (solo 71 nombres fijos), ni diseñar/guardar un timbre nuevo en kie.
- Documentado en [[voz-personaje-kie]] con la receta exacta, el `style` aprobado, las etiquetas y la tabla de costos. Skill `kie-audio-voice` actualizada.
- **Corrección de Arturo**: sí hay voces definidas y por eso siempre se usa la misma. Están en el `README.md` de ttchop-server: **JP = Announcer (masculino) `gU0LNdkMOQCOrPrwtbee`**, **MX = Jessica `cgSgspJ2msm6clMCkdW9`**, y **PumaVoice01 `ve7BOdejheJbgrBriBx4`** (clonada) para traducciones. El `scheduler` las lee de una plantilla de voz en Firestore; el ritmo se ajusta después con FFmpeg (atempo 1.4–1.5× + pausas 0.3–0.34 s). Añadido a [[voz-personaje-kie]].
- **Jerarquía de voces definida por Arturo**: **Opción 1 = `Charon`** (Gemini 3.8 Flash TTS en kie), y como **plan B** las de ElevenLabs que ya usaban los videos (Announcer JP `gU0LNdkMOQCOrPrwtbee`, Jessica MX `cgSgspJ2msm6clMCkdW9`, PumaVoice01 `ve7BOdejheJbgrBriBx4`). Anotado el aviso: Charon no puede ser default automático sin añadir una rama de TTS por kie en `ttchop-server` (hoy `pipeline/elevenlabs.js` es el único camino); por ahora se usa a mano con la receta de [[voz-personaje-kie]].

## [2026-11-25] fix/create | Dos collages por ttchop-server (Charon) + fix del modelo LLM + overlays
- **Fix `pipeline/llm.js`** (ttchop-server): el modelo hardcodeado `openai/o4-mini` fue **retirado** por OpenRouter (404) y rompía `/collage/dialogue` y el paso de receta de `/collage/create`. Cambiado a **`openai/gpt-4o-mini`** (verificado vivo) vía el perfil `developer`; commit **`762371f`** en `master` (push verificado con `git ls-remote`). **Reinicio autorizado** de `ttchop-server` (cola vacía): health OK y `/collage/dialogue` volvió a responder **200**.
- **Video 1 — `prod_edpjxug`** (Enchenal Lab 電動シェーバー, jp): diálogo casual-creator con **hook exagerado** (plantilla `temp_y3w17i3` "25 sec"). Voz **Charon** (Gemini en kie): como el pipeline solo habla ElevenLabs, el audio se **pre-renderizó** con Charon y se pasó a `/collage/create` como **`audioBase64`** (+ `audioDurationSeconds`), con `voiceId` válido solo para la validación. Sesión `sess_a033wym` (3 clips). Render `render_mwvftb1u_edpjxug` → 1080×1920 · 602 frames · 20.07 s; audio intacto (20.08 s).
- **Video 2 — `prod_vp68hs3`** (air fryer liners de silicón, jp): mismo flujo. Sesión `sess_46dulev` (4 clips). Audio Charon 18.52 s → **1.5×** (12.35 s) por petición de Arturo; renders `render_mwvgevu0_vp68hs3` (18.5 s) y `render_mwvgjtnb_vp68hs3_1p5x` (12.37 s).
- **Overlays** (opción a): sobre el collage de 12.35 s se quemó la composición Remotion **`caption-overlay`** de `ttchop-post_templates` — captions cortos (píldora blanca), **tag** 「リンクは/画面下」 + **flecha** + **descargo** 「※価格や割引は投稿時点の情報です」, y **portada nueva** (endCard) 「お手入れラク / くり返し使える」 (KeinannMaruPOPjp 80 px, x=540 / y=378). Remux del audio del base (`-c copy`, sin `-shortest`); audio idéntico al base (−17.2 / −1.5 dB).
- **Charon en kie**: el modelo `google/gemini-3-8-flash-tts` devolvía **524** (timeout del proveedor, **sin costo**); su variante **`gemini-3-8-flash-lite-tts`** sí funcionó (misma voz). Costos medidos: 0.43 + 0.39 créditos.
- **Archivos locales (vps-tools)**: `/root/.hermes/profiles/ttchop_robot/media/…` + scratch. **No publicado.** No se sube al NAS (regla de Arturo, 26-nov: publica a mano).

## [2026-11-25] create | Tercer collage (`prod_v2y1zfp`) + overlays + visual hook
- **Video — `prod_v2y1zfp`** (pen borrador de etiquetas térmicas + cuchilla, jp; sesión `sess_xna6p84`, 6 clips): diálogo casual-creator con hook exagerado, voz **Charon** a **1.5×** (17.76 s → 11.85 s) inyectada como `audioBase64`. Render `render_mwvj5nfj_v2y1zfp_1p5x` → 1080×1920 · **60 fps** · 11.82 s; audio 11.85 s.
  - **Falla del primer intento** (`render_mwvj3qzd`): el LLM metió una **expresión aritmética** en el recetario (`"trimStart": 6.456056274193548 - 0.5`) → `callLLMJson: Expected ',' or '}' ... at position 390`. Es intermitente y recurrente (también 10/10, 14/10, 22/10). El reintento pasó.
- **Overlays** (`caption-overlay`, opción a) sobre el collage: captions 伝票そのまま捨ててない？ / 住所も名前も丸見え / なぞるだけで消せる / 箱もこれで開けられる + tag 「リンクは/画面下」 + flecha + descargo + **portada nueva**「なぞるだけで / 個人情報を隠せる」. Remux de audio del base: idéntico (−16.9 / 0.0 dB). Salida 1080×1920 · 30 fps · 356 frames · 11.87 s.
- **Visual hook** al inicio: `hook07_ejercicio_casa` (3.51 s) por **concat directo** (JOIN de 2 archivos, sin `amix`/`adelay`/`atrim`) → 461 frames (105+356) · 15.37 s. **Regla corregida y documentada en [[hooks-para-inicio-de-video]] §10**: agregar un hook = unir 2 videos; **no** se re-edita ni se re-renderiza el render, y no se toca su audio/overlays.
- Archivos locales en `media/`; **no publicado**. Hooks ya usados: `hook05`, `hook09`, `hook07`.

## [2026-11-25] create | Cuarto collage (`prod_yrikq4i`) con **Plan B (Announcer)** + overlays + hook
- **Voz:** Charon (kie) quedó **caído** todo el día — `524 generate task timeout` en **13 intentos** (dos modelos, incluso con texto mínimo; **sin costo**). Arturo autorizó el **Plan B**: **Announcer** (ElevenLabs JP, `gU0LNdkMOQCOrPrwtbee`), que sí vive en el pipeline.
- **Audio:** generado con la API de ElevenLabs (mismo `eleven_v3` + `voice_settings` del pipeline, speed 0.5) y pasado a **1.5×** con `atempo` (18.80 s → 12.53 s), inyectado como `audioBase64`.
- **Video — `prod_yrikq4i`** (pouch 3-way botella+smartphone, jp; sesión `sess_5187cbp`, 5 clips): render `render_mwvr3xak_yrikq4i_1p5x` → 1080×1920 · 30 fps · 12.50 s; audio 12.53 s.
- **Overlays** (`caption-overlay`): captions スマホも水筒も手で持ってる？ / 両手ふさがって不便だった / 肩にかけるだけで全部すっきり / 雨の日も中身は濡れない + tag/flecha/descargo + **portada nueva**「肩にかけるだけ / 両手が空く」. Audio idéntico al base (−15.5 / −0.8 dB).
- **Visual hook:** `hook10_caida_comedia` (2.32 s) por **concat directo** → 445 frames (69+376) · 14.85 s. **Regla §10 aplicada tal cual** (JOIN de 2 archivos).
- Hooks ya usados: `hook05`, `hook07`, `hook09`, `hook10`. Archivos locales; **no publicado**.

## [2026-11-26] create | Quinto collage (`prod_c6ftp5t` en **ttchop2**) con clips nuevos + overlays + hook
- **Clips nuevos:** Arturo subió hoy (26-nov) **12 clips** a **ttchop2** para `prod_c6ftp5t` (Enchenal Lab ボディシェーバー メンズ) → **sesión nueva `sess_nzxwh8z`** (creada 2026-11-26 02:10 UTC), todos `source: recorded`, 8.0–33.2 s. Son tomas **de producto en mano** (unboxing), sin tomas de uso.
- **Voz:** kie seguía caído (524) → **Plan B Announcer** (ElevenLabs JP) generado aparte y a **1.5×** (18.16 s → 12.12 s), inyectado como `audioBase64`.
- **Render:** `render_mwx1qvjv_c6ftp5t_new` en **proyecto `ttchop2`** (`getDb('ttchop2')`; los renders y sesiones se leen de ese proyecto, no del default) → 1080×1920 · 30 fps · 12.11 s.
- **Overlays** (`caption-overlay`): まだカミソリで処理してる？ / 肌が荒れるし剃り残しも / 肌に当てるだけでツルツル / 細かいところもラクにケア + tag/flecha/descargo + **portada nueva**「肌に当てるだけ / ツルツル肌へ」. Audio idéntico al base (−15.7 / −0.7 dB).
- **Visual hook:** `hook01_pov_moto` (**2.60 s**) por concat directo → 442 frames (78+364) · **14.73 s**. Se
  descartó `hook12` (17.4 s) porque **la regla nueva es hook ≤3 s** (Arturo, 26-nov): si el clip dura más, se
  recorta al tramo del mejor beat. Duraciones medidas de la biblioteca: `hook01` 2.60 · `hook04` 2.60 ·
  `hook03` 3.25 · `hook02` 3.27 · `hook08` 4.50 · `hook06` 5.85 · `hook11` 6.85 · `hook12` 17.4 s.
- Hooks ya usados: `hook05`, `hook07`, `hook09`, `hook10`, `hook12` (descartado), `hook01`. Archivos locales; **no publicado**.

## [2026-11-26] create | Sexto collage (`prod_0skgwd3`, teclado AJAZZ AK820) + overlays + hook recortado
- **Producto:** AJAZZ AK820 (teclado mecánico gaming 75%, hot-swap, perilla, gasket) — región jp, sesión `sess_ozjfvbw` (6 clips).
- **Voz:** kie seguía caído (524) → **Announcer** generado aparte y a **1.5×** (18.88 s → 12.59 s), inyectado como `audioBase64`.
- **Render:** `render_mwx31pwh_kbd_1p5x` (el primero, `render_mwx30wlu`, falló con `Unknown source clip at recipe index 3` — el LLM generó un clip de relleno con origen inválido; el reintento pasó). 1080×1920 · 30 fps · 12.57 s.
- **Overlays** (`caption-overlay`): そのキーボード打ちにくくない？ / 打鍵感って本当に大事 / 押した瞬間カチッと決まる / キーを全部自分好みに + tag/flecha/descargo + **portada nueva**「押した瞬間 / カチッと決まる」. Audio idéntico al base (−16.1 / −0.4 dB).
- **Visual hook:** `hook03_demolicion` **recortado a 3.0 s** (el original 3.25 s; el beat del golpe queda dentro) — **primera aplicación de la regla hook ≤3 s**. Concat directo → 468 frames (90+378) · 15.6 s.
- **Entrega:** los videos se mandan también en versión mínima (720×1280, H.264 baseline + AAC mono) porque las versiones grandes no llegaban por Telegram.
- Hooks ya usados: `hook05`, `hook07`, `hook09`, `hook10`, `hook12` (descartado), `hook01`, `hook03`. Archivos locales; **no publicado**.

## [2026-11-26] fix | «No me mandaste el video» — entrega por Telegram
- **Diagnóstico con evidencia:** los logs del gateway son **por perfil** (`profiles/ttchop_robot/logs/gateway.log`, no el global). Una entrega normal deja `Delivering 1 non-image MEDIA attachment(s)` + `Sending video attachment (.mp4)`; un archivo ausente deja `Skipping MEDIA directive path (not found on this host)`. **El caso que falla no deja ninguna de las dos**: el turno termina en `Sending response (N chars)` y el tag `MEDIA:` nunca llegó al texto despachado.
- **Fix adoptado:** entregar el video **directo por la Bot API** (`sendVideo`) con el token del perfil y el chat `6407630145`, **verificando** `ok: true` + `message_id`. Script: [[entrega-de-videos-telegram]] / `scripts/tg_send_video.py`. Prueba real: `message_id 5221` (test) y `5223` (teclado AJAZZ, 2.0 MB).
- **Formato para el chat:** 720×1280 · H.264 baseline · AAC mono (~2 MB); los másters 1080×1920 se conservan aparte.
- **Regla:** si el video importa, se manda por el script y se reporta el `message_id`; el tag `MEDIA:` no es garantía.

## [2026-11-26] create | Séptimo collage (`prod_0lyigbp`, scrubber eléctrico) con **Charon energético 1.25×**
- **Producto:** Electric Spin Scrubber (inalámbrico, display LED, 7 cepillos; baño/piso/auto/tile) — `jp`, 4.1★, 18.5K vendidos; sesión `sess_y21dfje` (8 clips).
- **kie revivió** ese día: el test mínimo (`gemini-3-8-flash-lite-tts`) pasó y Charon se generó, pero **los 524 siguen siendo intermitentes** (falló 1 de cada 2 intentos).
- **Energía de voz:** Arturo pidió más energía → se cambió el `style` de «comercial carismático» a **explosivo/rapid-fire** (oleadas de entusiasmo, caídas conspiratorias, urgente y juguetón, cálido y sin falsete). Misma frase para poder comparar.
- **Velocidad:** se probaron las tres y Arturo eligió **1.25×** (18.16 s → 14.53 s). Las otras quedaron medidas: 1.0× = 18.16 s, 1.5× = 12.11 s.
- **Render:** `render_mwxdaoaa_scrub_energy125` · `done` al **2º intento** (el 1º, `render_mwxd9vxi`, cayó por el bug del recetario: `"trimStart": 5.146… - 1.0`). 1080×1920 · 30 fps · 14.53 s.
- **Entrega:** por `sendVideo` verificado (`message_id 5282`); audio por `sendAudio` verificado (`5261` 1.5×, `5265` 1.0×, `5269` 1.25×).
- **Pendiente sugerido:** endurecer `callLLMJson` (delegar al `developer`) — el bug de la aritmética ya tumbó **3 renders** en dos días.
- **Segunda pasada (mismo día):** Arturo pidió **otra edición desde cero** con el mismo audio (`render_mwxemzsj_scrub_newedit`) y luego **quitó un clip** de la sesión (quedó de 8 → **7 clips**, fuera `vid_ma1sodw` de 47.4 s) → re-edición `render_mwxgxgyn_scrub_7clips` (14.53 s). Sobre esa se quemaron **overlays** (captions まだ手でゴシゴシしてる？ / 腰も痛いし汚れも残る / スイッチひとつで自動できれい / ブラシを替えれば1本で全部 + tag/flecha/descargo + portada「スイッチひとつで / 掃除ラクラク」) y el hook `hook04_estructura_madera` (2.60 s, ≤3 s) → 514 frames · 17.13 s. Entregas verificadas: `5282`, `5291`, `5299`, `5311`.

## [2026-11-26] create | Cuentas de TikTok Shop affiliate y research de nicho para hamaca azul
- Arturo pidió un apartado de **cuentas de TikTok Shop affiliate**: **hamaca shop** es la principal y **todo el contenido hasta hoy es exclusivo de ella**; está creando **hamaca azul** como **cuenta secundaria nueva**, con objetivo de **subir seguidores primero** y después vender affiliate. Documentado en [[cuentas-tiktok-shop-affiliate]], con la regla de que el contenido no se recicla entre cuentas.
- **Extracción de un video** (23.5 s, Creator Search Insights, pestaña *Photo posts*): 23 cuadros, OCR con tesseract (jpn+eng) + lectura cuadro por cuadro de 15 fotogramas → **56 temas** (40 en japonés, 16 en inglés) con vistas y crecimiento. Crudos guardados en `raw/creator-search-insights-2026-11-26.csv` y `.md`.
- **Research de nicho** en [[nicho-cabello-tiktok]]: agrupados en 6 grupos, **cabello concentra el 87 %** de la demanda (27 temas, 17 por encima del piso) y **12 de los 15 primeros puestos**; salto grande entre el puesto 15 y 16 (168K → 30.7K, 5.5×). Nicho elegido para hamaca azul: **cabello → accesorios y herramientas de peinado** (pinzas 293K ▲1,000 %+, cabello ondulado 221K ▲1,000 %+, artículos de estilizado 344K ▲85.4 %), con plan B de bolsos (319K) y hogar (199K). Descartados tecnología y belleza (todo en el piso 99–400).
- **Advertencia registrada**: la herramienta mide **demanda, no competencia ni ingresos**, y es una sola captura de una cuenta; la mitad baja de la lista son valores de piso. Pendiente: validar competencia por tema y armar el plan de los primeros 10 videos.
- **Los 3 temas del nicho guardados con su japonés** (para poder buscar los posts después) en [[nicho-cabello-tiktok]]: **pinzas de cabello suaves** (293K ▲1,000 %+ — apareció **en inglés** en la herramienta, se añadió traducción al japonés), **rutina para cabello ondulado/rizado** (221K ▲1,000 %+ — original `くせ毛さんに◎おすすめのヘアケアルーティン`) y **artículos para estilizar** (344K ▲85.4 % — original `ヘアスタイリングにおすすめのアイテム`). Cada uno con términos de búsqueda en japonés. Aclarado también en la página que el **formato del contenido son carruseles de imágenes**, que es justo lo que mide la pestaña *Photo posts* de donde salieron los datos.

## [2026-11-26] extract | Segundo video de Creator Search Insights: pestaña *Suggested* (Searches by followers)
- Arturo mandó un segundo video (25.5 s) de la misma herramienta, ahora en la pestaña **Suggested** con el filtro **Searches by followers** (y el interruptor *Content gap*). Extraída con el mismo método: 25 cuadros, OCR de tesseract con **preprocesado mejorado** (recorte de la columna de texto + escala 4× + gris/contraste) y **lectura visual de los 25 cuadros** (el OCR solo no bastaba: dejaba fragmentos de líneas cortadas).
- **105 búsquedas** en total; el video termina en *“No more searches”*, así que la lista está completa. Guardada en `raw/creator-search-insights-2026-11-26-videos-suggested.md` con el orden del video y un top 25 por vistas.
- **Contenido muy distinto al de la lista de carruseles**: aquí es **cultura pop japonesa** (anime, videojuegos, famosos, memes), no producto. Los mayores: 私の魂の色 6.53M, 彼氏 848K, デスノート 429K, 多摩川で恋してみたい 330K. De cabello solo aparece 髪ゴム腕につける意味 (7.9K) y 男子中学生 髪型 (599) — o sea, el nicho de cabello **no** se refleja en esta pestaña.
- Lectura: esta pestaña sirve para **temas de entretenimiento/tendencias**, no para elegir nicho de producto; el nicho de producto se decidió con la lista de *Photo posts* ([[nicho-cabello-tiktok]]).

## Índice de videos recientes (nov-2026)

Piezas hechas con el pipeline `ttchop-server` (`/collage/create`) + voces + overlays + hook visual.
**Ninguna publicada.** Los másters viven en `~/.hermes/profiles/ttchop_robot/media/` (vps-tools) y en
`cache/scratch/`; los hooks en `P:\Tiktok\hamaca\assets\hooks\origen_creadores\2026-11-23_lote01\`.

| # | Producto | Caso | Voz (velocidad) | Collage | Final (+overlays+hook) | Hook | Archivo final |
|---|---|---|---|---|---|---|---|
| 1 | `prod_c6ftp5t` | `18_shaver` (variación) | PumaVoice01 1.38× | 60.04 s | 61.84 s | `hook05` (1.80 s) | `shaver18_v3_prod_c6ftp5t_hook05.mp4` |
| 2 | `prod_edpjxug` | collage | Charon 1.0× | 20.08 s | — | — | `edpjxug_collage_charon.mp4` |
| 3 | `prod_vp68hs3` | collage | Charon 1.5× | 12.37 s | 14.17 s | `hook09` (2.04 s) | `vp68hs3_overlay_hook09.mp4` |
| 4 | `prod_v2y1zfp` | collage | Charon 1.5× | 11.87 s | 15.37 s | `hook07` (3.51 s) | `v2y1zfp_overlay_hook07.mp4` |
| 5 | `prod_yrikq4i` | collage | **Announcer** 1.5× | 12.50 s | 14.85 s | `hook10` (2.32 s) | `yrikq4i_overlay_hook10.mp4` |
| 6 | `prod_c6ftp5t` (ttchop2) | clips nuevos | **Announcer** 1.5× | 12.11 s | 14.73 s | `hook01` (2.60 s) | `shaver_new_overlay_hook01.mp4` |
| 7 | `prod_0skgwd3` | teclado AJAZZ AK820 | **Announcer** 1.5× | 12.57 s | 15.60 s | `hook03` (3.00 s, **recortado**) | `kbd_overlay_hook03.mp4` |
| 8 | `prod_0lyigbp` | scrubber eléctrico | **Charon energético** 1.25× | 14.53 s | 17.13 s | `hook04` (2.60 s) | `scrub_overlay_hook04.mp4` |

- **Overlays** (todos salvo #1 y #2): composición Remotion `caption-overlay` — captions, tag 「リンクは/画面下」,
  flecha, descargo 「※価格や割引は投稿時点の情報です」 y **portada nueva** en cada pieza.
- **Entrega al chat:** `sendVideo`/`sendAudio` de la Bot API con verificación `ok`/`message_id`
  ([[entrega-de-videos-telegram]]); los `message_id` de las últimas: 5282, 5291, 5299, 5311.
- **Publicación y almacenamiento (regla de Arturo, 2026-11-26):** **él publica a mano** y **no hace falta subir
  los videos al NAS** — los archivos se quedan en `~/.hermes/profiles/ttchop_robot/media/` (vps-tools). No
  proponer subidas al NAS ni marcarlo como pendiente.
- **Hooks ya usados:** `hook01`, `hook03`, `hook04`, `hook05`, `hook07`, `hook09`, `hook10`; `hook12` descartado
  por largo. Sin usar: `hook02`, `hook06`, `hook08`, `hook11`.
- **Bug del recetario — ARREGLADO (commit `44cc142`, 26-nov):** `pipeline/llm.js` ahora pide
  `response_format: json_object`, **evalúa las expresiones aritméticas** fuera de cadenas cuando el parseo
  estricto falla y hace **un reintento correctivo**; verificado con 5 casos (5/5). **Reinicio autorizado y
  aplicado el 26-nov** (`ttchop-server` online, health 200, path JSON verificado en vivo).

## [2026-11-26] fix | Bug del recetario (`callLLMJson`) arreglado en el repo
- **Qué pasaba:** el LLM del recetario escribía una **expresión aritmética** en un campo numérico
  (`"trimStart": 5.146147180107526 - 1.0`) → JSON inválido → el render quedaba `failed` **sin `error` en el
  doc**. Tumbó 3 renders (`render_mwvj3qzd`, `render_mwxd9vxi` y otro el 25-nov).
- **Fix (`pipeline/llm.js`, commit `44cc142` en `master`):**
  1. `callLLM` acepta `jsonMode` y manda `response_format: { type: 'json_object' }` en el path JSON.
  2. Si el parseo estricto falla, `repairJsonArithmetic` **evalúa `NUM <op> NUM` fuera de cadenas** (nunca
     toca un documento que ya parsea) y reintenta el parseo.
  3. Un **reintento correctivo** con el error en el prompt.
- **Verificación:** 5 casos (el roto real, suma/división, JSON válido que **no** debe cambiar, exponentes
  `1e-5`, aritmética dentro de strings) → **5/5 PASS**; y el import del módulo con la reparación funcionando.
- **Desplegado:** reinicio autorizado por Arturo y aplicado — `ttchop-server` `online`, health **200**, el
  path JSON del módulo desplegado devuelve objeto con números (verificado en vivo). Respaldo del archivo viejo
  en `/root/llm.js.bak-*` (vps-projects).

## [2026-11-26] create | Desmenuzado de carrusel (método + caso 01: frases de Adler)
- Arturo pidió empezar a **generar carruseles de imágenes** (no video) para la cuenta nueva, y **recrear uno**: primero **desmenuzarlo**, luego **crearlo con variación** para hacer contenido único. Regla que fijó: **el desmenuzado de carrusel NO se mezcla con el de video** (procedimientos y artefactos distintos).
- **Entrada:** 11 imágenes (960×1280, 3:4) de una cuenta JP de frases (アドラー心理学), mandadas el 26-nov. **10 son contenido**; la **#11 es un anuncio de la app Motto** que Arturo pidió **ignorar**.
- **Método y caso documentados** en [[desmenuzado-carrusel]]: ficha técnica **medida** (fondo **idéntico en los 10 slides** — diferencia de fondo ≈0,2/255; texto blanco **#ffffff** centrado sin caja con sombra; gothic/rounded sans; cuerpo ≈48 px de tinta e interlineado ≈83 px a 960 de ancho; atribución fija 「アドラー心理学」; bloque centrado verticalmente a **≈53 %**), más los 10 slides con **JP original + traducción ES** y el **arco narrativo** (hook → … → cierre).
- **Artefacto:** nuevo store **separado** `/root/desmenuzados-carrusel/C01_adler-psicologia/` (`desmenuzado.md` + `slides/01..10.jpg` + `11_CTA_Motto_IGNORADO.jpg`), verificado por SHA-256. **No** en `/root/desmenuzados` (índice de video) ni en el dashboard `creators-research`.
- **Pendiente (Fase 2):** tema/temática de las frases, imagen de fondo (propia vs. reutilizada), y título/hashtags. Sin arrancar.

## [2026-11-26] create | Recreación del carrusel C01 (Adler) — Fase 2 montada
- Arturo mandó la imagen de fondo (`chmc-dubai.com/…/Alfred-Adler.jpg`, 432×553) y pidió: **cambiar el estilo del diseño (la fuente)**, **agregar un número de orden** y **blanco y negro** (no sepia). Fondo = misma imagen, diseño distinto.
- **Diseño elegido:** tipografía **`Noto Sans CJK JP` Bold** (gothic) 64 px / interlineado 98; texto blanco centrado con sombra; atribución 「アドラー心理学」; **número «N / 10» abajo**; bloque centrado a ≈53 %. Fondo B/N escalado a 1080×1440 con viñeta.
- **Fuentes disponibles vistas** (solo 3 familias JP reales en los hosts + mono): `KeinannMaruPOPjp` (redondeada, estándar de portadas ttchop, `/root/dualshaver-announcer/`), `Noto Sans CJK JP`, `Noto Serif CJK JP`. Se previsualizaron las 3; Arturo eligió la **sans**.
- **Entregado:** `final/01..10.png` (1080×1440, PNG, individuales) en `/root/desmenuzados-carrusel/C01_adler-psicologia/`; script `build_slides.py`. **Sin publicar** (publica Arturo).
- **Aviso dado:** el texto sigue siendo el **mismo** de la referencia (solo cambió el diseño); pendiente decidir si se reescriben las frases y el título/hashtags.
