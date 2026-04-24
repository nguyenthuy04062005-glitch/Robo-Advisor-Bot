from __future__ import annotations
import ccxt

def main() -> None:
    exchange = ccxt.bitget({
        "enableRateLimit": True,
        "options": {"defaultType": "spot"},
    })
    markets = exchange.load_markets()
    print("Markets containing 'on' and '/USDT':\n")
    found = 0
    for symbol in sorted(markets.keys()):
        s = symbol.upper()
        if "ON/" in s or s.endswith("ON/USDT") or "ON/USDT:" in s:
            print(symbol)
            found += 1
    print(f"\nFound: {found}")
    print("\nIf the list is empty, search manually in Bitget/ccxt market list for the tokenized stock symbols you need.")

if __name__ == "__main__":
    main()
