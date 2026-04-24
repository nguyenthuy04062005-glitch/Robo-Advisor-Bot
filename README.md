# Fintech Part A - Robo-Advisor Starter Kit

This is a **signal bot only** for Part A. It does **not** place orders.
You still trade manually on **Bitget Spot**, which matches the exam requirement.

## What this bot does
- Connects to Bitget Spot through `ccxt`
- Pulls OHLCV candles for the symbols you choose
- Calculates:
  - EMA(9) / EMA(21) momentum
  - RSI(14) mean reversion
  - Bollinger Bands(20, 2)
- Prints console alerts:
  - `LONG_CANDIDATE`
  - `SHORT_CANDIDATE`
  - `HOLD`

## 1) Install
Open CMD in this folder and run:

```bash
py -m pip install -r requirements.txt
```

## 2) Find the exact Bitget symbols
First run:

```bash
py discover_markets.py
```

Then open `config.py` and put the exact market symbols into `SYMBOLS`, for example:

```python
SYMBOLS = [
    "AAPLon/USDT",
    "TSLAon/USDT",
    "NVDAon/USDT",
]
```

If those exact names differ on your machine, use the names shown by `discover_markets.py`.

## 3) Start the advisor bot
```bash
py advisor_bot.py
```

## 4) How to use it in Part A
- Let the bot run on your laptop
- Watch the console alerts
- When the bot shows a signal candidate, you decide whether to place a **manual** trade on Bitget Spot
- Keep screenshots of:
  - the bot running
  - your Bitget UID
  - deposit
  - order history
  - final PnL
  - withdrawal

## 5) Notes
- This bot is intentionally simple so you can explain it to the lecturer
- You can turn sound alerts on in `config.py`
- You can relax/tighten RSI thresholds in `config.py`

## 6) Important
Part A in the exam is **manual trading**.
This starter kit is only a **Robo-Advisor / signal assistant**.
