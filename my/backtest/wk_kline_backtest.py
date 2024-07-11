import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from my.Base import FundType
from my.Base import FreqType
from my.Base import AutoInvestPlan
from my.Base import WeekDay
from my.Base import MonthInvest
from my.DataProcess import get_hist_data
from my.BaseUtils import cal_annual_compound_return, datestr2dtdate
from my.BaseUtils import get_all_weekdays
from my.BaseUtils import get_all_monthdays
from my.BaseUtils import get_drawdown

# 初始数据
# 回测数据及范围
stock_fund = FundType.NDX
bond_fund = FundType.TLT
start_date = '2010-07-05'
end_date = '2024-07-05'
year_interval = (datestr2dtdate(end_date) - datestr2dtdate(start_date)).days / 365

# 定投策略
invest_plan = AutoInvestPlan.MONTHLY
monthday = MonthInvest.FirstTradeDay
auto_invest_amt = 100  # 定投金额

invest_money = 300_0000
init_invest_money = invest_money
stock_rate = 0.7
bond_rate = 1 - stock_rate

# re_balance_stock_rate = 0.7

stock_df = get_hist_data(stock_fund,
                         index_ids=['Open', 'High', 'Low', 'Adj Close', 'Volume'],
                         start_date=start_date, end_date=end_date,
                         replace={"Adj Close": "Close", "收盘": "Close"}, freq=FreqType.Week)

bond_df = get_hist_data(bond_fund,
                        index_ids=['Open', 'High', 'Low', 'Adj Close', 'Volume'],
                        start_date=start_date, end_date=end_date,
                        replace={"Adj Close": "Close", "收盘": "Close"}, freq=FreqType.Week)

# all_money

# 股票初始的份额
stock_share = invest_money * stock_rate / stock_df.iloc[0]['Close']
stock_init_share = stock_share
# 债券金额
bond_share = invest_money * bond_rate / bond_df.iloc[0]['Close']
bond_init_share = bond_share

re_balance_invest = []


def re_balance_operation(stock_share, stock_close,
                         stock_balance_rate,
                         bond_share, bond_close):
    """
    rebalance操作
    stock_share：当前持有的 股票etf 份额
    stock_close：执行 rebalance 当天的 股票etf 收盘价
    stock_balance_rate：rebalance 后股票占比
    bond_share：债券份额
    bond_close：债券价格
    """
    # 当前总资产
    current_money = stock_share * stock_close + bond_share * bond_close

    re_stock_money = current_money * stock_balance_rate
    re_stock_share = re_stock_money / stock_close

    re_bond_money = current_money * (1 - stock_balance_rate)
    re_bond_share = re_bond_money / bond_close
    if re_stock_money < stock_share * stock_close:
        # 需要卖出股票买债券
        print(f"卖出股票{stock_share * stock_close - re_stock_money:.2f}，并买入等量债券")
    elif re_stock_money > stock_share * stock_close:
        # 需要卖出债券买股票
        print(f"卖出债券{re_stock_money - stock_share * stock_close:.2f}，并买入等量股票")
    return re_stock_share, re_bond_share


stock_df['MA_24'] = stock_df['Close'].rolling(window=24).mean()
stock_df['MA_48'] = stock_df['Close'].rolling(window=48).mean()
re_balance = stock_df['MA_24'] < stock_df['MA_48']
last_buy = stock_df['MA_24'] > stock_df['MA_48']
stock_df['re_balance'] = re_balance.astype(int).diff() == 1  # 从 False 变为 True 的转折点
stock_df['last_buy'] = last_buy.astype(int).diff() == 1

stock_df['operation'] = np.where(stock_df['re_balance'], 'balance',
                                 np.where(stock_df['last_buy'], 'buy', ''))

plt.figure(1)
plt.plot(stock_df.index, stock_df['Close'], color="red", linewidth=1, label='NDX_WEEK')

for index, row in stock_df.iterrows():
    stock_close = row['Close']
    bond_close = bond_df.loc[index]['Close']
    if row['operation'] == 'balance':
        print(f"日期：{index}，执行rebalance操作")
        stock_share, bond_share = re_balance_operation(stock_share, stock_close, stock_rate, bond_share, bond_close)
        plt.scatter(index, stock_close, marker='*')
    elif row['operation'] == 'buy':
        print(f"日期：{index}，是买入的时机")
        plt.scatter(index, row['Close'], marker='+')
        # stock_share, bond_share = re_balance_operation(stock_share, stock_close, stock_rate, bond_share, bond_close)
    else:
        pass
    invest_money = stock_close * stock_share + bond_close * bond_share
    re_balance_invest.append(invest_money)

# 计算最终收益
stock_money = stock_share * stock_df.iloc[-1]['Close']
bond_money = bond_share * bond_df.iloc[-1]['Close']
all_money = stock_money + bond_money
annual_return = cal_annual_compound_return(init_invest_money, all_money, year_interval)
re_balance_invest_df = pd.DataFrame(data=re_balance_invest, index=stock_df.index, columns=['money'])
re_balance_down = np.nanmin(get_drawdown(re_balance_invest_df['money']))
print(
    f"股票总价为{stock_money:.2f}, 债券总价为{bond_money:.2f}, 总金额为{all_money:.2f}, "
    f"投资{year_interval:.2f}年，平均年化收益{annual_return:.2%}，最大回撤{re_balance_down:.2%}")


# plt.plot(bond_df.index, bond_df['Close'], color="blue", linewidth=1, label='TLT_WEEK')
plt.legend()
plt.title("Invest")
plt.xlabel("Day")
plt.ylabel('Close')
plt.show()


plt.figure(2)
plt.plot(stock_df.index, stock_df['MA_24'], color="red", linewidth=1, label='MA_24')
plt.plot(stock_df.index, stock_df['MA_48'], color="blue", linewidth=1, label='MA_48')
for index, row in stock_df.iterrows():

    if row['operation'] == 'balance':
        plt.scatter(index, row['MA_24'], marker='*')
    elif row['operation'] == 'buy':
        plt.scatter(index, row['MA_48'], marker='+')
    else:
        pass

plt.legend()
plt.title("MA_24_48")
plt.xlabel("Day")
plt.ylabel('MA')
plt.show()


all_money_2 = stock_init_share * stock_df.iloc[-1]['Close'] + bond_init_share * bond_df.iloc[-1]['Close']
stable_invest_money = stock_init_share * stock_df['Close'] + bond_init_share * bond_df['Close']
annual_return = cal_annual_compound_return(init_invest_money, all_money_2, year_interval)
stable_invest_money = pd.DataFrame(data=stable_invest_money.array, index=stock_df.index, columns=['money'])
stable_down = np.nanmin(get_drawdown(stable_invest_money['money']))
print(f"梭哈的年化收益率为{annual_return:.2%}，最大回撤{stable_down:.2%}")