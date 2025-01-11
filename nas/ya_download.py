import yfinance as yf

# 定义股票代码和日期范围
ticker = "TQQQ"  # 苹果公司股票代码
start_date = "2010-02-11"  # 起始日期
end_date = "2024-12-30"  # 结束日期

# 获取股票历史价格

data = yf.download(ticker, start=start_date, end=end_date)

# 检查数据是否成功下载
if not data.empty:
    # 保存为 CSV 文件
    csv_file = f"{ticker}_historical_prices.csv"
    data.to_csv(csv_file)
    print(f"Data saved to {csv_file}")
else:
    print("No data found for the given ticker and date range.")

