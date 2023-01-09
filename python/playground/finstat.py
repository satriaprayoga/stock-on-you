import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

cwd=os.getcwd()
df = pd.read_csv(f'{cwd}/all_stocks_5yr.csv', parse_dates=True)

sbux=df[df['Name']=='SBUX'].copy()
print(sbux.head())

sbux['prev_close']=sbux['close'].shift(1)
sbux['return']=sbux['close']/sbux['prev_close'] - 1
sbux['pct_change']=sbux['close'].pct_change(1)
sbux['log_return']=np.log(sbux['return']+1)
print(sbux.head())
sbux['return'].hist(bins=200)
plt.show()
print(sbux['return'].mean(), sbux['return'].std())
