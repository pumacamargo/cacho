---
title: Acceso SSH a PumaDeskAsus
created: 2026-10-20
updated: 2026-11-21
type: runbook
tags: [infra, tailscale, runbook]
status: active
confidence: high
---

# Conectar a PumaDeskAsus

**Orden vigente para archivos del NAS (2026-10-28):** primero SMB directo VPS→Polaris con las credenciales protegidas existentes; después Windows por SSH con IP/FQDN si el trabajo requiere Windows; conservar el wrapper por nombre corto como alternativa histórica hoy fallida. Procedimiento, pruebas y límites en [[acceso-nas-polaris]]. Esta página conserva íntegros los comandos y antecedentes de acceso Windows; no implica que el VPS necesite `P:` para acceder a `Projects`.

Desde `vps-tools` (`100.116.242.53`), conéctate por Tailscale:

La interfaz Ethernet Realtek PCIe GbE, actualmente `Up`, tiene MAC
`F0:2F:74:00:8D:3B` (la dirección necesaria para Wake-on-LAN). La interfaz Wi-Fi
está desconectada.

```bash
ssh -i /root/.ssh/id_ed25519_pumadeskasus \
  -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=yes \
  puma_@100.126.157.51
```

Para ejecutar un comando sin abrir sesión, añádelo al final; `whoami` ya se
verificó y devolvió `pumadeskasus\puma_`. La cuenta es administradora. SSH da
control por comandos, **no acceso visual a pantalla y teclado**.

La clave privada se queda en el VPS. En Windows, la clave pública está en
`%ProgramData%\ssh\administrators_authorized_keys`. La huella ED25519 verificada
es `SHA256:SzDDMv1kz9aiv7XiB2tZ0q1toyDJ0Bwg4sJrTD8wDt0`.

El acceso SSH es por Tailscale, TCP/22; `OpenSSH-Server-In-TCP` permanece
desactivada y no se abrió ningún puerto del router.

## Por qué se caía el servicio SSH (diagnosticado y corregido el 2026-11-21)

Síntoma: de pronto el puerto 22 respondía *connection refused*, aunque la PC seguía encendida y con Tailscale activo (`tailscale ping` contestaba). No era red: **el servicio `sshd` estaba caído**.

Causas encontradas en los registros de Windows:

1. **`ListenAddress 100.126.157.51` en `sshd_config`**: sshd escucha *solo* en la IP de Tailscale. El servicio **no tenía dependencia** de `Tailscale`, así que en cada arranque competía con él; si el adaptador aún no tenía la IP, el *bind* fallaba y el proceso moría. Las caídas (evento 7034 "terminated unexpectedly") coincidían con reinicios: `2026-11-14 00:01-00:03` y `2026-11-20 17:29-17:30`.
2. **Sin acciones de recuperación** (`sc qfailure` vacío): cuando el proceso moría, Windows no lo levantaba. Por eso tras un reinicio quedaba apagado hasta que alguien lo arrancaba a mano.
3. La PC **se reinicia sola cuando está inactiva** (Windows Update; evento Kernel-Power 578 "system initiated reboot from Sleeping (Idle)"), lo que multiplica la ocasión de caer.
4. Aparte, **`LogLevel DEBUG3`**: el log `C:\ProgramData\ssh\logs\sshd.log` había llegado a **330 MB**.

Correcciones aplicadas (verificadas):

```powershell
sc.exe config sshd depend= Tailscale
sc.exe failure sshd reset= 86400 actions= restart/5000/restart/10000/restart/30000
# sshd_config: LogLevel DEBUG3 -> INFO (respaldo en sshd_config.bak-hermes, validado con `sshd -t`)
```

- El log viejo se rotó a `sshd.log.old-20261121-143956` (315 MB; se puede borrar).
- **Prueba real de recuperación:** se mató el proceso que escuchaba en el 22 y Windows lo reinició solo a los 10 s (evento 7031: *"corrective action will be taken in 10000 milliseconds: Restart the service"*), reconectando sin intervención.
- Al volver a arrancar, si Tailscale tarda, ahora sshd espera a esa dependencia en vez de morir.

**Cómo revisarlo si vuelve a fallar:**

```powershell
Get-Service sshd | Select Status,StartType
Get-WinEvent -LogName System -MaxEvents 300 | Where-Object { $_.Message -match 'OpenSSH' } | Select -First 5
Select-String "$env:ProgramData\ssh\sshd_config" -Pattern 'ListenAddress|LogLevel'
```

