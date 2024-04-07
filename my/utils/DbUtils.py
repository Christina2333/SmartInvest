from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

host = '127.0.0.1'
port = 3306
user = 'root'
pwd = 'Janet0425'
db = 'stock'


def connect_to_db():
    url = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}"
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    return Session()


session = connect_to_db()


def insert(ll: list):
    for l in ll:
        session.add(l)
    session.commit()
