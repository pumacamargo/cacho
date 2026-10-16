---
title: ttchop webapps (ttchop / ttchop2)
created: 2026-10-10
updated: 2026-10-16
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

## Analytics: importaciones de referencia y acceso seguro

### Dónde quedan los archivos de ventas

`AnalyticsView.tsx` llama a `db.importSalesReference(file, activeAccountId)`. La app
lee el `.xlsx`/`.csv` en el navegador; no guarda el libro original en Firebase
Storage. Guarda metadatos en `imports` (`type: sales_reference`, `label`,
`itemCount`, `importedAt` y `accountId` opcional) y filas parseadas en
`sales_reference_data/{uid}/rows/{rowId}`, con `importId` y `data`. Para localizar
una importación, filtra `imports` por `type`, identifica el `label`/`accountId` y
consulta solo las filas cuyo `importId` coincide. No mezcles esta fuente con
`analytics_orders`, que es la importación propia de Analytics. La relación de
referencia con Momo's Choice está descrita en [[ttchop-automatizaciones]].

### Cómo localizar la credencial correcta en `vps-projects`

En la configuración revisada el **2026-10-16**, los archivos de proyecto tenían
estas referencias (nombres de variables, no sus valores):

- `ttchop-bot/.env` → `GOOGLE_APPLICATION_CREDENTIALS`.
- `ttchop-server/.env` → `FIREBASE_SERVICE_ACCOUNT_PATH_TTCHOP2`.

Ambas resolvían a la misma credencial de servicio y su `project_id` era `ttchop2`.
El acceso se encontró siguiendo esas referencias de configuración y comprobando
programáticamente que el archivo existe y que el JSON declara el proyecto
esperado. La ruta resuelta y el contenido de la credencial no se guardan en esta
wiki.

Para repetir la verificación, lee las variables dentro de un proceso local y
reporta solo si están presentes, si el archivo destino existe y el valor de
`project_id`. **Nunca** imprimas o registres el valor de una variable, el JSON
completo, claves privadas o tokens; no hagas `cat` de `.env`/credenciales ni los
copies al chat o al wiki. La sesión shell puede no exportar estas variables: en
este VPS la configuración estaba en los `.env` del proyecto. Las variables
`VITE_FIREBASE_*` de `webapp2/.env` son configuración cliente; no son credenciales
de inicio de sesión ni sustituyen la credencial de servicio.

### Límites de uso

La credencial de servicio tiene privilegios de Admin y puede leer/escribir por
encima de las reglas de Firestore; **no es una sesión de usuario**. Para el uso
ordinario de Analytics, utiliza una sesión autenticada de TTChop2. Solo usa una
consulta administrativa si Arturo la autoriza explícitamente y especifica el
proyecto y el objetivo; mantenla de solo lectura y con alcance mínimo. Nunca la
uses para suplantar a un usuario, hacer un barrido amplio entre cuentas o escribir
datos. Si falta sesión o autorización para el acceso solicitado, detente y pide
una vía autenticada segura. Antes de inicializar Firebase Admin, confirma
`project_id == ttchop2` y establece explícitamente ese proyecto; no dependas de
defaults ni consultes el proyecto original `ttchop`.

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

### Template de guion: Confesión y giro de revancha (2026-10-16)

La incertidumbre de despliegue anotada en la sección anterior correspondía al corte del 15 de octubre; este template quedó integrado y verificado en producción el 16 de octubre.

- Se añadió como cuarto seed `carousel_script`, con `seedKey: carousel_script_reddit_confession_v1` y `seedVersion: 2`. El guion exige 7 slides exactos, portada que comienza con la narración (sin título independiente), resolución en la última lámina y sin CTA que sustituya el final. Máximo 160 caracteres por slide; idioma seleccionado `es`, `en` o `ja`, sin mezclarlos.
- El texto público presenta una confesión original en primera persona: no copia el post ni afirma que los hechos estén verificados. No incluye “Reddit”, subreddit, usuario/handle, etiquetas de “ficción” ni datos identificables. Caption opcional, en el idioma elegido. La dirección visual del ejemplo —hombre japonés adulto y atractivo— es opcional, no una regla fija.
- Procedencia editorial interna: post anónimo/no verificado usado como premisa: https://www.reddit.com/r/ProRevenge/comments/1d8rrg6/fired_from_my_job_but_received_a_years_worth_of/ . El permalink no forma parte del arte.

#### Flujo para futuros carruseles inspirados en Reddit

