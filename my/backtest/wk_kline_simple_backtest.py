import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from my.Base import FundType
from my.Base import FreqType
from my.DataProcess import get_hist_data
from my.BaseUtils import cal_annual_compound_return, datestr2dtdate
from my.BaseUtils import get_drawdown

# 初始数据
# 回测数据及范围
stock_fund = FundType.NDX
bond_fund = FundType.TLT
start_date = '2010-07-05'
end_date = '2024-07-05'
year_interval = (datestr2dtdate(end_date) - datestr2dtdate(start_date)).days / 365

invest_money = 300_0000
init_invest_money = invest_money
earning = 0

stock_df = get_hist_data(stock_fund,
                         index_ids=['Open', 'High', 'Low', 'Adj Close', 'Volume'],
                         start_date=start_date, end_date=end_date,
                         replace={"Adj Close": "Close", "收盘": "Close"}, freq=FreqType.Week)

# 股票初始的份额
stock_share = invest_money / stock_df.iloc[0]['Close']

# 盈利
earnings = []

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
    if row['operation'] == 'balance':
        print(f"日期：{index}，执行卖出操作")
        earning = stock_close * stock_share - invest_money
        plt.scatter(index, stock_close, marker='*')
    elif row['operation'] == 'buy':
        print(f"日期：{index}，是买入的时机")
        invest_money = stock_close * stock_share
        plt.scatter(index, row['Close'], marker='+')
    else:
        pass
    earnings.append(earning)

# 计算最终收益
stock_money = stock_share * stock_df.iloc[-1]['Close']
annual_return = cal_annual_compound_return(init_invest_money, stock_money, year_interval)
re_balance_invest_df = pd.DataFrame(data=earnings, index=stock_df.index, columns=['money'])
re_balance_down = np.nanmin(get_drawdown(re_balance_invest_df['money']))
print(
    f"股票总价为{stock_money:.2f}, "
    f"投资{year_interval:.2f}年，平均年化收益{annual_return:.2%}，最大回撤{re_balance_down:.2%}")


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