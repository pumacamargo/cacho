---
title: Comercial VOX Enchenal — Announcer y variación de imágenes
created: 2026-11-09
updated: 2026-11-19
type: runbook
tags: [runbook, pipeline, cli, arte, api]
status: active
confidence: high
related: [ttchop-video-paths, ttchop-popup-book-commercial, recrear-video-creadores-edits, ttchop-webapps, acceso-nas-polaris]
---

# VOX Enchenal: build final con Announcer e imágenes nuevas

Este es **otro build**, no una revisión del libro pop-up de [[ttchop-popup-book-commercial]]. Usa la misma referencia de `14_shaverAfter`, pero adopta collage editorial sobre negro con recortes, texturas y parallax. Para otros flujos consultar [[ttchop-video-paths]] y [[recrear-video-creadores-edits]]. Producto/fotos: [[ttchop-webapps]]; entrega: [[acceso-nas-polaris]]. No está integrado al Producer ni implica un despliegue.

## 1. Archivo canónico y respaldos

```text
NAS, recurso Projects:
tiktok/hamaca/edits/14_shaverAfter/vox_full_images_v2/
  vox_shaver_full_announcer_images_v2.mp4
  sourcepackage.tar.gz
  README.txt
  version_lock.json
  review.html
  contact_full.jpg
  before_after/
  approved_images/
  QA/
  NAS_READBACK.json
  VPS_READBACK.json
```

- MP4: **1080×1920 nativo, 30 fps, 1422 fotogramas, 47.400 s**, H.264/AAC.
- SHA-256: `9b1213fbaec8e8f292a846d8a38dce1837d3d8c2c59e5c60c4217e5ddf6533f7`.
- Respaldo persistente: `vps-projects:/root/shaver-vox-full-v2-images-delivery/`.
- Proyecto con secuencia PNG nativa: `vps-projects:/root/vox_full_images_v2/renders/native_png/` (inventario en QA). Para reconstrucción preferir el paquete autocontenido, no depender de esa carpeta.
- Copia del perfil: `/root/.hermes/profiles/ttchop_robot/cache/scratch/shaver-vox-full-v2-images-delivery/`; scratch se autolimpia y no es respaldo único.
- El recibo NAS acredita lectura y SHA de 191 archivos. La comprobación documental volvió a comparar el MP4 local y el respaldo persistente: hashes iguales. No confundir esta comprobación con una nueva reproducción completa del video.

## 2. Biblioteca y motor realmente usados

- Fuente: https://github.com/prakhar2603/vox-collage-skill ; commit upstream **`bee376459ef6547eea96b0fcf7bca3158d28bd04`**.
- Se usaron el kit real, sus texturas y generador de papel rasgado, adaptando sustancialmente el código para ocho escenas/objetos. No es la composición de Kolkata con texto cambiado.
- **HyperFrames 0.8.33, GSAP 3.14.2**, composición HTML por configuración, render Chromium y FFmpeg. No EffectCraft, FilmCraft ni libro Three.js. El tratamiento usa diagramas/capas 2.5D: no atribuir cámara 3D física por observar zoom.
- El template original es silencioso y no recomienda voz; **Announcer es una elección de Arturo**, no del skill. README: https://github.com/prakhar2603/vox-collage-skill#readme .
- Entorno exacto archivado en `version_lock.json`: Node **24.11.1**, Chrome **152.0.7977.30**, FFmpeg **6.1.1-3ubuntu5**, Python **3.10.12**, canvas 1080×1920. No reutilizar las versiones distintas del Book por memoria.
- Toolkit reutilizable registrado en el paquete: commit `9a9cb58111b73ddbb3fd04a69f31308b0e38247c`. Dependencias, fuentes/licencias y fuente upstream seleccionada quedan archivadas; no hace falta instalar el skill global para reconstruir.
- Ejecutar Node/HyperFrames con `DO_NOT_TRACK=1`. Los primeros snapshots de la prueba inicial no permiten certificar cero telemetría; no afirmar ausencia absoluta retroactiva.

## 3. Referencia, guion y voz

Referencia original: `14_shaverAfter/input/snaptik_7703511557459823880_v3.mp4`, aproximadamente **79.62 s**, 720×1280/30 fps. Se hizo primero una prueba VOX de tres shots (`vox_three_shots_v1/`) y luego ocho escenas completas (`vox_full_v1/`). La referencia aporta secuencia de ideas/estilo; el comercial propio es **una variación**, no una copia exacta ni un concepto totalmente independiente.

