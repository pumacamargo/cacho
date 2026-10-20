---
title: Acceso SSH a PumaDeskAsus
created: 2026-10-20
updated: 2026-10-20
type: runbook
tags: [infra, tailscale, runbook]
status: active
confidence: high
---

# Conectar a PumaDeskAsus

Desde `vps-tools` (`100.116.242.53`), conéctate por Tailscale:

La interfaz Ethernet Realtek PCIe GbE, actualmente `Up`, tiene MAC
`F0:2F:74:00:8D:3B` (la dirección necesaria para Wake-on-LAN). La interfaz Wi-Fi
está desconectada.

```bash
ssh -i /root/.ssh/id_ed25519_pumadeskasus \
  -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=yes \
  puma_@100.126.157.51
```

Para ejecutar un comando sin abrir sesión, añádelo al final; `whoami` ya se
verificó y devolvió `pumadeskasus\puma_`. La cuenta es administradora. SSH da
control por comandos, **no acceso visual a pantalla y teclado**.

La clave privada se queda en el VPS. En Windows, la clave pública está en
`%ProgramData%\ssh\administrators_authorized_keys`. La huella ED25519 verificada
es `SHA256:SzDDMv1kz9aiv7XiB2tZ0q1toyDJ0Bwg4sJrTD8wDt0`.

El acceso es por Tailscale, TCP/22; la regla general `OpenSSH-Server-In-TCP`
permanece desactivada y no se abrió ningún puerto del router. Si hay timeout,
comprueba que el PC esté encendido y conectado a Tailscale. La última prueba
expiró, aunque una conexión anterior sí funcionó.

Para revocar el acceso, elimina únicamente la línea `hermes-vps-to-pumadeskasus`
de `administrators_authorized_keys`. Consulta [[hardware-desktop-puma]] y
[[hardware-vps-tools]].