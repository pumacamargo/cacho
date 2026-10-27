---
title: Separar videos del NAS por cortes visuales
created: 2026-10-27
updated: 2026-10-28
type: runbook
tags: [runbook, pipeline, almacen, cli]
status: active
confidence: high
related: [acceso-remoto-pumadeskasus, ttchop-raw-asset-manual-edit]
---

# Separar videos del NAS por cortes visuales

Procedimiento usado el 2026-10-26 para dividir `Juice.mp4` y `EllisWhite.mp4` en clips independientes, preservando audio, dimensiones y originales. No fue un pipeline de Producer ni una función de OBS: se usaron **FFmpeg/ffprobe, Python y revisión visual de hojas de contacto** en `vps-tools`. El acceso a Polaris se describe en [[acceso-remoto-pumadeskasus]]; el montaje posterior de estos clips es otra operación, documentada en [[ttchop-raw-asset-manual-edit]].

El trabajo histórico usó `C:\staging`; las recetas reutilizables de staging en esta página usan ahora `D:\staging`, por solicitud de Arturo del 2026-10-27. Los registros históricos conservan la ruta efectivamente utilizada.

## 1. Resolver la fuente y preparar staging

**Prioridad para trabajos nuevos:** seguir [[acceso-nas-polaris]]: SMB directo VPS→NAS primero, Windows por SSH solo si hace falta o como alternativa. Los pasos y comandos siguientes conservan la ruta Windows usada por estos casos; no son un requisito para todo acceso al NAS. La prueba directa solo acreditó lectura/listado: verificar escritura antes de afirmar una entrega por ese cliente.

- Enumerar la ruta literal con `/root/.local/bin/pumassh` antes de copiar. La carpeta escrita inicialmente como `02_juiceDiscout` no existía; la enumeración de su padre identificó `02_JuiceDiscount`, que se comunicó a Arturo antes de usarla.
- `P:` es un PSDrive del proceso PowerShell de `pumassh`, no un montaje nativo disponible para scp o FFmpeg. Hacer `Copy-Item` en ese proceso hacia un directorio propio de `D:\staging\<id>`, luego scp al scratch del VPS.
- Verificar SHA-256 de la copia contra el origen. No imprimir credenciales ni usar el JSON privado de SMB como argumento. Si una copia grande falla por red, consultar la alternativa FileStream/reintentos de [[transcripcion-curso-gerardo-santiago]]; no confundir poder enumerar con poder transferir todo el archivo. FileStream solo aplica después de que `pumassh` preparó `P:`; no resuelve fallas previas de conexión/autenticación o de creación del PSDrive.

Ejemplo del caso Juice:

```bash
/root/.local/bin/pumassh '$d="D:\staging\hermes-juice-cuts"; New-Item -ItemType Directory -Path $d -Force | Out-Null; Copy-Item -LiteralPath "P:\tiktok\hamaca\edits\02_JuiceDiscount\Juice.mp4" -Destination "$d\Juice.mp4" -ErrorAction Stop; Get-FileHash -LiteralPath "$d\Juice.mp4" -Algorithm SHA256'
mkdir -p /root/.hermes/cache/scratch/juice-cuts
scp -i /root/.ssh/id_ed25519_pumadeskasus \
  -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=yes \
  'puma_@100.126.157.51:D:/staging/hermes-juice-cuts/Juice.mp4' \
  /root/.hermes/cache/scratch/juice-cuts/Juice.mp4
```

Los ejemplos son recetas para una tarea autorizada nueva, no deben ejecutarse al consultar esta página. Usar staging único y comprobar conflictos de nombres.

## 2. Detectar candidatos, después revisar imágenes

1. `ffprobe -v error -show_format -show_streams -of json INPUT.mp4`: medir streams, duración, dimensiones y frames reales; no asumir frame rate constante por `r_frame_rate`.
2. Calcular `scene_score` en **todos los frames** a 180×320 y guardar timestamp/score. Se conserva la relación de aspecto porque ambos ejemplos son verticales 720×1280; adaptar la escala a otra fuente.
3. Hacer una hoja de contactos general a 2 imágenes/s con timestamps y revisar los cambios posibles.
4. Para cada candidato, extraer el frame anterior, el candidato y el siguiente. En intervalos ambiguos, revisar una secuencia de frames consecutivos. Las imágenes se inspeccionaron visualmente mediante `vision_analyze`; no se eligieron todos los cortes con un único umbral automático.

