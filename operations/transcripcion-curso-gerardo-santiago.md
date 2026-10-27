---
title: Transcripción NAS del curso Gerardo Santiago
created: 2026-10-27
updated: 2026-10-28
type: runbook
tags: [runbook, pipeline, almacen]
status: active
confidence: high
related: [acceso-remoto-pumadeskasus, hermes-agentes]
---

# Transcripción de los ocho videos originales

El encargo original produjo archivos TXT UTF-8 con el mismo nombre base que cada MP4 en `P:\TikTok\Learning\gerardoSantiago_course\videos` (NAS Polaris). El 2026-10-26 a las 17:59:32 +0100, `pipeline.log` cerró con `FINISHED processed=5 verified=8/8`: cinco pendientes procesados en esa continuación, ocho TXT comprobados en total. `progress.json` registra los ocho como `verified_existing`. Es un trabajo terminado, **no un proceso que deba asumirse activo**. Los MP4 originales se conservaron.

El alcance es la lista explícita de ocho MP4 y tamaños en `manifest.json`, no todos los MP4 presentes en la carpeta. `2026-10-26 22-57-34.mp4` apareció después y quedó **fuera**: no atribuirle transcripción ni incluirlo al reanudar. `manifest.json` conserva campos históricos `status: partial` / `results_written: 1`; no usar esos campos como estado final: consultar `progress.json`, log y NAS.

| MP4 original (TXT = mismo nombre base + `.txt`) | Bytes TXT | SHA-256 TXT en `progress.json` |
| --- | ---: | --- |
| `01TiktokShop_01QueEsTiktokShop.mp4` | 7362 | `626866b66c6b089eab2c3a81cd9097f9575a8f661d462e207ae35db3b3c4f6c8` |
| `01TiktokShop_02ComoFuncionaTiktokShop.mp4` | 4694 | `c540ffe5bec78686c1740922929e29c2bf473ae696552a3cd261efbf5119d075` |
| `01TiktokShop_03ComoCrearVideosQueFacturen.mp4` | 9115 | `c3278d748259c1a17d1eee4cfee9e83d207cc16491881450b994d2b739e4d6bb` |
| `02SubeDeSeguidores_01CreaTuCuenta.mp4` | 3580 | `74af0525be2a69567166b0ddf01bb7a9023ee15734057ab20377a638af315c31` |
| `02SubeDeSeguidores_02ComoSubirDeSeguidores.mp4` | 9158 | `ad75ed16edfa56f8031748fdac6110fdd763cfb3382fce808ee08bef799d6615` |
| `02SubeDeSeguidores_03DesbloqueaTiktokShop.mp4` | 4772 | `54387577804189935ac582c1caadaea917073d9b11b8c55eb56351f2166841d2` |
| `02SubeDeSeguidores_04LoQueNoTienesQueHacer.mp4` | 6654 | `b8f4a4c1551feb2932788c764cbd7b83b6ab9f939eaa43d6eac38a021cd0a605` |
| `03VentasYTiktoShop_01ComoCrearContenidoQueVenda.mp4` | 22859 | `972b4cdb9a0294c88a9107efffe45e8300960cccef09bb84c61a4dfcdb897822` |

## Entorno y flujo efectivo

**Orden actualizado (2026-10-28):** para nuevas operaciones de archivos, consultar [[acceso-nas-polaris]] y priorizar SMB directo VPS→NAS. El detalle siguiente documenta el pipeline histórico, que no se migró automáticamente a SMB directo; no cambiar su transporte ni relanzarlo al leer esta página.

