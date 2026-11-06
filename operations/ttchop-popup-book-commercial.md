---
title: Comerciales con libro pop-up — Lemo-Opuscar y caso Enchenal
author: ttchop_robot
created: 2026-11-06
updated: 2026-11-06
type: runbook
tags: [runbook, pipeline, cli, arte, api]
status: active
confidence: high
related: [ttchop-video-paths, recrear-video-creadores-edits, ttchop-webapps, acceso-nas-polaris]
---

# Comercial Enchenal: libro pop-up hecho en código

Para elegir otros flujos, consultar [[ttchop-video-paths]]. La adaptación de guion y lectura de una referencia se relaciona con [[recrear-video-creadores-edits]]; las fotos vienen de [[ttchop-webapps]] y la entrega usa [[acceso-nas-polaris]]. Este flujo es manual y separado del Producer: no se integró ni desplegó en el bot o la webapp.

## 1. Qué se usó y qué NO

- Dirección visual: **Lemo-Opuscar / Paper Pop-up Book**, elegido por Arturo entre pruebas de EffectCraft, Drawn by Code y Lemo. Su nombre de galería era «Sabuda Pop-up Book on a Real Desk».
- Biblioteca: https://github.com/lemomo-ai/lemo-opuscar ; guía `styles/paper-popup/STYLE.md`. Consultar también `AGENTS.md`, `DIRECTOR.md` y `TECHNIQUE.md`; escribir tratamiento propio antes de tomar técnicas de la demo. No copiar sus personajes/historia.
- **Three.js 0.170 + Canvas2D**: libro, mesa, luces y cámara 3D; ilustraciones y recortes planos con textura/borde de cartulina. **No se hizo dentro de EffectCraft ni FilmCraft**, y no se usó Remotion para este render.
- Node/Chromium renderizan fotogramas deterministas; Python prepara audio/QA; FFmpeg codifica/ensambla H.264 y AAC. Mesa y materiales procedurales: no afirmar rodaje ni escritorio fotográfico.
- El proyecto editable es código y medios, no `.ecproj`/`.fcproj`. Importar el MP4 en un editor no recupera sus capas.
- Entorno probado del paquete final: Node 26.7.0, Chrome 150.0.7871.186/SwiftShader, FFmpeg 4.4.2 y Python con numpy/Pillow. No se garantiza identidad binaria entre navegadores/GPU distintos.

## 2. Entrega canónica: usar el archivo `fixed`

**NAS, recurso `Projects`:**

```text
tiktok/hamaca/edits/14_shaverAfter/lemo_opuscar_full_v3_camera/
  enchenal_book_camera_v3_fixed.mp4
  sourcepackage_fixed.tar.gz
  README_fixed.txt
  MANIFEST_fixed.json
  SHA256SUMS_fixed.txt
  NAS_READBACK_fixed.json
  VPS_PROJECTS_READBACK_fixed.json
  closing_last_frame_fixed.png
  QA_fixed/
```

- MP4 final entregado: **1080×1920 nativo, 30 fps, 1035 frames, 34.500 s**, H.264/AAC.
- SHA-256: `9f382df0a87ab0e1e7c0cd9c6734b8a6a80c60ce2e1eaf06880250074e9a5673`.
- Respaldo persistente: `vps-projects:/root/shaver-book-full-v3-camera-delivery/`.
- Copia de trabajo del perfil: `/root/.hermes/profiles/ttchop_robot/cache/scratch/shaver-book-full-v3-camera-delivery/`; la caché se limpia, **no usarla como único archivo**.
- El archivo sin `fixed`, `enchenal_book_camera_v3.mp4`, conserva un rótulo final parcialmente fuera de encuadre: es antecedente, NO la versión canónica. Sus recibos/QA sin sufijo no acreditan el fixed.
- La copia final del NAS se leyó y su SHA se comparó con el archivo enviado. No hubo publicación en TikTok. La aprobación expresa del usuario fue sobre v2/storyboard; no atribuir aprobación creativa posterior al fixed solo porque se entregó.

