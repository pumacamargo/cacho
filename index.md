# Wiki Index

> Catálogo de contenido. Toda página listada bajo su tipo con un resumen de una línea.
> Léeme primero para encontrar páginas relevantes para cualquier consulta.
> Last updated: 2026-10-31 | Total pages: 46

## Persona
- [[arturo]] — perfil: biografía, carrera (rigger), ubicación, gustos y preferencias

## Categorías de proyectos
- [[categorias-proyectos]] — mapa de las 6 categorías de proyectos de Arturo
- [[categoria-backpack]] — aprendizaje/práctica (Japanese, Drums, Draw, Singing)
- [[categoria-macanishi]] — proyectos familiares (Travel, Farmers)
- [[categoria-tts]] — TikTok Shop (ttchop affiliate, Lemon Sushi seller)
- [[categoria-moon]] — proyectos financieros (moon-sto, moon-fut)
- [[categoria-cliff]] — creación de contenido (Apex, Papa, Tacosdepulpo, Chava)
- [[categoria-sandbox]] — desarrollo (App, Game, Shortfilm)

## Proyectos
- [[proyecto-japanese]] — aprendizaje de japonés (Backpack)
- [[proyecto-drums]] — práctica de batería (Backpack)
- [[proyecto-draw]] — dibujo (Backpack)
- [[proyecto-singing]] — canto (Backpack)
- [[proyecto-travel]] — automatización de viajes + potencial vlog (Macanishi)
- [[proyecto-farmers]] — booth de tacos en farmers markets (Macanishi)
- [[ttchop]] — TikTok Shop affiliate, pipeline scout→producer (TT's)
- [[proyecto-lemon-sushi]] — TikTok Shop seller, playeras impresas (TT's)
- [[proyecto-moon-sto]] — portafolio de inversiones (Moon)
- [[proyecto-moon-fut]] — daytrading de futuros (Moon)
- [[proyecto-app-development]] — desarrollo de apps (Sandbox)
- [[proyecto-game-development]] — desarrollo de videojuegos (Sandbox)
- [[proyecto-shortfilm-development]] — desarrollo de cortometrajes (Sandbox)
- [[proyecto-ttchop]] — proyecto software ttchop: web app + editor de video + bot
- [[ttchop-automatizaciones]] — automatizaciones del bot (scheduler, pipeline scout→producer, defaults de render)
- [[ttchop-webapps]] — webapps ttchop/ttchop2: dashboard, productos, video, Analytics, distinción sales_file/sales_reference y límites de archivos fuente, acceso seguro y carruseles

## Hardware
- [[hardware-inventario]] — resumen de todo el hardware + red Tailscale
- [[hardware-vps-tools]] — VPS principal (este host), corre Hermes
- [[hardware-vps-projects]] — segundo VPS para proyectos
- [[hardware-raspberry-pi5]] — Raspberry Pi 5 (pi5puma01)
- [[hardware-desktop-puma]] — desktop Windows (PumaDeskAsus)
- [[hardware-celular-android]] — celular Android (draft)

## Sistemas
- [[hermes-agent]] — agente Hermes en vps-tools; voz local Vosk aislada y TTS es-MX
- [[hermes-agentes]] — agentes persistentes de Hermes (research, developer, jr_developer, ttchop_robot)

## Operaciones
- [[acceso-ftps-lemon-sushi]] — FTPS verificado al hosting; raíz /public_html/uploads/vps2, subcarpetas obligatorias, URL base y límites de privacidad pública
- [[acceso-nas-polaris]] — orden de acceso: SMB directo VPS→NAS primero; 5 MP4s y 3 PNGs escritos y verificados con hash de vuelta; Windows por IP/FQDN si se necesita; wrapper corto histórico conservado
- [[acceso-remoto-pumadeskasus]] — alternativa Windows: SSH por Tailscale, encendido/apagado y PowerShell a Polaris/P: con pumassh; mantiene historial y límites, no habilita acceso nativo global
- [[diagnostico-espacio-disco-vps]] — auditoría de solo lectura del disco: 96 % usado; Docker (~48 GB), caché npm (11 GB) y logs de contenedores sin rotación; 35–45 GB liberables, limpieza pendiente de autorización
- [[estudio-creadores-fuentes-datos]] — inventario del estudio de Asu y Sora: 43 videos y transcripciones en el NAS, 13 reportes publicados, historial de 11 versiones del estudio y dónde vive cada medición
- [[transcripcion-curso-gerardo-santiago]] — ocho videos originales del curso: transcripción NAS→TXT, hashes, reanudación y límites STT
- [[separar-videos-nas-por-cortes]] — FFmpeg y revisión visual para segmentar Juice/EllisWhite, cuatro partes iguales y QA de entrega al NAS; entregas Tagilas/Shampoo registradas en log.md el 2026-10-27
- [[ttchop-carousel-creation]] — runbook: Kie.ai local, composición de carruseles, créditos, autenticación y QA
- [[ttchop-video-generation]] — runbook: flujos UI/collage y traducción manual `ttchop-server` → FilmCraft con 3 pistas por defecto; Producer no usa FilmCraft
- [[ttchop-raw-asset-manual-edit]] — edición Producer-style sin catálogo; casos Juice Discount/ELLISS y Ellis if01; tres overlays nuevos, clips IF01 01–03 y montaje continuo 01–02–03 con instrumental aprobado actualizados en Polaris
- [[ttchop-filmcraft-video-tests]] — runbook FilmCraft (flujo local-first autorizado en `D:\staging`, transferencia a Polaris, relink/export/QA) y estado por caso: MAGINA Tagiras completado; Ellis if01 portable copiado y hash-verificado en Polaris, con reapertura GUI pendiente; no mezclar proyectos entre productos
- [[ttchop-music-generation]] — runbook: canto manual con ElevenLabs Music, montaje vía `audioBase64`, QA de duración y límites de publicación
- [[traduccion-video-pumasvoice-sincronizada]] — traducir ES→JA con TTS PumaVoice, alinear inicio/fin de voz mediante atempo/adelay, conservar imagen y medir créditos reales; no lip-sync

## Repositorio
- [[cacho]] — wiki versionada: aplicar documentación y código pedidos directamente en main; preservar autorización separada para producción/infra

## Concepts

## Comparisons

## Queries
