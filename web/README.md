# web/ — páginas publicadas

HTML de una sola página que se publican en el FTP para consultarlos desde el celular (no reemplazan al
wiki: son resúmenes visuales).

## `ttchop-mapa-documentacion.html`

Mapa de la documentación: las 3 herramientas (ttchop-server/FFmpeg, Remotion, FilmCraft) con el camino
por defecto, las vías para hacer un video y sus pasos previos, cómo está organizado el wiki y una tabla
de «si quieres X, esto hago».

- Editar aquí el archivo y republicar con el toolkit del repo `ttchop-server`:
  `python3 scripts/creators/shotlist/publish_ftp.py put web/ttchop-mapa-documentacion.html docs`
  (desde un host con la credencial FTPS: `/root/.config/ftp/ftpAccess.txt`).
- URL pública: <https://lemonsushi.com/uploads/vps2/docs/ttchop-mapa-documentacion.html>
- Es autónomo (sin CDN ni fuentes externas) y responsive: se ve en el celular.

## `mapa-ecosistema.html` — mapa completo (interactivo)

Todo el wiki en una página: la persona, las 6 categorías con sus proyectos, la plataforma
(hardware y sistemas) y los 15 runbooks, con **buscador**, filtros por área y fichas
desplegables. Cada ficha enlaza a su página completa en GitHub.

**No se edita a mano: se genera** desde las propias fichas del wiki (títulos, descripciones y tags).

```bash
python3 web/build-mapa.py            # regenera web/mapa-ecosistema.html
python3 scripts/creators/shotlist/publish_ftp.py put web/mapa-ecosistema.html docs   # publica (repo ttchop-server)
```

URL: <https://lemonsushi.com/uploads/vps2/docs/mapa-ecosistema.html>

> Al añadir una ficha nueva al wiki, volver a correr el generador: si es un proyecto o un runbook,
> también hay que añadir su id a las listas de `build-mapa.py` (categorías, `SISTEMAS`, `OPER_GROUPS`).

## `mapa-pecera.html` — la pecera 3D (navegable)

El mismo wiki, pero en 3D: un **cilindro de cristal** en medio de un cuarto donde el contenido
flota en capas (persona arriba, categorías, proyectos, runbooks y plataforma al fondo). Se puede
**girar alrededor**, hacer **zoom** y **entrar** a la pecera; al tocar un nombre se abre su ficha
con el enlace a GitHub.

- Se genera con `python3 web/build-pecera.py` (lee las fichas reales; mismas reglas que el mapa plano).
- **Necesita la librería local** `web/lib/` (three.js 0.160.0 vendorizado: `three.module.js`,
  `OrbitControls.js`, `CSS2DRenderer.js`) — no usa CDN. Al publicar hay que subir **la página y los 3 archivos**:

```bash
python3 scripts/creators/shotlist/publish_ftp.py put web/mapa-pecera.html docs
for f in three.module.js OrbitControls.js CSS2DRenderer.js; do
  python3 scripts/creators/shotlist/publish_ftp.py put web/lib/$f docs/lib
done
```

URL: <https://lemonsushi.com/uploads/vps2/docs/mapa-pecera.html>

### Color coding
Las **6 categorías tienen su color** y **sus proyectos usan el mismo color**, igual que las **líneas** que
los unen; los runbooks y la plataforma van en gris/azulado neutro para que la agrupación se lea de un golpe.
El color vive en `FAMILY` (generador), y la leyenda se genera de ahí.

### Controles
Los `OrbitControls` van enganchados al **canvas**, no a la capa de etiquetas: esa capa tiene
`pointer-events:none` y por eso el giro no respondía fuera de los botones. Con el canvas, se **rota
arrastrando en cualquier parte** de la página, se **panea** con botón derecho (escritorio) o **dos dedos**
(celular) y se hace zoom con rueda/pellizco.

### Dos trampas al tocar este archivo
1. **`CSS2DRenderer` reescribe `element.style.display` en cada frame.** Para ocultar etiquetas hay que
   usar una propiedad que él no toque: aquí es la clase `.lbl.off` (opacidad 0 + `pointer-events:none`).
   Con `display` parece funcionar y no funciona.
2. **Las etiquetas se filtran por nivel y por lado.** De lejos solo se ven las capas grandes
   (persona y categorías); al acercarte aparecen proyectos y luego todo. Además solo se muestran las
   del lado donde está la cámara (así se lee al girar). El umbral está en la constante `level` del loop.
