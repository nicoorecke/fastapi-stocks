import yfinance as yf
import json
import pandas as pd
import ta

def get_rsi_status(ticker: str):
    data = yf.download(ticker, period="3mo", interval="1d", auto_adjust=True)
    if data.empty:
        return {"ticker": ticker, "status": "no data"}
    
    close = data["Close"] if isinstance(data.columns, pd.Index) else data[("Close", ticker)]
    rsi = ta.momentum.RSIIndicator(close=close, window=14).rsi()
    last_rsi = rsi.iloc[-1]
    return {
        "ticker": ticker,
        "rsi": round(last_rsi, 2),
        "rsi_below_40": bool(last_rsi < 40)
    }

def actualizar():
    tickers = ["GGAL", "MELI"]
    resultados = [get_rsi_status(t) for t in tickers]
    with open("indicadores.json", "w") as f:
        json.dump(resultados, f, indent=2)

if __name__ == "__main__":
    actualizar()
