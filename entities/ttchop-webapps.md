---
title: ttchop webapps (ttchop / ttchop2)
created: 2026-10-10
updated: 2026-10-15
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

## Feature: carruseles de imágenes (image_carousel) — implementado y desplegado 2026-10-14

Carruseles de imágenes como **contenido orgánico para subir seguidores** de la
cuenta TikTok (NO comercial de producto). Publicación manual por Arturo.

- **Plan**: TTC-55 (Supervisor) — aprobado. **Implementación**: TTC-56 (Developer) — fases 0–4 completas, desplegadas en vivo (servidor + UI + reglas). **Fase 5** (ranking por follows, check automático anti-texto) queda en **TTC-57** (necesita 2–3 semanas de posts reales).
- **Flujo**: guion → expandido por LLM en N slides (texto en el idioma elegido, imagePrompt en inglés) → generación de fondos **photo-only** (sin texto) con kie.ai → composición final con texto en capa aparte (Remotion en ttchop-post) → `carousels` en Firestore.
- **Modelos de imagen** (kie.ai, `POST /jobs/createTask`): `seedream-v4` (default, 5 créd/img, batch≤6, seed), `gpt-image-2` (6 créd/img), `nano-banana-2` (8 créd/img), `nano-banana-2-lite` (añadido al catálogo; **precio y disponibilidad no confirmados**). Id de modelo configurable; idioma configurable (es/en/ja).
- **UI**: pestaña "Carousels" en webapp2 (entre Templates y Create). Templates de guion (`carousel_script`) y de estilo (`carousel_style`, conceptos de dirección de arte).
- **Reglas no negociables**: imágenes SIEMPRE photo-only (nunca texto dentro); texto SIEMPRE como overlay; `projectId` explícito (nunca inferido); callback con token + re-verificación + idempotente + sweep; URLs de kie temporales → re-subidas a Firebase Storage; la UI recuerda la etiqueta TikTok "AI-generated".
- **Smoke test real pasó** (2026-10-14): create→approve-text→kie batch→callbacks→composición→`ready` (40 créditos). Limitación conocida: el modelo a veces "pinta" texto en el fondo (lo mitigas con Regenerar slide; el check automático es la Fase 5).

### Catálogo de templates actualizado (2026-10-15)

- Los estilos seed anteriores se sustituyeron por cinco direcciones visuales: fotografía candid profesional de mujeres adultas, hombres adultos y familias; paisajes profesionales; y B-roll artístico. Las instrucciones especifican adultos para retratos y negative prompts contra texto, logos, ilustración y renders 3D.
- Los tres guiones seed actuales son: recomendación de libros/películas/TV/recetas; Problem + Fix (menopausia, sueño o baja energía); y lista/ranking con opiniones. Solicitan salida en el idioma seleccionado (es/en/ja) y roles hook/body/cta.
- En Firestore de **ttchop2**, los seeds de carrusel de Arturo fueron reemplazados y se verificaron de vuelta: **5 `carousel_style` + 3 `carousel_script`**, todos `seed: true`, `seedVersion: 1`. Se conservaron sus otros templates no relacionados con carruseles.
- Código en `master`, commits pusheados: webapp2 `d9b450b` y ttchop-server `32b4212`. `npm run build` fue reportado como exitoso por `jr_developer`. El despliegue de estos cambios posteriores a TTC-56 **no está confirmado**; no asumir que ya aparecen en la UI de producción. La prueba real de kie.ai para `nano-banana-2-lite` y su precio también quedan pendientes.

### Decisión visual: sombra de `image_carousel` (2026-10-15)

Arturo aprobó una sombra negra más grande y oscura, con poco difuminado y **sin recuadro ni gradiente**, exclusivamente para el texto de las diapositivas de carrusel:

- **Alcance exclusivo:** `image_carousel`, componente Remotion `CarouselSlide`. No aplicar a los overlays de texto de videos/collage de `ttchop-post`, ni cambiar el `OverlayKit.SHADOW` general. No es un estilo global.
- Fondo del texto del carrusel: `typography.background: 'none'`.
- Sombra probada: `0 0 2px rgba(0,0,0,1), 0 3px 6px rgba(0,0,0,1), 0 0 8px rgba(0,0,0,0.95)`.
- La prueba final fue un único slide PNG de 1080×1920, reutilizando un fondo ya existente; no generó imágenes con IA ni consumió créditos Kie. El override temporal se limitó al nodo de texto de `CarouselSlide`.
- **Estado:** decisión visual documentada, todavía no persistida en el template de Firestore ni integrada en el código de producción. El renderer actual no lee un `typography.textShadow` guardado y el template `temp_bi9e3iz` conserva `background: 'gradient'`. El ajuste de safe area está en la rama `fix/carousel-text-safe-area` (commit `737b80e`), sin despliegue confirmado.

## Documentación interna

- `CLAUDE.md` — arquitectura, esquema de datos, trampas conocidas.
- `PLAN.md` — estado por fase y pendientes.
- `PENDIENTES-SERVIDOR.md` — lo que la webapp ya llama y ttchop-server no implementa aún.

## Relaciones

- Proyecto: [[proyecto-ttchop]] · automatizaciones: [[ttchop-automatizaciones]]
- Servidor: `ttchop-server` (ver [[ttchop-automatizaciones]]) · categoría [[categoria-tts]]