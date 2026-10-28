---
title: Acceso a Polaris desde el VPS y orden de alternativas
created: 2026-10-28
updated: 2026-10-28
type: runbook
tags: [runbook, almacen, tailscale, cli]
status: active
confidence: high
related: [acceso-remoto-pumadeskasus, hardware-desktop-puma, transcripcion-curso-gerardo-santiago]
---

# Acceso a Polaris: elegir la ruta según el trabajo

Arturo pidió conservar los métodos anteriores y actualizar su prioridad. **Para operar sobre archivos de `Projects`, probar primero SMB directo VPS→NAS por Tailscale.** Windows no es intermediario obligatorio. La unidad `P:` pertenece a Windows; no es la carpeta compartida en sí. Reparar esa unidad o usar FilmCraft/otras aplicaciones Windows sigue siendo un trabajo distinto: ver [[acceso-remoto-pumadeskasus]] y [[hardware-desktop-puma]].

## Orden de opciones

1. **SMB directo desde vps-tools a `\\100.91.254.118\Projects`.** Usa las mismas credenciales protegidas que el wrapper anterior; no necesita SSH al NAS ni la computadora de Arturo encendida. Autenticación, listado y lectura con hash están verificados. El 2026-10-28 también se verificó por lectura de vuelta una escritura nueva de un MP4 de 3 303 002 bytes en `tiktok\hamaca\edits\07_ellis_if01`; esto prueba esa operación y destino, no rendimiento general con archivos grandes. Verifica cada destino nuevo antes de afirmar entrega.
2. **Windows por SSH, con recurso SMB por IP Tailscale o FQDN**, solo cuando el trabajo necesite Windows o el cliente directo no esté disponible. El adaptador temporal `/root/.hermes/cache/scratch/pumassh-nas-ip.py` cambia en memoria la raíz UNC del wrapper seguro, sin alterar el wrapper global ni el mapeo del escritorio. Se verificaron lectura/escritura por esa ruta en tareas anteriores; el 2026-10-28 también se copió el paquete FilmCraft Ellis if01 y se leyeron de vuelta proyecto, preview y 14 medios para comparar hashes (ver [[ttchop-filmcraft-video-tests]]). Esta verificación cubre ese destino; validar cada destino nuevo. FQDN probado en diagnóstico: `\\polaris.tail639785.ts.net\Projects`, con lectura/hash correctos. No confundir una prueba de lectura de ese FQDN con escritura verificada; esta copia tampoco prueba escritura del cliente SMB directo ni corrige el fallo por nombre corto de la opción 3.
3. **Wrapper histórico `/root/.local/bin/pumassh` con `\\Polaris\Projects`.** Se conserva para compatibilidad, diagnóstico y recuperación; actualmente falla en `New-PSDrive` por nombre corto. No reintentar indefinidamente ni tratar ese fallo como caída de todas las rutas. El acceso `\\192.168.0.2\Projects` también dio lectura/hash correctos desde Windows en el diagnóstico, pero la IP LAN debe verificarse de nuevo antes de usarla y no sustituye una ruta accesible directamente desde el VPS.

No cambiar DNS, credenciales, mappings, servicios o firewall para elegir una alternativa ya autorizada. No eliminar conexiones existentes para probar. La elección de transporte no amplía permisos de lectura/escritura de una tarea.

## Prueba directa ejecutada

