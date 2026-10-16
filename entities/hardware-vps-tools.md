---
title: Hardware VPS Tools
created: 2026-10-10
updated: 2026-10-16
type: entity
tags: [infra, vps, docker]
status: active
confidence: high
---

# Hardware: VPS Tools

VPS principal de Arturo, **este host** donde corre Hermes. Alojado en Contabo.

## Especificaciones

- **Hostname**: `vmi2536332.contaboserver.net` / nodo `vps-tools`
- **IP pública**: `161.97.163.67`
- **IP Tailscale**: `100.116.242.53`
- **CPU**: AMD EPYC, 4 cores
- **RAM**: 3.8 GiB (apretada, usa swap — cuidado al añadir servicios)
- **Disco**: 96 GB
- **OS**: Ubuntu 22.04

## Carga

Centro de la orquestación de IA:
- [[hermes-agent]] (gateway + dashboard, puerto 9119)
- Otros servicios Docker: n8n, Affine, RustDesk
- Empresa automatizada: [[ttchop]]

## Notas

- RAM es el recurso crítico (3.8G, swap presionado). Ver [[hardware-inventario]].
