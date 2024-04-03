import datetime

import numpy as np
import pandas as pd

from my.BaseUtils import datestr2dtdate


def simple_rate_stgy(fund_type, data, start_date, end_date, params):
    if type(start_date) is str:
        start_date = datestr2dtdate(start_date)
    if type(end_date) is str:
        end_date = datestr2dtdate(end_date)
    contains_rate = float(params['contains_rate'])
    sale_rate = float(params['sale_rate'])
    N = params['N']
    # 每天的涨跌幅
    N_day_ret = data.shift(1) / data.shift(N + 1) - 1  # 截止昨收的最近N个交易日涨幅
    # asset_ret = data.pct_change().loc[start_date:end_date].fillna(0)
    target_wgt = pd.DataFrame(index=data.index, columns=data.columns)
    target_wgt['hs300'] = [1 if r >= contains_rate else 0 if r <= sale_rate else np.nan for r in N_day_ret['hs300']]
    target_wgt = target_wgt.loc[start_date:end_date].fillna(0)

    # 打印全部买入卖出点
    # for i in range(len(target_wgt) - 1):
    #     if i == 0 and target_wgt.iloc[i, 2] == 1:
    #         print("买入日期为{}".format(target_wgt.index[0]))
    #     if i == len(target_wgt) - 1 and target_wgt.iloc[i, 2] == 0:
    #         print("卖出日期为{}".format(target_wgt.index[i]))
    #     if target_wgt.iloc[i, 2] == 0 and target_wgt.iloc[i+1, 2] == 1:
    #         print("买入日期为{}".format(target_wgt.index[i+1]))
    #     if target_wgt.iloc[i, 2] == 1 and target_wgt.iloc[i+1, 2] == 0:
    #         print("卖出日期为{}".format(target_wgt.index[i+1]))

    return target_wgt
