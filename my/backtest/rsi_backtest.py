import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from my.Base import FundType
from my.DataProcess import get_hist_data_from_ywcq
from my.utils.index_utils import weighed_sma

"""
根据 rsi 指标，大于 60时卖出，小于 20时买入进行回测
"""

fund = FundType.NDX
start_date = '2004-09-13'
end_date = '2024-09-13'


def calculate_rsi(data, period=20):
    # 计算差分
    delta = data.diff()

    # 分离出上涨的下跌
    gain = delta.where(delta > 0, 0)
    # loss = -delta.where(delta < 0, 0)
    gain_and_loss = abs(delta)

    # 计算平均收益和平均损失
    # avg_gain = gain.rolling(window=period).mean()
    avg_gain = weighed_sma(gain, period, 1)
    # avg_loss = loss.rolling(window=period).mean()
    avg_gain_and_loss = weighed_sma(gain_and_loss, period, 1)

    rsi = (avg_gain / avg_gain_and_loss) * 100

    return rsi


def process_series(arr):
    result = np.full_like(arr, fill_value=False)

    start_idx = None
    for idx, value in enumerate(arr):
        if value:
            if start_idx is None:
                start_idx = idx
        else:
            start_idx = None

        if start_idx is not None and start_idx == idx:
            result[idx] = True
    return result

# df = get_hist_data(fund, index_ids=['Adj Close'], start_date=start_date, end_date=end_date,
#                    replace={"Adj Close": "Close", "收盘": "Close"}, freq=FreqType.Week)
df = get_hist_data_from_ywcq("../data/usa/纳斯达克100指数历史数据_wk.csv",
                             index_ids=['收盘'],
                             start_date=start_date, end_date=end_date,
                             replace={"收盘": "Close"})


BUY_RSI = 30
SELL_RSI = 80
rsi = calculate_rsi(df).dropna()

rsi['buy_origin'] = rsi['Close'] <= BUY_RSI
rsi['buy'] = process_series(rsi['buy_origin'])

rsi['sell_origin'] = rsi['Close'] >= SELL_RSI
rsi['sell'] = process_series(rsi['sell_origin'])

rsi['operation'] = np.where(rsi['buy'], 'buy',
                            np.where(rsi['sell'], 'sell', ''))

df['rsi'] = rsi['Close']
df['buy_origin'] = rsi['buy_origin']
df['buy'] = rsi['buy']
df['sell_origin'] = rsi['sell_origin']
df['sell'] = rsi['sell']
df['operation'] = rsi['operation']
df = df.dropna()


invest_per_share = 10000
invest_money = 0

for idx, value in df.iterrows():
    if value['operation'] == 'buy':
        invest_money += invest_per_share
        print(f"买入时机，日期{idx}, 价格{value['Close']},买入份额{invest_per_share/value['Close']}，总投资金额{invest_money}")
    elif value['operation'] == 'sell':
        print(f"卖出时机，日期{idx}, 价格{value['Close']}")
        # if invest_money > 0:






fig, axs = plt.subplots(2, 1)
axs[0].plot(df.index, df['Close'], color="red", linewidth=1)
axs[0].set_xlabel('time')
axs[0].set_ylabel('Price')
axs[0].set_title('NDX')

for index, row in df.iterrows():
    if row['operation'] == 'sell':
        axs[0].scatter(index, row['Close'], marker='*')
    elif row['operation'] == 'buy':
        axs[0].scatter(index, row['Close'], marker='+')
    else:
        pass


axs[0].legend()
axs[1].plot(rsi.index, rsi['Close'], color='blue', linewidth=1)
axs[1].plot(rsi.index, pd.Series(np.ones(len(rsi.index)) * BUY_RSI), color = 'red', label='BUY RSI')
axs[1].plot(rsi.index, pd.Series(np.ones(len(rsi.index)) * SELL_RSI), color = 'green', label='SELL RSI')
axs[1].set_xlabel('time')
axs[1].set_ylabel('RSI-20')
axs[1].set_title('RSI-20')
axs[1].legend()
plt.tight_layout()
plt.show()




