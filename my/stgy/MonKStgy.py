"""
根据月K 的 5、10、20均线进行判断
买入：10在 20均线之上
卖出：5在 10均线之下
"""
import pandas as pd

from my.Base import FundType
from my.DataProcess import get_hist_data
from my.Base import Constant

import matplotlib.pyplot as plt


def month_k_stge(fund_type, data, start_date, end_date, params):
    """
    data为数据，index 为 datetime.date，Close 为收盘价
    """
    # 先把日数据处理为月数据
    dates = pd.Series(data.index, name='Date')
    closes = pd.Series(data['Close'], name='Close')
    closes.reset_index(drop=True, inplace=True)
    month = dates.apply(lambda date: date.strftime('%Y-%m'))
    df = pd.DataFrame({'Date': dates, 'Month': month, 'Close': closes})
    # 直接把 Month 作为 index
    df = df.groupby('Month').min()
    df = df.drop('Date', axis=1)
    # 计算 5、10、20均线
    df['5_day_avg'] = df['Close'].rolling(window=5).mean()
    df['10_day_avg'] = df['Close'].rolling(window=10).mean()
    df['20_day_avg'] = df['Close'].rolling(window=20).mean()
    df_clean = df.dropna()
    df_clean[Constant.Hold] = ((df['10_day_avg'] > df['20_day_avg']) & (df['5_day_avg'] < df['10_day_avg'])).astype(int)
    plt.figure()
    plt.plot(df_clean.index, df_clean['Close'], color="red", linewidth=1)
    plt.plot(df_clean.index, df_clean['5_day_avg'], color="blue", linewidth=1)
    plt.plot(df_clean.index, df_clean['10_day_avg'], color="yellow", linewidth=1)
    plt.plot(df_clean.index, df_clean['20_day_avg'], color="purple", linewidth=1)
    plt.scatter(df_clean.index, df_clean[Constant.Hold] * 1000, color="blue", s=5)
    return df_clean[Constant.Hold]


if __name__ == '__main__':
    fund = FundType.GEI
    start_date = '2014-03-20'
    end_date = '2024-03-20'
    df = get_hist_data(fund, index_ids=['收盘'], start_date=start_date, end_date=end_date,
                       replace={"Adj Close": "Close", "收盘": "Close"})
    month_k_stge(fund, df, start_date, end_date, {})
