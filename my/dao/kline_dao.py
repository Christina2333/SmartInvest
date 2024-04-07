from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy import and_
from my.utils.DbUtils import connect_to_db

Base = declarative_base()
db = 'stock'
session = connect_to_db(db)


class KLine(Base):
    __tablename__ = 'stock_kline'

    id = Column(Integer, primary_key=True)
    stock_id = Column(String(45), unique=False, nullable=False)
    dt = Column(Integer, unique=False, nullable=False)
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

    def __init__(self, id, stock_id, dt, stock_volume, open, close, change, change_percent, high, low,
                 turnover_rate, transaction_amt, pe, pb, ps, pcf, market_capital):
        self.id = id
        self.stock_id = stock_id
        self.dt = dt
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


def insert(klines: list):
    for kline in klines:
        session.add(kline)
    session.commit()


def get_by_stock_and_dt(stock_id, dt):
    query = session.query(KLine).filter(and_(KLine.stock_id == stock_id, KLine.dt == dt))
    if query.is_single_entity:
        return query.first()
    else:
        return None


# if __name__ == '__main__':
#     kline1 = KLine(id=None, stock_id='test', dt=20240403, stock_volume=1, open=1, close=1, change_percent=1, change=1,
#                    high=1, low=1,
#                    turnover_rate=1, transaction_amt=1, pe=1, pb=1, ps=1, pcf=1, market_capital=1)
#     kline2 = KLine(id=None, stock_id='test1', dt=20240403, stock_volume=1, open=1, close=1, change_percent=1, change=1,
#                    high=1, low=1,
#                    turnover_rate=1, transaction_amt=1, pe=1, pb=1, ps=1, pcf=1, market_capital=1)
#     # insert([kline1, kline2])
#     res = get_by_stock_and_dt('test', 20240403)
#     print(res)