## 3. Referencia y producto real

Caso: `14_shaverAfter`. Referencia: `input/snaptik_7703511557459823880_v3.mp4`, aproximadamente 79.62 s, 720×1280/30 fps; desglose en `breakdown/14_shaverAfter_breakdown.md` y análisis específico `analisis/shot1_analisis.md` dentro del caso. El breakdown inicial decía erróneamente «sin narración»; el ASR posterior en `effectcraft/transcript_plain_ja.txt` confirmó voz. Priorizar esa evidencia.

Producto **`ttchop2/products/prod_5k79pno`**, Enchenal Lab, con 19 entradas `modelSheetUrls`. Las fotos, diagramas e instrucciones se descargaron y revisaron: cuerpo alargado blanco, banda central rosado/dorada, trimmer rectangular y malla circular en extremos opuestos, puerto USB-C en la banda central. No inventar cabezales intercambiables ni ubicación del puerto. No exponer URLs tokenizadas o credenciales al documentar/archivar.

Arturo confirmó dos cabezales y USB-C. Las instrucciones indican trimmer primero y malla para acabado. El título comercial y las advertencias discrepan sobre agua; se eligió uso seco, sin inmersión ni promesa de impermeabilidad. Cifras de ventas, precio, porcentajes y garantías de irritación no pasaron al comercial. La historia de Alaska se narra como «se cuenta», no como hecho histórico comprobado.

## 4. Guion, voz y recorte final

1. Traducir la referencia para revisión y crear una variación propia. El español era para aprobar contenido; **la producción es japonesa**. En este caso se generó por error una prueba española antes de corregir: no reutilizarla ni considerarla parte de la voz final.
2. Aprobar la traducción japonesa antes de TTS. Se usó **PumaVoice01**, modelo `eleven_v3`, mediante el helper existente `ttchop-server/scripts/creators/tts/tts_lines.mjs` en vps-projects. Entregar por línea y unido. Las claves se leen del entorno, nunca se imprimen.
3. La narración japonesa completa medía **70.609 s** en MP3. Se hizo una prueba local `atempo=1.5`, sin nueva síntesis, conservando tono; resultado **47.099 s**. No llamar «velocidad natural» al default del servidor: el helper inspeccionado usaba `speed: 0.5`.
4. Tras la revisión visual, Arturo eliminó las antiguas escenas 3/4 (funcionamiento interno de malla y vello largo), con su explicación hablada. Se recortaron únicamente las líneas japonesas 3/4 del PCM de la voz acelerada, intervalo **11.252947846–23.839070295 s**. La narración editada quedó en **34.472879819 s**; video cuantizado a 34.5 s.
5. Las muestras retenidas del stem quedaron intactas antes de mezcla/AAC. El EDL, alineación, voz original/editada y QA están archivados; usar esos archivos, no volver a sumar duraciones de MP3 separados (su padding desplaza los cortes).
6. V3 y fixed **copian el AAC de v2 sin recodificar**: 1486 paquetes iguales, con timestamps/skip-samples. SHA elementary AAC: `953a82c61de1d30cc2acf3bddc565f1c3513099d27a805bebb21e91453aeadbb`.

No normalizar, comprimir, cambiar gain/tempo o regenerar la voz para un ajuste de cámara. Solo foley de papel procedural discreto; sin música en esta versión ni audio del creador. La reproducción de QA fue silenciada: no afirmar escucha humana ni validación fonética independiente del empalme.

## 5. Dirección final: un cuento continuo, seis páginas

Arturo rechazó escenas independientes que abandonaban al personaje y el paisaje. La solución aprobada mantiene **el mismo viejito y la montaña**, pero cambia encuadre, distribución y actividad en cada página. El libro sí pasa páginas. Las acciones del fondo no sustituyen la demostración comercial del primer término.

