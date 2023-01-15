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

values=sbux['return'].dropna().to_numpy()

mean = values.mean()
std = values.std(ddof=1)

low = mean - 1.96 * std /np.sqrt(len(values))
high = mean + 1.96 * std /np.sqrt(len(values))

sbux['return'].hist(bins=100,density=True)
plt.axvline(mean,label='mean', color='red')
plt.axvline(low,label='low', color='green')
plt.axvline(high,label='high', color='green')
plt.legend()
plt.show()
plt.axvline(mean,label='mean', color='red')
plt.axvline(low,label='low', color='green')
plt.axvline(high,label='high', color='green')
plt.axvline(0,label='zero', color='blue')
plt.legend()
plt.show()