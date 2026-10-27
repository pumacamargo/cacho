---
title: Desktop Puma (PumaDeskAsus, Windows)
created: 2026-10-10
updated: 2026-10-28
type: entity
tags: [infra]
status: active
confidence: high
---

# Hardware: Desktop Puma

Desktop (Windows) de Arturo, disponible para proyectos.

## Red y acceso remoto

- **Host Windows/Tailscale actual**: `PumaDeskAsus`, IP `100.126.157.51`.
- **MAC Ethernet (Wake-on-LAN)**: `F0:2F:74:00:8D:3B` (Realtek PCIe GbE).
- **OS**: Windows 11 Home (versión consultada: `10.0.26200`).
- Tras el formateo, el nodo anterior `desktop-puma` (`100.64.3.87`) quedó
  desconectado; no usarlo como endpoint actual.
- SSH por Tailscale está configurado desde `vps-tools` (`100.116.242.53`) al
  puerto TCP/22. El acceso se autenticó como `pumadeskasus\puma_` y la sesión
  mostró el grupo Administrators y nivel de integridad High. El 2026-10-21 se
  verificaron dos conexiones SSH independientes con lectura de Polaris mediante
  `/root/.local/bin/pumassh`; la prueba anterior que expiró ya no representa la
  última comprobación.
- Ver instrucciones, clave de cliente, huella verificada y límites operativos
  en [[acceso-remoto-pumadeskasus]].
- **NAS de proyectos**: `\\Polaris\Projects`, normalmente `P:` en el escritorio.
  Para archivos desde el VPS, priorizar SMB directo por Tailscale sin esta computadora: [[acceso-nas-polaris]]. No equivale a reparar el mapping `P:` de Windows.
  Para operaciones PowerShell por SSH, usar `pumassh` desde `vps-tools`; toma las
  credenciales de un archivo privado en el VPS y prepara `P:` en cada proceso.
  No es un montaje global para aplicaciones nativas. Procedimiento y límites en
  [[acceso-remoto-pumadeskasus]].

## Uso

Máquina de escritorio disponible para proyectos. Es el equipo donde Arturo
también trabaja (rigging 3D). Parte del inventario: [[hardware-inventario]].
Trabajo de [[arturo]].

## Pendiente

- Completar specs (GPU/CPU/RAM) cuando esté online.
