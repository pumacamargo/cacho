---
title: ttchop webapps (ttchop / ttchop2)
created: 2026-10-10
updated: 2026-10-10
type: entity
tags: [sistema, proyecto, negocio]
status: active
confidence: high
---

# ttchop — Webapps (ttchop / ttchop2)

Las aplicaciones web del proyecto ttchop (ver [[proyecto-ttchop]]). Componente #1:
web app para creación de contenido de comerciales de TikTok Shop Affiliate.

## Relación entre ttchop y ttchop2

- **`ttchop2` es un fork independiente de `ttchop`**, con su **propio proyecto de
  Firebase** (`ttchop2`).
- Ambos comparten el **`ttchop-server`** (render/TTS), que decide a qué proyecto
  escribir según el `projectId` recibido en cada llamada.
- **Regla crítica del proyecto**: `/root/ttchop` (la app original) y su proyecto
  de Firebase/datos son INTOCABLES — nada de ttchop2 puede tocar el repo, proyecto
  ni datos de ttchop.
- Producción ttchop2: **https://ttchop2.web.app**

## Qué es TTChop2

Webapp **móvil-first** para vendedores de TikTok Shop: gestiona productos y clips,
genera videos de marketing con IA (guion + voz + render), los agenda, y **cruza las
ventas reales de la tienda contra los videos publicados** para saber qué funciona.

## Secciones

- **Dashboard** — KPIs de ventas (GMV, comisión, % comisión, unidades, órdenes,
  vistas), tendencia período a período, desempeño diario.
- **Products** — librería de productos con pestañas Info, Clips y Renders.
- **Templates** — plantillas de guion, voz y prompt de IA.
- **Create Video** — generación: guion → voz → render.
- **Calendario** — agenda de publicaciones con estrategia en texto y propuesta
  automática.
- **Analytics** — importación de reportes `.xlsx` de TikTok Shop crusados con renders.
- **Brand Concept** — moodboard, paleta, tipografías, descripción del canal.
- **Reports** — reportes generados por LLM sobre qué está funcionando.
- **Video Editor / Tools** — placeholders/pendientes.

Además: cuentas múltiples de TikTok (contenedores de datos separados), páginas
públicas de producto en `/p/:id`, y páginas legales `/terms` y `/privacy`.

## Stack

- **Frontend**: React 19 + TypeScript + Vite 8 (plugin React basado en Oxc).
- **Backend**: Firebase (Auth, Firestore, Storage, Cloud Functions) + `ttchop-server`
  (VPS externo, `ttchop-server.lemonsushi.com`).
- **UI**: `lucide-react`, CSS plano con variables, dark theme.
- **Datos**: `xlsx` para importar reportes de TikTok Shop del lado del cliente.
- **Extensión**: Chrome MV3, JS plano sin build (`extension/`).

## Arquitectura clave

- **Sin router**: `main.tsx` decide por `window.location.pathname` entre páginas
  públicas (`/p/:id`, `/terms`, `/privacy`) y el resto (requiere sesión). Dentro,
  la navegación es un estado `ActiveTab` con panel lateral (hamburguesa).
- **Contenedores** (`ContainerContext`): separación de datos por cuenta TikTok.
  `accountId` ausente/null/`''` = contenedor general. Conectar cuenta es opcional;
  hay una sola noción de cuenta activa. (Relevante para la [[ttchop-automatizaciones |
  escalabilidad multi-cuenta]].)
- **Importaciones**: `analytics_orders` y `tiktok_videos` apuntan a un `imports/{id}`
  que lleva el `accountId` (reasignar una importación = 1 escritura, no 500).
- **Capa de datos** (`databaseService.ts`, singleton ~4000 líneas): toda query filtra
  por `userId`; `stripUndefined()` antes de escribir; normalización al leer (renombrar
  la interfaz de TS **no migra** los documentos viejos);
  `projectId: FIREBASE_PROJECT_ID` en todo payload (sin él cae a `ttchop` y escribe al
  proyecto equivocado).
- **Cloud Functions**: `productPage` (SSR de `/p/**`), `tiktokExchange`,
  `tiktokAccounts`, `tiktokDisconnect`, `tiktokUpload`. Los tokens de TikTok viven
  **solo** server-side en `tiktok_accounts`.

## Firestore (colecciones)

`products`, `sessions`, `templates` (compartidos, sin accountId), `renders`,
`scheduled_renders`, `master_videos`, `video_variations` (legacy), `imports` (ahí
vive el contenedor), `analytics_orders`, `tiktok_videos`, `tiktok_accounts`.

## Documentación interna

- `CLAUDE.md` — arquitectura, esquema de datos, trampas conocidas.
- `PLAN.md` — estado por fase y pendientes.
- `PENDIENTES-SERVIDOR.md` — lo que la webapp ya llama y ttchop-server no implementa aún.

## Relaciones

- Proyecto: [[proyecto-ttchop]] · automatizaciones: [[ttchop-automatizaciones]]
- Servidor: `ttchop-server` (ver [[ttchop-automatizaciones]]) · categoría [[categoria-tts]]