**Alternativa independiente:** `tailscale up --ssh` habilita el SSH de Tailscale, que no depende del servicio de OpenSSH; útil si se quiere una segunda vía de acceso.

**Nota de diagnóstico:** desde la LAN el puerto 22 no aparece, y es correcto: sshd está atado solo a la IP de Tailscale. Comprobarlo desde otra máquina de la red local da un falso negativo.

## Acceder a Polaris como P: desde SSH

Arturo eligió guardar las credenciales del NAS en **vps-tools** y usarlas en
cada conexión mediante un wrapper, en lugar de introducirlas en el escritorio
de Windows. Este es el camino probado para operaciones PowerShell sobre el NAS.

- Wrapper instalado: `/root/.local/bin/pumassh` (Python 3, permisos `700`).
- Archivo privado: `/root/.config/pumassh/polaris.json` (permisos `600`, propietario
  `root`); directorio `/root/.config/pumassh` con permisos `700`.
- El JSON contiene las claves `username` y `password`. Arturo lo completa o
  actualiza directamente en el VPS, por ejemplo con
  `nano /root/.config/pumassh/polaris.json`. Nunca imprimir su contenido ni copiarlo
  a chats, logs, commits o este repositorio. Es texto plano protegido por permisos,
  no un archivo cifrado; una cuenta con acceso root puede leerlo.
- Destino: `puma_@100.126.157.51`; recurso SMB `\\Polaris\Projects`.

Desde el VPS:

```bash
# Sin argumentos, lista las primeras entradas del recurso.
/root/.local/bin/pumassh

# Ejecuta una instrucción PowerShell después de conectar el recurso.
/root/.local/bin/pumassh 'Get-ChildItem P:\ -ErrorAction Stop | Select-Object -First 5 Name,Mode'

# Varias operaciones deben viajar juntas en la misma invocación.
/root/.local/bin/pumassh 'Get-Item P:\ -ErrorAction Stop; Get-ChildItem P:\AI -ErrorAction Stop | Select-Object -First 5 Name'
```

```bash
# Ejemplo de trabajo nuevo: staging local Windows en D:\staging.
/root/.local/bin/pumassh '$src="D:\staging\aretes-20261021-song3-ja.mp4"; $dst="P:\TikTok\Hamaca\edits\aretes-prod_3adbqgd"; New-Item -ItemType Directory -Path $dst -Force | Out-Null; Copy-Item -LiteralPath $src -Destination $dst -ErrorAction Stop; Get-FileHash -LiteralPath (Join-Path $dst (Split-Path $src -Leaf)) -Algorithm SHA256'
```

### Funcionamiento y límites

1. Lee el JSON local, rechaza archivos con permisos de grupo/otros, propietario
   distinto al usuario ejecutor, enlaces simbólicos o credenciales vacías.
2. Usa la clave SSH y comprobación estricta de host documentadas arriba, con
   `BatchMode=yes`. Envía credenciales e instrucción por **stdin cifrado de SSH**,
   nunca como argumentos del proceso. El `EncodedCommand` remoto contiene solo
   código, no credenciales; base64 no es cifrado.
3. Crea un `PSCredential` en memoria y un `New-PSDrive` de tipo `FileSystem`,
   nombre `P`, raíz `\\Polaris\Projects`, con `-Scope Global` dentro del proceso
   PowerShell. Si `P:` ya apunta a otra raíz, aborta sin reemplazarlo.
4. Comprueba acceso y ejecuta la instrucción en ese mismo proceso.

**No es un montaje global de Windows:** `-Scope Global` aquí es el ámbito de
PowerShell, no `New-SmbGlobalMapping`. No usa `-Persist`, no sustituye el mapeo
del escritorio y no instala un hook para conexiones `ssh` normales. Cada llamada
a `pumassh` vuelve a preparar el acceso; `P:` no queda disponible automáticamente
para procesos nativos externos como `cmd.exe`, FFmpeg o FilmCraft. Para estos
casos se necesita otro mecanismo validado; no asumir que este wrapper los resuelve.

### Estado verificado y diagnóstico