Se conserva el guion japonés aprobado de diez líneas: Alaska y agua congelada → afeitado sin agua → malla/cuchilla → limitación del pelo largo/acostado → dos cabezales → recorte/acabado → comodidad → USB-C → descuentos → enlace. Se reformularon frases y omitieron precio, porcentaje de descuento y cifras de ventas del original. La anécdota de Alaska mantiene el matiz «se cuenta», no verificación histórica.

- **Announcer JP**, ID `gU0LNdkMOQCOrPrwtbee`, reemplaza a PumaVoice01 por petición expresa.
- TTS con el helper versionado `ttchop-server/scripts/creators/tts/tts_lines.mjs`, modelo `eleven_v3`; inspeccionar y archivar configuración real, sin asumir que su default es velocidad natural.
- Announcer bruto: **71.04 s**; procesamiento local **1.5×**: aproximadamente **47.395 s**. Esa velocidad fue elegida originalmente con Puma y luego mantenida en este build Announcer; no atribuir una comparación auditiva de voces no realizada.
- A diferencia del Book final de 34.5 s, **este VOX conserva las diez líneas y la explicación de malla/vello**. No usar la voz recortada del Book para reconstruirlo.
- La variación de imágenes **no cambió una palabra, voz o velocidad**: sus **2043 paquetes AAC** son idénticos a `vox_shaver_full_announcer_v1.mp4`, incluidos PTS/DTS, duración, flags y side-data, mediante `-c:a copy`. No afirmar identidad binaria de una mezcla nueva si se recodifica.
- Sin música nueva ni audio del creador. TTS Announcer fue una generación nueva autorizada; no decir que todo el proyecto no usó APIs pagadas.

## 4. Ocho escenas y reloj

Tiempos de la versión Announcer, en segundos redondeados; usar timeline/alineación archivados para editar:

1. **0.000–3.750:** retrato del explorador, postal, frío, termómetro/manual/X.
2. **3.750–11.459:** lupa, agua que se congela y solución sin agua.
3. **11.459–16.954:** explicación de malla y cuchilla.
4. **16.954–23.303:** pelo largo/acostado y limitación de entrada.
5. **23.303–26.411:** presentación de dos cabezales.
6. **26.411–35.384:** trimmer → cabezal circular y comodidad de un aparato.
7. **35.384–39.811:** USB-C.
8. **39.811–47.400:** producto, abanico y CTA.

Son **45 estados de caption japonés**, no 45 shots. Fondo `#030508`, recortes y objetos por capas, nieve y movimientos de cámara/cues. No pasar la estructura del Book (montaña/personaje permanentes, pesca/oso y barrido de barba) a este video por confundir el caso.

Producto real TTChop2 **`products/prod_5k79pno`**, Enchenal Lab: cuerpo blanco alargado, banda central rose-gold, trimmer rectangular y foil circular en extremos opuestos, USB-C en la banda. Las 19 fotos originales y demostraciones reales del producto se conservaron. Diagramas esquemáticos, no ingeniería propietaria verificada; sin inmersión ni promesa de impermeabilidad (auditoría del agua y su aplicación a los casos 19/20 en [[recrear-video-creadores-edits]]).

## 5. Generación única de imágenes y aprobación

Tras aprobar la animación VOX, Arturo pidió imágenes distintas pero parecidas, conservando animación/voz/producto. Se autorizó **una única generación**, tope 18 créditos, y aprobación de la lámina/recortes antes de integrarlos.

- Modelo **`nano-banana-2`, 4K**; task **`43434461cc8c7dcfaaab397c60299f33`**.
- **1 createTask, 0 reintentos**, cargo reportado de **18 créditos**, saldo 734.46 → 716.46. Este cargo es de la variación VOX, **distinto** del lote previo de poses del Book que también costó 18 créditos.
- Hoja original **3584×4800**, ocho roles reales en una retícula de filas no uniformes; recortes nativos sin reescalar ni repintar. Archivo de generación: `14_shaverAfter/vox_image_variation_v1/`, con hoja, referencia, crops, taskmanifest/costreport y revisión.
- Se mostraron las reservas antes de aprobar: agua/hielo con geometrías distintas, lupa opaca que parece espejo y postal cercana a la base. Arturo respondió que estaban perfectas y autorizó continuar. **No corregir/redibujar esas decisiones aprobadas por iniciativa propia.**

Integración activa documentada en `QA/asset_mapping.json` y `QA/active_assets_camera.json`:

