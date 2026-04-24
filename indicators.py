from __future__ import annotations

import pandas as pd
import warnings

warnings.simplefilter("ignore", FutureWarning)

def ema(series: pd.Series, period: int) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    return s.ewm(span=period, adjust=False).mean()

def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")

    delta = s.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, pd.NA)
    out = 100 - (100 / (1 + rs))

    return pd.to_numeric(out, errors="coerce").fillna(50.0)

def bollinger_bands(series: pd.Series, period: int = 20, std_mult: float = 2.0):
    s = pd.to_numeric(series, errors="coerce")
    ma = s.rolling(period).mean()
    std = s.rolling(period).std(ddof=0)
    upper = ma + std_mult * std
    lower = ma - std_mult * std
    return ma, upper, lower