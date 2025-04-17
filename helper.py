from asyncore import write

import yfinance as yf
import mplfinance as mpf
import pandas as pd

def draw_upper_bound(price_data: pd.DataFrame):

    n = len(price_data)
    if n < 2:
        return dict()

    i_start = 0
    slope = 0
    for i in range(n-1):
        if price_data.iloc[i]["Open"] > price_data.iloc[i+1]["Open"]:
            continue

        i_start = i
        slope = price_data.iloc[i+1]["Open"] - price_data.iloc[i]["Open"]
        for offset in range(1, n-i):
            expected = price_data.iloc[i]["Open"] + slope * offset
            actual = price_data.iloc[i+offset]["Open"]
            if actual > expected:
                slope = 0
                i = i+offset
                break
    return [[(price_data.index[i_start], price_data.iloc[i_start]["Open"]), (price_data.index[n-1], price_data.iloc[i_start]["Open"] + slope * (n-i_start))]]
def draw_candlestick_graph(tickers, start, end, interval):
    # 下载AAPL日K线数据
    price_data = yf.download(tickers, start=start, end=end, interval=interval)

    # 将多重索引列转换为单层列名
    price_data.columns = [col[0] for col in price_data.columns]
    print("调整后的列名:", price_data.columns)

    # 清理数据：将价格列转换为数值，并移除包含非数值数据的行
    for column in ['Open', 'High', 'Low', 'Close']:
        price_data[column] = pd.to_numeric(price_data[column], errors='coerce')
    price_data = price_data.dropna(subset=['Open', 'High', 'Low', 'Close'])

    print(price_data)


    # 画线
    line_defs = dict(
        alines = draw_upper_bound(price_data),
    )

    # 绘制基础的日K线图
    mpf.plot(price_data, type='candle', volume=False, title="AAPL Daily Candlestick", **line_defs)

