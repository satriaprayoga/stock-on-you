import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

from scipy.stats import norm

cwd=os.getcwd()
df = pd.read_csv(f'{cwd}/all_stocks_5yr.csv', parse_dates=True)

sbux=df[df['Name']=='SBUX'].copy()
print(sbux.head())

sbux['prev_close']=sbux['close'].shift(1)
sbux['return']=sbux['close']/sbux['prev_close'] - 1
sbux['pct_change']=sbux['close'].pct_change(1)
sbux['log_return']=np.log(sbux['return']+1)
print(sbux.head())

print(sbux['return'].mean(), sbux['return'].std())

x_list= np.linspace(sbux['return'].min(),sbux['return'].max(),100)
y_list= norm.pdf(x_list, loc=sbux['return'].mean(),scale=sbux['return'].std())
plt.plot(x_list,y_list)
sbux['return'].hist(bins=100, density=True)
plt.show()

from scipy.stats import probplot

probplot(sbux['return'].dropna(), dist='norm', fit=True, plot=plt)
plt.show()

import statsmodels.api as sm

sm.qqplot(sbux['return'].dropna(),line='s')
plt.show()