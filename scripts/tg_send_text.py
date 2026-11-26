#!/usr/bin/env python3
"""Manda un mensaje de texto plano a Arturo por la Bot API de Telegram.

Por qué existe: en el chat, un texto largo o con formato no se puede seleccionar
para copiar. Mandando cada término en su propio mensaje, con texto plano (sin
parse_mode), se puede mantener pulsado y copiar.

Uso:  python3 tg_send_text.py "texto"
"""
import json
import os
import sys
import urllib.parse
import urllib.request

ENV = '/root/.hermes/profiles/ttchop_robot/.env'
CHAT = '6407630145'          # DM de Arturo
TOKEN_KEY = 'TELEGRAM_BOT_TOKEN'


def token() -> str:
    for line in open(ENV, encoding='utf-8'):
        line = line.strip()
        if line.startswith(TOKEN_KEY + '='):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise SystemExit(f'{TOKEN_KEY} no está en {ENV}')


def send_text(text: str, chat: str = CHAT) -> dict:
    data = urllib.parse.urlencode({
        'chat_id': chat,
        'text': text,
        'disable_web_page_preview': 'true',
    }).encode()
    url = f'https://api.telegram.org/bot{token()}/sendMessage'
    with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=30) as r:
        return json.loads(r.read().decode())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit('uso: tg_send_text.py "texto"')
    res = send_text(sys.argv[1])
    if not res.get('ok'):
        raise SystemExit(f'FALLO: {res}')
    print(f"ok message_id={res['result']['message_id']} texto={sys.argv[1]!r}")
