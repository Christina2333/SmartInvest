import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from my.Base import FundType
from my.Base import AutoInvestPlan
from my.Base import MonthInvest
from my.DataProcess import get_hist_data
from my.BaseUtils import cal_annual_compound_return
from my.BaseUtils import get_all_monthdays
from my.BaseUtils import get_drawdown
from datetime import datetime

"""
每月第一个交易日定投，计算 NDX 和 SPY 的收益率和最大回撤对比
"""

# 2000年互联网泡沫
# start_date = '2000-03-10'
start_date = '1999-07-05'
# 2007次贷危机
# start_date = '2007-10-31'
# 2020年疫情
# start_date = '2020-02-01'
# 2021底
# start_date = '2022-01-01'
end_date = '2024-07-05'
# 时间差
year_interval = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days / 365.0
close = 'Adj Close'

# 定投策略
invest_plan = AutoInvestPlan.MONTHLY
monthday = MonthInvest.FirstTradeDay
auto_invest_amt = 100  # 定投金额

df_ndx = get_hist_data(FundType.NDX, index_ids=[close], start_date=start_date, end_date=end_date,
                       replace={"Adj Close": "Close", "收盘": "Close"})
df_spy = get_hist_data(FundType.SPY, index_ids=[close], start_date=start_date, end_date=end_date,
                       replace={"Adj Close": "Close", "收盘": "Close"})

# 计算买入的日期
dates_ndx = pd.Series(df_ndx.index, name=df_ndx.index.name)
buy_days = get_all_monthdays(dates_ndx, monthday)


def get_margin(df, buy_dates):
    # 买入总金额
    total_investment = 0
    # 买入总份额
    total_shares = 0
    margin = []
    invest_days = []
    invest_close = []
    for date in buy_dates:
        if date in df.index:
            weekly_data = df.loc[date]
        else:
            continue

        total_investment += auto_invest_amt

        # 计算可以购买的份额（假设没有交易费用）
        shares = auto_invest_amt / weekly_data['Close']
        total_shares += shares
        current = total_shares * weekly_data['Close']
        margin.append((current - total_investment) / total_investment)
        invest_days.append(date)
        invest_close.append(weekly_data['Close'])
    return invest_days, margin, total_shares, total_investment, invest_close


invest_days_ndx, ndx_margin, total_shares_ndx, total_investment_ndx, ndx_close = get_margin(df_ndx, buy_days)
invest_days_spy, spy_margin, total_shares_spy, total_investment_spy, spy_close = get_margin(df_spy, buy_days)
ndx_close = (ndx_close / ndx_close[1]) - 1
spy_close = (spy_close / spy_close[1]) - 1

final_value_ndx = total_shares_ndx * df_ndx.iloc[-1]['Close']
final_value_spy = total_shares_spy * df_spy.iloc[-1]['Close']

print(f"NDX 近{year_interval}年的总收益为: {df_ndx.iloc[-1]['Close'] / df_ndx.iloc[1]['Close']:.4%}")
print(f"NDX 定投收益率: {final_value_ndx / total_investment_ndx:.4%}")
print(
    f"NDX 近{year_interval}年的年均复合收益为: {cal_annual_compound_return(df_ndx.iloc[1]['Close'], df_ndx.iloc[-1]['Close'], year_interval):.4%}")
print(f"NDX 定投 年复合收益：{cal_annual_compound_return(total_investment_ndx, final_value_ndx, year_interval):.4%}")
print(f"NDX 最大回撤为{np.nanmin(get_drawdown(df_ndx['Close'])):.4%}")
print(f"NDX定投 最大回撤为{min(ndx_margin):.4%}")

print(f"SPY 近{year_interval}年的总收益为: {df_spy.iloc[-1]['Close'] / df_spy.iloc[1]['Close']:.4%}")
print(f"SPY 定投收益率: {final_value_spy / total_investment_spy:.4%}")
print(
    f"SPY 近{year_interval}年的年均复合收益为: {cal_annual_compound_return(df_spy.iloc[1]['Close'], df_spy.iloc[-1]['Close'], year_interval):.4%}")
print(f"SPY 定投 年复合收益：{cal_annual_compound_return(total_investment_spy, final_value_spy, year_interval):.4%}")
print(f"SPY 最大回撤为{np.nanmin(get_drawdown(df_spy['Close'])):.4%}")
print(f"SPY定投 最大回撤为{min(spy_margin):.4%}")

# 画图
plt.figure(2)
plt.plot(invest_days_ndx, ndx_margin, color="red", linewidth=1, label='NDX_AUTO_INVEST')
plt.plot(invest_days_ndx, ndx_close, color="red", linestyle='--', linewidth=1, label='NDX')
plt.plot(invest_days_ndx, spy_margin, color="blue", linewidth=1, label='SPY_AUTO_INVEST')
plt.plot(invest_days_ndx, spy_close, color="blue", linestyle='--', linewidth=1, label='SPY')
plt.plot(invest_days_ndx, pd.Series(np.zeros(len(invest_days_ndx))), color="green", linewidth=1, label='zero')
plt.legend()
plt.title(f"Investing in SPY/NDX Every {monthday.name} in a month")
plt.xlabel("Day")
plt.ylabel('Close')
plt.show()
