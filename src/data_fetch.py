import yfinance as yf
import os

# 銘柄リストファイルのパス
tickers_file = os.path.join(os.path.dirname(__file__), "../../env/tickers.txt")

# ファイルが存在するか確認
if not os.path.exists(tickers_file):
    print(f"❌ tickers.txt が見つかりません: {tickers_file}")
    exit()

# 銘柄リストを読み込む（ティッカーのみを取得）
with open(tickers_file, "r", encoding="utf-8") as f:
    tickers = [line.split(",")[0].strip() for line in f.readlines() if line.strip()]

print(f"✅ 読み込んだ銘柄リスト: {tickers}")

# データを保存するディレクトリ
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../env/data"))
os.makedirs(data_dir, exist_ok=True)

# 銘柄ごとにデータを取得
for ticker in tickers:
    print(f"📊 {ticker} のデータを取得中...")

    # 取得期間を10年分（2014年以降）に変更
    data = yf.download(ticker, start="2014-01-01", end="2024-03-01")

    # "Date" カラムをインデックスに設定
    if 'Date' not in data.columns:
        data.reset_index(inplace=True)

    # 保存先のファイルパス
    file_path = os.path.join(data_dir, f"{ticker}_stock_data.csv")

    # データをCSVに保存
    data.to_csv(file_path, index=False)
    print(f"✅ {ticker} のデータを保存しました: {file_path}")

print("📊 データ取得が完了しました！")
