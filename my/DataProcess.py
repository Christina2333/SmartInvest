import pandas as pd

from my.Base import FundType
from my.BaseUtils import datestr2dtdate


def get_hist_data(fund_type: FundType, index_ids=None, start_date=None, end_date=None):
    """
    根据起始时间和列名获取dataset
    index_ids: []，表示需要的列
    start_date：开始时间，str类型
    end_date：结束时间，str 类型
    """
    if fund_type == FundType.NDX:
        data = pd.read_csv('data/usa/^NDX.csv').set_index('Date')
    elif fund_type == FundType.HS300 or fund_type == FundType.CSI500:
        data = pd.read_csv('data/a/basic_data.csv').set_index('datetime')
    elif fund_type == FundType.GEI:
        data = pd.read_csv('data/a/159915_SZ_mo.csv').set_index('Date')
    elif fund_type == FundType.SPY:
        data = pd.read_csv('data/usa/SPY.csv').set_index('Date')
    else:
        raise RuntimeError('不存在的fund类型')
    data.index = [datestr2dtdate(e) for e in data.index]
    if isinstance(start_date, str):
        start_date = datestr2dtdate(start_date)
    if isinstance(end_date, str):
        end_date = datestr2dtdate(end_date)
    print('基础数据起止日期: %s, %s' % (data.index[0], data.index[-1]))
    if index_ids is not None:
        data = data.loc[:, index_ids]
    if start_date is not None:
        data = data.loc[start_date:, :]
    if end_date is not None:
        data = data.loc[:end_date, :]
    return data


def get_trading_dates(fund_type: FundType, start_date=None, end_date=None):
    """
    获取start到end的交易日
    返回
        dates：交易日的datetime
    """
    if fund_type == FundType.NDX:
        dates = pd.read_csv('data/usa/^NDX.csv')['Date'].to_list()
        dates = [datestr2dtdate(e) for e in dates]
    elif fund_type == FundType.HS300 or fund_type == FundType.CSI500:
        dates = pd.read_csv('data/a/trading_date.csv')['trade_date'].to_list()
        dates = [datestr2dtdate(e, format='%Y/%m/%d') for e in dates]
    else:
        raise RuntimeError('不存在的fund类型')
    # dates = [datestr2dtdate(e) for e in dates]
    if start_date is not None:
        dates = [e for e in dates if e >= start_date]
    if end_date is not None:
        dates = [e for e in dates if e <= end_date]
    return dates
