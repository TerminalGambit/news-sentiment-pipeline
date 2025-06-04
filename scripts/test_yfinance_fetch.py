import yfinance as yf
import pandas as pd

if __name__ == "__main__":
    ticker = "NVDA"
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        print("INFO:")
        for k, v in info.items():
            print(f"{k}: {v}")
        hist = stock.history(period="1y")
        print("\nHISTORY HEAD:")
        print(hist.head())
        print("\nHISTORY COLUMNS:", hist.columns)
        print("\nHISTORY INDEX TYPE:", type(hist.index[0]))
    except Exception as e:
        print(f"Error: {e}") 