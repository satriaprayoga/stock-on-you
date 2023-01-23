import pandas as pd
import numpy as np
import os


from scipy.stats import jarque_bera, normaltest, t



cwd=os.getcwd()
df = pd.read_csv(f'{cwd}/all_stocks_5yr.csv', parse_dates=True)
goog=df[df['Name']=='GOOG'].copy()
#goog['close'].plot()

#plt.show()

close = pd.read_csv(f'{cwd}/sp500_close.csv', parse_dates=True)
symbols = ['AAPL','GOOG','IBM','NFLX','SBUX']
sub = close[symbols].copy()
sub.dropna(axis=0, how='all', inplace=True)

for symbol in symbols:
    sub[symbol + '_prev']=sub[symbol].shift(1)
    sub[symbol + '_ret']=sub[symbol]/sub[symbol + '_prev'] - 1

rets=sub[[symbol + '_ret' for symbol in symbols]].copy()
print(rets.head())


import matplotlib.pyplot as plt
import seaborn as sns

sns.pairplot(rets)

plt.show()
