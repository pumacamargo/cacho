---
title: Transcripción con GPU en PumaDeskAsus (Windows)
created: 2026-11-17
updated: 2026-11-17
type: runbook
tags: [runbook, pipeline, almacen, cli]
status: active
confidence: high
related: [acceso-nas-polaris, acceso-remoto-pumadeskasus, transcripcion-curso-gerardo-santiago]
---

# Transcripción con GPU en PumaDeskAsus

Cómo correr una transcripción **en la PC de Arturo** (no en el VPS) leyendo el NAS por SMB. Es la ruta correcta para audio largo: la PC tiene GPU y RAM de sobra; el VPS tiene 3,9 GB y **el proceso muere por falta de memoria** con audios de una hora (ver más abajo).

## Entorno ya instalado (verificado 2026-11-17)

| Pieza | Ruta |
| --- | --- |
| Python del entorno | `D:\staging\hermes-transcription\venv\Scripts\python.exe` (3.11.9) |
| Modelo whisper | `D:\staging\hermes-transcription\model` (`model.bin`, 483 MB) |
| ffmpeg / ffprobe | `D:\staging\creator-av-audit\bin\ffmpeg.exe` (no está en PATH) |
| Runner de referencia del curso | `D:\staging\hermes-transcription-course\runner.py` |
| Estado y eventos del curso | `…\hermes-transcription-course\{manifest.json, events.jsonl, *.segments.json}` |
| GPU | RTX 2060 SUPER, 8 GB |

Paquetes: `faster-whisper` 1.2.1, `ctranslate2` 4.8.4, `smbprotocol` 1.15.0, `pyspnego` 0.12.4.

## Tres trampas que cuestan una hora si no se saben

1. **La autenticación SMB falla en Windows** aunque las credenciales sean idénticas a las que el VPS usa bien: sale `SMBAuthenticationError … SpnegoError … WinError -2146893043` (“credentials supplied to the package were not recognized”). Hay que **desactivar el cliente nativo de Windows** y forzar NTLM en Python:

   ```python
   import spnego, smbclient
   native = spnego.client
   def ntlm(*a, **kw):
       kw['options'] = kw.get('options', spnego.NegotiateOptions.none) | spnego.NegotiateOptions.use_ntlm
       return native(*a, **kw)
   spnego.client = ntlm
   smbclient.register_session('100.91.254.118', username=u, password=p,
                              encrypt=True, auth_protocol='ntlm', connection_timeout=30)
   ```

   Pasar `auth_protocol='ntlm'` **sin** ese parche no basta.

2. **Las credenciales van por stdin y se leen con `read()`, nunca `readline()`.** El JSON es **multilínea**; `readline()` solo devuelve `{` y falla con `JSONDecodeError: Expecting property name … line 2 column 1`. Enviar el archivo con `scp` y usar `Start-Process -RedirectStandardInput`.

3. **Mapear una unidad no funciona por SSH.** `New-SmbMapping`/`net use` responden *“A specified logon session does not exist”* porque la sesión SSH no es interactiva. No insistas con `Z:`/`P:`: usa `smbclient` con el parche del punto 1.

## Lanzar un trabajo en segundo plano

- El runner **lee las credenciales al arrancar** y luego ya no necesita stdin, así que se puede lanzar desprendido:

  ```powershell
  $p = Start-Process -FilePath 'D:\staging\hermes-transcription\venv\Scripts\python.exe' `
       -ArgumentList @('C:\Users\puma_\runner.py') `
       -WorkingDirectory 'D:\staging\hermes-transcription-course' `
       -RedirectStandardInput 'C:\Users\puma_\.nas-cred.json' `
       -RedirectStandardOutput '…\stdout.log' -RedirectStandardError '…\stderr.log' `
       -WindowStyle Hidden -PassThru
  ```

- Deja el archivo de credenciales con ACL restringida (`icacls $f /inheritance:r` y `grant:r 'puma_:(R,W)'`). Se puede crear con `scp` del `polaris.json` del VPS (nunca imprimir el contenido) y el runner lo borra en cuanto lo lee.
- Para la GPU hay que añadir las DLL de cuBLAS/cuDNN al PATH antes de cargar el modelo:

  ```python
  package = BASE / 'venv' / 'Lib' / 'site-packages' / 'nvidia'
  for dll in [package / 'cublas' / 'bin', package / 'cudnn' / 'bin']:
      os.add_dll_directory(str(dll)); os.environ['PATH'] = str(dll) + os.pathsep + os.environ['PATH']
  model = WhisperModel(str(BASE / 'model'), device='cuda', compute_type='int8_float16',
                       cpu_threads=2, num_workers=1, local_files_only=True)
  ```

  Sin el modelo en `local_files_only=True` intenta descargar; el modelo ya está en disco.
- Ajustes de transcripción usados en el curso: `language='es'`, `beam_size=5`, `vad_filter=True`, `condition_on_previous_text=True`.
- Verifica el avance leyendo `events.jsonl` (`stage_start`, `progress`, `verified`, `finished`) y con `nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader`.

## Por qué no hacerlo en el VPS con audio largo

El 2026-11-16 un lote en el VPS murió con **OOM killer**: `Memory cgroup out of memory: Killed process (python) anon-rss: 1891760kB` al transcribir un video de 1,93 GB (70 min de audio) con el modelo `small`. La máquina tiene 3,9 GB y whisper carga el audio completo.

- Si por algún motivo hay que hacerlo en el VPS: **cortar el audio en trozos de ~5 min** con ffmpeg, transcribir cada trozo y concatenar. Así la memoria se mantiene acotada.
- Para trabajo serio de audio, usar la PC con GPU: es más rápido y no compite por memoria.

## Verificación al terminar

Cada TXT publicado se comprueba leyéndolo de vuelta del NAS y comparando tamaño y SHA-256 (nunca por HTTP ni por el mero “éxito” del script). El runner del curso además revalida los TXT preexistentes **antes y después** para demostrar que no tocó nada.
