import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

cwd=os.getcwd()
df = pd.read_csv(f'{cwd}/all_stocks_5yr.csv')
# print(df.head())
# print(df.info())
# print(df['Name'].unique())
# print(df['Name'].unique().shape)
# print(df[df['Name']=='IBM'])
ibm = df[df['Name']=='IBM']
# print(ibm['close'])
# ibm['close'].plot()
# plt.show()

#################################
# create new dataframe with dates as index

dates= pd.date_range(df['date'].min(),df['date'].max())
print(dates)

close_prices=pd.DataFrame(index=dates)
print(close_prices.head())

symbols = df['Name'].unique()

df2 = pd.DataFrame(data=ibm['close'].to_numpy(),index=ibm['date'], columns=['IBM'])
print(df2.head())

for symbol in symbols:
    df_sym=df[df['Name']==symbol]
    df_sym=pd.DataFrame(data=df_sym['close'].to_numpy(),index=pd.to_datetime(df_sym['date']), columns=[symbol])
    close_prices=close_prices.join(df_sym)

#print(close_prices.head())

#print(close_prices.info())

close_prices.to_csv(f'{cwd}/sp500_close.csv')

#close2=pd.read_csv(f'{cwd}/sp500_close.csv',index_col=0, parse_dates=True)
#print(close2.head())


close_prices.dropna(axis=0,how='all', inplace=True)

print(close_prices.isna().sum().sum())

print(close_prices.iloc[0,:].isna().sum()) #1st row Nan value

#fill 1st row Nan value
close_prices.fillna(method='ffill',inplace=True)

print(close_prices.isna().sum().sum())
#backward fill the rest of the data
close_prices.fillna(method='bfill',inplace=True)
print(close_prices.isna().sum().sum())

close_prices.plot(legend=False, figsize=(10,10))
plt.show()