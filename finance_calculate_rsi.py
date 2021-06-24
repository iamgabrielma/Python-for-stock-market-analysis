# Resource: https://www.investopedia.com/terms/r/rsi.asp
import pandas_datareader as pdr
import datetime as dt
import sys

_debug_show_details = False

tickerList = ['MU','INTC', 'BP', 'TROX', 'MMM', 'UL', 'SFTBY', 'CRSR', 'ATVI', 'EA']

def calc_rsi(t):
	
	stockDictionary = {}
	# Initial data source
	ticker = pdr.get_data_yahoo(t, dt.datetime(2021,1,1), dt.datetime.now())
	
	# We're looking for the difference between sessions in closing price
	delta = ticker['Close'].diff()
	
	# We need to transform the data we got into input to feed the RSI indicator:
	# up = Average of all up-moves in the last N price bars
	# down = Average of all down-moves in the last N price bars
	up = delta.clip(lower=0)
	down = -1*delta.clip(upper=0)
	
	# Calculates the exponential weighted (EW) functions for a 14 period serie, recursively, and returns the mean of the values
	ema_up = up.ewm(com=13, adjust=False).mean()
	ema_down = down.ewm(com=13, adjust=False).mean()
	
	# Relative strength
	rs = ema_up/ema_down
	
	print('-----------------------------')
	# Relative strength indexes column for each ticker
	ticker['RSI'] = 100 - ( 100 / (1+rs) )

	# Skip first 14 days to have real values
	ticker = ticker.iloc[14:]
	if _debug_show_details == True:
		print(ticker)

	# Get and print the latest RSI value in order to make informed decisions:
	length_of_dataframe = len(ticker)
	latest_rsi_value = ticker['RSI'][length_of_dataframe-1]
	oversold = 30
	overbought = 70

	## Filling dictionary
	stockDictionary['ticker'] = t
	stockDictionary['rsi'] = str(latest_rsi_value)

	if latest_rsi_value.astype(int) > overbought:
		stockDictionary['signal'] = 'SELL signal'
		print(t + ' RSI: ' + str(latest_rsi_value) + ' - SELL signal')
	elif latest_rsi_value.astype(int) < oversold:
		stockDictionary['signal'] = 'BUY signal'
		print(t + ' RSI: ' + str(latest_rsi_value) + ' - BUY signal')
	else:
		stockDictionary['signal'] = 'Neutral signal'
		print(t + ' RSI: ' + str(latest_rsi_value) + ' - Neutral signal')

	print(stockDictionary)

for t in tickerList:
	calc_rsi(t)
