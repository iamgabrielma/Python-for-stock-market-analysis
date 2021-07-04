#!/usr/bin/env python3
import pandas_datareader as pdr
import datetime as dt
import sys
import json

# This version of the script has been created specifically to create JSON output for the iOS app.

_debug_show_details = False

# 1 - Read tickers from file
def read_tickers_from_txt(market):

	with open(market) as file:
		#print(file.readlines()) # it comes with a \n character:
		lines = [line.rstrip() for line in file]
	
	return lines


# 2 - Calculate their RSI
def calc_rsi(t, ticker_id):
	 
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
	#print(ticker['RSI'])

	# Skip first 14 days to have real values , no need because we're checking 6 months back
	#ticker = ticker.iloc[14:]
	if _debug_show_details == True:
		print(ticker)

	# Latest RSI value:
	length_of_dataframe = len(ticker)
	latest_rsi_value = ticker['RSI'][length_of_dataframe-1]
	oversold = 30
	overbought = 70

	stockDictionary['id'] = ticker_id
	stockDictionary['ticker'] = t
	stockDictionary['rsi'] = str(latest_rsi_value)


	if latest_rsi_value.astype(int) > overbought:

		stockDictionary['signal'] = 'SELL signal'
		print(t + ' RSI: ' + str(latest_rsi_value) + ' - SELL')

	elif latest_rsi_value.astype(int) < oversold:
	#elif latest_rsi_value < oversold:
		
		stockDictionary['signal'] = 'BUY signal'
		print(t + ' RSI: ' + str(latest_rsi_value) + ' - BUY')
	else:
		#print(type(latest_rsi_value))
		#print(type(oversold))
		stockDictionary['signal'] = 'Neutral signal'
		print(t + ' RSI: ' + str(latest_rsi_value) + ' - Neutral')


	return stockDictionary

#3 - Convert data to JSON
def convertToJson(mydict):

	today = dt.date.today()
	today.strftime("%Y-%m-%d")
	#print(today)
	#sys.exit()
	with open( str(today) + "-rsi.json", "w") as file:
		json.dump(mydict, file, indent = 4)


def main():
	print("Starting script...")

	# Creating the ticker list from the txt file:
	tickerList = read_tickers_from_txt("custom-tickers.txt")
	print(str(len(tickerList)) + " tickers in " + "custom-tickers.txt")
	output_list = []

	#exit()
	
	try:
		for t in tickerList:
			print("Analyzing " + t )
			ticker_id = tickerList.index(t) # assign a ticker_id so later we can parse JSON properly via iOS app.
			item = calc_rsi(t, ticker_id) # calculates the RSI for each item
			output_list.append(item) # adds all info to a list of dictionaries
		convertToJson(output_list) # At this point we have a list of all items, moving to iOS.	
	except:
		print("oopsie...")


if __name__ == "__main__":
	main()