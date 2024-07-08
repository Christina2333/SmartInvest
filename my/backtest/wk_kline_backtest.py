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
fund = FundType.NDX
start_date = '2010-07-05'
start_datetime = datestr2dtdate(start_date)
end_date = '2024-07-05'
year_interval = 14

# 定投策略
invest_plan = AutoInvestPlan.MONTHLY
monthday = MonthInvest.FirstTradeDay
auto_invest_amt = 100  # 定投金额

invest_money = 300_0000
stock_rate = 0.5
bond_rate = 1 - stock_rate
bond_yield = 0.03

re_balance_stock_rate = 0.7



weekly_df = get_hist_data(fund, index_ids=['Open', 'High', 'Low', 'Adj Close', 'Volume'], start_date=start_date,
                          end_date=end_date,
                          replace={"Adj Close": "Close", "收盘": "Close"}, freq=FreqType.Week)

# 股票初始的份额
stock_share = invest_money * stock_rate / weekly_df.iloc[0]['Close']
# 债券金额
bond_money = invest_money * bond_rate
# 空闲金钱
free_money = 0


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
        print(f"卖出股票{stock_share * stock_close - re_stock_money}，并买入等量债券")
    elif re_stock_money > stock_share * stock_close:
        # 需要卖出债券买股票
        print(f"卖出债券{re_stock_money - stock_share * stock_close}，并买入等量股票")
    return re_stock_share, re_bond_share



weekly_df['MA_24'] = weekly_df['Close'].rolling(window=24).mean()
weekly_df['MA_48'] = weekly_df['Close'].rolling(window=48).mean()
re_balance = weekly_df['MA_24'] < weekly_df['MA_48']
last_buy = weekly_df['MA_24'] > weekly_df['MA_48']
weekly_df['re_balance'] = re_balance.astype(int).diff() == 1  # 从 False 变为 True 的转折点
weekly_df['last_buy'] = last_buy.astype(int).diff() == 1

weekly_df['operation'] = np.where(weekly_df['re_balance'], 'balance',
                                  np.where(weekly_df['last_buy'], 'buy', ''))

for index, row in weekly_df.iterrows():
    if row['operation'] == 'balance':
        print(f"日期：{index}，执行rebalance操作")
    elif row['operation'] == 'buy':
        if free_money == 0:
            print(f"日期：{index}，本该执行买入操作，但是空闲现金为 0，无法买入")
        else:
            # 买入指数
            print(f"日期：{index}，执行买入操作")
    else:
        pass





# print(weekly_df)
