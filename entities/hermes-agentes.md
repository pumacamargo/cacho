---
title: Hermes — Agentes persistentes (research, developer, jr_developer, ttchop_robot)
created: 2026-10-14
updated: 2026-10-16
type: entity
tags: [sistema, papel-agente, rol-agente, personal]
status: active
confidence: high
related: hermes-agent, ttchop
---

# Agentes persistentes de Hermes

Bot Mode de [[hermes-agent]]: cada Bot es un **perfil** de Hermes con su propio
`SOUL.md` (instrucciones), memoria (`memories/`), skills, config y credenciales
bajo `~/.hermes/profiles/<nombre>/`. Son agentes persistentes (no subagentes
descartables): hablarlos por CLI (`hermes -p <nombre> chat` / alias) o bot-a-bot
(`@<nombre>` / `message_agent`).

## Roster de agentes Hermes

| Agente | Alias | Misión (única) | Modelo | Telegram |
|---|---|---|---|---|
| **Research** | `research` | Investigar y resumir con fuentes verificables | gpt-6-luna | — |
| **Developer** | `developer` | Desarrollar proyectos con código (escribir, arreglar, probar, entregar) | gpt-6-sol | — |
| **jr_developer** | `jr_developer` | Ejecutar tareas pequeñas y bien delimitadas de desarrollo | gpt-6-luna | — |
| **ttchop_robot** | `ttchop_robot` | Asistir el proyecto ttchop (pipeline, bot, webapps, servidores) | gpt-6-luna | conectado como @Puma_gym_bot |

## Notas comunes

- **Modelos**: los cuatro usan la **suscripción de ChatGPT** de Arturo vía el
  proveedor `openai-codex` (OAuth nativa en cada `credential_pool`). Comparten
  la misma familia de token de esa cuenta (openai-codex no admite los modelos
  `-mini`/`-nano` ni las series 5.4 en una suscripción normal; funcionan los
  flagships nuevos, p. ej. gpt-6-sol / gpt-6-luna).
- **Skills**: Research y el roster heredan las skills del perfil base; los cuatro
  heredan el contexto de infra (hosts y ttchop).
- **Telegram**: cada uno tiene su propio bot token (nunca compartido). Hoy solo
  `ttchop_robot` está en Telegram; la allowlist se restringe al user id de Arturo.

## Relaciones

- Mecanismo: [[hermes-agent]] (Bot Mode = perfiles).
- Código portal: ChatGPT OAuth (`openai-codex`), que usa la suscripción de Arturo.
- ttchop_robot asiste el pipeline documentado en [[ttchop]] y [[ttchop-webapps]].