- Origen: `vps-tools` (`100.116.242.53`). NAS: `100.91.254.118`, TCP/445 accesible por Tailscale.
- Entorno aislado: `/root/.hermes/cache/scratch/nas-direct-smb-venv/`, creado con `/usr/bin/python3.10 -m venv`; instalado `smbprotocol`, que expone el módulo Python `smbclient`. No se instaló un cliente global ni se montó un filesystem de Linux.
- Sesión directa con `encrypt=True`: autenticación exitosa usando el archivo privado ya existente. Se enumeraron los Markdown del curso y `reporte-curso.html`.
- Se leyó `\\100.91.254.118\Projects\tiktok\learning\gerardoSantiago_course\01TiktokShop.md`: **21277 bytes**, SHA-256 `f7b2908fdbd602633d329999027620b9570f6eb09936e89c120f8fe5d4738f47`, coincidente con la copia anterior.
- La prueba inicial de lectura no modificó ningún archivo. El 2026-10-28 se verificaron por SMB directo y lectura de vuelta en `P:\Tiktok\hamaca\edits\07_ellis_if01` cuatro MP4s (la primera versión y tres clips actualizados) y tres PNGs 540×540. Tamaños y hashes exactos están en [[ttchop-raw-asset-manual-edit]]. Son operaciones verificadas en ese destino; no se probó rendimiento de archivos grandes ni recuperación tras reboot.

El venv y el adaptador viven en **scratch sujeto a limpieza**, no son herramientas persistentes desplegadas para todos los agentes. Verificar existencia, dependencias y host real antes de delegar. Clonar Cacho no instala nada automáticamente. Para nuevas instalaciones aisladas, revisar compatibilidad y dependencias; no modificar Python global ni los entornos de transcripción ya usados en [[transcripcion-curso-gerardo-santiago]].

## Reproducir lectura sin revelar credenciales

Esta receta lee el archivo privado solo internamente, nunca lo imprime ni coloca usuario/contraseña en argumentos. Requiere ejecutar con el Python del venv anterior. Las rutas de destino deben estar dentro del alcance autorizado.

```python
import os
import stat
import json
import hashlib
import smbclient

fd = os.open('/root/.config/pumassh/polaris.json', os.O_RDONLY | os.O_NOFOLLOW)
with os.fdopen(fd, 'r', encoding='utf-8') as handle:
    info = os.fstat(handle.fileno())
    if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
            or stat.S_IMODE(info.st_mode) & 0o077):
        raise RuntimeError('Unsafe credential permissions')
    credentials = json.load(handle)

server = '100.91.254.118'
root = r'\\100.91.254.118\Projects'
try:
    smbclient.register_session(server, username=credentials['username'],
        password=credentials['password'], encrypt=True, connection_timeout=10)
    credentials.clear()
    digest = hashlib.sha256()
    path = root + r'\tiktok\learning\gerardoSantiago_course\01TiktokShop.md'
    with smbclient.open_file(path, mode='rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    print(digest.hexdigest())
finally:
    smbclient.reset_connection_cache()
```

El archivo privado y sus permisos siguen documentados en [[acceso-remoto-pumadeskasus]]; reutilizarlo no requiere copiarlo a repositorios, otros hosts o chats. No bajar a conexión sin cifrado por conveniencia. Ante un error, informar etapa, tipo y código sin volcar credenciales o payloads.

## Diagnóstico del nombre corto: conservar la distinción

El diagnóstico de Developer localizó el error nativo Windows **8** en `New-PSDrive` sobre `\\Polaris\Projects`, antes de leer archivos. El nombre corto resolvía a la misma IP Tailscale que sí funcionó; IP Tailscale, IP LAN y FQDN devolvieron el mismo hash. Por tanto no se confirmó cambio de IP, fallo general del NAS ni agotamiento de RAM física.

La hipótesis principal es estado de sesión, mapping o autenticación SMB ligado al alias corto; **la causa raíz sigue sin confirmarse**. El mapping global `P:` figuraba `Unavailable`, pero ya había aparecido así antes del wrapper, por lo que no demuestra qué cambió. No se limpiaron sesiones ni se reparó Windows. Informe privado local: `/root/.hermes/profiles/developer/workspace/nas-diagnostico/informe-2026-10-27.md`.

La ruta directa evita ese intermediario para archivos del NAS, pero **no repara `P:` ni acredita medios online en FilmCraft**. Si un `.fcproj` usa rutas Windows, siguen siendo necesarias verificación de esas rutas desde Windows y reapertura del proyecto. Tampoco convierte entregables pendientes de copiar al NAS en entregados: cada operación conserva su estado hasta lectura/hash de vuelta.
