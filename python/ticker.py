import pandas as pd
import yfinance as yf
from datetime import datetime

default_end_date = datetime.now().strftime('%Y-%m-%d')

def get_tickers_from_wiki(url='https://en.wikipedia.org/wiki/IDX_Composite',index=5,suffix=''):
    idx=pd.read_html(url)[index]
    idx=idx.drop(labels=0,axis=0)
    idx=idx[1].to_list()
    idx=[i + suffix for i in idx]
    return idx

def get_ticker_info(ticker_symbol):
    try:
        ticker=yf.Ticker(ticker_symbol)
        return ticker.get_info()
    except:
        print("Something when wrong")
        
#bris=download_ticker_prices('BRIS.JK','2000-01-01')
#print(bris)