import datetime

from my.Base import FundType
from my.BaseUtils import cal_period_perf_indicator
from my.DataProcess import get_hist_data
from my.stgy.CalendarStgy import calendar_stgy
from my.stgy.RotationStgy import rotation_stgy, rotation_stgy1
from my.stgy.SimpleRateStgy import simple_rate_stgy

if __name__ == '__main__':
    # 设置回测参数
    start_date = datetime.date(2020, 7, 31)  # 回测起始日期
    end_date = datetime.date(2021, 7, 31)  # 回测截止日期
    print("回测日期[{}]-[{}]".format(start_date, end_date))
    fund_type = FundType.HS300

    # 读取基础数据
    data = get_hist_data(fund_type=fund_type, end_date=end_date)

    # 调用策略模块生成目标组合权重
    # 沪深300的日历策略
    target_wgt1 = calendar_stgy(fund_type, data, start_date, end_date, params={'index_id': 'hs300', 't1': 1, 't2': 5})
    # 中证1000的日历策略
    target_wgt2 = calendar_stgy(fund_type, data, start_date, end_date, params={'index_id': 'csi1000', 't1': 1, 't2': 5})
    # 不可空仓的轮动策略（沪深300，中证500）
    target_wgt3 = rotation_stgy(data, start_date, end_date, params={'N': 20})
    # 可空仓的轮动策略（沪深300，中证500）
    target_wgt4 = rotation_stgy1(data, start_date, end_date, params={'N': 20})
    target_wgt5 = simple_rate_stgy(fund_type, data, start_date, end_date, params={'contains_rate': -0.02, 'sale_rate': 0.03, 'N': 1})
    target_wgt = 0 * target_wgt1 + 0 * target_wgt2 + 0 * target_wgt3 + 0 * target_wgt4 + 1 * target_wgt5  # 多策略目标组合整合

    # 产生每日持仓权重
    hold_wgt = target_wgt  # 假设每天都可以准确地执行交易计划

    # 指数的收益
    asset_ret = data.pct_change().loc[start_date:end_date]
    res = (1 + asset_ret).cumprod()
    res['account'] = (1 + (hold_wgt.shift(1) * asset_ret).sum(axis=1)).cumprod()
    # tmp = hold_wgt.shift(1) * asset_ret
    # tmp1 = tmp.sum(axis=1)
    # tmp2 = tmp1 + 1
    # tmp3 = tmp2.cumprod()

    # 展示净值曲线图和业绩指标表
    res.loc[:, ['hs300', 'csi500', 'account']].plot(figsize=(16, 8), grid=True)
    result = cal_period_perf_indicator(res.loc[:, ['hs300', 'csi500', 'account']])
    print(result)