from enum import Enum

import pysnowball as ball
import pandas as pd
from my.BaseUtils import get_dividend_per_share
from my.BaseUtils import cal_annual_compound_return
from my.dao.kline_dao import get_year_avg
from my.dao.kline_dao import get_by_stock_and_dt
from my.dao.dividend_dao import Dividend
from my.utils.KLineUtils import get_time
from my.utils.DbUtils import insert
from datetime import datetime

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
stock_list = ['SH688303', 'SH601988', 'SH601939', 'SH601919', 'SH601916', 'SH601838', 'SH601818', 'SH601699',
              'SH601658', 'SH601398', 'SH601377', 'SH601328', 'SH601318', 'SH601288', 'SH601229', 'SH601225',
              'SH601169', 'SH601166', 'SH601088', 'SH601009', 'SH601006', 'SH600919', 'SH600741', 'SH600585',
              'SH600438', 'SH600188', 'SH600089', 'SH600048', 'SH600039', 'SH600036', 'SH600028', 'SH600016',
              'SH600015', 'SZ002555', 'SZ002466', 'SZ002027', 'SZ000983', 'SZ000895', 'SZ000425', 'SZ000408',
              'SZ000002']
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


def get_dividend(d, stock_id):
    """
    根据分红接口
    """
    # 决定分红的财报 【2022年报】
    dividend_year = d['dividend_year']
    year = int(dividend_year[:4])
    # 派息日 yyyyMMdd
    equity_date = get_time(dividend['equity_date'])
    if equity_date is None:
        print('')
    # 派息方案【10派 36元（实施方案）】
    plan_explain = dividend['plan_explain']
    stock_code = stock_id.replace('SH', '').replace('SZ', '')
    # 每股分红金额
    dividend_per_share = get_dividend_per_share(plan_explain)
    if dividend_per_share is None:
        # 分红不发钱
        return Dividend(stock_id=stock_code, year=year, dividend_dt=equity_date, dividend_info=plan_explain,
                        price=None, dividend_type=0,
                        dividend_rate=None, dividend_per_share=None), False
    else:
        # 分红发钱
        mock = False
        if equity_date is None:
            equity_date = 20240403
            mock = True
            plan_explain += '(未确定具体日期)'
        # 派息日股价
        close = get_year_avg(stock_code, year)
        if close is not None and dividend_per_share is not None:
            # 分红当天股价
            price = float(close)
            # 股息率
            dividend_rate = dividend_per_share / price
        else:
            price = None
            dividend_rate = None
        return Dividend(stock_id=stock_code, year=year, dividend_dt=equity_date, dividend_info=plan_explain,
                        price=price, dividend_type=1,
                        dividend_rate=dividend_rate, dividend_per_share=dividend_per_share), mock


def get_annual_return(stock_id, begin_dt, end_dt):
    """
    计算年化收益率
    """
    begin = get_by_stock_and_dt(stock_id, begin_dt)
    end = get_by_stock_and_dt(stock_id, end_dt)
    if begin is None or end is None:
        return None
    date1 = datetime.strptime(str(begin_dt), '%Y%m%d')
    date2 = datetime.strptime(str(end_dt), '%Y%m%d')
    delta = (date2 - date1).days / 365
    return cal_annual_compound_return(float(begin.close), float(end.close), delta)


plan_list = []
stock_dividends = []
for stock_id in stock_list:
    res = ball.bonus(stock_id, 1, 20)
    dividend_list = res['data']['items']
    for dividend in dividend_list:
        d, mock = get_dividend(dividend, stock_id)
        stock_dividends.append(d)
        dividend_year = dividend['dividend_year']
        if mock:
            dividend_year += '(未公布具体日期)'
        stock_code = stock_id.replace('SH', '').replace('SZ', '')
        five_year_return = get_annual_return(stock_code, 20190403, 20240403)
        ten_year_return = get_annual_return(stock_code, 20140403, 20240403)
        if d.year >= 2013:
            plan = [stock_id, stock_name[stock_id], dividend_year, d.dividend_dt, d.dividend_info,
                    d.dividend_per_share,
                    d.price, d.dividend_rate, five_year_return, ten_year_return]
            plan_list.append(plan)
# insert(stock_dividends)

df = pd.DataFrame(plan_list,
                  columns=['股票代码', '公司名称', '分红财报', '分红日期', '分红信息', '每股分红', '分红股价',
                           '股息率', '近5年年化收益', '近10年年化收益'])

df['平均股息率'] = df.groupby('股票代码')['股息率'].transform('mean')
df.to_excel('out.xlsx', index=False)
