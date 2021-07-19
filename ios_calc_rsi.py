#!/usr/bin/env python3
import pandas as pd
from pandas_datareader import data as pdr
import pandas_ta as ta

import datetime as dt
import sys
import json
import yfinance as yfin
#import yahoo_fin
#from yahoo_fin import stock_info as si
import os

# This override fixes (for the moment) get_data_yahoo not retrieving the stock data: https://github.com/pydata/pandas-datareader/issues/868#issuecomment-873381817
yfin.pdr_override()

# This version of the script has been created specifically to create JSON output for the iOS app.
data_source = ""
_debug_show_details = False
_debug_print_date_in_json = False
_debug_is_options = True

df = pd.DataFrame() # Pandas empty dataframe


def read_tickers_from_txt(data_source):
	'''
	Reads all company tickers fed to the function, line by line, and returns a list
	'''
	#exit()
	with open(data_source) as file:
		#print(file.readlines()) # it comes with a \n character:
		lines = [line.rstrip() for line in file]
	
	return lines

def calc_sma(ticker, period):

	#ticker = "AAPL"
	start = dt.datetime(2020,1,1)
	end = dt.datetime.now()
	data = pdr.get_data_yahoo(ticker, start, end)
	
	if period == 100:
		data['MA100'] = data['Close'].rolling(100).mean()
		sma = str(data['MA100'].iloc[-1].round(decimals=2))
	
	elif period == 200:
		data['MA200'] = data['Close'].rolling(200).mean()
		sma = str(data['MA200'].iloc[-1].round(decimals=2))
	else:
		sma = "Null"

	return sma


# def calc_ema200():

# 	pass

def calc_rsi(t, ticker_id):

	stockOrOption = ""
	if _debug_is_options == True:
		stockOrOption = " - Sell PUT"
	else:
		stockOrOption = " - Buy"
	'''
	Calculates RSI
	'''
	 
	stockDictionary = {}

	# Last 6 months only:
	try:
		ticker = pdr.get_data_yahoo(t, dt.datetime(2021,1,1), dt.datetime.now())
	except:
		print("Was not possible to retrieve data from Yahoo. Check the network.")
	
	delta = ticker['Close'].diff()
	
	up = delta.clip(lower=0)
	down = -1*delta.clip(upper=0)

	#Adjusted to 2 periods
	ema_up = up.ewm(com=2, adjust=False).mean()
	ema_down = down.ewm(com=2, adjust=False).mean()
	
	rs = ema_up/ema_down
	
	#print('######## ' + t + ' ########')
	print('-----------------------------')
	#print(ticker)
	ticker['RSI'] = 100 - ( 100 / (1+rs) )
	#ticker['RSI'] = str(round(ticker['RSI'], 2))
	#print(ticker['RSI'])

	# Skip first 14 days to have real values , no need because we're checking 6 months back
	#ticker = ticker.iloc[14:]
	if _debug_show_details == True:
		print(ticker)

	# Latest RSI value:
	length_of_dataframe = len(ticker)
	latest_rsi_value = ticker['RSI'][length_of_dataframe-1]
	#print(type(latest_rsi_value)) # numpy.float64
	latest_rsi_value = latest_rsi_value.round(decimals=2)
	oversold = 30
	overbought = 70

	stockDictionary['id'] = ticker_id
	stockDictionary['ticker'] = t
	stockDictionary['rsi'] = str(latest_rsi_value)

	# IMPLEMENTING EMA:
	#try:
	stockDictionary['ema100'] = str(calc_sma(t, 100))
	stockDictionary['ema200'] = str(calc_sma(t, 200))
		#stockDictionary['ema200'] = calc_ema200()
	#except:
		#print("Failed to calculate EMA100")


	if latest_rsi_value.astype(int) > overbought:

		stockDictionary['signal'] = 'Sell'
		print(t + ' RSI: ' + str(latest_rsi_value) + ' - Sell')

	elif latest_rsi_value.astype(int) < oversold:
	#elif latest_rsi_value < oversold:
		
		stockDictionary['signal'] = 'Buy'
		print(t + ' RSI: ' + str(latest_rsi_value) + stockOrOption) # Testing _debug_is_options
	else:
		#print(type(latest_rsi_value))
		#print(type(oversold))
		stockDictionary['signal'] = 'Neutral'
		print(t + ' RSI: ' + str(latest_rsi_value) + ' - Neutral')


	return stockDictionary

def convertToJson(mydict):
	''' 
	Converts data to JSON
	''' 
	print("Creating JSON file at..." + str(os.getcwd()))
	#subfolder_path = "/testData/"
	today = dt.date.today()
	today.strftime("%Y-%m-%d")
	#print(today)
	#sys.exit()
	with open( str(today) + "-rsi.json", "w") as file:
		json.dump(mydict, file, indent = 4)
	print("Done!")


def main():
	'''
	Runs the main script
	'''
	print("Starting script...")

	# Creating the ticker list from the txt file, use custom-tickers.txt by default unless we pass a different list.
	# Check if a parameter exists first:
	if (len(sys.argv)) <= 1:
		data_source = "custom-tickers.txt" # If no aguments have been passed, use the default
	else:
		data_source = sys.argv[1]

	print("Reading data from " + data_source)
	## 1. READ TICKERS WE'LL ANALYZE
	tickerList = read_tickers_from_txt(data_source)
	
	print(str(len(tickerList)) + " tickers in " + data_source)
	output_list = []
	#latestFetch["Date"] = dt.date.today().strftime("%Y-%m-%d")
	#output_list.append(latestFetch)
	
	try:
		print("Analyzing...")

		## Adding fetch time as a dict object
		if _debug_print_date_in_json == True:
			latestFetch = {}
			latestFetch["date"] = dt.date.today().strftime("%Y-%m-%d")
			output_list.append(latestFetch)

		for t in tickerList:
			print(t, end="\r")
			ticker_id = tickerList.index(t) # assign a ticker_id so later we can parse JSON properly via iOS app.
			## 2. CALCULATE RSI
			item = calc_rsi(t, ticker_id) # calculates the RSI for each item
			output_list.append(item) # adds all info to a list of dictionaries
		convertToJson(output_list) # At this point we have a list of all items, moving to iOS.	
	except:
		print("oopsie...")


if __name__ == "__main__":
	main()
