import yfinance as yf
import pandas as pd
import time

def fetch_stock_data(ticker, start="2023-01-01", end="2024-01-01"):
    """
    指定した銘柄の株価データを取得し、CSVに保存する
    """
    time.sleep(2)  # 2秒待機（API制限回避）

    data = yf.download(ticker, start=start, end=end)

    if data.empty:
        print(f"⚠️ {ticker} のデータが見つかりませんでした。")
    else:
        data.to_csv(f"../env/data/{ticker}.csv")
        print(f"✅ {ticker} のデータを保存しました")

if __name__ == "__main__":
    fetch_stock_data("7203.T")  # トヨタ自動車のデータを取得
