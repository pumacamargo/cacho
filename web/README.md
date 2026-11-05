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
