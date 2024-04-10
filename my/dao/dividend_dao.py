from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DECIMAL

Base = declarative_base()


class Dividend(Base):
    __tablename__ = 'stock_dividend'

    id = Column(Integer, primary_key=True)
    stock_id = Column(String(45), unique=False, nullable=False)
    year = Column(Integer, unique=False, nullable=False)
    dividend_dt = Column(Integer, unique=False, nullable=False)
    dividend_info = Column(String(1024), unique=False, nullable=False)
    dividend_type = Column(Integer, unique=False, nullable=False)
    dividend_per_share = Column(DECIMAL, unique=False, nullable=False)
    price = Column(DECIMAL, unique=False, nullable=False)
    dividend_rate = Column(DECIMAL, unique=False, nullable=False)

    def __init__(self, stock_id, year, dividend_dt, dividend_info, dividend_type, dividend_per_share, price, dividend_rate):
        self.stock_id = stock_id
        self.year = year
        self.dividend_dt = dividend_dt
        self.dividend_info = dividend_info
        self.dividend_type = dividend_type
        self.dividend_per_share = dividend_per_share
        self.price = price
        self.dividend_rate = dividend_rate
