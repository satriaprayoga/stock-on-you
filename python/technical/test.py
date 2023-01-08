import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

from datetime import datetime

from macd import MACD
from macrossover import MACrossOver

default_end_date = datetime.now().strftime('%Y-%m-%d')

bbri=yf.Ticker('BBRI.JK')
data=bbri.history(period='2y',actions=False)

macd=MACD(dataFrame=data)
macd.apply_macd()
macd.build_macd_signal()

maco=MACrossOver(dataFrame=data,fast=9,slow=26,ma="ema")
maco.apply_ma()
maco.build_MA_Signal()
print(data[["Close","MACD","MACD_Signal","MACD_Position","MA_Signal","Position"]])
print(data["Close"].iloc[-1])