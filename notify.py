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

BOT_TOKEN = os.getenv("BOT_TOKEN")       # guarda esto en .env o en variables de entorno
CHAT_IDS  = os.getenv("CHAT_IDS", "")    # puede ser 1 o varios separados por coma
# Ejemplo .env:
# BOT_TOKEN=123456:ABC-DEF...
# CHAT_IDS=-1001234567890,987654321

def send_telegram_message(token: str, chat_id: str, text: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    r = requests.post(url, data=data, timeout=20)
    return r.ok

# notify_telegram.py  (solo cambia esta función)
def filtrar_señales(ruta_json="data/indicadores.json"):
    with open(ruta_json, "r") as f:
        data = json.load(f)

    def b(x):  # convierte None en False y asegura bool
        return bool(x) if x is not None else False

    seleccion = []
    for d in data:
        if d.get("status") == "no data":
            continue

        # Condición "todo verde"
        todo_verde = (
            b(d.get("rsi_cruce_arriba_sma")) and
            b(d.get("macd_cruce_arriba_signal")) and
            b(d.get("precio_ema_20")) and
            b(d.get("precio_ema_50")) and
            b(d.get("precio_ema_100")) and
            b(d.get("precio_ema_200")) and
            b(d.get("precio_sma_21")) and
            b(d.get("precio_sma_30"))
        )

        # 1 día desde los cruces
        rsi_1d  = d.get("dias_desde_cruce_rsi") == 1
        macd_1d = d.get("dias_desde_cruce_macd") == 1

        if todo_verde and rsi_1d and macd_1d:
            seleccion.append(d)

    return seleccion

def armar_mensaje(seleccion):
    if not seleccion:
        return "No hay señales verdes con 1 día desde cruce RSI y MACD."

    lineas = ["✅ Señales (verde + 1d RSI & MACD):"]
    for d in seleccion:
        lineas.append(
            f"- {d['ticker']}: precio={d['precio']} | RSI={d['rsi']} "
        )
    return "\n".join(lineas)

def notify():
    if not BOT_TOKEN:
        raise RuntimeError("Falta BOT_TOKEN (definilo en .env o variable de entorno).")
    if not CHAT_IDS:
        raise RuntimeError("Falta CHAT_IDS (uno o varios separados por coma).")

    seleccion = filtrar_señales("data/indicadores.json")
    mensaje = armar_mensaje(seleccion)

    ok_todos = True
    for chat in [c.strip() for c in CHAT_IDS.split(",") if c.strip()]:
        ok = send_telegram_message(BOT_TOKEN, chat, mensaje)
        ok_todos = ok_todos and ok

    if ok_todos:
        print("Mensajes enviados ✅")
    else:
        print("Algunos mensajes fallaron ⚠️")