```bash
ffmpeg -v error -i INPUT.mp4 \
  -vf "scale=180:320,select='gte(scene,0)',metadata=print:file=scores.txt" \
  -an -f null -
ffmpeg -v error -i INPUT.mp4 \
  -vf "fps=2,scale=135:240,drawtext=text='%{pts\:hms}':fontsize=16:fontcolor=white:box=1:boxcolor=black,tile=8x10" \
  -frames:v 1 overview.jpg
# Ejemplo de una terna, sustituyendo N por el frame elegido:
# select='eq(n,N-1)+eq(n,N)+eq(n,N+1)',scale=180:320
```

El tamaño del mosaico debe cubrir toda la duración o paginarse: `8x10` a 2 imágenes/s cubre aproximadamente 40 s. No limitar una revisión larga al primer mosaico.

**Límites:** movimiento brusco, texto y filtros pueden dar falsos positivos; un jump cut de cámara fija puede tener score bajo. En EllisWhite la desaparición/reaparición del filtro facial con movimiento continuo no se consideró un corte de montaje. La segmentación histórica de Juice sí incluye límites elegidos en cambios de máscara de score bajo: se conservan como evidencia de lo entregado, pero esos dos límites no demuestran por sí solos un corte editorial. Si se exige solo montaje real, revalidarlos con el original antes de reutilizar esa decisión; esta documentación no rehízo los archivos.

## 3. Exportar por límites de frame y tiempos reales

Extraer timestamps del video, usando los índices de frame aprobados visualmente:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries frame=best_effort_timestamp_time -of json INPUT.mp4
```

Para el intervalo `[F0,F1)`, `T0` y `T1` son los timestamps de esos límites; en el último intervalo, usar la duración final aplicable del medio. Conservar un manifiesto JSON de nombres, índices/tiempos, frames, duración exportada, tamaño y SHA-256. Los contenedores y streams pueden diferir unos milisegundos.

```bash
ffmpeg -v error -n -i INPUT.mp4 \
  -filter_complex "[0:v:0]trim=start_frame=F0:end_frame=F1,setpts=PTS-STARTPTS[v];[0:a:0]atrim=start=T0:end=T1,asetpts=PTS-STARTPTS[a]" \
  -map '[v]' -map '[a]' -c:v libx264 -preset fast -crf 18 -threads 2 \
  -vsync 0 -enc_time_base:v 1:90000 -video_track_timescale 90000 \
  -c:a aac -b:a 256k -movflags +faststart OUTPUT.mp4