- Worker en `vps-tools`: `/root/.hermes/profiles/jr_developer/cache/scratch/gerardoSantiago_transcription/`. Allí están `pipeline.py`, `HANDOFF.md`, `manifest.json`, `progress.json`, `pipeline.log`, `pipeline.lock`, `staging/`, `venv/` y `models/`. No son parte de Cacho; no copiar aquí videos, audio ni el texto íntegro del curso. `HANDOFF.md` relata un estado anterior mientras el proceso corría: para estado final prevalecen log, progress y lectura NAS.
- Python 3.10.12 en `venv/`, `faster-whisper` 1.2.1 con modelo small multilingüe (`models/`), CPU `int8`, `cpu_threads=2`, `num_workers=1`; `/usr/bin/ffmpeg` (4.4.2) convierte cada MP4 a WAV PCM mono 16 kHz. Whisper transcribe con `language='es'`, `beam_size=3`, `condition_on_previous_text=True`, `vad_filter=True`; escribe líneas de segmentos no vacíos en UTF-8, sin marcas de tiempo. Las dependencias de `faster-whisper` fallaban con el Python 3.14 de Hermes: se aisló este Python 3.10 **sin cambiar el STT global** de [[hermes-agent]].
- Acceso a NAS de este pipeline histórico exclusivamente por PowerShell en `/root/.local/bin/pumassh`: `P:` es un PSDrive de proveedor dentro de esa invocación, no una unidad nativa para FFmpeg ni `scp`. Véase [[acceso-remoto-pumadeskasus]]. La copia grande con `Copy-Item` falló; el pipeline usa `FileStream` remoto, `Seek` y lecturas de 1 MiB codificadas en base64 por el SSH del wrapper, con tres intentos por comando. `scp` no resuelve por sí solo el acceso al PSDrive `P:`; **`pipeline.py` no invoca `scp`**. La descarga parcial descarta el último bloque incompleto antes de reanudar y contrasta el SHA-256 local del MP4 con el remoto antes de transcribir.
- Recorre los ocho nombres ordenados, uno por uno. Tras transcribir, conserva TXT local en `staging/`. Publica fragmentos de 3072 bytes a un temporal `.gerardo-upload-part` mediante escrituras por offset; verifica tamaño y SHA-256 del temporal, mueve sin sobrescribir el destino y vuelve a leer tamaño y SHA-256 del TXT final en NAS. El estado se guarda con reemplazo atómico en `progress.json`; hitos y errores van a `pipeline.log`. Después de publicar, elimina solo el MP4 y WAV temporales del video; no elimina el original NAS ni el TXT local.
- Si el TXT ya existe en NAS, `pipeline.py` lo registra como `verified_existing` y calcula su hash, pero **no coteja automáticamente ese hash con una versión previa en progress**: para detectar cambios posteriores, comparar explícitamente contra los hashes de la tabla. Si hay TXT local de un upload interrumpido, lo reutiliza sin volver a transcribir; no sobrescribe un TXT final existente. El `flock` no bloqueante en `pipeline.lock` evita dos instancias de este script en el mismo worker.

## Inspección segura y reanudación excepcional

Primero inspeccionar, **sin relanzar la transcripción por rutina**:

```bash
D=/root/.hermes/profiles/jr_developer/cache/scratch/gerardoSantiago_transcription
ps -eo pid,cmd | grep '[p]ipeline.py' || true
tail -30 "$D/pipeline.log"
python3 -m json.tool "$D/progress.json" >/dev/null
# Listar archivos del NAS mediante el wrapper; no mostrar credenciales ni contenido del curso.
/root/.local/bin/pumassh 'Get-ChildItem -LiteralPath "P:\TikTok\Learning\gerardoSantiago_course\videos" -File | Where-Object { $_.Extension -in ".mp4", ".txt" } | Select-Object Name,Length'
```

Para comprobar integridad de cada salida, obtener `Get-FileHash -LiteralPath <ruta TXT> -Algorithm SHA256` **dentro de la misma invocación** de `pumassh` y cotejar longitud y hash con `progress.json`/tabla, no con el mero `status`. Si falta un TXT o cambió su hash, investigar antes de ejecutar o sustituir nada. No leer ni imprimir el archivo de credenciales; no usar `continue_remaining.py` ni `copy_small.py` (herramientas preparatorias antiguas con garantías inferiores). Comprobar espacio con `df -h /root` y memoria con `free -h` antes de cualquier reanudación; la copia de un MP4 y el WAV ocupan disco local.

Solo si hay trabajo pendiente legítimo en **estos ocho** MP4, no hay otra instancia y se investigó cualquier discrepancia, la forma documentada de reanudar es:

```bash
D=/root/.hermes/profiles/jr_developer/cache/scratch/gerardoSantiago_transcription
nohup env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 "$D/venv/bin/python" -u "$D/pipeline.py" >> "$D/pipeline.log" 2>&1 < /dev/null &
echo $!
# Para limitar a un pendiente, añadir --one después de "$D/pipeline.py".
```

La ejecución valida que los ocho MP4 esperados siguen presentes con sus tamaños de manifiesto; ignora otros MP4. Errores de origen, TXT o hash se investigan antes de reintentar: no borrar staging ni modificar el manifiesto para forzar resultados. El texto es **STT automático, no revisión humana**; los hashes prueban identidad de bytes, no fidelidad literal. Si se requiere exactitud, escuchar y revisar manualmente cada transcripción.

Relacionado con el inventario de hardware [[hardware-desktop-puma]] y la operación de agentes [[hermes-agentes]].
