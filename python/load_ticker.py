import pandas as pd
import os

cwd=os.getcwd()

df=pd.read_csv(f'{cwd}/stocks.csv')
print(df)

