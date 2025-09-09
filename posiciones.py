import yfinance as yf
import json
import pandas as pd
import ta
import subprocess
from telegram import mensaje_general
from telegram import send_telegram_message
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")       # guarda esto en .env o en variables de entorno
CHAT_IDS  = os.getenv("TEST_IDS", "")  

# Filtra todas las verdes
def status_posiciones(ruta_json="data/compras.json"):
    with open(ruta_json, "r") as f:
        data = json.load(f)
    
    mensaje_general(BOT_TOKEN, CHAT_IDS, f" Actualizando posiciones")

    # seleccion = []
    for d in data:
        ticker = d['ticker']
        precio = d['precio']
        data = yf.download(ticker, period="1d", interval="1h", auto_adjust=True)
        actual = round(data.iloc[len(data)-1]["Close",ticker],3)


        if actual < precio:
            perdida = round(((actual-precio)/precio)*100, 2)
            if perdida< -2.5:
                mensaje_general(BOT_TOKEN, CHAT_IDS, f" {ticker} - ⚠️Stop loss 2.5%⚠️")
            
                # mensaje_general(BOT_TOKEN, CHAT_IDS, f" {ticker} - Pérdida del {perdida}%")

            # print(str(round(((actual-precio)/precio)*100, 2))+ "%")

        else:
            ganancia = round(((actual-precio)/precio)*100, 2)
            if ganancia > 7:
                mensaje_general(BOT_TOKEN, CHAT_IDS, f" {ticker} - ✅Ganancia en 7%✅")
            
                # mensaje_general(BOT_TOKEN, CHAT_IDS, f" {ticker} - Ganancia del {ganancia}%")

status_posiciones()