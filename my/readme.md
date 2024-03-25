数据：
data/a：a股数据
data/usa：美股数据

代码：
`Base.py`：基础枚举
`DataProcess.py`：处理数据，获取数据，获取交易日期数据
`BaseUtils.py`：基础工具，*计算各种指标*
stgy/：策略
    `CalendarStgy.py`：日历策略，每个月的第一~第五个交易日持有，其他时间空仓
    `RotationStgy.py`：如果沪深300近20日涨幅大，就买沪深300；如果中证500近20日涨幅大，就买和中证500
backtest/：回测
    `Abacktest.py`：
    `USbacktest.py`：