1. **Frío:** viejo barbado, montaña, termómetro y agua congelada; arranque basado en la prueba preferida.
2. **Pesca:** viejo pescando sobre hielo, montaña desde otro encuadre; afeitado sin agua en primer término.
3. **Leña:** viejo cortando madera al fondo; producto y sus dos cabezales grandes delante.
4. **Oso:** viejo huyendo de un oso de cuento; recorte/acabado en primer término, sin diagramas de los antiguos shots 3/4.
5. **Campamento:** viejo con leña y refugio; USB-C grande delante, conector alineado al puerto de la banda central.
6. **Remate:** viejo aún barbado → el producto cruza rápidamente y oculta el rostro → revela al mismo personaje sin barba. Conservar edad/ropa, libro abierto y producto/CTA visibles hasta el último frame. Es gag ilustrado, no prueba de afeitado real en una pasada.

En páginas 2–5, el storyboard aprobado **v5** redujo al personaje aproximadamente a dos tercios del tamaño de v4 sin cambiar cámara global ni achicar foreground. No volver a agrandarlo al animar. Son poses rígidas de cartulina: importa la silueta bien dibujada, no un rig corporal fluido.

## 6. Poses: una única generación Kie, luego recorte local

Las poses programáticas parecían ensambladas/rotas. Arturo pidió usar al viejito del primer shot como referencia y **una sola generación API** para una hoja con ocho variaciones, no ocho llamadas.

- Modelo: **`nano-banana-2`**, 4K solicitado; salida real **3584×4800**.
- Task ID: `62bfacc4a13b8081259fb50f264d552a`.
- **1 createTask, 0 reintentos; 18 créditos**, cargo de tarea y saldo 752.46 → 734.46 coincidentes. No es el costo total del proyecto: TTS previo y uso del modelo Hermes son conceptos distintos; no hay total monetario verificado de ellos aquí.
- El proveedor produjo 10 figuras en disposición 3+3+4, no el grid 2×4 pedido. Se conservaron hoja original y ocho recortes de entrega: siete distintos y una repetición del frontal barbado como base del wipe. Arturo aprobó los recortes, incluida la caña extraña y la leña sostenida con un brazo; no redibujarlos por iniciativa propia.
- Archivo NAS del lote: `14_shaverAfter/poses_kie_onegen_v1/`: `reference.png`, `original_sheet.png`, `pose_01.png`…`pose_08.png`, `taskmanifest.json`, `costreport.json`.
- Se retiró magenta localmente con máscara alfa; conservar originales y sprites aparte. Medir fondo, evitar halos/agujeros, no restar el vector magenta a toda la ropa. Revisar sobre claro/oscuro ampliado. Las diferencias originales entre figura con/sin barba se esconden bajo el producto, no con deformación facial.

Después de la generación única de poses, storyboard, integración, renders y movimientos de cámara no llamaron APIs de generación ni TTS.

## 7. Aprobación de storyboard y cámara final

Storyboards: v2/v3 con poses programáticas superadas; v4 integra las poses Kie aprobadas; **v5 es la composición aprobada para producir**. Seis escenas y ocho imágenes, contando antes/durante/después del cierre.

- NAS storyboard: `14_shaverAfter/lemo_opuscar_storyboard_v5/`.
- Revisión publicada: https://lemonsushi.com/uploads/vps2/creators-research/14_shaverAfter/storyboard-continuity-v5/review.html . Son stills, no la película final.
- El primer full v1 duraba 47.1 s y tenía ocho escenas; full v2 de 34.5 s aplica la nueva dirección. No confundir su desglose GIF antiguo con los seis shots actuales.

La petición posterior fue movimiento real de cámara 3D **muy sutil**, sin bounce:

1. Push 2 %.
2. Pan horizontal +0.006 m.
3. Órbita yaw +1°.
4. Pan opuesto −0.010 m.
5. Push adicional 1.2 % para USB-C.
6. Después del wipe: arco −0.6° y pullback 0.6 %; producto hero aumenta **8 %** uniformemente. Un intento de 14 % se descartó por interferir con el rótulo.

