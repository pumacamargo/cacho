#!/usr/bin/env python3
"""Entrega verificable de un video a Arturo por la Bot API de Telegram.

Por qué existe: el mecanismo `MEDIA:<path>` del gateway a veces no entrega el
video (el tag no llega al texto final y el gateway no registra ni entrega ni
"Skipping"), así que el video nunca aparece en el chat. Este script manda el
archivo directo por `sendVideo` y **verifica** la respuesta (ok + message_id),
que es la única prueba real de entrega.

Uso:  python3 tg_send_video.py <ruta.mp4> [caption]
"""
import os, sys, json, urllib.request, urllib.error, uuid

ENV = '/root/.hermes/profiles/ttchop_robot/.env'
CHAT = '6407630145'          # DM de Arturo
TOKEN_KEY = 'TELEGRAM_BOT_TOKEN'


def token() -> str:
    for line in open(ENV, encoding='utf-8'):
        line = line.strip()
        if line.startswith(TOKEN_KEY + '='):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise SystemExit(f'{TOKEN_KEY} no está en {ENV}')


def send_video(path: str, caption: str = '', chat: str = CHAT) -> dict:
    if not os.path.isfile(path):
        raise SystemExit(f'no existe: {path}')
    tok = token()
    boundary = '----hermes' + uuid.uuid4().hex
    chunks = []
    for name, value in (('chat_id', chat), ('caption', caption),
                        ('supports_streaming', 'true')):
        if value:
            chunks.append(f'--{boundary}\r\nContent-Disposition: form-data; '
                          f'name="{name}"\r\n\r\n{value}\r\n'.encode())
    fn = os.path.basename(path)
    chunks.append(f'--{boundary}\r\nContent-Disposition: form-data; name="video"; '
                  f'filename="{fn}"\r\nContent-Type: video/mp4\r\n\r\n'.encode())
    with open(path, 'rb') as fh:
        chunks.append(fh.read())
    chunks.append(f'\r\n--{boundary}--\r\n'.encode())
    req = urllib.request.Request(
        f'https://api.telegram.org/bot{tok}/sendVideo',
        data=b''.join(chunks),
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {'ok': False, 'error': e.read()[:400].decode('utf-8', 'replace')}


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    res = send_video(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '')
    ok = res.get('ok')
    mid = (res.get('result') or {}).get('message_id')
    print('ok:', ok, '| message_id:', mid, '| size:', os.path.getsize(sys.argv[1]))
    if not ok:
        print('error:', res.get('error') or res.get('description'))
        raise SystemExit(1)
