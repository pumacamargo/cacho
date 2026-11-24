---
title: Dashboards publicados en el hosting Lemon Sushi
created: 2026-11-24
updated: 2026-11-24
type: runbook
tags: [runbook, almacen, red, integracion, proceso]
status: active
confidence: high
related: [acceso-ftps-lemon-sushi, estudio-creadores-fuentes-datos, ttchop-webapps]
---

# Dashboards publicados en el hosting Lemon Sushi

Índice de los **tableros** que viven en el hosting de [[proyecto-lemon-sushi]] (raíz autorizada `/public_html/uploads/vps2`, acceso en [[acceso-ftps-lemon-sushi]]) y de sus generadores en [[hardware-vps-tools]]. Todos verificados por HTTP (200) y hash el 2026-11-24.

## Dashboard central (índice de todo el hosting)

- **URL:** https://lemonsushi.com/uploads/vps2/central/
- Página con **4 botones** (grupos colapsables): *Tableros y mapas* · *Estudios de creadores* · *Planes de video nuevo* · *Desmenuzados de video*. Dentro de cada grupo los documentos son enlaces (no botones); el enlace principal de un desmenuzado abre el desmenuzado real y lo demás queda anidado. Abajo lleva un índice plano de respaldo con **todos** los HTML.
- **Generador:** `/root/central/build_central.py` (vps-tools). **Auto-descubre** los HTML del FTP, agrupa por creador / producto / caso y publica en `/central/index.html` verificando por lectura de vuelta + SHA-256. Se re-ejecuta para refrescar.
- Vive en subcarpeta porque la política del hosting no admite archivos sueltos en la raíz de `vps2`.
- Ubicación del archivo local: `/root/central/index.html`.

## Dashboard de desmenuzados

- **URL:** https://lemonsushi.com/uploads/vps2/creators-research/ (también `/desmenuzados.html`)
- Reúne **todos los desmenuzados** (listas de tomas con GIFs): agrupa por fecha o idioma, con buscador; cada tarjeta enlaza a su HTML y páginas auxiliares. Incluye una sección colapsada "Estudios de creadores".
- **Generador:** `/root/desmenuzados/build_dashboard.py` (vps-tools); datos en `/root/desmenuzados/dashboard_data.json`. Toma de cada página publicada el número de tomas y la duración reales (bloque `const SHOTS`).

## Dashboard integrado del estudio de creadores (los 3 creadores)

- **URL (activa, 3 creadores):** https://lemonsushi.com/uploads/vps2/creators-research/study-standard-3c-281212a2a442/index.html
  - 26 632 479 B · SHA-256 `281212a2a442b7134ac327dd726335a2c8edaa61c781c9ee527652fa0a069d6d`
  - Selector por creador **Asu · Sora · Taku** (`perspectives: ["asu_kurashi","sora_no_kurashi3","taku_takkun_"]`), 5 secciones colapsables (Script, Video Recording, Video Editing, Audio) y sin «Hybrid».
- **Versión previa (Asu + Sora), conservada:** `study-standard-63f35614c4fc/index.html` — 16 306 232 B · SHA-256 `63f35614c4fc39508c20e4ff5a236ecdef77e36c57738162b91a3a0fc0137a03`.
- **Generador:** workspace `creator-standardize/` del perfil `developer` (`build.py` parametrizado para los 3 creadores); el pipeline y los datos del estudio se versionan en el repo **privado** `github.com/pumacamargo/creator-av-audit` (commit `f62bcc5`). Los datos de Taku vienen del estudio ya hecho en `creator-av-audit/taku-run` (ver [[estudio-creadores-fuentes-datos]]).
- Al agregar a Taku se preservó Asu/Sora (hash de datos antes = después) y no se tocó la versión anterior.

## Estudios por creador (páginas individuales)

En `creators-research/<creador>/`: `index.html` (guía de estructura de guion) + `audiovisual-audit.html` (auditoría audiovisual).

- Asu (`asu_kurashi`), Sora (`sora_no_kurashi3`), Taku (`taku_takkun_`).

## Mapas de documentación

En `docs/`: `ttchop-mapa-documentacion.html` (índice de la documentación), `mapa-ecosistema.html` (ecosistema wiki cacho) y `mapa-pecera.html` (wiki cacho en 3D).

## Reglas y límites

- Publicar solo en la raíz autorizada y en subcarpeta; verificar el archivo final por lectura de vuelta + hash y comprobar la URL por HTTP **antes** de afirmar que está disponible (el hosting da 404 intermitentes: comprobar por lectura FTP, no solo por HTTP).
- Nunca publicar secretos ni material privado (transcripciones, QA, medios fuente).
- Regenerar tras publicar o quitar desmenuzados/estudios; el generador del central auto-descubre, así que refleja altas y bajas.
- **No borrar** la versión previa del estudio sin autorización explícita de Arturo.

## Relacionado

- [[acceso-ftps-lemon-sushi]] — acceso y organización del hosting.
- [[estudio-creadores-fuentes-datos]] — inventario del estudio de creadores (fuentes, versiones y datos).
- [[planes-de-video-nuevos]] — planes de video nuevo (pestaña *Planes*).
- [[ttchop-webapps]] — las webapps del proyecto (distintas de estos dashboards estáticos).
