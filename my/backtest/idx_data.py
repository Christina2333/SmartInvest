import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from my.Base import FundType
from my.Base import AutoInvestPlan
from my.Base import MonthInvest
from my.DataProcess import get_hist_data
from my.BaseUtils import cal_annual_compound_return
from my.BaseUtils import get_drawdown

# 初始数据
# 回测数据及范围
fund = FundType.SPY
# 2007.11月是美股之前的最高值，随后跌了好多年
# start_date = '2007-11-01'
# 2000年金融危机
start_date = '2022-01-01'
# start_date = '2014-03-20'
# end_date = '2024-03-20'
end_date = '2024-01-01'
year_interval = 2
close = 'Adj Close'

# 定投策略
invest_plan = AutoInvestPlan.MONTHLY
monthday = MonthInvest.FirstTradeDay
auto_invest_amt = 100  # 定投金额

spy_df = get_hist_data(FundType.SPY, index_ids=[close], start_date=start_date, end_date=end_date,
                       replace={"Adj Close": "Close", "收盘": "Close"})
ndx_df = get_hist_data(FundType.NDX, index_ids=[close], start_date=start_date, end_date=end_date,
                       replace={"Adj Close": "Close", "收盘": "Close"})

# 画图
plt.figure(1)
plt.plot(spy_df.index, spy_df['Close'], color="red", linewidth=1)
plt.plot(spy_df.index, spy_df['Close'][0] * np.ones(len(spy_df.index)), color='blue', linewidth=1)
plt.legend()
plt.title(f"SPY")
plt.xlabel("Day")
plt.ylabel('Close')
plt.show()
print(f" SPY 近{year_interval}年的总收益为: {spy_df.iloc[-1]['Close'] / spy_df.iloc[1]['Close']:.4%}")
print(
    f" SPY 近{year_interval}年的年均复合收益为: {cal_annual_compound_return(spy_df.iloc[1]['Close'], spy_df.iloc[-1]['Close'], year_interval):.4%}")
print(f"最大回撤为{np.nanmin(get_drawdown(spy_df['Close'])):.4%}")


plt.figure(2)
plt.plot(ndx_df.index, ndx_df['Close'], color="red", linewidth=1)
plt.plot(ndx_df.index, ndx_df['Close'][0] * np.ones(len(ndx_df.index)), color='blue', linewidth=1)
plt.legend()
plt.title(f"NDX")
plt.xlabel("Day")
plt.ylabel('Close')
plt.show()
print(f"NDX 近{year_interval}年的总收益为: {ndx_df.iloc[-1]['Close'] / ndx_df.iloc[1]['Close']:.4%}")
print(
    f"NDX 近{year_interval}年的年均复合收益为: {cal_annual_compound_return(ndx_df.iloc[1]['Close'], ndx_df.iloc[-1]['Close'], year_interval):.4%}")
print(f"最大回撤为{np.nanmin(get_drawdown(ndx_df['Close'])):.4%}")