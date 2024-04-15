import pandas as pd
import matplotlib.pyplot as plt
import re
from my.dao.kline_dao import get_by_stock_and_months

df = pd.read_excel('../data/pig_cycle/猪肉价格.xls', header=None, index_col=0)
df = df.T.dropna()
df = df.reindex(index=df.index[::-1])
normalize = True


def date_to_int(date):
    match = re.match(r'(\d{4})年(\d{1,2})月', date)
    year = match.group(1)
    month = match.group(2)
    return year.zfill(4) + month.zfill(2)


df['日期'] = df['指标'].apply(date_to_int)

SZ_002714 = get_by_stock_and_months('SZ002714', df['日期'])
SZ_000895 = get_by_stock_and_months('SZ000895', df['日期'])


def normalize_min_max(data):
    """
    数据归一化
    """
    min_val = min(data)
    max_val = max(data)

    if max_val == min_val:  # 防止除以零
        return [0] * len(data)  # 若所有值相等，则全部赋值为0
    else:
        normalized_data = [(x - min_val) / (max_val - min_val) for x in data]
        return normalized_data


if normalize:
    df_pig_price = normalize_min_max(df['猪肉（去骨统肉）集贸市场价格当期值(元/公斤)'])
    df_muyuan = normalize_min_max(SZ_002714)
    df_shuanghui = normalize_min_max(SZ_000895)
else:
    df_pig_price = df['猪肉（去骨统肉）集贸市场价格当期值(元/公斤)']
    df_muyuan = SZ_002714
    df_shuanghui = SZ_000895

plt.figure()
plt.tick_params(axis='x', labelsize=3)
plt.plot(df['日期'], df_pig_price, label='pig price', color='red')
plt.plot(df['日期'], df_muyuan, label='muyuan', color='green')
plt.plot(df['日期'], df_shuanghui, label='shuanghui', color='blue')
plt.legend()
plt.title(f"pig price")
plt.xlabel("Month")
plt.ylabel('Price')
plt.show()
