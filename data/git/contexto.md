# VPS Git Configuration Context

## SSH Key Setup

El VPS ya tiene configurada una SSH key para GitHub:
- **Key location**: `~/.ssh/id_ed25519` (generada el 19 de enero)
- **Status**: Registrada en GitHub (https://github.com/settings/keys)
- **SSH Config**: Configurado en `~/.ssh/config`

## Para nuevos proyectos

Cuando clones o crees un nuevo repositorio en este VPS, **NO necesitas volver a configurar SSH**.

Solo ejecuta:
```bash
git clone git@github.com:usuario/repo.git
```

O si ya tienes el repo con HTTPS, cambia la URL:
```bash
git remote set-url origin git@github.com:usuario/repo.git
git push
```

## Remote URL Format

- **SSH** (recomendado para VPS): `git@github.com:usuario/repo.git`
- **HTTPS**: `https://github.com/usuario/repo.git` (requiere token o credenciales)

## Security Notes

- La SSH key privada (`id_ed25519`) está en `~/.ssh/` con permisos 600
- Nunca commitees archivos con credenciales al repositorio
- Usa `.gitignore` para excluir: `.env`, `*.key`, `*.pem`, `.github-token`
