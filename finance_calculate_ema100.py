import numpy as np
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime, date

def calculate_ema(prices, days, smoothing=2):
    ema = [sum(prices[:days]) / days]
    for price in prices[days:]:
        ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days)))) # adds to list
    return ema


symbol = 'PSTH'
# Last 3 months ~ 100 days.
df = pdr.DataReader(symbol, 'yahoo', '2021-03-01', '2021-06-21') # Example output: [23.471000099182127, 23.288999956304373, 23.127363531254534, 23.056933756684284, 22.992036848730677, 22.938939378586817]

print(symbol)

## EMA100
ema = calculate_ema(df['Close'], 10)
print('EMA100: ' + str(ema[-1])) # Last value in the list is the most recent price, so we'll get the [-1] value in order to compare it with the price

## PRICE TODAY
psth = pdr.get_data_yahoo(symbols='PSTH', start = date.today(), end = date.today())
print( 'Price: ' + str(psth['Adj Close'].tail(1)))
