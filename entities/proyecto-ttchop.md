---
title: ttchop (proyecto)
created: 2026-10-10
updated: 2026-10-10
type: entity
tags: [proyecto, negocio, monetizacion, sistema, pipeline]
status: active
confidence: high
---

# ttchop — proyecto TikTok Shop Affiliate

Proyecto de **creación automatizada de contenido (comerciales) para TikTok Shop
Affiliate**. Categoría [[categoria-tts]]. Su objetivo: correr una cuenta de
TikTok Shop Affiliate de forma **automatizada** con un bot.

> Nota: en el wiki, "ttchop" puede referirse a la empresa/pipeline en
> [[ttchop]] (página de empresa) o a este proyecto software. Esta página es el
> proyecto software/documentación técnica.

## Componentes (3)

1. **Web app** (`ttchop`, `ttchop2`) — app web para creación de contenido de
   comerciales para TikTok Shop Affiliate (gestión de productos y planes).
   Detalle en [[ttchop-webapps]].
2. **Herramienta de edición y creación de videos** (`ttchop-server`, `post`) —
   render/TTS, montaje de videos de convenio.
3. **Bot de automatización** (`ttchop-bot`) — automatiza todo el proceso de
   correr una cuenta de TikTok Shop Affiliate: scout → plan → producir.

## La idea

**`ttchop-bot` hace todo; Arturo ayuda con lo físico**: grabar videos, pedir
samples y subir los videos a TikTok. A TikTok **no le gustan los bots**, así que
la automatización ha sido complicada (la parte física es de Arturo).

## Automatizaciones

Detalle de las automatizaciones internas en [[ttchop-automatizaciones]].

## Estado / infra

- Repos en el VPS de proyectos: `ttchop-bot` (scout + scheduler + producer) y
  `ttchop-server` (render/TTS), en `vps-projects`.
- Pipeline diario: scout → producer; crons 06:00/09:00/19:00/21:00 JST.
- Ver [[hardware-vps-projects]] y el pipeline en [[ttchop]].

## Relaciones

- Categoría: [[categoria-tts]] (junto a [[proyecto-lemon-sushi]]).
- Empresa/pipeline: [[ttchop]].
- Orquestación: [[paperclip]], [[hermes-agent]].