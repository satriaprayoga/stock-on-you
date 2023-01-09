import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

cwd=os.getcwd()
df = pd.read_csv(f'{cwd}/sp500sub.csv',index_col='Date', parse_dates=True)
print(df.head())
google=df[df['Name']=='GOOG']
google[['Close','Adj Close']].plot(figsize=(10,10))
plt.show()
aapl=df[df['Name']=='AAPL']
aapl[['Close','Adj Close']].plot(figsize=(10,10))
plt.show()
