---
title: Hardware (inventario)
created: 2026-10-10
updated: 2026-10-16
type: concept
tags: [infra, red, vps, docker]
status: active
confidence: high
---

# Hardware — Inventario

Total del hardware de Arturo para proyectos, todo conectado vía **Tailscale**
(red privada). Cada dispositivo tiene una página con sus detalles.

## Resumen de dispositivos

| Dispositivo | Tailscale IP | Nodo | Estado |
|---|---|---|---|
| VPS contabo-tools | 100.116.242.53 | vps-tools | activo |
| VPS proyectos | 100.68.238.117 | vps-projects | activo |
| Raspberry Pi 5 | 100.117.79.114 | pi5puma01 | activo |
| Desktop (Windows) | 100.64.3.87 | desktop-puma | offline (2d) |
| Celular Android | — | — | — |
| (nodo helper) | 100.83.201.72 | helper | activo |

## Páginas por dispositivo

- [[hardware-vps-tools]] — VPS principal (este host), donde corre Hermes.
- [[hardware-vps-projects]] — segundo VPS para proyectos.
- [[hardware-raspberry-pi5]] — Raspberry Pi 5 (pi5puma01).
- [[hardware-desktop-puma]] — desktop Windows (desktop-puma).
- [[hardware-celular-android]] — celular Android.

## Reglas de uso

- Todo acceso entre dispositivos es por Tailscale (no por IP pública).
- Estos nodos son para **proyectos** de Arturo; no confundir con infra productiva
  de [[ttchop]] salvo que se indique.
- El VPS tools es el centro de la orquestación ([[hermes-agent]], [[hermes-agentes]]).
