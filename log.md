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
