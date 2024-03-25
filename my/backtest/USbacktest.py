import datetime

from my.Base import FundType
from my.BaseUtils import cal_period_perf_indicator
from my.DataProcess import get_hist_data
from my.stgy.CalendarStgy import calendar_stgy

if __name__ == '__main__':
    start_date = datetime.date(2013, 1, 1)
    end_date = datetime.date(2023, 12, 13)
    fund_type = FundType.NDX

    data = get_hist_data(fund_type, index_ids=['Close'], start_date=start_date, end_date=end_date)

    # 计算日历策略每天的持仓
    target_wgt = calendar_stgy(fund_type, data, start_date, end_date, params={'index_id': 'Close', 't1': 1, 't2': 5})
    hold_wgt = target_wgt

    # 指数每天的涨跌百分比
    asset_ret = data.pct_change().loc[start_date:end_date]
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