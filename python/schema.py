import sqlalchemy
import pymysql
import ticker
from datetime import datetime

pymysql.install_as_MySQLdb()

default_end_date = datetime.now().strftime('%Y-%m-%d')

def create_schema():
    engine=sqlalchemy.create_engine('mysql://root:asdqwe123@localhost:3306/')
    inspector=sqlalchemy.inspect(engine)
    if "idx" in inspector.get_schema_names() :
        print("IDX Schema exists")
    else:
        engine.execute(sqlalchemy.schema.CreateSchema('IDX'))
    return engine
        

def create_stock_tables(engine,stock_name,start_date,end_date):
    stock=ticker.download_ticker_prices(stock_name+".JK",start_date,end_date)
    stock.reset_index()
    stock.to_sql(stock_name,engine)
    

engine=sqlalchemy.create_engine('mysql://root:asdqwe123@localhost:3306/idx')
idx=ticker.get_tickers_from_wiki()
for i in idx:
    create_stock_tables(engine,i,'2022-12-23',default_end_date)
engine.close()