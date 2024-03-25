import datetime
import pandas as pd
import numpy as np
from my.Base import WeekDay
from my.Base import MonthInvest


def datestr2dtdate(datestr, format='%Y-%m-%d'):
    """
    日期格式转换
    """
    return datetime.datetime.strptime(datestr, format).date()


def date_count_in_month(dates):
    """
    获取dates，只有一列datetime类型的日期，获取每个日期是本月的第几个交易日
    返回值
        counts：对应dates的每个日期，是该月的第几个交易日
    """
    cur_count = 1
    counts = [cur_count]
    for i in range(1, len(dates)):
        if dates[i].month == dates[i - 1].month:
            cur_count = cur_count + 1
        else:
            cur_count = 1
        counts.append(cur_count)
    return counts


def cal_period_perf_indicator(adjnav):
    """
    计算衡量投资的各种指标
    """
    if type(adjnav) == pd.DataFrame:
        # '年化收益率'，'年化波动率'，'夏普率'，'最大回撤'，'卡玛比率'
        res = pd.DataFrame(index=adjnav.columns, columns=['AnnRet', 'AnnVol', 'SR', 'MaxDD', 'Calmar'])
        for col in adjnav:
            res.loc[col] = cal_period_perf_indicator(adjnav[col])
        return res

    # 每天的波动
    ret = adjnav.pct_change()
    # 年化收益率
    annret = (adjnav[-1] / 1) ** (242 / len(adjnav)) - 1  # 复利
    # 年化波动率
    annvol = np.nanstd(ret) * np.sqrt(242)  # 波动的标准差 * 根号(242)，假设一年有242的交易日
    # 年化收益/年化波动
    sr = annret / annvol
    # 计算每天的回撤
    dd = get_drawdown(adjnav)
    # 返回最小值
    mdd = np.nanmin(dd)
    # 年化收益率/最大回撤
    calmar = annret / -mdd
    return [annret, annvol, sr, mdd, calmar]


def get_drawdown(p):
    """
    计算净值回撤
    """
    T = len(p)
    # 计算累计最大值
    hmax = p.cummax()
    dd = p / hmax - 1
    return dd


def cal_annual_compound_return(start_amt: float, end_amt: float, years: int):
    """
    计算年均复合收益
    """
    annual_return = (end_amt / start_amt) ** (1 / years) - 1
    return annual_return


def get_all_weekdays(start_time, end_time, weekday: WeekDay):
    """
    从起始日期范围中返回全部的 weekday
    """
    if isinstance(start_time, str):
        start_time = datestr2dtdate(start_time)
    if isinstance(end_time, str):
        # end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d")
        end_time = datestr2dtdate(end_time)

    all_days = []
    current = start_time
    while current <= end_time:
        if current.weekday() == weekday.value:
            all_days.append(current)
        current += datetime.timedelta(days=1)

    return all_days


def get_all_monthdays(dates, monthday: MonthInvest):
    month = dates.apply(lambda date: date.strftime('%Y-%m'))
    df = pd.DataFrame({'Date': dates, 'Month': month})
    if monthday == MonthInvest.FirstTradeDay:
        monthly_min_days = df.groupby('Month').min()['Date']
        return monthly_min_days
    if monthday == MonthInvest.LastTradeDay:
        monthly_max_days = df.groupby('Month').max()['Date']
        return monthly_max_days
