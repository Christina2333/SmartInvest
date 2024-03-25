from enum import Enum


class FundType(Enum):
    # 纳斯达克指数
    NDX = 1
    # 沪深300
    HS300 = 2
    # 中证500
    CSI500 = 3
    # 创业板
    GEI = 4
    # 标普 500
    SPY = 5


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