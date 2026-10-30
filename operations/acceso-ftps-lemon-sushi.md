---
title: Acceso FTPS y publicaciones web Lemon Sushi
created: 2026-10-30
updated: 2026-10-30
type: runbook
tags: [runbook, red, almacen, vps]
status: active
confidence: high
---

# Acceso FTPS y publicaciones web Lemon Sushi

Configuración de acceso desde [[hardware-vps-tools]] al hosting de [[proyecto-lemon-sushi]]. No confundir este destino con Polaris/NAS ni con la carpeta web del NAS suspendida para otros trabajos.

## Configuración y autenticación

- Archivo de configuración local: `/root/.config/ftp/config.json`.
- Credenciales locales protegidas: `/root/.config/ftp/ftpAccess.txt`; primera línea usuario, segunda contraseña. Archivo propiedad de `root`, permisos `600`. No copiar su contenido al repositorio, argumentos, logs ni publicaciones web.
- Usuario autorizado: `vps2@lemonsushi.com`.
- Servidor: `server310.web-hosting.com`, puerto `21`.
- Protocolo: **FTPS explícito**, con certificado verificado y cifrado de la conexión de datos. No es SFTP ni FTP sin cifrar.
- Comprobación real: certificado válido, TLS 1.3, autenticación y listado de directorio cifrado correctos. No se probó escritura ni se publicó contenido durante esa comprobación.
- El alias `ftp.lemonsushi.com` presentó certificado `*.web-hosting.com`, incompatible con el alias. Usar el hostname autorizado del hosting; nunca desactivar la validación TLS para evitar ese error.

## Raíz autorizada y organización

Arturo fijó `/public_html/uploads/vps2` como raíz de trabajo permitida para este acceso:

1. No escribir fuera de esa raíz.
2. No guardar archivos sueltos directamente en la raíz.
3. Crear o utilizar subcarpetas claras por proyecto o tarea, por ejemplo `/public_html/uploads/vps2/proyecto/reporte.html`.
4. Conservar el contenido existente; no sobrescribir o borrar sin alcance autorizado.
5. La configuración establece límites, pero no es por sí sola autorización para subir archivos. Antes de cada transferencia, leer la configuración y comprobar el destino normalizado, incluidos escapes mediante `..` o enlaces simbólicos.

## Equivalencia con URL pública

**Si `/public_html` es el document root de `lemonsushi.com`**, la equivalencia es:

- Raíz FTPS: `/public_html/uploads/vps2/`.
- URL base: `https://lemonsushi.com/uploads/vps2/`.
- Archivo FTPS: `/public_html/uploads/vps2/proyecto/reporte.html`.
- URL equivalente: `https://lemonsushi.com/uploads/vps2/proyecto/reporte.html`.

Se elimina el prefijo `/public_html` para construir la ruta web; no aparece en la URL. Codificar correctamente los componentes de nombres con espacios o caracteres especiales.

La equivalencia está guardada en `public_base_url`, junto con `web_document_root` y una nota de su supuesto. **No se ha comprobado mediante HTTP** la correspondencia ni la accesibilidad de un archivo concreto. Un acceso FTPS correcto no demuestra que haya listado web, que la carpeta exista o que un recurso publicado responda por HTTPS. No crear archivos de prueba ni cambiar configuración del hosting sin alcance autorizado.

## Privacidad y transferencia segura

Los archivos bajo esa ruta **pueden quedar públicamente accesibles**. Publicar únicamente contenido autorizado para acceso público; nunca contraseñas, tokens, archivos de credenciales, datos privados o respaldos sensibles. La ausencia de listado de directorio no convierte una URL en privada.

Camino probado con Python: `ftplib.FTP_TLS(context=ssl.create_default_context())`, conectar al hostname correcto en puerto 21, `auth()`, autenticar con valores cargados solo en memoria, `prot_p()` y modo pasivo antes del listado o transferencia. Proteger la apertura del archivo local con `O_NOFOLLOW` y verificar propietario/permisos.

Cuando se solicite una subida, validar la subcarpeta autorizada y verificar el archivo final mediante lectura de vuelta y hash; comprobar la URL por separado antes de afirmar que está disponible en la web.

## Relacionado

- [[hardware-vps-tools]] — host que conserva la configuración local y ejecuta el acceso.
- [[proyecto-lemon-sushi]] — contexto del proyecto Lemon Sushi.
- [[acceso-nas-polaris]] — almacenamiento privado del NAS, independiente de este hosting público.
