import sys
from helper import draw_candlestick_graph

def main(**kwargs):
    print("tickers:")
    tickers = input()
    print("start:")
    start = input()
    print("end:")
    end = input()
    print("interval:")
    interval = input()
    draw_candlestick_graph(tickers, start, end, interval)

def test():
    draw_candlestick_graph("aapl", "2025-03-01", "2025-04-10", "1d")
if __name__ == '__main__':
    test()
    #main()