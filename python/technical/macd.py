import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

from datetime import datetime

default_end_date = datetime.now().strftime('%Y-%m-%d')

class MACD:
    
    def __init__(self,dataFrame,fast=12,slow=26,signal=9) -> None:
        self.dataFrame=dataFrame
        self.fast=fast
        self.slow=slow
        self.signal=signal
        
    def apply_macd(self):
        data=self.dataFrame
        data[f'fast_ewm{self.fast}']=data['Close'].ewm(span=self.fast,adjust=False).mean()
        data[f'slow_ewm{self.slow}']=data['Close'].ewm(span=self.slow,adjust=False).mean()
        data['MACD']=data[f'fast_ewm{self.fast}']-data[f'slow_ewm{self.slow}']
        data['MACD_SS']=data['MACD'].ewm(span=self.signal,adjust=False).mean()
        data['MACD_Hist']=data['MACD']-data['MACD_SS']
        self.dataFrame=data
        
    def build_macd_signal(self):
        data=self.dataFrame
        data['MACD_Signal']=0.0
        data['MACD_Signal']=np.where(data['MACD']>data['MACD_SS'],1.0,0.0)
        data['MACD_Position']=data['MACD_Signal'].diff()
        data['MACD_Buy']=np.where(self.dataFrame['MACD_Position'] == 1.0,data['Close'],np.nan)
        data['MACD_Sell']=np.where(self.dataFrame['MACD_Position'] == -1.0,data['Close'],np.nan) 
        self.dataFrame=data

# bbri=yf.Ticker('BBRI.JK')
# data=bbri.history(period='1y',actions=False)

# macd=MACD(dataFrame=data)
# macd.apply_macd()
# macd.build_signal()
# print(macd.dataFrame.tail(50))

# plt.figure(figsize=(20,10))

# data=macd.dataFrame
# ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 5, colspan = 1)
# ax2 = plt.subplot2grid((8,1), (5,0), rowspan = 3, colspan = 1)

# ax1.plot(data['Close'],color='skyblue',label='BBRI')
# ax1.plot(data.index,data['MACD_Buy'],marker = '^', color = 'green', markersize = 10, label = 'BUY SIGNAL', linewidth = 0)
# ax1.plot(data.index,data['MACD_Sell'],marker = 'v', color = 'r', markersize = 10, label = 'SELL SIGNAL', linewidth = 0)


# ax2.plot(data['MACD'],color = 'grey', linewidth = 1.5, label = 'MACD')
# ax2.plot(data['MACD_SS'],color = 'skyblue', linewidth = 1.5, label = 'Signal')

# for i in range(len(data['Close'])):
#     if str(data['MACD_Hist'][i])[0]=='-':
#         ax2.bar(data.index[i],data['MACD_Hist'][i],color='#ef5350')
#     else:
#         ax2.bar(data.index[i],data['MACD_Hist'][i],color='#26a69a')

# plt.legend(loc = 'lower right')

# plt.grid()
# plt.show()