import datetime
import matplotlib.pyplot as plt

from my.Base import FundType
from my.BaseUtils import cal_period_perf_indicator
from my.DataProcess import get_hist_data
from my.stgy.avg_9 import avg_9_stgy

if __name__ == '__main__':
    fund_type = FundType.GEI

    data = get_hist_data(fund_type, index_ids=['Close'], start_date=None, end_date=None)

    # 计算日历策略每天的持仓
    target_wgt = avg_9_stgy(data, params={'r1': 10, 'r2': 28})
    hold_wgt = target_wgt

    # 指数每天的涨跌百分比
    asset_ret = data.pct_change()
    # 指数每天的收益
    res = (1 + asset_ret).cumprod()
    tmp = hold_wgt.shift(1) * asset_ret
    tmp = tmp.sum(axis=1)
    tmp = tmp + 1
    tmp = tmp.cumprod()
    res['account'] = (1 + (hold_wgt.shift(1) * asset_ret).sum(axis=1)).cumprod()

    res.loc[:, ['Close', 'account']].plot(figsize=(16, 8), grid=True)
    result = cal_period_perf_indicator(res.loc[:, ['Close', 'account']])
    print(result)
