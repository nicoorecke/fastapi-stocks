import yfinance as yf
import json
import pandas as pd
import ta

def get_rsi_status(ticker: str):
    data = yf.download(ticker, period="3mo", interval="1d", auto_adjust=True)
    if data.empty:
        return {"ticker": ticker, "status": "no data"}
    
    close = data["Close", ticker] if isinstance(data.columns, pd.Index) else data[("Close", ticker)]
    rsi = ta.momentum.RSIIndicator(close=close, window=14).rsi()
   
    sma_rsi = rsi.rolling(window=14).mean()
    # Últimos 2 valores válidos del RSI y su SMA
    rsi_ultimos = rsi.dropna().iloc[-4:]
    sma_ultimos = sma_rsi.dropna().iloc[-4:]

    cruce_compra = (len(rsi_ultimos) == 4 and
        ((rsi_ultimos.iloc[0] < sma_ultimos.iloc[0] and
        rsi_ultimos.iloc[1] > sma_ultimos.iloc[1])
        or
        (rsi_ultimos.iloc[1] < sma_ultimos.iloc[1] and
        rsi_ultimos.iloc[2] > sma_ultimos.iloc[2])
        or
        (rsi_ultimos.iloc[2] < sma_ultimos.iloc[2] and
        rsi_ultimos.iloc[3] > sma_ultimos.iloc[3]))
    )

    print(ticker)
    print(rsi_ultimos, sma_ultimos)
    print(cruce_compra)

    return {
        "ticker": ticker,
        "rsi": round(rsi.iloc[-1], 2),
        "sma_rsi": round(sma_rsi.iloc[-1], 2),
        "rsi_cruce_arriba_sma": bool(cruce_compra)
    }

def actualizar():
    tickers = ["GGAL", "MELI", "EDN", "TSLA", "NVDA"]
    resultados = [get_rsi_status(t) for t in tickers]
    with open("data/indicadores.json", "w") as f:
        json.dump(resultados, f, indent=2)

if __name__ == "__main__":
    actualizar()
