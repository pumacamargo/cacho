---
title: Estudio de creadores — fuentes, datos y versiones
created: 2026-10-31
updated: 2026-10-31
type: runbook
tags: [runbook, almacen, vps, red, decision]
status: active
confidence: high
---

# Estudio de creadores — fuentes, datos y versiones

Inventario de todo el material generado al estudiar a los dos creadores japoneses de TikTok Shop (Asu y Sora) para [[proyecto-ttchop]]: videos, transcripciones, reportes y datos de medición, con sus rutas y enlaces verificados. Sirve para responder cualquier duda sobre una cifra de la guía revisando la fuente original. El acceso al NAS se documenta en [[acceso-nas-polaris]] y el hosting en [[acceso-ftps-lemon-sushi]].

## Videos fuente (43)

- 20 de Asu y 23 de Sora. Son los videos que mide la guía.
- NAS: `\\Polaris\Projects\Tiktok\hamaca\creators_research\<creador>\videos` (por IP: `\\100.91.254.118\Projects\...`; requiere red local o Tailscale).
- Los 43 se midieron por código en la computadora con NAS directo; **no se copiaron al VPS**.

## Transcripciones (43)

- Un TXT en japonés (UTF-8) por video, con reconocimiento de voz local (faster-whisper) en la PC; nunca pasaron al VPS como audio.
- NAS: `creators_research\<creador>\transcripts`.
- Copia en el VPS para el análisis de escritura: `creator-script-language/inputs` (20 + 23 archivos).

## Reportes en el NAS

En `Projects\Tiktok\hamaca\creators_research\`:

| Archivo | Contenido | Tamaño |
|---|---|---|
| `asu_kurashi\script-structure-report.md` | Análisis largo de guiones de Asu | 50 164 B |
| `sora_no_kurashi3\script-structure-report.md` | Análisis largo de guiones de Sora | 74 952 B |
| `asu_kurashi\audiovisual-audit.html` | Auditoría audiovisual de Asu | 9 408 129 B |
| `sora_no_kurashi3\audiovisual-audit.html` | Auditoría audiovisual de Sora | 10 192 783 B |
| `creator-study-*.html` | Una copia por versión del estudio (10 archivos, de 247 KB a 9.3 MB) | — |

## Reportes publicados (5 enlaces, verificados HTTP 200)

Base: `https://lemonsushi.com/uploads/vps2/creators-research/`

- Guía de estructura de guion (inglés) de Asu: `asu_kurashi/index.html` (47 494 B) y su auditoría audiovisual `asu_kurashi/audiovisual-audit.html` (9 408 129 B).
- Guía de estructura de guion (inglés) de Sora: `sora_no_kurashi3/index.html` (42 268 B) y su auditoría audiovisual `sora_no_kurashi3/audiovisual-audit.html` (10 192 783 B).
- Los 5 enlaces se comprobaron con HTTP 200 y hash exacto el 2026-10-31. **Los reportes por creador se conservan en el hosting.**

## Versiones del estudio y su historial

