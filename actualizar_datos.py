import yfinance as yf
import json
import pandas as pd
import ta

def get_rsi_status(ticker: str):
    data = yf.download(ticker, period="1y", interval="1d", auto_adjust=True)
    if data.empty:
        return {"ticker": ticker, "status": "no data"}

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
    dias_desde_cruce_rsi = None
    for i in range(len(rsi_ultimos)-1, 0, -1):
        if rsi_ultimos.iloc[i - 1] < sma_ultimos.iloc[i - 1] and rsi_ultimos.iloc[i] > sma_ultimos.iloc[i]:
            cruce_rsi = True
            dias_desde_cruce_rsi = len(rsi_ultimos) - i
            break

    # SMAs del precio
    sma_21 = close.rolling(window=21).mean()
    sma_30 = close.rolling(window=30).mean()

    # EMAs
    ema_20 = ta.trend.EMAIndicator(close=close, window=20).ema_indicator()
    ema_50 = ta.trend.EMAIndicator(close=close, window=50).ema_indicator()
    ema_100 = ta.trend.EMAIndicator(close=close, window=100).ema_indicator()
    ema_200 = ta.trend.EMAIndicator(close=close, window=200).ema_indicator()

    # MACD
    macd = ta.trend.MACD(close=close)
    macd_line = macd.macd()
    signal_line = macd.macd_signal()

    macd_line_recent = macd_line.dropna().iloc[-7:]
    signal_line_recent = signal_line.dropna().iloc[-7:]

    cruce_macd = False
    dias_desde_cruce_macd = None
    for i in range(len(macd_line_recent)-1, 0, -1):
        if macd_line_recent.iloc[i - 1] < signal_line_recent.iloc[i - 1] and \
           macd_line_recent.iloc[i] > signal_line_recent.iloc[i]:
            cruce_macd = True
            dias_desde_cruce_macd = len(macd_line_recent) - i
            break

    precio_actual = close.iloc[-1]

    return {
        "ticker": ticker,
        "rsi": round(rsi.iloc[-1], 2),
        "sma_rsi": round(sma_rsi.iloc[-1], 2),
        "rsi_cruce_arriba_sma": cruce_rsi,
        "dias_desde_cruce_rsi": dias_desde_cruce_rsi,
        "macd": round(macd_line.iloc[-1], 2),
        "macd_signal": round(signal_line.iloc[-1], 2),
        "macd_cruce_arriba_signal": cruce_macd,
        "dias_desde_cruce_macd": dias_desde_cruce_macd,
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
    # no estan: "AAl",
    tickers = [
        'AAL', 'AAPL', 'ABEV', 'ABT', 'ACN', 'ADBE', 'ALUA.BA', 'AMD', 'AMAT', 'AMX', 'AMZN',
        'ANF', 'ARCO', 'ARKK', 'ASML', 'AVGO', 'AXP', 'AZN', 'BA', 'BABA', 'BAC', 'BB',
        'BBD', 'BHP', 'BIDU', 'BK', 'BMA', 'BRFS', 'BYMA.BA', 'C', 'CAT', 'CEPU',
        'COME.BA', 'COIN', 'COST', 'CRM', 'CSCO', 'CVS', 'DE', 'DEO', 'DIA', 'DIS', 'DOCU',
        'EA', 'EBAY', 'EBR', 'EDN', 'EEM', 'EFX', 'EQNR', 'ERIC', 'ETSY', 'ETHA', 'EWJ',
        'EWZ', 'FDX', 'FMX', 'FSLR', 'FXI', 'GGAL', 'GLOB', 'GM', 'GOOGL', 'GPRK', 'GRMN',
        'GS', 'GT', 'HD', 'HL', 'HOG', 'HSY', 'IBM', 'IBIT', 'IEUR', 'INFY', 'INTC', 'IRSA.BA',
        'ITUB', 'JD', 'JNJ', 'JPM', 'KOF', 'LLY', 'LOMA', 'LRCX', 'MCD', 'MDLZ', 'MELI',
        'META', 'METR.BA', 'MMM', 'MO', 'MRK', 'MRNA', 'MSFT', 'MSI', 'NFLX', 'NIO', 'NKE',
        'NOK', 'NTES', 'NU', 'NVDA', 'ORCL', 'ORLY', 'PAAS', 'PAGS', 'PAMP.BA', 'PBR', 'PCAR',
        'PEP', 'PFE', 'PG', 'PLTR', 'PM', 'PSX', 'PYPL', 'QQQ', 'RIO', 'RIOT', 'ROKU', 'SBUX',
        'SCCO', 'SHOP', 'SLB', 'SNAP', 'SPOT', 'SPY', 'STLA', 'TGSU2.BA', 'TGT', 'TGNO4.BA', 'TM',
        'TRAN.BA', 'TSLA', 'TSM', 'TXAR.BA', 'UNH', 'VALE', 'VALO.BA', 'VIST', 'VRSN', 'XP', 'XLV',
        'XLC', 'XLP', 'XLY', 'YELP', 'YPFD.BA', 'ZM']

    resultados = [get_rsi_status(t) for t in tickers]
    with open("data/indicadores.json", "w") as f:
        json.dump(resultados, f, indent=2)

if __name__ == "__main__":
    actualizar()
