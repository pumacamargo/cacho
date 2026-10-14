---
title: Hermes Agent
created: 2026-10-10
updated: 2026-10-14
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

## Voz (STT / TTS) — configurada 2026-10-11

- **Entrada (voz → texto)**: STT local con **Vosk** (modelo ES) vía
  `HERMES_LOCAL_STT_COMMAND` → `/root/.hermes/bin/stt-vosk.sh` (wrapper que
  resuelve python/ffmpeg de `/root/.hermes/tools`). `stt.provider: local_command`.
- **Salida (texto → voz)**: **Edge TTS**, voz `es-MX-JorgeNeural` (español
  mexicano). Edge a veces da un 403 transitorio → reintentar.
- **Modo `/voice`** en Telegram: `off` (texto) | `voice_only` (voz solo si el
  usuario mandó audio) | `tts` (voz en cada respuesta). Estado por chat en
  `gateway_voice_mode.json`.
- Nota: `faster-whisper` roto en este Python 3.14 (PyAV `metadata_errors`) — por
  eso se usa Vosk vía `local_command`.

## Agentes persistentes (Bot Mode) — 2026-10-14

Hermes corre ahora **tres agentes persistentes** (bot = perfil con SOUL.md y
memoria propias): **Research** (investiga/resume), **Developer** (desarrolla
código) y **ttchop_robot** (asiste ttchop). Detalle, modelos y estado de
Telegram en [[hermes-agentes]].

## Relaciones

- Orquestado por / conectado a [[paperclip]].
- Comparte VPS con la infraestructura de Docker (n8n, Affine, RustDesk).
- Empresa automatizada: [[ttchop]].
