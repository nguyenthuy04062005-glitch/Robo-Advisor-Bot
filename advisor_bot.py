from __future__ import annotations
import time
from datetime import datetime, timezone
from typing import Dict, Any
import ccxt
import pandas as pd
import config
from indicators import ema, rsi, bollinger_bands
from notifier import notify, send_telegram_message

def build_exchange() -> ccxt.Exchange:
    # Khởi tạo kết nối Bitget
    exchange = ccxt.bitget({
        "enableRateLimit": True,
        "options": {"defaultType": "spot"},
    })
    return exchange

def fetch_ohlcv_df(exchange: ccxt.Exchange, symbol: str) -> pd.DataFrame:
    # Lấy dữ liệu nến
    rows = exchange.fetch_ohlcv(symbol, timeframe=config.TIMEFRAME, limit=config.CANDLE_LIMIT)
    if not rows:
        raise ValueError(f"Không lấy được dữ liệu nến cho {symbol}")
    df = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "volume"])
    return df

def evaluate_symbol(df: pd.DataFrame) -> Dict[str, Any]:
    close = pd.to_numeric(df["close"], errors="coerce")
    out: Dict[str, Any] = {}
    
    # Tính toán EMA, RSI, BB
    df["ema9"] = ema(close, config.EMA_FAST)
    df["ema21"] = ema(close, config.EMA_SLOW)
    df["rsi"] = rsi(close, config.RSI_PERIOD)
    _, bb_up, bb_low = bollinger_bands(close, config.BB_PERIOD, config.BB_STD)

    row = df.iloc[-1]
    out.update({
        "last_price": float(row["close"]),
        "ema9": float(row["ema9"]),
        "ema21": float(row["ema21"]),
        "rsi": float(row["rsi"]),
        "dp": ((row["close"] - row["open"]) / row["open"]) * 100,
        "vol": float(row["volume"])
    })

    # Logic tín hiệu (EMA Cross + RSI)
    sig = "HOLD"
    if out["ema9"] > out["ema21"] and out["rsi"] < config.RSI_OVERBOUGHT:
        sig = "LONG_CANDIDATE"
    elif out["ema9"] < out["ema21"] and out["rsi"] > config.RSI_OVERSOLD:
        sig = "SHORT_CANDIDATE"
    
    out["final_signal"] = sig
    return out

def print_decision(symbol: str, decision: Dict[str, Any]) -> None:
    now = datetime.now().strftime("%H:%M:%S")
    emoji = "🟡" if decision["final_signal"] == "HOLD" else ("🟢" if "LONG" in decision["final_signal"] else "🔴")
    status = "CANH MUA" if "LONG" in decision["final_signal"] else "CANH THEO DÕI"

    message = (
        f"📊 ROBO-ADVISOR SIGNAL\n\n"
        f"{emoji} Token: {symbol}\n"
        f"💰 Giá: {decision['last_price']:.4f} USDT\n"
        f"🎯 Tín hiệu: {decision['final_signal']}\n"
        f"📈 Biến động: {decision['dp']:+.2f}%\n"
        f"📊 RSI: {decision['rsi']:.2f}\n"
        f"📉 EMA9: {decision['ema9']:.4f}\n"
        f"📉 EMA21: {decision['ema21']:.4f}\n"
        f"🔊 Volume: {decision['vol']:.2f}\n"
        f"⏰ Thời gian: {now}\n\n"
        f"👉 {status}"
    )

    if decision["final_signal"] != "HOLD":
        print(message)
        send_telegram_message(message)
    elif config.PRINT_HOLD_SIGNALS:
        print(message)

def main() -> None:
    ex = build_exchange()
    print("Bot đang chạy... Đang quét tín hiệu.")
    while True:
        for sym in config.SYMBOLS:
            try:
                df = fetch_ohlcv_df(ex, sym)
                dec = evaluate_symbol(df)
                print_decision(sym, dec)
            except Exception as e:
                print(f"[ERROR] {sym}: {e}")
        time.sleep(config.POLL_SECONDS)

if __name__ == "__main__":
    main()