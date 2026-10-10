---
title: Hermes Agent
created: 2026-10-10
updated: 2026-10-10
type: entity
tags: [sistema, infra, rol-agente]
status: active
confidence: high
---

# Hermes Agent

Agente de IA de Nous Research, instalado y operando en el VPS principal de
Arturo (`vps-tools`). Es una de las "IAs que consumen" la wiki.

## Despliegue

- **Host**: VPS Contabo (hostname `vmi2536332.contaboserver.net`),
  IP pública `161.97.163.67`, IP Tailscale `100.116.242.53`.
- **Instalación**: `~/.hermes/hermes-agent`.
- **Dashboard**: `172.17.0.1:9119`.
- Acceso vía Tailscale (nodo `vps-tools`).

## Rol en el stack

- Integra con [[paperclip]] vía el adapter nativo Hermes (`hermes_local` /
  `hermes_gateway`); la vía recomendada es `hermes_gateway`.
- Lee y mantiene esta wiki (`/root/cacho`).
- Corre como gateway + dashboard.

## Relaciones

- Orquestado por / conectado a [[paperclip]].
- Comparte VPS con la infraestructura de Docker (n8n, Affine, RustDesk).
- Empresa automatizada: [[ttchop]].
