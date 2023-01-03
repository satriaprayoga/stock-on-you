import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

from datetime import datetime

default_end_date = datetime.now().strftime('%Y-%m-%d')


class MACrossOver:
    
    def __init__(self,dataFrame,fast,slow,ma='sma'):
        self.dataFrame=dataFrame
        self.fast=fast
        self.slow=slow
        self.ma=ma

    def apply_ma(self):
        if self.ma=="sma":
            self.dataFrame[f'fast_{self.ma}_{self.fast}']=self.dataFrame['Close'].rolling(window=self.fast,min_periods=1).mean()
            self.dataFrame[f'slow_{self.ma}_{self.slow}']=self.dataFrame['Close'].rolling(window=self.slow,min_periods=1).mean()
        elif self.ma=="ema":
            self.dataFrame[f'fast_{self.ma}_{self.fast}']=self.dataFrame['Close'].ewm(span=self.fast,adjust=False).mean()
            self.dataFrame[f'slow_{self.ma}_{self.slow}']=self.dataFrame['Close'].ewm(span=self.slow,adjust=False).mean()
        else:
            raise Exception("MA type is not recognized")

    def build_MA_Signal(self):
        self.dataFrame['MA_Signal']=0.0
        self.dataFrame['MA_Signal']=np.where(self.dataFrame[f'fast_{self.ma}_{self.fast}']>self.dataFrame[f'slow_{self.ma}_{self.slow}'],1.0,0.0)
        self.dataFrame['Position']=self.dataFrame['MA_Signal'].diff()
        self.dataFrame['MA_Buy']=np.where(self.dataFrame['Position'] == 1.0,self.dataFrame['Close'],np.nan)
        self.dataFrame['MA_Sell']=np.where(self.dataFrame['Position'] == -1.0,self.dataFrame['Close'],np.nan) 
        
    def plot_line(self,dataColor='k',dataLabel='Close',fastColor='b',slowColor='g'):
        self.dataFrame['Close'].plot(color=dataColor,label=dataLabel)
        self.dataFrame[f'fast_{self.ma}_{self.fast}'].plot(color=fastColor,label=f'fast_{self.ma}_{self.fast}')
        self.dataFrame[f'slow_{self.ma}_{self.slow}'].plot(color=slowColor,label=f'slow_{self.ma}_{self.slow}')
        
    def plot_MA_Signal(self,plt):
        #plot buy MA_Signal
        plt.plot(self.dataFrame[self.dataFrame['Position']==1].index, self.dataFrame[f'fast_{self.ma}_{self.fast}'][self.dataFrame['Position']==1],'^', markersize = 15, color = 'g', label = 'buy')

        #plot sell MA_Signal
        plt.plot(self.dataFrame[self.dataFrame['Position']==-1].index, self.dataFrame[f'fast_{self.ma}_{self.fast}'][self.dataFrame['Position']==-1],'v', markersize = 15, color = 'r', label = 'sell')
        





# default_end_date = datetime.now().strftime('%Y-%m-%d')

# bbri=yf.Ticker('BBRI.JK')
# data=bbri.history(period='1y',actions=False)

# maco=MACrossOver(dataFrame=data,fast=9,slow=26,ma="ema")
# maco.apply_ma()
# maco.build_MA_Signal()
# plt.figure(figsize=(20,10))

# maco.plot_line()
# maco.plot_MA_Signal(plt)

# plt.title('BBRI',fontsize=20)
# plt.legend()
# plt.grid()
# plt.show()

# print(maco.dataFrame.tail(50))