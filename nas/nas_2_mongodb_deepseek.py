import yfinance as yf
from datetime import datetime
from pymongo import MongoClient

# 连接 MongoDB
client = MongoClient("mongodb://localhost:27017/")  # 替换为你的 MongoDB 连接字符串
db = client["stock_data"]  # 数据库名称
collection = db["TQQQ"]  # 集合名称（假设集合名称为 TQQQ）

# 查询 RSI 高于 70 或低于 30 的数据
def query_rsi_extremes():
    try:
        # 查询条件：RSI > 70 或 RSI < 30
        query = {
            "$or": [
                {"RSI": {"$gt": 70}},  # RSI 高于 70
                {"RSI": {"$lt": 30}}   # RSI 低于 30
            ]
        }

        # 查询数据
        results = collection.find(query, {"Date": 1, "Close": 1, "RSI": 1, "_id": 0})

        # 打印结果
        for doc in results:
            print(f"日期: {doc['Date']}, 收盘价: {doc['Close']}, RSI: {doc['RSI']}")
    except Exception as e:
        print(f"查询失败: {e}")

# 示例使用
query_rsi_extremes()
# 连接 MongoDB
client = MongoClient("mongodb://localhost:27017/")  # 替换为你的 MongoDB 连接字符串
db = client["stock_data"]  # 数据库名称

# 计算 RSI
def calculate_rsi(data, period=14):
    delta = data["Close"].diff()  # 计算价格变化
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()  # 平均增益
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()  # 平均损失

    rs = gain / loss  # 相对强度
    rsi = 100 - (100 / (1 + rs))  # RSI
    return rsi

# 下载股票数据并存入 MongoDB
def download_and_store_stock_data(ticker, start_date, end_date):
    try:
        # 使用 yfinance 下载股票数据
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        data.reset_index(inplace=True)  # 将索引转换为列

        # 计算 RSI
        data["RSI"] = calculate_rsi(data)

        # 添加股票代码和下载日期
        data["Ticker"] = ticker
        data["DownloadDate"] = datetime.now()

        # 将数据转换为字典格式
        data_dict = data.to_dict("records")

        # 获取以股票代码命名的集合
        collection = db[ticker]

        # 插入数据到 MongoDB
        if data_dict:
            collection.insert_many(data_dict)
            print(f"数据已存入 MongoDB: {ticker} ({start_date} 到 {end_date})")
        else:
            print(f"未找到数据: {ticker}")
    except Exception as e:
        print(f"下载或存储失败: {e}")

# 示例使用
ticker = "AAPL"  # 股票代码
start_date = "2010-02-11"  # 起始日期
end_date = "2025-01-16"  # 结束日期

import csv

