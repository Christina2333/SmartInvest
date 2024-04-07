from enum import Enum

import pysnowball as ball
import pandas as pd
import datetime
from my.BaseUtils import get_dividend_per_share
from my.dao.kline_dao import get_by_stock_and_dt
from my.utils.KLineUtils import get_time


token = '117c88d07cecb77a9963ff144c803750b02ec004'

class A_IDX(Enum):
    # 沪深 300
    SH300 = 0
    # 上证 50
    SZ50 = 1
    # 科创 50
    KC50 = 2
    # 中证 500
    ZZ500 = 3


ball.set_token(f'xq_a_token={token}')

dividend_threshold = 5


def prefix_and_zfill(x):
    if len(x) < 6:
        x = x.zfill(6)
    prefix = 'SH' if x.startswith('6') else 'SZ'
    return f"{prefix}{x}"


df = pd.read_excel('../data/a/a股股票.xlsx', sheet_name=A_IDX.SH300.value)
df['股票代码'] = df['股票代码'].astype(str)
df['股票代码'] = df['股票代码'].apply(prefix_and_zfill)
stock_list = ['SH688303', 'SH601988', 'SH601939', 'SH601919', 'SH601916', 'SH601838', 'SH601818', 'SH601699', 'SH601658', 'SH601398', 'SH601377', 'SH601328', 'SH601318', 'SH601288', 'SH601229', 'SH601225', 'SH601169', 'SH601166', 'SH601088', 'SH601009', 'SH601006', 'SH600919', 'SH600741', 'SH600585', 'SH600438', 'SH600188', 'SH600089', 'SH600048', 'SH600039', 'SH600036', 'SH600028', 'SH600016', 'SH600015', 'SZ002555', 'SZ002466', 'SZ002027', 'SZ000983', 'SZ000895', 'SZ000425', 'SZ000408', 'SZ000002']
# stock_list = []
stock_name = {}

for index, row in df.iterrows():
    stock_id = row['股票代码']
    if stock_id in stock_list:
        stock_name[stock_id] = row['股票简称']
    # res = ball.quote_detail(stock_id)
    # res = res['data']['quote']
    # if res['name'] != row['股票简称']:
    #     print(f"股票代码{stock_id}有问题")
    # elif res['dividend_yield'] is not None and res['dividend_yield'] > dividend_threshold:
    #     stock_list.append(stock_id)
    #     stock_name[stock_id] = res['name']
    #     print(f"股票{res['name']}, 股票代码{stock_id}，股息为{res['dividend']}, 股息率为{res['dividend_yield']}%")


# print(stock_list)

plan_list = []
for stock_id in stock_list:
    res = ball.bonus(stock_id, 1, 20)
    dividend_list = res['data']['items']
    for dividend in dividend_list:
        share_date = None
        if dividend['ashare_ex_dividend_date'] is not None:
            share_date = get_time(dividend['ashare_ex_dividend_date'])
        plan_explain = dividend['plan_explain']
        dividend_per_share = get_dividend_per_share(plan_explain)
        if share_date is not None:
            stock_code = stock_id.replace('SH', '').replace('SZ', '')
            kline = get_by_stock_and_dt(stock_code, share_date)
        else:
            kline = None
        if kline is not None:
            dividend_price = float(kline.close)
            dividend_rate = dividend_per_share / dividend_price
        else:
            dividend_price = None
            dividend_rate = None
        plan = [stock_id, stock_name[stock_id], dividend['dividend_year'], share_date, plan_explain, dividend_per_share, dividend_price, dividend_rate]
        plan_list.append(plan)

df = pd.DataFrame(plan_list, columns=['股票代码', '公司名称', '分红财报', '分红日期', '分红信息', '每股分红', '分红股价', '股息率'])
df.to_excel('out.xlsx', index=False)
