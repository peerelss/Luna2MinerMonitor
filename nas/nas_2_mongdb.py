import yfinance as yf
import pandas as pd
import numpy as np
from pymongo import MongoClient

def calculate_rsi(data, window=14):
    # 确保有 'Close' 列
    if 'Close' not in data.columns:
        if 'Adj Close' in data.columns:
            data['Close'] = data['Adj Close']
        else:
            raise KeyError("数据中没有 'Close' 或 'Adj Close' 列。")

    # 计算 RSI
    delta = data['Close'].diff()
    gain = np.where(delta > 0, delta, 0).flatten()
    loss = np.where(delta < 0, -delta, 0).flatten()
    avg_gain = pd.Series(gain).rolling(window=window).mean()
    avg_loss = pd.Series(loss).rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data

# 下载数据
ticker = "AAPL"
data = yf.download(ticker, start="2020-01-01", end="2023-12-31")

# 检查并修复列
data.reset_index(inplace=True)
data.columns = data.columns.map(str)  # 确保列名为字符串

# 计算 RSI
data = calculate_rsi(data)

# 插入 MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["stock_data"]
collection = db[ticker]
records = data.to_dict("records")
collection.insert_many(records)

print(f"成功插入 {len(records)} 条记录到 MongoDB!")
