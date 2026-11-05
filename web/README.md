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
