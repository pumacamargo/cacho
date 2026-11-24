# Wiki Index

> Catálogo de contenido. Toda página listada bajo su tipo con un resumen de una línea.
> Léeme primero para encontrar páginas relevantes para cualquier consulta.
> Last updated: 2026-11-24 | Total pages: 56

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
- [[chromecast-gtv-debloat]] — runbook: limpiar la Chromecast con Google TV 4K (CleanYourTV); acceso por depuración inalámbrica, respaldo previo y regreso con una línea
- [[moonlight-sunshine-tv]] — runbook: poner el escritorio de la PC en la Chromecast con Moonlight (TV) + Sunshine (PC); por qué se descartaron Chrome Remote Desktop y RDP, instalación, emparejado y verificación NVENC

## Sistemas
- [[hermes-agent]] — agente Hermes en vps-tools; voz local Vosk aislada y TTS es-MX
- [[hermes-agentes]] — agentes persistentes de Hermes (research, developer, jr_developer, ttchop_robot)

## Operaciones
- [[acceso-ftps-lemon-sushi]] — FTPS verificado al hosting; raíz /public_html/uploads/vps2, subcarpetas obligatorias, URL base y límites de privacidad pública
- [[dashboards-hosting]] — tableros publicados en el hosting Lemon Sushi: dashboard central (4 grupos), desmenuzados, estudio integrado con los 3 creadores (Asu/Sora/Taku), estudios por creador y mapas; con sus generadores y reglas
- [[acceso-nas-polaris]] — orden de acceso: SMB directo VPS→NAS primero; 5 MP4s y 3 PNGs escritos y verificados con hash de vuelta; Windows por IP/FQDN si se necesita; wrapper corto histórico conservado
- [[acceso-remoto-pumadeskasus]] — alternativa Windows: SSH por Tailscale, encendido/apagado y PowerShell a Polaris/P: con pumassh; mantiene historial y límites, no habilita acceso nativo global
- [[diagnostico-espacio-disco-vps]] — auditoría de solo lectura del disco: 96 % usado; Docker (~48 GB), caché npm (11 GB) y logs de contenedores sin rotación; 35–45 GB liberables, limpieza pendiente de autorización
- [[estandar-thumbnail-video]] — **estándar fijo de portada/thumbnail**: 1080×1920, último fotograma, ≤2 líneas JP, KeinannMaruPOPjp Regular 400, fontSize 80 / lineHeight 1.15 / #ffffff + contorno #101010 (6), texto **siempre centrado (x=540) con centro del bloque en y=378** (19.7 %) vía `endCard` prop-driven; incluye las mediciones reales de `17_carpet` y `18_shaver` (se quedan como están, Arturo 2026-11-19) y la verificación de que **19 y 20 sí cumplen**; desde el **2026-11-23** añade la trampa del **último cuadro en negro** (el `endCard` puede quedar vacío, también en el render de Arturo), cómo **recomponer** una portada a mano con **KeinannMaruPOPjp** (no el *fallback* Noto: rompe el formato) y **la portada de una variación** (otro cuadro y otro texto)
- [[estudio-creadores-fuentes-datos]] — inventario del estudio de creadores (Asu, Sora y desde 2026-11-24 Taku): 43+19 videos y transcripciones en el NAS, reportes publicados, historial de 11 versiones del estudio y dónde vive cada medición
- [[montaje-video-en-pc]] — montar con `collage_builder` en la PC: causa real (CIFS del VPS a ~0,12 MB/s por 243 ms de latencia), comparación medida **10.4 s vs 213 s** para la misma receta, montador adaptado a Windows, requisitos que ya existen en la máquina y las trampas resueltas
- [[recrear-video-creadores-edits]] — runbook: recrear un video de creador paso a paso (transcripción en la PC, desglose script/recordings/editing, **lista de shots para grabar en HTML con GIFs** y publicación por FTPS, variación de guion, TTS, montaje con `ttchop-server` leyendo el NAS por CIFS y subtítulos/overlays con la composición Remotion `caption-overlay`); casos verificados **`10_squishy01`**, **`11_blanket`**, **`12_suitcase`**, **`13_NachoShampoo01`**, **`17_carpet`**, **`18_shaver`**, **`19_dualshaver`** y **`20_dualshaver`** (los tres primeros reubicados el 2026-11-05 en `tiktok/hamaca/edits/`, con los archivos internos bajo su prefijo viejo `01_/02_/03_`; `12_suitcase` trae **dos productos**: `cicilife` y `other`); **§8 «hacer una variación»** — con **§8a–8d** desde el 2026-11-23: la base correcta es **el render de FilmCraft que terminó Arturo** (no el del pipeline; 48 kHz estéreo vs 44,1 mono), variación con guion nuevo y **reorden de tomas**, hook visual al inicio y **portada de la variación** — y cada caso entregado lleva un **`<caso>_MANIFEST.md`** en el NAS con el mapeo plano→clip, la voz, los captions y la cadena de comandos para rehacerlo (la **segunda parte** de 02_blanket — overlays y montaje dentro de FilmCraft — se documenta en [[ttchop-filmcraft-video-tests]])
- [[transcripcion-curso-gerardo-santiago]] — ocho videos originales del curso: transcripción NAS→TXT, hashes, reanudación y límites STT
- [[transcripcion-gpu-pumadeskasus]] — runbook: transcribir en la PC con GPU leyendo el NAS por SMB; las tres trampas (parche spnego/ntlm, credenciales multilínea por stdin, mapeo imposible por SSH) y por qué el VPS muere con audio largo
- [[separar-videos-nas-por-cortes]] — FFmpeg y revisión visual para segmentar Juice/EllisWhite, cuatro partes iguales y QA de entrega al NAS; entregas Tagilas/Shampoo registradas en log.md el 2026-10-27
- [[ttchop-carousel-creation]] — runbook: Kie.ai local, composición de carruseles, créditos, autenticación y QA
- [[ttchop-popup-book-commercial]] — comercial Enchenal con Lemo-Opuscar/Three.js: cuento continuo, poses Kie en una generación, voz japonesa a 1.5×, storyboard, cámara sutil y reconstrucción de la entrega final `v3_fixed`
- [[ttchop-vox-collage-commercial]] — build VOX Enchenal separado del Book: HyperFrames, ocho escenas, Announcer JP, variación de imágenes Kie aprobadas y reproducción offline de `vox_shaver_full_announcer_images_v2.mp4`
- [[ttchop-video-paths]] — **punto de entrada**: las 3 vías (más 1 sub-caso y 1 entorno alternativo) para hacer un video, cuándo usar cada una, qué necesitas y las piezas compartidas (`collage_builder`, `caption-overlay`, PumaVoice, manifiestos por caso); incluye **dónde montar** (VPS por CIFS o **PC ~20× más rápida**, [[montaje-video-en-pc]])
- [[planes-de-video-nuevos]] — runbook: armar un plan de video para un producto que **aún no se ha filmado** (shot list HTML con las 3 vistas + imágenes IA + animatic); la estructura y los tiempos salen de un desmenuzado pasado y el **guion sale de la documentación de Asu** (4 movimientos, familias de apertura, reglas de honestidad); incluye puertas de calidad, pitfalls y un changelog para que el documento siga creciendo con cada plan nuevo
- [[hooks-para-inicio-de-video]] — runbook: **cómo usar un clip de hook al inicio** (visual + texto + VO apuntando a la misma idea), las ventanas y umbrales de retención, el dato de 43 videos de Shop (los ganadores abren con una persona/momento/resultado, no con el producto), las dos trampas (promesa que el producto no paga y **derechos de clips de terceros**), la plantilla de tiempos 0–3 s, el mapeo de los **12 hooks de referencia** de la biblioteca (no publicables), el **shot list de 12 estilos propios** para grabar en una sesión y la **matriz de 3 variantes** (dolor / curiosidad / resultado) para A/B; **§10 el empalme (prepend)** con la receta y las trampas medidas (audio en una sola pasada de filtro con `adelay` exacto, y el offset medido por **mínimo del RMS de la diferencia**)
- [[ttchop-video-generation]] — runbook: flujos UI/collage y traducción manual `ttchop-server` → FilmCraft con 3 pistas por defecto; Producer no usa FilmCraft
- [[ttchop-raw-asset-manual-edit]] — edición Producer-style sin catálogo; casos Juice Discount/ELLISS y Ellis if01; tres overlays nuevos, clips IF01 01–03 y montaje continuo 01–02–03 con instrumental aprobado actualizados en Polaris
- [[ttchop-filmcraft-video-tests]] — runbook FilmCraft (flujo local-first autorizado en `D:\staging`, transferencia a Polaris, relink/export/QA) y estado por caso: MAGINA Tagiras completado; Ellis if01 portable copiado y hash-verificado en Polaris, con reapertura GUI pendiente; **02_blanket** reconstruido desde el recetario de `collage_builder` (799 frames, 1080×1920 a 30 fps, sin medios offline) con **overlays de texto nativos dentro de FilmCraft**, **layout escalonado en 3 pistas** y el **portable relinkeado a `P:` y validado en la GUI**; **`19_dualshaver`** y **`20_dualshaver`** reconstruidos en `filmcraft-20261119` (proyecto local + portable a `P:`) con 3 pitfalls nuevos; no mezclar proyectos entre productos
- [[ttchop-music-generation]] — runbook: canto manual con ElevenLabs Music, montaje vía `audioBase64`, QA de duración y límites de publicación
- [[traduccion-video-pumasvoice-sincronizada]] — traducir ES→JA con TTS PumaVoice, alinear inicio/fin de voz mediante atempo/adelay, conservar imagen y medir créditos reales; no lip-sync

## Repositorio
- [[cacho]] — wiki versionada: aplicar documentación y código pedidos directamente en main; preservar autorización separada para producción/infra

## Concepts

## Comparisons

## Queries
