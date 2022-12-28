import sqlalchemy
import pymysql
import ticker
import yfinance as yf
import pandas as pd
import ta
import numpy as np

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
        

def create_stock_tables(engine,stock_list,start_date,end_date):
    for s in stock_list:
        #stock=yf.Ticker(s+'.JK')
        #info = None
        data=None
        try:
            #info = stock.info
            data=yf.download(s+".JK",start_date,end_date)
            print("get data for {} ",s)
            data.reset_index()
            #print("get data for {} ",data)
            data.to_sql(s,engine)
        except:
            print(f"Cannot get info of {s}, it probably does not exist")
            continue
        print(f"Info of {s}")
        
def get_tables_name(engine,index):
    query=f"""SELECT table_name FROM information_schema.tables WHERE table_schema='{index}'"""
    df = pd.read_sql(query,engine)
    df["Schema"]=index
    return df

def get_prices(engine,which):
    prices=[]
    for table, schema in zip(which.TABLE_NAME, which.Schema):
        sql = schema+'.'+f'`{table}`'
        prices.append(pd.read_sql(f"SELECT * FROM {sql}",engine))
    return prices
    
def get_price(engine,table_name,index):
    sql=f"SELECT * FROM {index}.{table_name}"
    return pd.read_sql(sql,engine)

def MACD(df):
    df['MACD_diff']=ta.trend.macd_diff(df.Close)
    df['Suggestions']=np.where((df.MACD_diff > 0) & (df.MACD_diff.shift(1) < 0),True,False)
    return df
    

engine=sqlalchemy.create_engine('mysql://root:asdqwe123@localhost:3306')
#idx=ticker.get_tickers_from_wiki()
#create_stock_tables(engine,idx,'2012-01-01',default_end_date)
#engine.close()
idx=get_tables_name(engine,'idx')
print(idx)

bris=get_price(engine,'bris','idx')
bris=MACD(bris)
print(bris)