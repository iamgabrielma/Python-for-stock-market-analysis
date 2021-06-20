## Calculating EMA100 with Pandas

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import pandas

import threading
import time

class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)
		self.data = []
		
	def historicalData(self, reqId, bar):
		print(f'Time: {bar.date} Close: {bar.close}')
		self.data.append([bar.date, bar.close])
		
def run_loop():
	app.run()

## Making errors more descriptive:
def error(self, reqId, errorCode, errorString):
	if errorCode == 162:
		print('Retrieving historical data requires a market data lvl 1 subscription ')

app = IBapi()
app.connect('127.0.0.1', 7497, 1)

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1) #Sleep interval to allow time for connection to server

#Create contract object
stock_contract = Contract()
stock_contract.symbol = 'AMD'
stock_contract.secType = 'STK'
stock_contract.exchange = 'SMART'
stock_contract.currency = 'USD'


#Request historical candles
# https://interactivebrokers.github.io/tws-api/historical_bars.html , duration = 6 months , granularity = 1 day
app.reqHistoricalData(1, stock_contract, '', '6 M', '1 day', 'MIDPOINT', 0, 2, False, [])

print("Plotting data. Please wait 5 seconds...")
time.sleep(5) #sleep to allow enough time for data to be returned

df = pandas.DataFrame(app.data, columns=['DateTime', 'Close'])
df['DateTime'] = pandas.to_datetime(df['DateTime'],unit='s') 


### Calculate 20 SMA Using Pandas
df['100SMA'] = df['Close'].rolling(100).mean()
print(df.tail(10))


app.disconnect()