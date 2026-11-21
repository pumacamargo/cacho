---
title: Escritorio de la PC en la Chromecast (Moonlight + Sunshine)
created: 2026-11-21
updated: 2026-11-21
type: runbook
tags: [runbook, infra, tv, remoto]
status: active
confidence: high
related: [chromecast-gtv-debloat, acceso-remoto-pumadeskasus]
---

# Escritorio de la PC en la Chromecast (Moonlight + Sunshine)

Poner la pantalla de la PC en la TV y manejarla desde ahí. **Moonlight** (cliente) va en la TV; **Sunshine** (host) en la PC.

## Por qué esta vía y no otra

| Opción | Veredicto |
| --- | --- |
| **Chrome Remote Desktop (el de Google)** | **No sirve por esta vía.** Google no publica versión para Android TV (la tienda de la TV solo muestra apps con interfaz de control remoto, igual que pasa con Chrome). La app actual es un **envoltorio web (TWA)** que necesita **Chrome** instalado —la TV no lo tiene— y está hecha para pantalla táctil. Se puede *instalar* a mano (Downloader, Aptoide, o adb) pero lo más probable es que se abra en blanco. |
| **Microsoft Windows App (Remote Desktop)** | La ficha existe en la tienda pero la TV responde **“Your device isn't compatible with this version”**. Además RDP exige **Windows Pro** y la PC de Arturo es **Home** (verificado: `EditionID=Core`, `fDenyTSConnections=1`, servicio `TermService` detenido). |
| **Moonlight + Sunshine** | **La que quedó.** Moonlight está en la tienda de la TV (botón INSTALL confirmado), es nativa de TV y funciona con el control. Sunshine es gratis, corre en **Windows Home** y aprovecha NVENC. |

## Estado instalado (2026-11-21)

- **TV**: `com.limelight` versión **12.2**, instalada desde la tienda de Google TV (se pulsó INSTALL por adb; ver más abajo). La TV también tiene **Aptoide** (`cm.aptoide.pt`) como segunda tienda.
- **PC** (`PumaDeskAsus`, 192.168.0.20 Ethernet): **Sunshine v2026.914.233613**, instalado por MSI en silencio (`msiexec /i <msi> /qn /norestart`). Servicio `SunshineService` en **Running/Automatic**; escucha en 47984/47989/47990.
- **Emparejado**: el cliente aparece como “TV Moonlight” en Sunshine (`/api/clients/list`).
- **Verificado transmitiendo**: Sunshine codificando con **`hevc_nvenc`** (RTX 2060 SUPER), captura 1920x1080, y la TV con la capa `SurfaceView[com.limelight.Game]` actualizándose cada ~5 s.

## Credenciales de la web de Sunshine

- URL: `https://<ip-de-la-pc>:47990` (desde la PC, `https://localhost:47990`; desde Tailscale, `https://100.126.157.51:47990`).
- Usuario **`admin`**; la contraseña está guardada en el VPS en `/root/.config/sunshine/sunshine.txt` (permisos 600). Se cambia desde la propia web.

## Cómo se hizo (por si hay que repetirlo)

```bash
# 1) Instalar Moonlight en la TV desde la tienda, pulsando el boton por adb
#    (abrir la ficha y luego buscar el boton INSTALL con uiautomator; ver tools/tap_install.py)
adb -s $TV_HOST shell 'am start -a android.intent.action.VIEW -d "market://details?id=com.limelight" -p com.android.vending'

# 2) Instalar Sunshine en la PC (MSI oficial; el proyecto vive en SunshineStream/Sunshine, NO en LizardByte)
#    https://github.com/SunshineStream/Sunshine/releases/latest -> Sunshine-Windows-AMD64-installer.msi
msiexec /i sunshine.msi /qn /norestart

# 3) Crear credenciales de la web (no pide autenticacion la primera vez)
curl -sk -X POST https://<pc>:47990/api/password -H 'Content-Type: application/json' \
  -d '{"newUsername":"admin","newPassword":"<pass>","confirmNewPassword":"<pass>"}'

# 4) Emparejar: en la TV abrir Moonlight -> elegir la PC -> aparece un PIN de 4 digitos
#    Leer los emparejamientos pendientes y enviar el PIN:
curl -sk -u admin:<pass> https://<pc>:47990/api/pin
curl -sk -u admin:<pass> -X POST https://<pc>:47990/api/pin -H 'Content-Type: application/json' \
  -d '{"pairing_id":"<32 hex del GET>","pin":"<los 4 digitos de la TV>","name":"TV Moonlight"}'

# 5) En la TV: elegir la PC -> DESKTOP (o STEAM)
```

Notas de la API: los clientes que no son navegador (curl) están **exentos de CSRF**; `/api/password` **no pide autenticación** mientras no haya usuario configurado; `/api/pin` sí la pide.

## Trampas aprendidas

- **`screencap` de Android devuelve negro para la capa de video por hardware.** Que las capturas de la TV salgan negras durante el streaming **no** significa que falle. Comprobarlo por otro lado: `dumpsys SurfaceFlinger --list | grep limelight` (capa `SurfaceView[...Game]`) y las entradas `TimeStats` de esa superficie cada pocos segundos; en la PC, el registro de Sunshine mostrando `Creating encoder [hevc_nvenc]`.
- **`adb mdns services` puede venir vacío**; para hallar el puerto de depuración, `nmap -Pn -p 30000-50000 --open <ip>` y quedarse con el que `adb devices` marca como `device` (los fallidos quedan `offline` y aparecen primero).
- **El repo de Sunshine se mudó**: `LizardByte/Sunshine` redirige a **`SunshineStream/Sunshine`**. La API de GitHub sin `User-Agent` devuelve un JSON de redirección, no los datos.
- **Moonlight abre en Ajustes** si se lo lanza con `am start -n com.limelight/.PcView` tras un uso previo; conviene `am force-stop` y abrirlo con el `monkey` de LEANBACK_LAUNCHER.
- Las etiquetas de los mosaicos de apps (DESKTOP, STEAM) **no son nodos de texto** para uiautomator: hay que pulsarlas por coordenadas.
- **Control**: el menú de Moonlight se maneja con el control de la TV, pero para el cursor del escritorio hace falta **mouse** (o un control de juegos, que Moonlight usa para emular el mouse).

## Pendiente / límites

- Para el cursor del escritorio: conectar un mouse Bluetooth a la TV (o usar un gamepad).
- Fuera de casa funcionaría por Tailscale, pero no está probado.
- Al reiniciar la TV, la depuración inalámbrica se apaga (ver [[chromecast-gtv-debloat]]); Moonlight y Sunshine no dependen de eso.