```

`F0/F1/T0/T1` son marcadores que hay que sustituir, no sintaxis ejecutable literal. La receta supone audio presente y reloj fuente de 90 kHz como en estos casos. Es una **recodificación**, no una copia sin pérdidas; conserva 720×1280 y audio AAC, no los bytes originales del stream.

- En Juice funcionó `-vsync 2`, manteniendo los 948 frames entre cinco clips.
- En EllisWhite, `-vsync 2` eliminó un frame inicial muy cercano al anterior. Se corrigió usando `-vsync 0` y time base de 90 kHz; los cuatro resultados conservaron los 1162 frames.
- El FFmpeg instalado entonces no aceptó `-fps_mode`; por eso se usó `-vsync`. No copiar opciones de otra versión sin comprobarlas.

## 4. QA y devolución al NAS

- Decodificar cada resultado: `ffmpeg -v error -i OUTPUT.mp4 -f null -`.
- Comprobar video/audio, dimensiones, frames y duraciones con ffprobe. Los intervalos de frame no se solapan ni dejan huecos; la suma debe igualar el total fuente. Para la subdivisión temporal posterior de Juice se normalizó a 30 fps: no aplicarle la prueba de igualdad de frames con el VFR original.
- Subir por scp a `D:\staging\<id>` en Windows; copiar desde allí mediante PowerShell/pumassh a la **misma carpeta de origen**.
- Antes de escribir, comprobar **todos** los nombres destino y abortar si existe cualquiera; no sobrescribir ni borrar archivos ajenos.
- Leer cada tamaño y SHA-256 desde el NAS y compararlos programáticamente con el manifiesto local. Comprobar además que el hash del original no cambió. Un scp o Copy-Item exitoso por sí solo no certifica la entrega.

## Resultados entregados el 2026-10-26

### Juice Discount

Carpeta `P:\tiktok\hamaca\edits\02_JuiceDiscount\`; fuente `Juice.mp4`, 948 frames, 720×1280. SHA-256 original: `5559A6A3791F933D13BB673B596D248C6E9B0F846214ACC56776608370E655E1`.

| Archivo | Intervalo fuente, segundos | Frames | Duración contenedor |
|---|---|---:|---:|
| Juice_corte_01.mp4 | 0–3.455278 | 104 | 3.456 s |
| Juice_corte_02.mp4 | 3.455278–6.391722 | 88 | 2.937 s |
| Juice_corte_03.mp4 | 6.391722–7.357978 | 28 | 0.967 s |
| Juice_corte_04.mp4 | 7.357978–8.957322 | 47 | 1.600 s |
| Juice_corte_05.mp4 | 8.957322–31.769678 | 681 | 22.808 s |

Límites por frame: `0,104,192,220,267,948`. La distinción entre cortes editoriales y cambios del filtro en Juice tiene la salvedad de la sección 2.

Después Arturo pidió dividir `Juice_corte_05.mp4` en cuatro partes iguales: se midió el contenedor (22.808 s), se dividió en cuatro intervalos temporales de **5.702 s**, se usó `trim/atrim`, `setpts/asetpts`, `fps=30` y padding/recorte de audio al intervalo; H.264 CRF 18/AAC 256k. `ffprobe` confirmó 5.702 s en los cuatro MP4. Se guardaron `Juice_corte_05_parte_01.mp4` a `Juice_corte_05_parte_04.mp4` sin modificar `Juice_corte_05.mp4`; hash de ese padre: `087553D87C78F4319580295E0088B0871BE6F2CB60B652F44AA8AFFE3E554D53`.

### EllisWhite

Carpeta `P:\tiktok\hamaca\edits\03_ellisWhiteDiscount\`; fuente `EllisWhite.mp4`, 1162 frames, 720×1280. SHA-256 original: `31DA334172A0BC9EB96F078C674851F5C917C39619E54A01F9B7D3DA2EAD58EF`.

| Archivo | Intervalo fuente, segundos | Frames | Duración contenedor |
|---|---|---:|---:|
| EllisWhite_corte_01.mp4 | 0–6.199833 | 186 | 6.200 s |
| EllisWhite_corte_02.mp4 | 6.199833–18.214056 | 359 | 12.015 s |
| EllisWhite_corte_03.mp4 | 18.214056–26.449778 | 246 | 8.236 s |
| EllisWhite_corte_04.mp4 | 26.449778–38.893424 | 371 | 12.444 s |

Límites por frame: `0,186,545,791,1162`. Los tres cortes principales se contrastaron con imágenes antes/después y la hoja general; no se segmentaron pérdidas de tracking de máscara.

### Evidencia y alcance

En la ejecución se verificaron decodificación, conteo de frames y hashes de todos los clips devueltos al NAS; los originales mantuvieron sus hashes. Manifiestos de la sesión: `/root/.hermes/cache/scratch/juice-cuts/manifest.json`, `juice-cuts/quarters_manifest.json` y `elliswhite-cuts/manifest.json`, bajo el mismo scratch. Son temporales sujetos a limpieza, **no dependencias durables del runbook**. Las tablas anteriores conservan el inventario y límites de lo entregado. Esta página se documentó el 2026-10-27 desde esos manifiestos y la ejecución registrada; no volvió a renderizar, copiar ni alterar medios. No se incorporaron videos al repositorio.
