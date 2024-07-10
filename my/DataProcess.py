import pandas as pd
import numpy as np

from datetime import datetime
from my.Base import FundType
from my.Base import FreqType
from my.BaseUtils import datestr2dtdate


def get_hist_data(fund_type: FundType, index_ids=None, start_date=None, end_date=None, replace: dict = None, freq: FreqType=FreqType.Day):
    """
    根据起始时间和列名获取dataset
    index_ids: []，表示需要的列
    start_date：开始时间，str类型
    end_date：结束时间，str 类型
    """
    if fund_type == FundType.NDX:
        if freq == FreqType.Day:
            data = pd.read_csv('../data/usa/^NDX.csv').set_index('Date')
        elif freq == FreqType.Week:
            data = pd.read_csv('../data/usa/^NDX_wk.csv').set_index('Date')
        else:
            raise RuntimeError('不支持的 freqType 类型')
    elif fund_type == FundType.Test:
        data = pd.read_csv('../data/a/basic_data.csv').set_index('datetime')
    elif fund_type == FundType.GEI:
        data = pd.read_csv('../data/a/创业板指数（价格）历史数据.csv')
        data['收盘'] = data['收盘'].str.replace(',', '')
        data['收盘'] = pd.to_numeric(data['收盘'])
        data = data.set_index('日期')
        data = data.iloc[::-1]
    elif fund_type == FundType.SPY:
        if freq == FreqType.Day:
            data = pd.read_csv('../data/usa/SPY.csv').set_index('Date')
        elif freq == FreqType.Week:
            data = pd.read_csv('../data/usa/SPY_wk.csv').set_index('Date')
        else:
            raise RuntimeError('不支持的 freqType 类型')
    elif fund_type == FundType.TLT:
        if freq == FreqType.Week:
            data = pd.read_csv('../data/usa/TLT_wk.csv').set_index('Date')
        elif freq == FreqType.Day:
            data = pd.read_csv('../data/usa/TLT.csv').set_index('Date')
        else:
            raise RuntimeError('不支持的 freqType 类型')
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
    # 字段名称替换
    if replace is not None:
        for old_key, new_key in replace.items():
            if old_key in data.columns:
                data = data.rename(columns={old_key: new_key})
    return data


def get_hist_data_from_ywcq(file_name, index_ids=None, start_date=None, end_date=None, replace: dict = None):
    """
    从英为财情网站获取数据
    @param file_name 文件路径
    @param index_ids 需要的字段，不含日期字段
    @param start_date 开始时间字符串yyyy-MM-dd格式
    @param end_date 结束时间字符串yyyy-MM-dd格式
    @param replace  替换的字段
    """
    data = pd.read_csv(file_name)
    if not data['收盘'].dtype.name == 'float64':
        data['收盘'] = data['收盘'].str.replace(',', '')
    data['收盘'] = pd.to_numeric(data['收盘'])
    data = data.set_index('日期')
    data = data.iloc[::-1]
    data.index = [datestr2dtdate(e) for e in data.index]
    if index_ids is not None:
        data = data.loc[:, index_ids]
    if start_date is not None:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        data = data.loc[start_date:, :]
    if end_date is not None:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        data = data.loc[:end_date, :]
    # 字段名称替换
    if replace is not None:
        for old_key, new_key in replace.items():
            if old_key in data.columns:
                data = data.rename(columns={old_key: new_key})
    return data


def get_trading_dates(fund_type: FundType, start_date=None, end_date=None):
    """
    获取start到end的交易日
    返回
        dates：交易日的datetime.date，Close 为收盘价
    """
    if fund_type == FundType.NDX:
        dates = pd.read_csv('../data/usa/^NDX.csv')['Date'].to_list()
        dates = [datestr2dtdate(e) for e in dates]
    elif fund_type == FundType.Test:
        dates = pd.read_csv('../data/a/trading_date.csv')['trade_date'].to_list()
        dates = [datestr2dtdate(e, format='%Y/%m/%d') for e in dates]
    elif fund_type == FundType.GEI:
        dates = get_hist_data(fund_type, ['日期'], start_date, end_date)
    else:
        raise RuntimeError('不存在的fund类型')
    # dates = [datestr2dtdate(e) for e in dates]
    if start_date is not None:
        dates = [e for e in dates if e >= start_date]
    if end_date is not None:
        dates = [e for e in dates if e <= end_date]
    return dates
