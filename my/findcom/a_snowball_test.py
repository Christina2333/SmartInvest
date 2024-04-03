from enum import Enum

import pysnowball as ball
import pandas as pd
import json


class A_IDX(Enum):
    # 沪深 300
    SH300 = 0
    # 上证 50
    SZ50 = 1
    # 科创 50
    KC50 = 2
    # 中证 500
    ZZ500 = 3


ball.set_token('xq_a_token=a803f604aa4e3ac6eda2cab6cdb26a76b83f4c04')


def prefix_and_zfill(x):
    if len(x) < 6:
        x = x.zfill(6)
    prefix = 'SH' if x.startswith('6') else 'SZ'
    return f"{prefix}{x}"


df = pd.read_excel('../data/a/a股股票.xlsx', sheet_name=A_IDX.SH300.value)
df['股票代码'] = df['股票代码'].astype(str)
df['股票代码'] = df['股票代码'].apply(prefix_and_zfill)

for index, row in df.iterrows():
    stock_id = row['股票代码']
    res = ball.quote_detail(stock_id)
    res = res['data']['quote']
    if res['name'] != row['股票简称']:
        print(f"股票代码{stock_id}有问题")
    elif res['dividend_yield'] is not None and res['dividend_yield'] > 6:
        print(f"股票{res['name']}, 股票代码{stock_id}，股息为{res['dividend']}, 股息率为{res['dividend_yield']}%")
