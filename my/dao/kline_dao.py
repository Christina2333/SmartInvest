from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DECIMAL, text
from sqlalchemy import and_
from my.utils.DbUtils import session

Base = declarative_base()


class KLine(Base):
    __tablename__ = 'stock_kline'

    id = Column(Integer, primary_key=True)
    stock_id = Column(String(45), unique=False, nullable=False)
    stock_code = Column(String(45), unique=False, nullable=False)
    dt = Column(Integer, unique=False, nullable=False)
    month = Column(Integer, unique=False, nullable=False)
    year = Column(Integer, unique=False, nullable=False)
    stock_volume = Column(Integer, unique=False, nullable=False)
    open = Column(DECIMAL, unique=False, nullable=False)
    close = Column(DECIMAL, unique=False, nullable=False)
    change = Column(DECIMAL, unique=False, nullable=False)
    change_percent = Column(DECIMAL, unique=False, nullable=False)
    high = Column(DECIMAL, unique=False, nullable=False)
    low = Column(DECIMAL, unique=False, nullable=False)
    turnover_rate = Column(DECIMAL, unique=False, nullable=False)
    transaction_amt = Column(DECIMAL, unique=False, nullable=False)
    pe = Column(DECIMAL, unique=False, nullable=False)
    pb = Column(DECIMAL, unique=False, nullable=False)
    ps = Column(DECIMAL, unique=False, nullable=False)
    pcf = Column(DECIMAL, unique=False, nullable=False)
    market_capital = Column(DECIMAL, unique=False, nullable=False)

    def __init__(self, stock_code, dt, stock_volume, open, close, change, change_percent, high, low,
                 turnover_rate, transaction_amt, pe, pb, ps, pcf, market_capital):
        self.stock_code = stock_code
        stock_id = stock_code.replace('SH', '').replace('SZ', '')
        self.stock_id = stock_id
        self.dt = dt
        self.month = round(dt / 100)
        self.year = round(dt / 10000)
        self.stock_volume = stock_volume
        self.open = open
        self.close = close
        self.change = change
        self.change_percent = change_percent
        self.high = high
        self.low = low
        self.turnover_rate = turnover_rate
        self.transaction_amt = transaction_amt
        self.pe = pe
        self.pb = pb
        self.ps = ps
        self.pcf = pcf
        self.market_capital = market_capital

    def __str__(self):
        return 'stock_id=' + self.stock_id

def get_by_stock_and_dt(stock_id, dt):
    """
    获取股票当天的价格
    """
    query = session.query(KLine).filter(and_(KLine.stock_id == stock_id, KLine.dt == dt))
    if query.is_single_entity:
        return query.first()
    else:
        return None


def get_by_stock_and_dt_section(stock_code, start_dt, end_dt):
    sql = text(f"select * from stock_kline where stock_code = '{stock_code}' and dt between {start_dt} and {end_dt}")
    query = session.execute(sql)
    return query.fetchall()


def get_by_stock_and_month(stock_id, month):
    """
    获取股票某个月底的价格
    """
    sql = text(f"select * from `stock_kline` where `stock_id` = '{stock_id}' and `month` = {month} "
               f"order by `dt` desc limit 1")
    query = session.execute(sql)
    if query is not None:
        return query.first()
    else:
        return None


def get_by_stock_and_months(stock_id, months):
    result = []
    for month in months:
        res = get_by_stock_and_month(stock_id, month)
        result.append(res.close)
    return result


def get_by_stock_and_year(stock_id, year):
    """
    获取股票某个年底的价格
    """
    sql = text(f"select * from `stock_kline` where `stock_id` = '{stock_id}' and `year` = {year} "
               f"order by `dt` desc limit 1")
    query = session.execute(sql)
    if query is not None:
        return query.first()
    else:
        return None


def get_year_avg(stock_id, year):
    """
    获取股票某年的均价
    """
    sql = text(f"select avg(`close`) from `stock_kline` where `stock_id` = '{stock_id}' and year = {year}")
    query = session.execute(sql)
    if query is not None:
        return query.first()[0]
    else:
        return None


if __name__ == '__main__':
    # res = get_by_stock_and_month('000895', 202403)
    # avg1 = get_year_avg('000895', 2024)
    # avg2 = get_year_avg('000895', 2023)
    res = get_by_stock_and_dt_section('SH600036', 20140411, 20240411)
    print(res)


