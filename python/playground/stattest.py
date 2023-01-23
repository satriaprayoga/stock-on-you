import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

from scipy.stats import jarque_bera, normaltest, t

cwd=os.getcwd()
df = pd.read_csv(f'{cwd}/all_stocks_5yr.csv', parse_dates=True)

sbux=df[df['Name']=='SBUX'].copy()

sbux['prev_close']=sbux['close'].shift(1)
sbux['return']=sbux['close']/sbux['prev_close'] - 1
sbux['pct_change']=sbux['close'].pct_change(1)
sbux['log_return']=np.log(sbux['return']+1)

values=sbux['return'].dropna().to_numpy()

# check p value using jarque-bera or normaltest, if p < 5 %, reject null hypothesis i.e the data does not come from normal distribution
jb = jarque_bera(values)
print(jb)

nt = normaltest(values)
print(nt)

from scipy.stats import kstest

df, loc, scale = t.fit(values)

def cdf(x):
    return t.cdf(x,df,loc,scale)

# check p value using kolmogorov-smirnov, if p < 5 %, reject null hypothesis i.e the data does not come from normal distribution
kt = kstest(values,cdf)
print(kt)

from scipy.stats import ttest_1samp

ttest=ttest_1samp(values,0)
print(ttest)

##change stock
df = pd.read_csv(f'{cwd}/all_stocks_5yr.csv', parse_dates=True)
mmm=df[df['Name']=='MMM'].copy()

mmm['prev_close']=mmm['close'].shift(1)
mmm['return']=mmm['close']/mmm['prev_close'] - 1
mmm['pct_change']=mmm['close'].pct_change(1)
mmm['log_return']=np.log(mmm['return']+1)

print(mmm['return'].mean(), mmm['return'].std())
#mmm['return'].hist(bins=100,density=True)
#plt.show()

ttest=ttest_1samp(mmm['return'].dropna(),0)
print(ttest)