- **01 retrato + 02 postal:** escena 1, alfas independientes, misma altura/centro de figura y parallax.
- **03 rasuradora manual:** escenas 1/2, sin sustituir la eléctrica real; mango/cabezal enteros.
- **04 agua + 05 hielo + 06 lupa:** escena 2, misma composición y cues; transición de opacidad, no morph nuevo. Interrogante separado intacto.
- **07:** malla/piel en escenas 3/4 y puntas verticales para grupos de pelo en escena 3. No contenía cuchilla interna ni pelo doblado equivalente: se conservaron esos vectores y cues originales, en lugar de fingir que todo era nuevo.
- **08 abanico:** cierre de escena 8; el abanico de escena 5 no era parte de esa sustitución y quedó intacto.

## 6. Alfa, conservación y límites

Se conservaron los ocho crops originales y la hoja; máscaras/alfas van en archivos separados. El magenta no era uniforme ni exactamente `#FF00FF`: medir fondo, estimar matte sin borrar textura, pelo, mango o agujeros de malla. No usar largest-component que borre piezas independientes de crop07, ni despill por resta global del vector magenta que vuelve verde el sujeto.

`approved_images/README_ALPHA.md`, originales, scripts y QA claro/oscuro documentan extracción. Se comprobaron 50 agujeros de la malla y 165 aserciones; alfa subpíxel estimado desde imagen aplanada, no transparencia original del proveedor. RGB opaco conservado. Ajustar bounding boxes/centros para encajar nueva ilustración, no redibujar anatomía ni cambiar movimientos.

Reloj, cortes, cámaras, easing, fuentes y 45 captions se compararon contra v1 en 40 sondas; todos los 1422 tiempos tienen escena y caption sin clipping. La versión anterior se conserva. **Esta integración no llamó de nuevo generación, TTS ni compró licencias.** El gasto del modelo Hermes es separado del gasto de medios; no hay total monetario global comprobado aquí.

## 7. Reconstrucción offline

Copiar `sourcepackage.tar.gz` desde NAS/respaldo a una carpeta nueva. Contiene `project/` y dependencias, imágenes, alfas, voz de referencia, fuentes/licencias, scripts y lockfile. Leer primero `README.txt` y `version_lock.json`.

```bash
mkdir -p /ruta/nueva/rebuild
tar -xzf sourcepackage.tar.gz -C /ruta/nueva/rebuild
cd /ruta/nueva/rebuild/project
# Si Chromium está en otra ruta, indicar el ejecutable existente:
# export PUPPETEER_EXECUTABLE_PATH=/ruta/al/chrome-headless-shell
sh reproduce_images_v2.sh
```

Salida: `project/renders/vox_shaver_full_announcer_images_v2_reproduced.mp4`.

El script verificado: activa `DO_NOT_TRACK=1`; verifica/reconstruye alfas y registros; ejecuta `source/upstream/kit/vox.mjs`, lint y QA de composición; renderiza PNG nativos con HyperFrames (`--fps 30 --workers 1 --no-best-effort`); aplana RGBA sobre `#030508`; codifica H.264 `medium/CRF18`; copia el AAC de `voice_reference/approved_v1.mp4` **sin `-shortest`**; ejecuta `qa_final.py` y `qa_delivery_v2.py` en `QA/reproduced/`. No llama APIs de medios/TTS.

Node/Chromium/FFmpeg y bibliotecas Python son requisitos locales, no instalados automáticamente por ese script. La reconstrucción/relocación comprobó **24 PNG nativos y HTML idénticos en el mismo entorno**: no prometer un MP4 byte-idéntico en otra GPU/navegador ni afirmar una nueva reconstrucción solo por leer el script.

## 8. QA y archivo

- Decode íntegro, 1422 fotogramas y 47.4 s; audio sin clipping y paquete AAC idéntico a v1.
- Ocho stills finales y 27 eventos del MP4 exacto; `contact_full.jpg`, `events_contact.jpg`, comparativas mismo frame/PTS y reportes `QA/final_qa.json`.
- Verificar último frame/captions, geometría de cabezales/puerto y activos realmente visibles; archivos nuevos en disco no bastan para acreditar sustitución.
- Audio comprobado instrumentalmente; reproducción/QA no equivale a escucha humana. Diagramas propios, lente opaca y recipientes distintos son límites documentados, no defectos ocultados.
- NAS por SMB directo desde vps-tools y lectura SHA de destino; montaje `/mnt/polaris` de vps-projects deliberadamente solo lectura. No cambiar mounts/mappings: ver [[acceso-nas-polaris]].
- Conservar fuente y activos fuera de scratch; no subir secretos o URLs tokenizadas a Git. El build no publicó en TikTok; publicación manual corresponde a Arturo. La aprobación de imágenes no debe registrarse como aprobación final del MP4 si no la expresó.
