import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

host = '127.0.0.1'
port = 3306
user = 'root'
pwd = 'Janet0425'


def connect_to_db(db):
    url = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}"
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    # connection = pymysql.connect(
    #     host=host,
    #     port=port,
    #     user=user,
    #     password=pwd,
    #     db=db,
    #     charset='utf8mb4'
    # )
    return Session()
