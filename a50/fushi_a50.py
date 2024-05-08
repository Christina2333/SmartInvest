import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


def str_2_time(str_time):
    return datetime.strptime(str_time, '%Y-%m-%d')


select_columns = ['日期', '收盘']
df = pd.read_csv('富时中国A50指数历史数据.csv')
df = df[select_columns]
df['日期'] = df['日期'].apply(str_2_time)
df = df.sort_values(by='日期', ascending=True)
df.set_index('日期', inplace=True)
# print(df)

plt.figure()
plt.plot(df.index, df['收盘'])
plt.show()

