import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from my.Base import FundType
from my.Base import FreqType
from my.DataProcess import get_hist_data
from my.BaseUtils import cal_annual_compound_return, datestr2dtdate
from my.BaseUtils import get_drawdown
from calculate_utils import calculate_slope

"""
选择 周K的 30均线，当斜率接近 0 时卖出
"""

# 初始数据
# 回测数据及范围
stock_fund = FundType.NDX
start_date = '1999-07-05'
end_date = '2024-07-05'
year_interval = (datestr2dtdate(end_date) - datestr2dtdate(start_date)).days / 365

invest_money = 300_0000
cash = 0

stock_df = get_hist_data(stock_fund,
                         index_ids=['Open', 'High', 'Low', 'Adj Close', 'Volume'],
                         start_date=start_date, end_date=end_date,
                         replace={"Adj Close": "Close", "收盘": "Close"}, freq=FreqType.Week)

# 周 k30均线
stock_df['MA_30'] = stock_df['Close'].rolling(window=30).mean()
calculate_slope(stock_df, 'MA_30')

print(stock_df)
