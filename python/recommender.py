import pandas as pd
import ta
import numpy as np

class Recomender:
    
    def __init__(self,engine,index="idx") -> None:
        self.index = index
        self.engine= engine
        
    def get_tables_name(self):
        query=f"""SELECT table_name FROM information_schema.tables WHERE table_schema='{self.index}'"""
        df = pd.read_sql(query,self.engine)
        df["Schema"]=self.index
        return df
    
    def get_prices(self):
        prices=[]
        for table, schema in zip(self.get_tables_name().TABLE_NAME, self.get_tables_name().Schema):
            sql = schema+'.'+f'`{table}`'
            prices.append(pd.read_sql(f"SELECT * FROM {sql}",self.engine))
        return prices
    
    def get_price(self,table_name):
        sql=f"SELECT * FROM {self.index}.{table_name}"
        return pd.read_sql(sql,self.engine)
    
    def MACD(self,df):
        df['MACD_diff']=ta.trend.macd_diff(df.Close)
        df['Decision MACD']=np.where((df.MACD_diff > 0) & (df.MACD_diff.shift(1) < 0),True,False)
   

    def Goldencross(self,df):
        df['SMA20']=ta.trend.sma_indicator(df.Close, window=20)
        df['SMA50']=ta.trend.sma_indicator(df.Close, window=50)
        df['Signal']=np.where(df['SMA20']>df['SMA50'],True,False)
        df['Decision GC']=df.Signal.diff()


    def RSI_SMA(self,df):
        df['RSI']=ta.momentum.rsi(df.Close,window=10)
        df['SMA200']=ta.trend.sma_indicator(df.Close,window=200)
        df['Decision RSI/SMA']=np.where((df.Close > df.SMA200) & (df.RSI < 30),True,False)