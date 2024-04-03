import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from my.Base import FundType
from my.Base import AutoInvestPlan
from my.Base import WeekDay
from my.Base import MonthInvest
from my.DataProcess import get_hist_data
from my.BaseUtils import cal_annual_compound_return
from my.BaseUtils import get_all_weekdays
from my.BaseUtils import get_all_monthdays
from my.BaseUtils import get_drawdown

# 初始数据
# 回测数据及范围
fund = FundType.SPY
start_date = '2014-03-26'
end_date = '2024-03-25'
year_interval = 10
close = 'Adj Close'

# 定投策略
invest_plan = AutoInvestPlan.MONTHLY
weekday = WeekDay.Friday
monthday = MonthInvest.FirstTradeDay
auto_invest_amt = 100  # 定投金额


df = get_hist_data(fund, index_ids=[close], start_date=start_date, end_date=end_date)

# 计算买入的日期
buy_days = []
if AutoInvestPlan.WEEKLY == invest_plan:
    buy_days = get_all_weekdays(start_date, end_date, weekday)
elif AutoInvestPlan.MONTHLY == invest_plan:
    dates = pd.Series(df.index, name=df.index.name)
    buy_days = get_all_monthdays(dates, monthday)
elif AutoInvestPlan.DAILY == invest_plan:
    buy_days = pd.Series(df.index, name=df.index.name)

initial_capital = 0  # 初始资金
total_investment = 0  # 买入总金额
total_shares = 0  # 买入总份额
invest_days = []  # 定投买入日期
invest_close = []  # 定投买入价格

for date in buy_days:
    if date in df.index:
        weekly_data = df.loc[date]
    else:
        continue

    total_investment += auto_invest_amt

    # 计算可以购买的份额（假设没有交易费用）
    shares = auto_invest_amt / weekly_data[close]
    total_shares += shares
    invest_days.append(date)
    invest_close.append(weekly_data[close])

final_value = total_shares * df.iloc[-1][close]

if AutoInvestPlan.WEEKLY == invest_plan:
    print(f"近{year_interval}年，Investing in {fund.name} Every {weekday.name}")
elif AutoInvestPlan.MONTHLY == invest_plan:
    print(f"近{year_interval}年，Investing in {fund.name} Every {monthday.name} in a month")
elif AutoInvestPlan.DAILY == invest_plan:
    print(f"近{year_interval}年，Investing in {fund.name} Everyday")
print(f"总投入: {total_investment}")
print(f"结果值: {final_value}")
print(f"总收益率: {final_value / total_investment:.4%}")
print(f"年复合收益：{cal_annual_compound_return(total_investment, final_value, year_interval):.4%}")
print(f"{fund.name}近{year_interval}年的总收益为: {df.iloc[-1][close] / df.iloc[1][close]:.4%}")
print(f"{fund.name}近{year_interval}年的年均复合收益为: {cal_annual_compound_return(df.iloc[1][close], df.iloc[-1][close], year_interval):.4%}")
print(f"最大回撤为{np.nanmin(get_drawdown(df[close])):.4%}")

# 画图
plt.figure()
plt.plot(df.index, df[close], color="red", linewidth=1)
plt.scatter(invest_days, invest_close, color="blue", s=5)
plt.legend()
if AutoInvestPlan.WEEKLY == invest_plan:
    plt.title(f"Investing in {fund.name} Every {weekday.name}")
elif AutoInvestPlan.MONTHLY == invest_plan:
    plt.title(f"Investing in {fund.name} Every {monthday.name} in a month")
elif AutoInvestPlan.DAILY == invest_plan:
    plt.title(f"Investing in {fund.name} Everyday")

plt.xlabel("Day")
plt.ylabel(close)
plt.show()
