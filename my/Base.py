from enum import Enum


class Constant:
    # 收盘表示
    Close = 'Close'
    # 持仓
    Hold = 'wgt'
    # 账户收益
    Account = 'account'


class FundType(Enum):
    Test = 1
    # 纳斯达克指数
    NDX = 2
    # 创业板
    GEI = 3
    # 标普 500
    SPY = 4
    # 美国国债
    TLT = 5


class FreqType(Enum):
    # 每日数据
    Day = 1
    # 每周数据
    Week = 2


class AutoInvestPlan(Enum):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3


class WeekDay(Enum):
    Monday = 0
    TuesDay = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6


class MonthInvest(Enum):
    FirstTradeDay = 0
    LastTradeDay = 1
