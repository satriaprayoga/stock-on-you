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
            data.to_sql(s.lower(),engine)
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
    df['Decision MACD']=np.where((df.MACD_diff > 0) & (df.MACD_diff.shift(1) < 0),True,False)
   

def Goldencross(df):
    df['SMA20']=ta.trend.sma_indicator(df.Close, window=20)
    df['SMA50']=ta.trend.sma_indicator(df.Close, window=50)
    df['Signal']=np.where(df['SMA20']>df['SMA50'],True,False)
    df['Decision GC']=df.Signal.diff()


def RSI_SMA(df):
    df['RSI']=ta.momentum.rsi(df.Close,window=10)
    df['SMA200']=ta.trend.sma_indicator(df.Close,window=200)
    df['Decision RSI/SMA']=np.where((df.Close > df.SMA200) & (df.RSI < 30),True,False)


def apply(engine,stock_name,index):
    price=get_price(engine,stock_name,index)
    MACD(price)
    Goldencross(price)
    RSI_SMA(price)
    return price
    
def applytechnicals(engine, which):
    prices=get_prices(engine,which)
    for frame in prices:
        MACD(frame)
        Goldencross(frame)
        RSI_SMA(frame)
    return prices

def recommender(engine,which):
    indicators=['Decision MACD','Decision GC','Decision RSI/SMA']
    for symbol,frame in zip(which.TABLE_NAME,applytechnicals(engine,which)):
        if frame.empty is False:
            for indicator in indicators:
                if frame[indicator].iloc[-1]==True:
                    print(f"{indicator} Buying Signal for "+symbol)
                

    
engine=sqlalchemy.create_engine('mysql://root:asdqwe123@localhost:3306/')
#idx=ticker.get_tickers_from_wiki()
#create_stock_tables(engine,idx,'2017-01-01',default_end_date)
#engine.close()
#idx=get_tables_name(engine,'idx')
#print(idx)

#bris=apply(engine,'btps','idx')
#print(bris)
idx=get_tables_name(engine,"idx")
recommender(engine,idx)
print(recommender)