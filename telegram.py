# notify_telegram.py
import os
import json
import requests
from pathlib import Path

try:
    from dotenv import load_dotenv  # pip install python-dotenv
    load_dotenv()
except Exception:
    pass  # si no está python-dotenv, igual uso variables de entorno si ya existen

# BOT_TOKEN = os.getenv("BOT_TOKEN")       # guarda esto en .env o en variables de entorno
# CHAT_IDS  = os.getenv("TEST_IDS", "")    # puede ser 1 o varios separados por coma

# Función mensaje de telegram
def send_telegram_message(token: str, chat_id: str, text: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    r = requests.post(url, data=data, timeout=20)
    return r.ok

# Funció para mandar mensajes generales a todos los grupos
def mensaje_general(bot_token: str, chat_ids: str, msj: str):

    btoken = bot_token
    chid = chat_ids

    if not btoken:
        raise RuntimeError("Falta BOT_TOKEN (definilo en .env o variable de entorno).")
    if not chid:
        raise RuntimeError("Falta CHAT_IDS (uno o varios separados por coma).")

    mensaje = msj

    ok_todos = True
    for chat in [c.strip() for c in chid.split(",") if c.strip()]:
        ok = send_telegram_message(btoken, chat, mensaje)
        ok_todos = ok_todos and ok

    if ok_todos:
        print("Mensajes enviados ✅")
    else:
        print("Algunos mensajes fallaron ⚠️")