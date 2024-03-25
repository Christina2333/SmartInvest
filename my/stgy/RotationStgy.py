import datetime
import numpy as np

import pandas as pd

from my.Base import FundType
from my.BaseUtils import datestr2dtdate
from my.DataProcess import get_trading_dates


def rotation_stgy(data, start_date, end_date, params):
    """
    轮动策略，不可空仓
    Input:
        data: df(date*, index1, index2, ...), basic data
        start_date, end_date: 'yyyy-mm-dd' or datetime.date
        params: dict, format {'index_list':['N':20}
    Output:
        target_wgt: df(trade_date*, index1, index2, ...) 目标权重
    """
    if type(start_date) is str:
        start_date = datestr2dtdate(start_date)
    if type(end_date) is str:
        end_date = datestr2dtdate(end_date)
    N = params['N']

    start_date0 = start_date - datetime.timedelta(N) * 2
    dates0 = get_trading_dates(FundType.HS300, start_date0, end_date)
    data0 = data.reindex(index=dates0)
    N_day_ret = data0.shift(1) / data0.shift(N + 1) - 1  # 截止昨收的最近N个交易日涨幅
    target_wgt = pd.DataFrame(index=data0.index, columns=data0.columns)
    target_wgt['hs300'] = [1 if e > 0 else 0 if e <= 0 else np.nan for e in N_day_ret['hs300'] - N_day_ret['csi500']]
    target_wgt['csi500'] = 1 - target_wgt['hs300']
    target_wgt = target_wgt.loc[start_date:end_date].fillna(0)

    return target_wgt


def rotation_stgy1(data, start_date, end_date, params):
    """
    轮动策略（可空仓），当hs300涨幅大时持有hs300，当csi500涨幅大时买入csi500，否则空仓
    输入
        data：'hs300'， 'csi500'
    """
    if type(start_date) is str:
        start_date = datestr2dtdate(start_date)
    if type(end_date) is str:
        end_date = datestr2dtdate(end_date)
    N = params['N']

    start_date0 = start_date - datetime.timedelta(N) * 2
    dates0 = get_trading_dates(FundType.HS300, start_date0, end_date)
    data0 = data.reindex(index=dates0)
    # N个交易日涨幅 =》(data0[1] - data0[N+1])/data0[N+1]
    N_day_ret = data0.shift(1) / data0.shift(N + 1) - 1
    target_wgt = pd.DataFrame(0, index=data0.index, columns=data0.columns)
    for i in range(1, len(target_wgt)):
        t = target_wgt.index[i]
        t0 = target_wgt.index[i - 1]
        if N_day_ret.loc[t0, 'hs300'] >= N_day_ret.loc[t0, 'csi500'] and N_day_ret.loc[t0, 'hs300'] > 0:
            target_wgt.loc[t, 'hs300'] = 1
        elif N_day_ret.loc[t0, 'hs300'] < N_day_ret.loc[t0, 'csi500'] and N_day_ret.loc[t0, 'csi500'] > 0:
            target_wgt.loc[t, 'csi500'] = 1
    target_wgt = target_wgt.loc[start_date:end_date].fillna(0)
    return target_wgt