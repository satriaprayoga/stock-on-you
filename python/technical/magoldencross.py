import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

from datetime import datetime

default_end_date = datetime.now().strftime('%Y-%m-%d')


class MAGoldenCross:
    
    def __init__(self,dataFrame,fast=9,slow=26,ma='sma'):
        self.dataFrame=dataFrame
        self.fast=fast
        self.slow=slow
        self.ma=ma

    def apply_ma(self):
        '''pass'''

    def build_signal(self):
        '''pass'''





default_end_date = datetime.now().strftime('%Y-%m-%d')

bbri=yf.Ticker('BBRI.JK')
data=yf.download('BBRI.JK',start='2022-01-02',end=default_end_date)# history(period='1y',actions=False)

# data['Close'].plot(figsize=(15,8))
# plt.grid()
# plt.ylabel('Price in IDR')
# plt.show()

fast=9
#data[f'fast_sma_{fast}']=data['Close'].rolling(window=fast,min_periods=1).mean()
data[f'fast_sma_{fast}']=data['Close'].ewm(span=fast,adjust=False).mean()
print(data.tail())

slow=26
#data[f'slow_sma_{slow}']=data['Close'].rolling(window=slow,min_periods=1).mean()
data[f'slow_sma_{slow}']=data['Close'].ewm(span=slow,adjust=False).mean()

data['Signal']=0.0
data['Signal']=np.where(data[f'fast_sma_{fast}']>data[f'slow_sma_{slow}'],1.0,0.0)
data['Position']=data['Signal'].diff() 

print(data.tail())

plt.figure(figsize=(20,10))

#plot close price, fast sma, and slow sma
data['Close'].plot(color='k',label='Close')
data[f'fast_sma_{fast}'].plot(color='b',label=f'fast_sma_{fast}')
data[f'slow_sma_{slow}'].plot(color='g',label=f'slow_sma_{slow}')

#plot buy signal
plt.plot(data[data['Position']==1].index, data[f'fast_sma_{fast}'][data['Position']==1],'^', markersize = 15, color = 'g', label = 'buy')

#plot sell signal
plt.plot(data[data['Position']==-1].index, data[f'fast_sma_{fast}'][data['Position']==-1],'v', markersize = 15, color = 'r', label = 'sell')


plt.title('BBRI',fontsize=20)
plt.legend()
plt.grid()
plt.show()