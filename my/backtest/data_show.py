import matplotlib.pyplot as plt

from my.Base import FundType
from my.DataProcess import get_hist_data

"""
NDX 和 SPY 的历史数据绘制
"""


close = 'Adj Close'
df_ndx = get_hist_data(FundType.NDX, index_ids=[close], start_date=None, end_date=None,
                       replace={"Adj Close": "Close", "收盘": "Close"})
df_spy = get_hist_data(FundType.SPY, index_ids=[close], start_date=None, end_date=None,
                       replace={"Adj Close": "Close", "收盘": "Close"})

plt.figure(1)
plt.plot(df_ndx.index, df_ndx['Close'], color="red", linewidth=1, label='NDX')
plt.title(f"^NDX(NASDAQ 100)")
plt.xlabel("Day")
plt.ylabel('Close')
plt.show()

plt.figure(2)
plt.plot(df_spy.index, df_spy['Close'], color="blue", linewidth=1, label='SPY')
plt.title(f"SPY")
plt.xlabel("Day")
plt.ylabel('Close')
plt.show()

