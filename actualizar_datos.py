import yfinance as yf
import json
import pandas as pd
import ta

def get_rsi_status(ticker: str):
    data = yf.download(ticker, period="1y", interval="1d", auto_adjust=True)
    if data.empty:
        return {"ticker": ticker, "status": "no data"}

    # Ajuste si los datos vienen con columnas multiíndice
    if isinstance(data.columns, pd.MultiIndex):
        close = data[("Close", ticker)]
    else:
        close = data["Close"]

    # RSI y SMA del RSI
    rsi = ta.momentum.RSIIndicator(close=close, window=14).rsi()
    sma_rsi = rsi.rolling(window=14).mean()

    rsi_ultimos = rsi.dropna().iloc[-7:]
    sma_ultimos = sma_rsi.dropna().iloc[-7:]

    cruce_rsi = False
    if len(rsi_ultimos) == 7:
        for i in range(1, 7):
            if rsi_ultimos.iloc[i - 1] < sma_ultimos.iloc[i - 1] and rsi_ultimos.iloc[i] > sma_ultimos.iloc[i]:
                cruce_rsi = True
                break

    # SMAs del precio
    sma_21 = close.rolling(window=21).mean()
    sma_30 = close.rolling(window=30).mean()

    # EMAs
    ema_20 = ta.trend.EMAIndicator(close=close, window=20).ema_indicator()
    ema_50 = ta.trend.EMAIndicator(close=close, window=50).ema_indicator()
    ema_100 = ta.trend.EMAIndicator(close=close, window=100).ema_indicator()
    ema_200 = ta.trend.EMAIndicator(close=close, window=200).ema_indicator()

    precio_actual = close.iloc[-1]

    return {
        "ticker": ticker,
        "rsi": round(rsi.iloc[-1], 2),
        "sma_rsi": round(sma_rsi.iloc[-1], 2),
        "rsi_cruce_arriba_sma": cruce_rsi,
        "precio": round(precio_actual, 2),
        "ema_20": round(ema_20.iloc[-1], 2),
        "ema_50": round(ema_50.iloc[-1], 2),
        "ema_100": round(ema_100.iloc[-1], 2),
        "ema_200": round(ema_200.iloc[-1], 2),
        "precio_ema_20": bool(precio_actual > ema_20.iloc[-1]),
        "precio_ema_50": bool(precio_actual > ema_50.iloc[-1]),
        "precio_ema_100": bool(precio_actual > ema_100.iloc[-1]),
        "precio_ema_200": bool(precio_actual > ema_200.iloc[-1]),
        "sma_21": round(sma_21.iloc[-1], 2),
        "sma_30": round(sma_30.iloc[-1], 2),
        "precio_sma_21": bool(precio_actual > sma_21.iloc[-1]),
        "precio_sma_30": bool(precio_actual > sma_30.iloc[-1])
    }

def actualizar():
    tickers = ["GGAL", "MELI", "EDN", "TSLA", "NVDA", "AMZN", "MMM"]
    resultados = [get_rsi_status(t) for t in tickers]
    with open("data/indicadores.json", "w") as f:
        json.dump(resultados, f, indent=2)

if __name__ == "__main__":
    actualizar()
