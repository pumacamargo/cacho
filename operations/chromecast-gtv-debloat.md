---
title: Limpiar la Chromecast con Google TV (CleanYourTV)
created: 2026-11-21
updated: 2026-11-21
type: runbook
tags: [runbook, infra, tailscale]
status: active
confidence: high
related: [hardware-celular-android, acceso-nas-polaris]
---

# Limpiar la Chromecast con Google TV (CleanYourTV)

Proyecto: [Gathin23/cleanyourtv](https://github.com/Gathin23/cleanyourtv). **No desinstala nada**: desactiva paquetes con `pm disable-user` (el mismo interruptor que Ajustes → Aplicaciones → Desactivar) y **escribe un registro antes de tocar nada**, para poder devolver todo a su estado anterior.

## El dispositivo de Arturo

| Dato | Valor |
| --- | --- |
| Modelo | **Chromecast con Google TV 4K** (nombre en clave `sabrina`) |
| Android | 14 (SDK 34) |
| Build | `UTTC.250917.004` (14193937) |
| IP | `192.168.0.14` por Wi-Fi (al pasar de cable a Wi-Fi **cambió de IP**: antes `.6`) |
| MAC Wi-Fi | `DC:E5:5B:49:8F:1E` (la que hay que reservar en el router) |
| Paquetes instalados | 133 |
| Otros equipos Cast en la red | `Living room display` = **Nest Hub** (`192.168.0.8`) — no le aplica este proyecto; y un grupo “Home group” |

## Cómo se obtuvo el acceso (depuración inalámbrica)

**“USB debugging” NO abre el puerto de red.** Con solo eso, `5555` y `4321` siguen cerrados y el barrido de la red no encuentra nada. Lo que funciona en este modelo:

1. En la TV: Opciones de desarrollador → **Depuración inalámbrica** → activarla.
2. Entrar a **“Emparejar dispositivo con código”**: aparece un **código de 6 dígitos** y una **IP con puerto** (el puerto de emparejar). El código **caduca en minutos**: hay que usarlo al instante.
3. Desde el equipo de trabajo:

```bash
adb pair 192.168.0.14:<puerto-de-emparejar> <codigo>
adb connect 192.168.0.14:<puerto-de-conexion>     # el de la pantalla principal, distinto del anterior
```

- Si el emparejamiento falla con *protocol fault*, casi siempre es **código caducado** o **puerto equivocado**: el puerto del diálogo de emparejar no es el de la pantalla principal.
- Los puertos son aleatorios y **cambian** al reiniciar o al reactivar la depuración. Hay que volver a leerlos. Para no depender de recordarlos: `adb mdns services` lista los puertos vigentes.
- El equipo de trabajo elegido fue el **Raspberry Pi** (`192.168.0.15`), que ya está en la red y tiene `adb`: así no se instala nada en la PC.

## Entorno de trabajo (en el Pi)

```bash
cd /root && git clone https://github.com/Gathin23/cleanyourtv.git
cd cleanyourtv && python3 -m venv tools/venv
tools/venv/bin/pip install -r tools/requirements.txt      # adb-shell, rsa, cryptography

export TV_ADB_BINARY=/usr/bin/adb      # usa el adb ya emparejado
export TV_HOST=192.168.0.14:<puerto-de-conexion>
tools/venv/bin/python -I tools/tv.py --probe
```

`TV_ADB_BINARY` + `TV_HOST` hacen que todas las herramientas usen la conexión inalámbrica ya emparejada, sin abrir el 5555 (ver `tools/native-adb.md` del repo).

## Respaldo y regreso

- **Respaldo (no cambia nada):** `tools/venv/bin/python -I tools/recovery.py --save <lista>` → escribe el registro en `~/.cleanyourtv/`, un archivo por TV y lista, **nombrado con la dirección** con la que se alcanzó la TV.
- **Regreso:** `TV_HOST=<ip> tools/restore.sh <la misma lista> com.google.android.apps.tv.launcherx` (en Google TV va el lanzador de fábrica como argumento).
- **Registros de esta TV (2026-11-21)**, copia también en `/root/.config/cleanyourtv/` del VPS:
  - `recovery-192.168.0.14-215a911f.json` — lista que **conserva el casting** (14 paquetes)
  - `recovery-192.168.0.14-7cd89ce7.json` — lista **completa** (17 paquetes)
  - En ambos, todos los paquetes estaban `enabled` y el Home era `com.google.android.apps.tv.launcherx/.home.HomeActivity`.
- **Clave:** el registro se identifica por la **dirección**. Si la TV cambia de IP, el regreso no encuentra el registro y cae al modo burdo (reactiva toda la lista). Conviene **fijarle IP** antes de aplicar nada.

## Las dos listas disponibles para este modelo

- `examples/google-chromecast-gtv-4k/debloat-keep-cast.txt` — **conserva el casting del teléfono y el Home original**, sin lanzador nuevo. Quita telemetría, publicidad, Privacy Sandbox, feedback, Google TV/Play Movies, impresión y TalkBack.
- `examples/google-chromecast-gtv-4k/debloat.txt` — la completa: añade `dreamx`, `backdrop` y `tungsten.setupwraith`, y es la que **exige el lanzador propio**.

## Estado aplicado (2026-11-21): lista completa + lanzador propio

Se aplicó la **lista completa** y se instaló el **lanzador propio como Home por defecto**, por decisión de Arturo.

- Home por defecto: **`com.gathin.tvhome/.MainActivity`**; el de fábrica (`com.google.android.apps.tv.launcherx`) quedó **desactivado**.
- 17 paquetes desactivados (los 12 de la lista que conserva casting + `dreamx`, `backdrop`, `setupwraith` + 2 que ya venían desactivados de fábrica: `cast2class`, `tvrecommendations`).
- **Hora corregida**: la TV estaba en `America/Vancouver` (7 horas atrasada). Se puso en **`Asia/Tokyo`** con `cmd alarm set-timezone Asia/Tokyo` y `settings put global auto_time 1` + `auto_time_zone 1`.

### Compilar el lanzador: **en el VPS, no en el Pi**

`aapt2` de las build-tools de Android **solo se distribuye para x86-64**; en ARM (Pi) el build muere con *“Aapt2Daemon: Daemon startup failed”*. La compilación se hace en el **VPS** (x86-64) y el APK se pasa al Pi, que sí puede instalarlo por adb.

```bash
# en el VPS
apt-get install -y openjdk-17-jdk-headless unzip
# command line tools + sdkmanager "platforms;android-34" "build-tools;34.0.0"
git clone --depth 1 https://github.com/Gathin23/cleanyourtv.git
cd cleanyourtv/launcher && echo "sdk.dir=/root/android-sdk" > local.properties
JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 ANDROID_HOME=/root/android-sdk \
  ./gradlew assembleRelease --console=plain --max-workers=2 -Dorg.gradle.jvmargs=-Xmx1536m
# APK: launcher/app/build/outputs/apk/release/app-release.apk (575 KB)
```

Con el APK en el Pi, el traspaso del Home es el script del repo (con `SKIP_BUILD=1` para que no intente recompilar en ARM):

```bash
cd /root/cleanyourtv/launcher
TV_HOST=192.168.0.14:<puerto> TV_ADB_BINARY=/usr/bin/adb SKIP_BUILD=1 bash build-and-install.sh
```

### Trampa encontrada: `setupwraith` también reclama el Home

Con **solo** la lista que conserva casting, el traspaso **falla y se revierte solo**: el script arranca el lanzador nuevo (`Status: ok`), desactiva el de fábrica, pero entonces el Home resuelve a **`com.google.android.tungsten.setupwraith/.RecoveryActivity`** (el asistente de configuración), y el script lo detecta y devuelve el Home al de fábrica. **Hay que aplicar la lista completa primero** (que desactiva `setupwraith`) y después correr el traspaso.

### Intercambios aceptados

- **El casting desde el teléfono se rompe tras reiniciar la TV**: el receptor de Cast lee sus credenciales de fábrica de un proveedor dentro de `setupwraith`; sin él, el teléfono responde *“Untrusted device… couldn't be verified”*. Mientras la TV no se reinicie, la credencial vive en memoria y puede seguir funcionando. El repo documenta un remedio frágil (reactivar `setupwraith` tras cada arranque, esperar a `ClientAuthSigner` y volver a desactivarlo).
- **Antes de desactivar `setupwraith` hay que verificar quién creó la red Wi-Fi**: `adb shell "dumpsys wifi | grep -o 'cname=[^ ]*'"`. Si dice `com.google.android.tungsten.setupwraith`, desactivarlo **borra esa red** y la TV se queda sin Wi-Fi ni adb. En esta TV dice `android.uid.system:1000` → seguro.
- **Se pierde el salvapantallas ambiente** (fotos + Spotify): viene de `dreamx` y `backdrop`, que la lista completa desactiva. Se puede volver a encender con `pm enable` si se extraña.

### Verificación del resultado

```bash
adb -s $TV_HOST shell "cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.HOME"
# -> com.gathin.tvhome/.MainActivity
adb -s $TV_HOST shell "input keyevent KEYCODE_HOME"     # simula el botón Inicio del control
adb -s $TV_HOST shell "dumpsys window | grep mCurrentFocus"
# -> mCurrentFocus=Window{... com.gathin.tvhome/com.gathin.tvhome.MainActivity}
```

## Límites

- El lanzador nuevo **se queda**; se quita a mano desde Ajustes → Aplicaciones (o revirtiendo la lista).
- Una **actualización de firmware** revierte el debloat; se vuelve a aplicar con `check.py --fix`. Ojo: tras una actualización puede volver el lanzador de fábrica como Home.
- Riesgo real: desactivar algo de lo que la TV dependa. Por eso se aplica con el registro ya escrito y el script de regreso a mano. Si la TV no arrancara lo suficiente, el último recurso es un restablecimiento de fábrica desde el menú de recuperación.
- Al terminar, apagar la depuración inalámbrica y revocar las autorizaciones.
