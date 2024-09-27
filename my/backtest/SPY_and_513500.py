import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime, timedelta

from my.DataProcess import get_hist_data_from_ywcq

spy_df = get_hist_data_from_ywcq("../data/usa/SPY历史数据.csv", ['收盘'], replace={'收盘':'Close'})
new_spy_index = []
for date in spy_df.index:
    new_date = date - timedelta(days=0)
    new_spy_index.append(new_date)

spy_df.index = pd.to_datetime(new_spy_index)


# 513500数据需要处理，2022.3.28之前的数据需要除以2，因为之后发生了 1 拆 2
cn_spy_df = get_hist_data_from_ywcq("../data/usa/513500历史数据.csv", ['收盘'], replace={'收盘':'Close'})
mask = cn_spy_df.index < datetime.strptime('2022-03-30', "%Y-%m-%d").date()
cn_spy_df.loc[mask, 'Close'] /= 2
cn_spy_df['Close'] *= 360
# 时间偏移，中国的周一偏移到美国周五（向前三天），其他情况向前偏移一天
new_index = []
for date in cn_spy_df.index:
    if date.weekday() == 0:
        new_date = date - timedelta(days=3)
    else:
        new_date = date - timedelta(days=1)
    new_index.append(new_date)

cn_spy_df.index = pd.to_datetime(new_index)

common_dates = spy_df.index.intersection(cn_spy_df.index)
aligned_spy = spy_df.loc[common_dates]
aligned_cn_spy = cn_spy_df.loc[common_dates]


aligned_spy['pct_change'] = aligned_spy['Close'].pct_change() * 100
aligned_spy = aligned_spy.dropna()

aligned_cn_spy['pct_change'] = aligned_cn_spy['Close'].pct_change() * 100
aligned_cn_spy = aligned_cn_spy.dropna()

df_spy_diff = pd.DataFrame({'SPY_PCT': aligned_spy['pct_change'], '513500_PCT': aligned_cn_spy['pct_change']})


def is_abnormal(spy_pct, cn_spy_pct):
    # return (np.sign(spy_pct) != np.sign(cn_spy_pct)) or (abs(spy_pct - cn_spy_pct) > 0.02)
    if spy_pct > 0 > cn_spy_pct:
        if abs(spy_pct - cn_spy_pct) > 1:
            return True
    return False


def check_abnormal(series):
    sign_spy = np.sign(series['SPY_PCT'])
    sign_cn_spy = np.sign(series['513500_PCT'])
    return (sign_spy * sign_cn_spy < 0).sum() >= 3

df_spy_diff['abnormal'] = df_spy_diff.apply(
    lambda row: is_abnormal(row['SPY_PCT'], row['513500_PCT']), axis=1
)

plt.figure(1)
plt.plot(aligned_spy.index, aligned_spy['Close'], color='red', label='SPY')
plt.plot(aligned_cn_spy.index, aligned_cn_spy['Close'], color='blue', label='513500')
plt.legend()
plt.title("SPY ETF")
plt.xlabel("Day")
plt.ylabel('Price')
plt.show()

plt.figure(2)
plt.plot(aligned_spy.index, aligned_spy['pct_change'], color='red', label='SPY')
plt.plot(aligned_cn_spy.index, aligned_cn_spy['pct_change'], color='blue', label='513500')
plt.legend()
plt.title("SPY ETF")
plt.xlabel("Day")
plt.ylabel('Price ratio')
plt.show()