def save_rsi_extremes_to_csv(filename="rsi_extremes.csv"):
    try:
        # 查询条件：RSI > 70 或 RSI < 30
        query = {
            "$or": [
                {"RSI": {"$gt": 70}},
                {"RSI": {"$lt": 30}}
            ]
        }

        # 查询数据
        results = collection.find(query, {"Date": 1, "Close": 1, "RSI": 1, "_id": 0})

        # 将结果保存到 CSV 文件
        with open(filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Date", "Close", "RSI"])
            writer.writeheader()
            for doc in results:
                writer.writerow(doc)

        print(f"结果已保存到文件: {filename}")
    except Exception as e:
        print(f"保存失败: {e}")
def save_rsi_extremes_to_csv(filename="rsi_extremes.csv"):
    try:
        # 查询条件：RSI > 70 或 RSI < 30
        query = {
            "$or": [
                {"RSI": {"$gt": 70}},
                {"RSI": {"$lt": 30}}
            ]
        }

        # 查询数据
        results = collection.find(query, {"Date": 1, "Close": 1, "RSI": 1, "_id": 0})

        # 将结果保存到 CSV 文件
        with open(filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Date", "Close", "RSI"])
            writer.writeheader()
            for doc in results:
                writer.writerow(doc)

        print(f"结果已保存到文件: {filename}")
    except Exception as e:
        print(f"保存失败: {e}")


def calculate_rsi_strategy_return():
    try:
        # 查询 TQQQ 数据，按日期排序
        results = collection.find().sort("Date", 1)  # 按日期升序排列

        # 初始化变量
        buy_price = None  # 买入价格
        total_return = 0  # 总收益率
        trade_count = 0  # 交易次数

        # 遍历数据
        for doc in results:
            rsi = doc["RSI"]
            close_price = doc["Close"]

            # 买入条件：RSI < 30 且未持有
            if rsi < 30 and buy_price is None:
                buy_price = close_price
                print(f"买入日期: {doc['Date']}, 买入价格: {buy_price}")

            # 卖出条件：RSI > 70 且已持有
            elif rsi > 70 and buy_price is not None:
                sell_price = close_price
                return_per_trade = (sell_price - buy_price) / buy_price  # 单次收益率
                total_return += return_per_trade
                trade_count += 1
                print(f"卖出日期: {doc['Date']}, 卖出价格: {sell_price}, 单次收益率: {return_per_trade:.2%}")

                # 重置买入价格
                buy_price = None

        # 打印总收益率
        print(f"总交易次数: {trade_count}")
        print(f"总收益率: {total_return:.2%}")
    except Exception as e:
        print(f"计算失败: {e}")
def calculate_rsi_strategy_final_amount():
    try:
        # 查询 TQQQ 数据，按日期排序
        results = collection.find().sort("Date", 1)  # 按日期升序排列

        # 初始化变量
        initial_capital = 100  # 初始本金 100 元
        capital = initial_capital  # 当前剩余金额
        shares_held = 0  # 持有的股票数量
        buy_price = None  # 买入价格
        trade_count = 0  # 交易次数

        # 遍历数据
        for doc in results:
            rsi = doc["RSI"]
            close_price = doc["Close"]

            # 买入条件：RSI < 30 且未持有
            if rsi < 30 and shares_held == 0:
                buy_price = close_price
                shares_held = capital / buy_price  # 用全部资金买入
                capital = 0  # 资金全部用于买入
                trade_count += 1
                print(f"买入日期: {doc['Date']}, 买入价格: {buy_price}, 买入数量: {shares_held:.2f}")

            # 卖出条件：RSI > 70 且已持有
            elif rsi > 70 and shares_held > 0:
                sell_price = close_price
                capital = shares_held * sell_price  # 卖出全部股票
                shares_held = 0  # 清空持有数量
                trade_count += 1
                print(f"卖出日期: {doc['Date']}, 卖出价格: {sell_price}, 卖出后金额: {capital:.2f}")

        # 最终剩余金额
        if shares_held > 0:
            # 如果最后仍持有股票，按最后一天的收盘价计算剩余金额
            final_price = doc["Close"]
            capital = shares_held * final_price
            print(f"最终持有股票，按最后一天收盘价计算金额: {capital:.2f}")

        # 打印结果
        print(f"初始本金: {initial_capital} 元")
        print(f"最终剩余金额: {capital:.2f} 元")
        print(f"总交易次数: {trade_count}")
        print(f"总收益率: {(capital - initial_capital) / initial_capital * 100:.2f}%")
    except Exception as e:
        print(f"计算失败: {e}")
def calculate_rsi_strategy_return_next_day():
    try:
        # 查询 TQQQ 数据，按日期排序
        results = list(collection.find().sort("Date", 1))  # 按日期升序排列

        # 初始化变量
        initial_capital = 100  # 初始本金 100 元
        capital = initial_capital  # 当前剩余金额
        shares_held = 0  # 持有的股票数量
        buy_price = None  # 买入价格
        trade_count = 0  # 交易次数

        # 遍历数据
        for i in range(len(results) - 1):  # 避免最后一天越界
            current_doc = results[i]
            next_doc = results[i + 1]  # 下一天的数据

            rsi = current_doc["RSI"]
            next_close_price = next_doc["Close"]  # 下一天的收盘价

            # 买入条件：RSI < 30 且未持有
            if rsi < 30 and shares_held == 0:
                buy_price = next_close_price  # 第二天买入
                shares_held = capital / buy_price  # 用全部资金买入
                capital = 0  # 资金全部用于买入
                trade_count += 1
                print(f"买入日期: {next_doc['Date']}, 买入价格: {buy_price}, 买入数量: {shares_held:.2f}")

            # 卖出条件：RSI > 70 且已持有
            elif rsi > 70 and shares_held > 0:
                sell_price = next_close_price  # 第二天卖出
                capital = shares_held * sell_price  # 卖出全部股票
                shares_held = 0  # 清空持有数量
                trade_count += 1
                print(f"卖出日期: {next_doc['Date']}, 卖出价格: {sell_price}, 卖出后金额: {capital:.2f}")

        # 最终剩余金额
        if shares_held > 0:
            # 如果最后仍持有股票，按最后一天的收盘价计算剩余金额
            final_price = results[-1]["Close"]
            capital = shares_held * final_price
            print(f"最终持有股票，按最后一天收盘价计算金额: {capital:.2f}")

        # 打印结果
        print(f"初始本金: {initial_capital} 元")
        print(f"最终剩余金额: {capital:.2f} 元")
        print(f"总交易次数: {trade_count}")
        print(f"总收益率: {(capital - initial_capital) / initial_capital * 100:.2f}%")
    except Exception as e:
        print(f"计算失败: {e}")

# 示例使用

def calculate_rsi_strategy_final_amount_with_condition():
    try:
        # 查询 TQQQ 数据，按日期排序
        results = list(collection.find().sort("Date", 1))  # 按日期升序排列

        # 初始化变量
        initial_capital = 100  # 初始本金 100 元
        capital = initial_capital  # 当前剩余金额
        shares_held = 0  # 持有的股票数量
        buy_price = None  # 买入价格
        trade_count = 0  # 交易次数

        # 遍历数据
        for i in range(len(results) - 1):  # 避免最后一天越界
            current_doc = results[i]
            next_doc = results[i + 1]  # 下一天的数据

            rsi = current_doc["RSI"]
            next_close_price = next_doc["Close"]  # 下一天的收盘价

            # 买入条件：RSI < 30 且未持有
            if rsi < 30 and shares_held == 0:
                buy_price = next_close_price  # 第二天买入
                shares_held = capital / buy_price  # 用全部资金买入
                capital = 0  # 资金全部用于买入
                trade_count += 1
                print(f"买入日期: {next_doc['Date']}, 买入价格: {buy_price}, 买入数量: {shares_held:.2f}")

            # 卖出条件：RSI > 70 且已持有
            elif rsi > 70 and shares_held > 0:
                sell_price = next_close_price  # 第二天卖出价
                if sell_price > buy_price:  # 只有卖出价高于买入价时才卖出
                    capital = shares_held * sell_price  # 卖出全部股票
                    shares_held = 0  # 清空持有数量
                    trade_count += 1
                    print(f"卖出日期: {next_doc['Date']}, 卖出价格: {sell_price}, 卖出后金额: {capital:.2f}")
                else:
                    print(f"卖出价低于买入价，不操作。当前持有股票数量: {shares_held:.2f}")

        # 最终剩余金额
        if shares_held > 0:
            # 如果最后仍持有股票，按最后一天的收盘价计算剩余金额
            final_price = results[-1]["Close"]
            capital = shares_held * final_price
            print(f"最终持有股票，按最后一天收盘价计算金额: {capital:.2f}")

        # 打印结果
        print(f"初始本金: {initial_capital} 元")
        print(f"最终剩余金额: {capital:.2f} 元")
        print(f"总交易次数: {trade_count}")
        print(f"总收益率: {(capital - initial_capital) / initial_capital * 100:.2f}%")
    except Exception as e:
        print(f"计算失败: {e}")
def calculate_rsi_strategy_final_amount_with_extra_condition():
    try:
        # 查询 TQQQ 数据，按日期排序
        results = list(collection.find().sort("Date", 1))  # 按日期升序排列

        # 初始化变量
        initial_capital = 100  # 初始本金 100 元
        capital = initial_capital  # 当前剩余金额
        shares_held = 0  # 持有的股票数量
        buy_price = None  # 买入价格
        last_sell_price = None  # 上次的卖出价格
        trade_count = 0  # 交易次数

        # 遍历数据
        for i in range(len(results) - 1):  # 避免最后一天越界
            current_doc = results[i]
            next_doc = results[i + 1]  # 下一天的数据

            rsi = current_doc["RSI"]
            next_close_price = next_doc["Close"]  # 下一天的收盘价

            # 买入条件：RSI < 30 且未持有
            if rsi < 30 and shares_held == 0:
                if last_sell_price is None or next_close_price < last_sell_price:  # 买入价低于上次的卖出价
                    buy_price = next_close_price  # 第二天买入
                    shares_held = capital / buy_price  # 用全部资金买入
                    capital = 0  # 资金全部用于买入
                    trade_count += 1
                    print(f"买入日期: {next_doc['Date']}, 买入价格: {buy_price}, 买入数量: {shares_held:.2f}")
                else:
                    print(f"买入价高于上次的卖出价，不操作。上次卖出价: {last_sell_price}, 当前买入价: {next_close_price}")

            # 卖出条件：RSI > 70 且已持有
            elif rsi > 70 and shares_held > 0:
                sell_price = next_close_price  # 第二天卖出价
                if sell_price > buy_price:  # 只有卖出价高于买入价时才卖出
                    capital = shares_held * sell_price  # 卖出全部股票
                    shares_held = 0  # 清空持有数量
                    last_sell_price = sell_price  # 更新上次的卖出价格
                    trade_count += 1
                    print(f"卖出日期: {next_doc['Date']}, 卖出价格: {sell_price}, 卖出后金额: {capital:.2f}")
                else:
                    print(f"卖出价低于买入价，不操作。当前持有股票数量: {shares_held:.2f}")

        # 最终剩余金额
        if shares_held > 0:
            # 如果最后仍持有股票，按最后一天的收盘价计算剩余金额
            final_price = results[-1]["Close"]
            capital = shares_held * final_price
            print(f"最终持有股票，按最后一天收盘价计算金额: {capital:.2f}")

        # 打印结果
        print(f"初始本金: {initial_capital} 元")
        print(f"最终剩余金额: {capital:.2f} 元")
        print(f"总交易次数: {trade_count}")
        print(f"总收益率: {(capital - initial_capital) / initial_capital * 100:.2f}%")
    except Exception as e:
        print(f"计算失败: {e}")
if __name__ == '__main__':
   # download_and_store_stock_data(ticker, start_date, end_date)
     #query_rsi_extremes()
  # save_rsi_extremes_to_csv()
   #calculate_rsi_strategy_return()
   #calculate_rsi_strategy_final_amount()
  # calculate_rsi_strategy_return_next_day()
    calculate_rsi_strategy_final_amount_with_condition()
 #  calculate_rsi_strategy_final_amount_with_extra_condition()