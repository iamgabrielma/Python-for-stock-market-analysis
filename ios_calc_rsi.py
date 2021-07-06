#!/usr/bin/env python3
from pandas_datareader import data as pdr
import datetime as dt
import sys
import json
import yfinance as yfin

# This override fixes (for the moment) get_data_yahoo not retrieving the stock data: https://github.com/pydata/pandas-datareader/issues/868#issuecomment-873381817
yfin.pdr_override()

# This version of the script has been created specifically to create JSON output for the iOS app.
data_source = ""
_debug_show_details = False


def read_tickers_from_txt(data_source):
	'''
	Reads all company tickers fed to the function, line by line, and returns a list
	'''
	print("Reading data from " + str(sys.argv))
	#exit()
	with open(data_source) as file:
		#print(file.readlines()) # it comes with a \n character:
		lines = [line.rstrip() for line in file]
	
	return lines

def calc_rsi(t, ticker_id):
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

def convertToJson(mydict):
	''' 
	Converts data to JSON
	''' 
	print("Creating JSON file...")
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

	tickerList = read_tickers_from_txt(data_source)
	
	print(str(len(tickerList)) + " tickers in " + data_source)
	output_list = []
	
	try:
		print("Analyzing...")
		for t in tickerList:
			print(t, end="\r")
			ticker_id = tickerList.index(t) # assign a ticker_id so later we can parse JSON properly via iOS app.
			item = calc_rsi(t, ticker_id) # calculates the RSI for each item
			output_list.append(item) # adds all info to a list of dictionaries
		convertToJson(output_list) # At this point we have a list of all items, moving to iOS.	
	except:
		print("oopsie...")


if __name__ == "__main__":
	main()