**Antecedente por nombre corto (2026-10-27):** `pumassh` falló al preparar `P:` con `pumassh: Not enough memory resources are available to process this command`. Esa operación no completó lectura/escritura. Developer después aisló el fallo en `New-PSDrive`/error nativo 8 para `\\Polaris\Projects`; el nombre resolvía a la misma IP que sí funcionó. No se confirmó causa raíz ni falta de RAM física. La prueba directa del 2026-10-28 sí verificó autenticación/listado/lectura desde el VPS sin Windows: ver [[acceso-nas-polaris]]. TCP/445 por sí solo no basta y la escritura directa sigue sin probar; una transferencia concreta solo está verificada tras comprobar su salida por la ruta elegida. El fallo del wrapper corto no invalida otras rutas verificadas ni repara la unidad del escritorio.

El **2026-10-21**, tras Arturo completar el archivo, dos conexiones SSH nuevas
e independientes mediante el wrapper terminaron con código `0`: se enumeró la
raíz del NAS (incluidas `3Dprinter`, `AI`, `Animation` y `Chimo`) y se confirmó
`P` como unidad del proveedor `Microsoft.PowerShell.Core\FileSystem`.

- **Verificado:** autenticación SMB, lectura y copia/escritura por PowerShell en
  conexiones SSH nuevas. El 2026-10-21 se copiaron cinco entregables FilmCraft a
  `P:\TikTok\Hamaca\edits\aretes-prod_3adbqgd`; sus tamaños se leyeron de vuelta
  y los SHA-256 coincidieron con los archivos locales.
- **No probado:** acceso de FilmCraft/FFmpeg u otros procesos nativos a `P:` ni
  recuperación después de reiniciar Windows o el VPS. El PSDrive de `pumassh` es
  temporal y no vuelve `P:` un montaje global.
- Antes del wrapper, SSH normal no podía enumerar `P:` ni el UNC; el mapeo
  consultado con `Get-SmbGlobalMapping` figuraba `Unavailable`. Polaris respondía
  en TCP/445: eso probaba transporte, no autenticación ni acceso al recurso.
- Si falla, revisar permisos del archivo **sin mostrar su contenido**, disponibilidad
  de la PC/Polaris y el mensaje de error. Para renovar la contraseña, Arturo edita
  el JSON localmente; no incluirla en comandos `net use`, argumentos SSH o scripts.
- El wrapper y las credenciales viven fuera de Cacho; este runbook documenta sus
  rutas y uso, pero no instala el wrapper en otro VPS al clonar el repositorio.
- Ejemplo de lectura serial de MP4 grandes vía FileStream del PSDrive y publicación
  verificada de TXT al NAS: [[transcripcion-curso-gerardo-santiago]]. FileStream sirve
  para leer/copiar datos **después** de que `pumassh` prepare `P:`; no puede corregir
  un fallo al preparar la unidad. En un trabajo FilmCraft autorizado local-first,
  mantén los archivos locales y marca la entrega NAS pendiente hasta que `P:` pueda
  verificarse. Para nuevas operaciones de archivos, usar el orden de [[acceso-nas-polaris]] con las mismas credenciales protegidas; no improvisar credenciales ni alterar mappings. Ese
  pipeline no convierte `P:` en montaje nativo ni altera la configuración del wrapper.

## Encender y apagar

Wake-on-LAN se envía desde la Pi, que está en la misma LAN. Desde `vps-tools`:

```bash
tailscale ssh root@pi5puma01 python3 - <<'PY'
import socket, time
mac = bytes.fromhex("f02f74008d3b")
packet = b"\xff" * 6 + mac * 16
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    for _ in range(3):
        print(sock.sendto(packet, ("192.168.0.255", 9)))
        time.sleep(1)
PY
```

Después espera a que Windows inicie y verifica con `tailscale ping
100.126.157.51`.

Para apagar Windows sin forzar el cierre de aplicaciones:

```bash
ssh -i /root/.ssh/id_ed25519_pumadeskasus \
  -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=yes \
  puma_@100.126.157.51 'shutdown.exe /s /t 0'
```

Tras apagar, la falta de respuesta de Tailscale y SSH confirma que quedó fuera de
línea. El ciclo de encendido y apagado se verificó el 2026-10-21.

Para revocar el acceso, elimina únicamente la línea `hermes-vps-to-pumadeskasus`
de `administrators_authorized_keys`. Consulta [[hardware-desktop-puma]] y
[[hardware-vps-tools]].