1. **Buscar y seleccionar primero un post público** (antes de escribir el carrusel). Elegir un relato con conflicto entendible, detalles suficientes para conocer al protagonista y un giro/resolución que sostenga siete láminas. Guardar permalink, subreddit y fecha solo como procedencia editorial interna; no hace falta conservar ni publicar nombres de usuario/handles. Nunca asumir que un post anónimo está verificado. El precedente fue el post de r/ProRevenge publicado el 5 de junio de 2024 sobre el creador de videos universitarios despedido antes de completar su meta anual.
2. **Leer y resumir la fuente**: separar lo que el post afirma de lo que se puede comprobar; extraer premisa, personajes, agravios, acciones y desenlace. No copiar frases; no inventar atribuciones ni presentar los hechos como confirmados.
3. **Adaptar como una historia original**, en primera persona y en un solo idioma. Reordenar o cambiar personajes, oficio, escenario y detalles para hacer un arco coherente y reconocible, conservando solo la premisa inspiradora. La procedencia se queda en Cacho, no dentro de las láminas; para este encargo Arturo pidió que el arte mostrara solo la historia, sin “Reddit”, subreddit, usuario/handle ni etiquetas de ficción.
4. **Guion aprobado como precedente (2026-10-16, japonés)**: (1) gancho: seis meses después, el narrador vuelve a encontrarse con el jefe que lo despidió en un rodaje subcontratado; (2) protagonista de 29 años que hace guion, cámara, edición y subtítulos para una universidad, con meta anual de 85 videos y largas jornadas; (3) en seis meses produjo 30 videos con reproducciones muy altas, aunque el jefe lo consideró atrasado; (4) el jefe termina su contrato y entrega el resto a una productora; (5) el protagonista contacta a un viejo amigo con productora y le presenta datos y un plan realista; (6) la empresa del amigo gana el contrato, el narrador vuelve como líder de producción y el jefe queda bajo investigación por inflar el presupuesto; (7) el jefe es removido, la comisión de referencia equivale a 15 meses de sueldo y el protagonista la usa para estudiar cine, donde acredita por primera vez como director. Estos son beats de la adaptación, no hechos verificados.
5. **Dirección visual y montaje del precedente**: Arturo pidió fondos AI llamativos y un protagonista japonés adulto, guapo y consistente. Se generaron siete fondos de escena (oficina/universidad/rodaje) con Kie.ai; el modelo exacto no quedó anotado, así que no asumirlo al recrear. Se compusieron localmente como PNG verticales 1080×1920, texto japonés en capa aparte con Noto Sans CJK, gradiente lateral oscuro y sombra suave; se añadieron contador/progreso. Se hizo contact sheet y revisión visual de portada, láminas densas y cierre; se ajustó el wrapping japonés para no separar puntuación. La entrega final fue de siete PNG individuales y ZIP; no se publicó en TikTok. No incluir créditos de generación/modelo ni regenerar fondos sin autorización de gasto.
6. **QA y entrega**: confirmar siete slides, continuidad del personaje y causalidad del arco, legibilidad móvil, sin texto cortado ni sobre la cara, y final satisfactorio; mandar PNGs individuales en orden y, si conviene, ZIP. No publicar sin aprobación explícita.

- La migración verifica Firestore aunque exista la marca local v2; para cuentas con seeds de carrusel previos solo agrega el seed nuevo con clave estable, transacción create-if-absent y sin sobrescribir ediciones. Una cuenta nueva recibe el catálogo completo. El backfill ocurre desde `getTemplates()` para el usuario autenticado; no se hizo una escritura manual a Firestore.
- Fix de permisos posterior al despliegue: la transacción leía el ID estable antes de crearlo; la regla anterior, basada en `resource.data.userId`, denegaba ese get cuando el documento no existía. Se añadió una excepción autenticada, limitada al ID exacto del seed del usuario y solo cuando falta el documento; ownership de documentos existentes y regla de creación permanecen intactos. `ttchop2` PR #2 / commit `3b203e0` se desplegó con `firebase deploy --only firestore:rules --project ttchop2`; Firebase compiló y publicó las reglas. Emulator de reglas no ejecutado porque el VPS no tiene Java; la confirmación de lectura desde la sesión del usuario queda pendiente de recargar y abrir Templates.
- El cambio quedó integrado en `master` de webapp2 (commit de integración por squash `6fa2ee0`) y desplegado a Firebase Hosting del proyecto `ttchop2` únicamente; no se tocaron `/root/ttchop`, reglas de Firestore ni `ttchop-server` en ese primer deploy. Verificación final en vivo: `https://ttchop2.web.app` respondió HTTP 200, el login se renderizó sin errores de Firebase y el bundle `index-4FlHiNuC.js` incluye el título y la clave estable del template. Build y 5 tests de backfill pasan. La copia temporal del `.env` se eliminó tras el despliegue.

## Documentación interna

- `CLAUDE.md` — arquitectura, esquema de datos, trampas conocidas.
- `PLAN.md` — estado por fase y pendientes.
- `PENDIENTES-SERVIDOR.md` — lo que la webapp ya llama y ttchop-server no implementa aún.

## Relaciones

- Proyecto: [[proyecto-ttchop]] · automatizaciones: [[ttchop-automatizaciones]]
- Servidor: `ttchop-server` (ver [[ttchop-automatizaciones]]) · categoría [[categoria-tts]]