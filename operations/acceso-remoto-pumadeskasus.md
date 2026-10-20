---
title: Acceso SSH a PumaDeskAsus
created: 2026-10-20
updated: 2026-10-21
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

El acceso SSH es por Tailscale, TCP/22; `OpenSSH-Server-In-TCP` permanece
desactivada y no se abrió ningún puerto del router.

## Encender y apagar

Wake-on-LAN se envía desde la Pi, que está en la misma LAN. Desde `vps-tools`:

```bash
tailscale ssh root@pi5puma01 python3 - <<'PY'
import socket, time
mac = bytes.fromhex("f02f74008d3b")
packet = b"\xff" * 6 + mac * 16
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    for _ in range(3):
        print(sock.sendto(packet, ("192.168.0.255", 9)))
        time.sleep(1)
PY
```

Después espera a que Windows inicie y verifica con `tailscale ping
100.126.157.51`.

Para apagar Windows sin forzar el cierre de aplicaciones:

```bash
ssh -i /root/.ssh/id_ed25519_pumadeskasus \
  -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=yes \
  puma_@100.126.157.51 'shutdown.exe /s /t 0'
```

Tras apagar, la falta de respuesta de Tailscale y SSH confirma que quedó fuera de
línea. El ciclo de encendido y apagado se verificó el 2026-10-21.

Para revocar el acceso, elimina únicamente la línea `hermes-vps-to-pumadeskasus`
de `administrators_authorized_keys`. Consulta [[hardware-desktop-puma]] y
[[hardware-vps-tools]].