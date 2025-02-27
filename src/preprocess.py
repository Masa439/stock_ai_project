import pandas as pd
import numpy as np
import os

def preprocess_stock_data(file_path):
    """
    株価データを前処理し、移動平均線（SMA_50, SMA_200）を追加する
    """
    try:
        # CSV を読み込み
        df = pd.read_csv(file_path)

        # "Date" カラムがあるか確認
        if "Date" not in df.columns:
            print(f"⚠️ {file_path} に 'Date' カラムがありません。")
            return

        # "Date" を日付型に変換（無効な日付はNaTに変換）
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])
        df.set_index("Date", inplace=True)

        # 数値型に変換
        cols_to_convert = ["Close", "High", "Low", "Open", "Volume"]
        for col in cols_to_convert:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # 欠損値処理
        df.ffill(inplace=True)  # 欠損値を前の値で埋める

        # 移動平均線を追加
        df["SMA_50"] = df["Close"].rolling(window=50, min_periods=1).mean()
        df["SMA_200"] = df["Close"].rolling(window=200, min_periods=1).mean()

        # RSIの計算
        def compute_rsi(df, window=14):
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi

        # EMAの計算
        def compute_ema(df, window=50):
            return df['Close'].ewm(span=window, adjust=False).mean()

        # RSIとEMAを計算して特徴量に追加
        df['RSI'] = compute_rsi(df)
        df['EMA_50'] = compute_ema(df, window=50)

        # 処理後のデータを保存
        save_path = file_path.replace(".csv", "_processed.csv")
        df.to_csv(save_path)

        print(f"✅ {os.path.basename(file_path)} の前処理データを保存しました: {save_path}")

    except Exception as e:
        print(f"❌ {file_path} の処理中にエラーが発生しました: {e}")

if __name__ == "__main__":
    # 修正したパス
    data_dir = "C:/Users/Nedet/Desktop/project_root/env/data"
    csv_files = [f for f in os.listdir(data_dir) if f.endswith(".csv") and not f.endswith("_processed.csv")]

    print(f"📂 {len(csv_files)} 件のデータを前処理します...")

    for csv_file in csv_files:
        preprocess_stock_data(os.path.join(data_dir, csv_file))
