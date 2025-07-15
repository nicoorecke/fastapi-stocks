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

    rsi = ta.momentum.RSIIndicator(close=close, window=14).rsi()
    sma_rsi = rsi.rolling(window=14).mean()

    # Últimos 4 valores válidos del RSI y su SMA
    rsi_ultimos = rsi.dropna().iloc[-4:]
    sma_ultimos = sma_rsi.dropna().iloc[-4:]

    cruce_compra = (len(rsi_ultimos) == 4 and
        ((rsi_ultimos.iloc[0] < sma_ultimos.iloc[0] and
          rsi_ultimos.iloc[1] > sma_ultimos.iloc[1]) or
         (rsi_ultimos.iloc[1] < sma_ultimos.iloc[1] and
          rsi_ultimos.iloc[2] > sma_ultimos.iloc[2]) or
         (rsi_ultimos.iloc[2] < sma_ultimos.iloc[2] and
          rsi_ultimos.iloc[3] > sma_ultimos.iloc[3]))
    )

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
        "rsi_cruce_arriba_sma": bool(cruce_compra),
        "precio": round(precio_actual, 2),
        "ema_20": round(ema_20.iloc[-1], 2),
        "ema_50": round(ema_50.iloc[-1], 2),
        "ema_100": round(ema_100.iloc[-1], 2),
        "ema_200": round(ema_200.iloc[-1], 2),
        "precio_ema_20": bool(precio_actual > ema_20.iloc[-1]),
        "precio_ema_50": bool(precio_actual > ema_50.iloc[-1]),
        "precio_ema_100": bool(precio_actual > ema_100.iloc[-1]),
        "precio_ema_200": bool(precio_actual > ema_200.iloc[-1])
    }

def actualizar():
    tickers = ["GGAL", "MELI", "EDN", "TSLA", "NVDA", "AMZN"]
    resultados = [get_rsi_status(t) for t in tickers]
    with open("data/indicadores.json", "w") as f:
        json.dump(resultados, f, indent=2)

if __name__ == "__main__":
    actualizar()
