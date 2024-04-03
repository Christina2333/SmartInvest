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

# 初始数据
# 回测数据及范围
fund = FundType.SPY
# 2007.11月是美股之前的最高值，随后跌了好多年
# start_date = '2007-11-01'
# 2000年金融危机
start_date = '2000-09-01'
end_date = '2015-09-01'
year_interval = 15
close = 'Adj Close'

# 定投策略
invest_plan = AutoInvestPlan.MONTHLY
monthday = MonthInvest.FirstTradeDay
auto_invest_amt = 100  # 定投金额

df = get_hist_data(fund, index_ids=[close], start_date=start_date, end_date=end_date,
                   replace={"Adj Close": "Close", "收盘": "Close"})

# 计算买入的日期
dates = pd.Series(df.index, name=df.index.name)
buy_days = get_all_monthdays(dates, monthday)

initial_capital = 0  # 初始资金
total_investment = 0  # 买入总金额
total_shares = 0  # 买入总份额
invest_days = []  # 定投买入日期
invest_close = []  # 定投买入价格
current_price = []  # 当前价格
margin = []  # 盈利

for date in buy_days:
    if date in df.index:
        weekly_data = df.loc[date]
    else:
        continue

    total_investment += auto_invest_amt

    # 计算可以购买的份额（假设没有交易费用）
    shares = auto_invest_amt / weekly_data['Close']
    total_shares += shares
    current = total_shares * weekly_data['Close']
    current_price.append(current / total_investment)
    margin.append(current - total_investment)
    invest_days.append(date)
    invest_close.append(weekly_data['Close'])

final_value = total_shares * df.iloc[-1]['Close']

print(f"近{year_interval}年，Investing in {fund.name} Every {monthday.name} in a month")
print(f"总投入: {total_investment}")
print(f"结果值: {final_value}")
print(f"总收益率: {final_value / total_investment:.4%}")
print(f"年复合收益：{cal_annual_compound_return(total_investment, final_value, year_interval):.4%}")
print(f"{fund.name}近{year_interval}年的总收益为: {df.iloc[-1]['Close'] / df.iloc[1]['Close']:.4%}")
print(
    f"{fund.name}近{year_interval}年的年均复合收益为: {cal_annual_compound_return(df.iloc[1]['Close'], df.iloc[-1]['Close'], year_interval):.4%}")
print(f"最大回撤为{np.nanmin(get_drawdown(df['Close'])):.4%}")

# 画图
plt.figure(1)
plt.plot(df.index, df['Close'], color="red", linewidth=1)
plt.scatter(invest_days, invest_close, color="blue", s=5)
plt.legend()
plt.title(f"Investing in {fund.name} Every {monthday.name} in a month")
plt.xlabel("Day")
plt.ylabel('Close')
plt.show()


plt.figure(2)
# plt.plot(invest_days, current_price, color="red", linewidth=1, label='current price')
plt.plot(invest_days, current_price, color="red", linewidth=1, label='margin')
plt.plot(invest_days, pd.Series(np.ones(len(invest_days))), color="blue", linewidth=1, label='one')
plt.legend()
plt.title(f"Investing in {fund.name} Every {monthday.name} in a month")
plt.xlabel("Day")
plt.ylabel('Close')
plt.show()