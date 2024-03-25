import datetime

import pandas as pd

from my.BaseUtils import datestr2dtdate, date_count_in_month
from my.DataProcess import get_trading_dates


def calendar_stgy(fund_type, data, start_date, end_date, params):
    """
    日历策略
    输入
        start_date：开始日期，可以是str或者datetime
        end_date：
        params：dict，
            index_id: [] 需要的列
            t1：开始买入的日期，每个月的第几个交易日
            t2：持有的最后一天，每个月的第几个交易日
    返回值
        target_wgt：每天的持仓，1表示满仓，0表示空仓
    """
    if type(start_date) is str:
        start_date = datestr2dtdate(start_date)
    if type(end_date) is str:
        end_date = datestr2dtdate(end_date)
    index_id = params['index_id']
    t1 = params['t1']
    t2 = params['t2']

    start_date0 = start_date - datetime.timedelta(31)
    # 获取全部交易日
    dates0 = get_trading_dates(fund_type, start_date0, end_date)
    # 获取每个日期是该月的第几个交易日
    dates0_rank = date_count_in_month(dates0)
    target_wgt = pd.DataFrame(data=0, index=dates0, columns=data.columns)
    target_wgt[index_id] = [1 if (t1 <= e <= t2) else 0 for e in dates0_rank]
    target_wgt = target_wgt.loc[start_date:end_date]
    return target_wgt
