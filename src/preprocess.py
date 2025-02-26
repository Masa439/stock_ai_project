import pandas as pd

def preprocess_stock_data(ticker):
    """
    取得した株価データを前処理し、移動平均線を追加する
    """
    file_path = f"../env/data/{ticker}.csv"
    df = pd.read_csv(file_path, index_col="Date", parse_dates=True)

    # 移動平均線を追加
    df["SMA_50"] = df["Close"].rolling(window=50).mean()
    df["SMA_200"] = df["Close"].rolling(window=200).mean()

    # 保存
    df.to_csv(f"../env/data/{ticker}_processed.csv")
    print(f" {ticker} の前処理データを保存しました")

if __name__ == "__main__":
    preprocess_stock_data("AAPL")  # Appleのデータを前処理
