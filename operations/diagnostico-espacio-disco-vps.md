---
title: Diagnóstico de espacio en disco en vps-tools
created: 2026-10-31
updated: 2026-10-31
type: runbook
tags: [runbook, docker, vps, almacen, hermes]
status: active
confidence: high
---

# Diagnóstico de espacio en disco en vps-tools

Auditoría de solo lectura del disco de [[hardware-vps-tools]] tras la alerta de poco espacio. Complementa la operación de [[hermes-agent]] y el inventario de [[hardware-inventario]]. **No se ejecutó ninguna limpieza ni borrado en esta tarea.**

## Situación detectada (2026-10-31)

`/dev/sda3` (raíz `/`): 96 GB totales, 87 GB usados, **4.4 GB libres (96 %)**.

Confirmado en la revisión: **el espacio NO lo consumen copias de videos del NAS**. Todo el material audiovisual del VPS —clips de ttchop_robot, salidas de n8n y postiz, y el material del curso Gerardo Santiago— suma menos de 1 GB. Del curso solo hay 49 MB de video temporal y ~1.5 GB de entornos/modelos de transcripción en el scratch de `jr_developer`.

## Consumidores principales

| Causa | Tamaño | Detalle |
|---|---|---|
| Docker (`/var/lib/docker`) | ~48 GB | Más de la mitad del disco |
| └ Capas de imágenes (`overlay2`) | 49 GB | 33 imágenes; 11.6 GB recuperables y 13 imágenes huérfanas `<none>` (tres de 2.2 GB) |
| └ Build cache | 5.9 GB | 100 % recuperable |
| └ Volúmenes | 7.5 GB | `paperclip_paperclip-data` 3.6 GB (servicio obsoleto), `n8n_n8n_data` 2.4 GB, `tradenote_mongo` 509 MB, `postiz-uploads` 493 MB |
| └ Logs de contenedores | 4.0 GB | `postiz-postgres` 3.1 GB + `postiz` 479 MB + otros |
| └ Imagen Paperclip | 5.1 GB | `ghcr.io/paperclipai/paperclip:latest` |
| `/root/.npm` | 11 GB | `_cacache` 9.3 GB + `_npx` 1.5 GB (caché pura) |
| `/root/n8n-server/n8n-backup` | 2.2 GB | `database.sqlite` de mayo 2025 |
| `/root/.codex` | 1.6 GB | Varias releases del binario (0.163.0 a 0.166.0) |
| `/var/cache/apt` | 1.9 GB | Paquetes `.deb`, incluido `linux-firmware` de 300 MB |
| `/root/.hermes` | 8.6 GB | `jr_developer` 2.0 GB, `ttchop_robot` 1.0 GB, caché global 697 MB |
| Otros en `/root` | — | `.cache` 819 MB, `.nvm` 768 MB, `cacho_inmotion` 717 MB, `.local` 552 MB (`opencode.db` 0.4 GB), `.claude` 301 MB, `.opencode` 238 MB |

## Causa raíz de los logs gigantes

Ningún contenedor tiene rotación de logs salvo `affine_app` (`max-size: 500m`). El daemon no configura log driver en `/etc/docker/daemon.json` (solo DNS). `postiz-postgres` acumuló 3.1 GB desde el 18 de octubre, lo que indica que ese contenedor está registrando errores de forma continua: **conviene investigar el motivo, no solo truncar el archivo**, porque el problema se repetirá.

## Acciones y su estado de autorización

| # | Acción | Ahorro | Estado |
|---|---|---|---|
| 1 | `npm cache clean --force` | ~11 GB | **Ejecutada 2026-10-31** (11 GB → 1.5 GB) |
| 2 | `docker builder prune -af` | ~5.9 GB | **Ejecutada 2026-10-31** (caché a 0) |
| 3 | `docker image prune -f` (huérfanas) | ~11.6 GB | **Ejecutada 2026-10-31** (33 → 20 imágenes, 0 huérfanas) |
| 4 | Truncar logs de contenedores | ~4.0 GB | **Ejecutada 2026-10-31** (4.0 GB → 864 KB) |
| 5 | `apt-get clean` | ~1.9 GB | **Ejecutada 2026-10-31** (1.9 GB → 48 KB) |
| 6 | Eliminar Paperclip (imagen + volumen + `pgdata`) | ~8.5 GB | Pendiente de autorización de Arturo |
| 7 | Borrar respaldo de n8n de mayo 2025 | 2.0 GB | Pendiente de autorización de Arturo |
| 8 | Tradenote (contenedores detenidos 3 meses + volumen mongo) | ~0.5 GB | Pendiente de autorización de Arturo |
| 9 | Releases viejas de Codex (0.163.0, 0.165.0) | ~0.9 GB | Pendiente de autorización de Arturo |
| 10 | Modelos de transcripción duplicados en `jr_developer` | ~1 GB | Pendiente de autorización de Arturo |
| 11 | Caché `_npx` restante | 1.5 GB | Opcional |

### Resultado de la limpieza autorizada (2026-10-31)

Ejecutadas las acciones 1–5 tras autorización de Arturo: el disco pasó de **87 GB usados / 4.4 GB libres (96 %)** a **58 GB usados / 34 GB libres (64 %)** — unos **29.6 GB liberados**. Servicios verificados después: n8n y Affine responden HTTP 200 y ningún contenedor se detuvo.

Quedan ~14 GB adicionales en las acciones 6–11, todas pendientes de autorización explícita.

Evidencia cruda de la auditoría: `/root/.hermes/cache/scratch/disk-audit/disk-report.md` (escaneo completo) y `Reporte-espacio-disco-vps.md` (resumen entregado). No se incorporaron al repositorio.

## Reglas para futuras limpiezas

- Ejecutar las limpiezas de caché/logs con autorización dentro de la misma conversación; **no borrar respaldos, volúmenes ni imágenes de servicios** sin autorización aparte.
- Antes de vaciar una caché de `npx`/Docker, verificar que no haya un worker o build en curso.
- Al añadir contenedores nuevos, fijar rotación de logs desde el inicio para no repetir este caso.
