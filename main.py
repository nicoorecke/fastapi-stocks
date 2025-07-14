from fastapi import FastAPI
from pydantic import BaseModel
import yfinance as yf
import pandas as pd
import ta
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Función para obtener RSI
def get_rsi_status(ticker: str):
    data = yf.download(ticker, period="3mo", interval="1d", auto_adjust=True)
    if data.empty:
        return {"ticker": ticker, "status": "no data"}

    rsi = ta.momentum.RSIIndicator(close=data['Close', ticker], window=14).rsi()
    last_rsi = rsi.iloc[-1]
    return {
        "ticker": ticker,
        "rsi": round(float(last_rsi), 2),
        "rsi_below_40": bool(last_rsi < 40)  # conversión explícita
    }

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/indicadores")
def indicadores():
    tickers = ["GGAL",'MELI']
    return [get_rsi_status(t) for t in tickers]