Mantener continuidad de camera offsets en cinco cambios físicos de página; comprobar cabezales, USB y cobertura de barba con la nueva cámara. El padre rechazó el rótulo del primer v3 por cortarse/solaparse: el **fixed** eleva/estrecha solo esa tarjeta y deja ambas líneas completas («2つのヘッド / これ1台で»), margen derecho aproximado 54 px y separación al producto de 31 px en el último frame.

## 8. Reconstruir exactamente la entrega final

Copiar `sourcepackage_fixed.tar.gz` del NAS o respaldo persistente a una carpeta nueva. **Usar el paquete fixed**, no `sourcepackage.tar.gz` del v3 rechazado. El paquete contiene `project/`, dependencias locales/lock, fuentes/licencias, sprites aprobados, medios y referencias v2/v3 necesarias para la reconstrucción parcial.

```bash
mkdir -p /ruta/nueva/rebuild
# Ejecutar desde la carpeta que contiene el paquete:
tar -xzf sourcepackage_fixed.tar.gz -C /ruta/nueva/rebuild
bash /ruta/nueva/rebuild/project/build_label_fixed.sh /ruta/absoluta/output
/usr/bin/python3 /ruta/nueva/rebuild/project/qa_label_fixed.py /ruta/absoluta/output
node /ruta/nueva/rebuild/project/playback_camera.mjs \
  /ruta/absoluta/output/enchenal_book_camera_v3_fixed.mp4 \
  /ruta/absoluta/output/QA_fixed/playback_fixed.json
```

Seguir `project/README_LABEL_FIXED.txt` para la referencia previa exigida por QA; también está en `reference/previous_camera_v3.mp4`. No asumir que el comando de playback escucha el audio.

El builder conserva el prefijo aprobado de **809 frames** y renderiza únicamente la escena 6 desde tiempos globales originales: concat stream-copy con duración explícita `809/30`, AAC de referencia v2 con `-c:a copy` y **sin `-shortest`**. Esto evita cortar el último frame y la cola de voz; redondear el prefijo a milisegundos produjo un desvío de mux que se corrigió. Para cambios futuros de otras escenas, no reutilizar ese prefijo sin regenerar lo afectado: inspeccionar fuente y scripts del paquete.

La reconstrucción del paquete se probó en otra ubicación con checkpoint idéntico al render nativo. Esto acredita el entorno probado, no cualquier máquina. Para repetir el proceso creativo: ficha/fotos → guion JA aprobado → audición/velocidad → poses aprobadas → storyboard con encuadres → animatic → cámara/eventos → render nativo → QA y NAS; no regenerar por API medios que ya existen.

## 9. QA y entrega segura

- `ffprobe`: formato, resolución, 30 fps, 1035 frames y 34.5 s; decode íntegro sin errores.
- Auditoría ampliada de imágenes y secuencias temporales: siluetas, manos, magenta, texto, puerto, page turns y wipe. El cumplimiento técnico no sustituye calidad artística.
- Comparar AAC por paquetes/timestamps; distinguir identidad del stem/copia de la recodificación AAC de las primeras mezclas.
- Inspeccionar **último frame exacto** y extremos de cámara: no aceptar etiqueta cortada aunque sus palabras puedan adivinarse. El fixed no modifica las primeras cinco escenas; las pruebas preservan sus 809 frames.
- Reproducción automatizada silenciada no equivale a escucha humana. El primer v3 reportó tres drops de presentación de Chrome, no frames faltantes; consultar QA específico del fixed para no mezclar resultados.
- El montaje CIFS de vps-projects `/mnt/polaris` es deliberadamente **solo lectura**. Escribir por SMB directo desde vps-tools con el venv `/root/.venvs/nas-smb` y la referencia local de credencial documentada en [[acceso-nas-polaris]], nunca remontarlo ni cambiar mappings.
- Conservar scripts, activos, paquetes y recibos fuera de scratch. Releer SHA desde destino exacto antes de decir entregado; no subir secretos ni URLs tokenizadas al wiki. Publicar en TikTok corresponde a Arturo.
