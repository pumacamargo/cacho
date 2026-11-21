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
- Los puertos son aleatorios y **cambian** al reiniciar o al reactivar la depuración. Hay que volver a leerlos.
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
- `examples/google-chromecast-gtv-4k/debloat.txt` — la completa: añade `dreamx`, `backdrop` y `tungsten.setupwraith`, y está pensada para acompañarse del **lanzador propio** (requiere JDK 17–22 y Android SDK 34, que hoy no están instalados en la PC).

## Límites

- El lanzador nuevo, si se instala, **se queda**; se quita a mano desde Ajustes → Aplicaciones.
- Una **actualización de firmware** revierte el debloat; se vuelve a aplicar con `check.py --fix`.
- Riesgo real: desactivar algo de lo que la TV dependa. Por eso se aplica con el registro ya escrito y el script de regreso a mano. Si la TV no arrancara lo suficiente, el último recurso es un restablecimiento de fábrica desde el menú de recuperación.
- Al terminar, apagar la depuración inalámbrica y revocar las autorizaciones.
