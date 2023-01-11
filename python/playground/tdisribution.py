import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.stats import t


cwd=os.getcwd()
df = pd.read_csv(f'{cwd}/all_stocks_5yr.csv', parse_dates=True)

sbux=df[df['Name']=='SBUX'].copy()
print(sbux.head())

sbux['prev_close']=sbux['close'].shift(1)
sbux['return']=sbux['close']/sbux['prev_close'] - 1
sbux['pct_change']=sbux['close'].pct_change(1)
sbux['log_return']=np.log(sbux['return']+1)

sbux['return'].skew()
sbux['return'].kurtosis()


print(sbux.head())

print(sbux['return'].mean(), sbux['return'].std())

x_list= np.linspace(sbux['return'].min(),sbux['return'].max(),100)

#degree of freedom, loc, scale
params=t.fit(sbux['return'].dropna())
print(params)
df,loc,scale=params 

y_list=t.pdf(x_list,df,loc,scale)
plt.plot(x_list,y_list)
sbux['return'].hist(bins=100,density=True)
plt.show()

import statsmodels.api as sm

class myt:
    def __init__(self,df):
        self.df=df

    def fit(self,x):
        return t.fit(x)

    def ppf(self, x, loc=0,scale=1):
        return t.ppf(x,self.df,loc,scale)

sm.qqplot(sbux['return'].dropna(),dist=myt(df),line='s')
plt.show()