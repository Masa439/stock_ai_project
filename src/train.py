import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import glob
import os

# `tickers.txt` からティッカーのみを取得（銘柄名は無視）
tickers_file = "C:/Users/Nedet/Desktop/project_root/env/tickers.txt"
with open(tickers_file, "r", encoding="utf-8") as f:
    tickers = [line.split(",")[0].strip() for line in f.readlines() if line.strip()]

# データの読み込み（すべての `_processed.csv` を結合）
data_dir = "C:/Users/Nedet/Desktop/project_root/env/data"
file_paths = [os.path.join(data_dir, f"{ticker}_stock_data_processed.csv") for ticker in tickers if os.path.exists(os.path.join(data_dir, f"{ticker}_stock_data_processed.csv"))]

df_list = []
for file_path in file_paths:
    df_temp = pd.read_csv(file_path)
    df_temp["Ticker"] = os.path.basename(file_path).split("_")[0]  # ティッカー名を追加
    df_list.append(df_temp)

df = pd.concat(df_list, ignore_index=True)

# 'Date' を日付型に変換し、並べ替え
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by=['Date', 'Ticker'])

# ** 各銘柄のデータを均一化**
median_size = int(df['Ticker'].value_counts().median())
df_balanced = df.groupby('Ticker', group_keys=False).apply(lambda x: x.sample(n=min(len(x), median_size), replace=False)).reset_index(drop=True)

# 特徴量とターゲットを作成
df_balanced['Target'] = (df_balanced.groupby("Ticker")['Close'].shift(-1) > df_balanced['Close']).astype(int)

# ** `Ticker` の影響を下げるために数値エンコーディング**
le = LabelEncoder()
df_balanced['Ticker_Label'] = le.fit_transform(df_balanced['Ticker'])

# **使用する特徴量**
features = ['Close', 'SMA_50', 'SMA_200', 'RSI', 'EMA_50', 'Ticker_Label']
X = df_balanced[features]
y = df_balanced['Target']

# **特徴量のスケールを統一**
scaler = StandardScaler()
X.loc[:, features] = scaler.fit_transform(X[features])

# 学習データとテストデータに分割（クラスのバランスを維持）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# クラスの不均衡を補正
num_neg = sum(y_train == 0)
num_pos = sum(y_train == 1)
scale_pos_weight = max(num_neg / num_pos, 1)

# XGBoost モデルの作成
model = xgb.XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    use_label_encoder=False,
    eval_metric='logloss'
)

# モデル学習
model.fit(X_train, y_train)

# 予測と評価
y_pred = model.predict(X_test)
print(f" Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(" Classification Report:")
print(classification_report(y_test, y_pred, zero_division=1))

# 特徴量の重要度をプロット
feature_importances = model.feature_importances_
plt.barh(features, feature_importances)
plt.xlabel('Importance')
plt.title('Feature Importance')
plt.show()