El hosting conserva **solo la última versión**; las anteriores se borraron del FTP el 2026-10-31 por petición de Arturo (ver [[#Limpieza del hosting|Limpieza del hosting]]). Su contenido sigue disponible en el NAS y en los espacios de trabajo del VPS.

| Versión | Qué es | Estado en el hosting |
|---|---|---|
| `study` (sin hash) | Primer volcado del estudio | Borrada |
| `study-97a276b8cae6` | Primer estudio integrado (5 grupos / 31 temas) | Borrada |
| `study-stitch-01aad09306bf` | Versión con el diseño de Stitch | Borrada |
| `study-complete-f49ae44b9303` | Reescritura completa con introducciones prácticas | Borrada |
| `study-evidence-2f685f21a16b` | Versión con evidencia y capturas reales (a la que Arturo regresó en su momento) | Borrada |
| `asu-script-pilot-93c58ce1deec` | Piloto de Script de Asu aprobado (fórmula editorial) | Borrada |
| `study-script-layout-1eb2e94a3542` | Script con dos guiones reales anotados y ejemplos al final | Borrada |
| `study-script-three-82ca7d46c1b1` | Tercer guion real; "Edition" renombrado a "Video Editing" | Borrada |
| `study-script-language-c9ed0947f474` | Script + análisis de escritura de todo el corpus (43 guiones) | Borrada |
| `study-av-collapse-b58470cb13b0` | Grabación con casos plegables y segmentos con solo la duración | Borrada |
| `study-production-preview-6d019d36afd4` y `study-production-preview-8cf3205b762e` | Reescritura de producción (rechazada por Arturo) | Borradas |
| `study-recording-editing-09be762d3696abfd` y `study-recording-editing-dd70e1ca628cd380` | Integración de la muestra visual de Grabación/Edición | Borradas |
| `study-standard-4ab186c1e022` | Estandarización antes de dejarla desplegada por defecto | Borrada |
| `study-sources-d3e378514b07` | Añadía el bloque de fuentes en el pie (Arturo pidió quitarlo de la guía) | Borrada |
| **`study-standard-63f35614c4fc`** | **Versión activa**: páginas estandarizadas en 5 secciones, todo desplegado por defecto, sin Hybrid | **Conservada** |

- Versión activa: `https://lemonsushi.com/uploads/vps2/creators-research/study-standard-63f35614c4fc/index.html` — SHA-256 `63f35614c4fc39508c20e4ff5a236ecdef77e36c57738162b91a3a0fc0137a03`, 16 306 232 B.

## Limpieza del hosting

- El 2026-10-31 se borraron **16 carpetas de versiones anteriores** de `/public_html/uploads/vps2/creators-research/` (~146 MB liberados): todas las `study-*` salvo la activa, la primera carpeta `study`, `asu-script-pilot-93c58ce1deec` y las dos `study-production-preview-*`.
- Se conservaron la versión activa y los dos reportes por creador (`asu_kurashi`, `sora_no_kurashi3`), verificados por lectura exacta antes y después del borrado.
- Comprobación del resultado: listado FTP con solo esas tres carpetas, lectura exacta de la guía activa (hash correcto) y de los 4 archivos de reportes (tamaños 47 494 / 9 408 129 / 42 268 / 10 192 783 B), y las 16 URLs antiguas sin responder.
- Detalle importante del hosting: **devuelve 404 intermitentes en archivos que sí existen**, así que la prueba de existencia o borrado se hace por lectura y listado FTP, no por HTTP.
- Para publicar una versión nueva, cada una va en su propia carpeta con hash en el nombre; si se decide limpiar, borrar antes de subir o listar candidatos y confirmar.

## Datos de medición guardados en el VPS

- **Mediciones automáticas de los 43 videos** (tomas/cortes candidatos, movimiento, iluminación, texto, audio, integridad): `~/.hermes/profiles/developer/workspace/creator-av-audit/verification/results` (20 Asu + 23 Sora).
- **Muestras revisadas visualmente**: 6 videos (3 por creador) con observaciones guardadas, frames exactos y tiempos: `creator-av-audit/semantic-results` y `semantic-evidence`.
- **Construcción de la guía activa** (datos, pruebas y publicación): `~/.hermes/profiles/developer/workspace/creator-standardize`.
- Regla vigente: la interpretación visual con IA se limitó a 3 videos por creador; medir por código sí se hizo sobre los 43.

## Reglas y límites registrados

- Las transcripciones y paquetes de auditoría **no se publican**; el hosting sólo recibe el HTML de la guía.
- Los tiempos de corte e intervalo son estimaciones automáticas, no cortes confirmados; el detalle vive en las mediciones guardadas.
- El material del NAS requiere acceso a la red local (Polaris); los enlaces públicos no.
- No incluir credenciales en el wiki ni en los reportes.
