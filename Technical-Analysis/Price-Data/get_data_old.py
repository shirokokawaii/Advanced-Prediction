from binance.client import Client
import numpy as np
np.set_printoptions(suppress=True)
import datetime
from time import strftime

intervals = {720: '1d', 240: '4h', 60: '1h', 15: '15m', 5: '5m', 1: '1m'}
now = datetime.datetime.now()
before = now - datetime.timedelta(days=60)
end = now.strftime("%d %m, %Y")
start = before.strftime("%d %m, %Y")
start = '01 01, 2010'
end = '30 12, 2022'

trading_pair = 'BTCUSDT'

# load key and secret and connect to API
keys = open('Price-Data/keys.txt').readline()
print('Connecting to Client...')
api = Client(keys[0], keys[1])

# fetch desired candles of all data
print('Fetching data (may take multiple API requests)')
hist = api.get_historical_klines(trading_pair, intervals[720], start, end)
print('Finished.')

# create numpy object with closing prices and volume
hist = np.array(hist, dtype=np.float32)
#hist = hist[:, 4]
hist = hist[:, 1:6]

# data information. Opening, Highest, Lowest, Closing, Volume
print("\nDatapoints:  {0}".format(hist.shape[0]))
print("Memory:      {0:.2f} Mb\n".format((hist.nbytes) / 1000000))

# save to file as numpy object
np.save("hist_data", hist)

#print the data
data=np.load("hist_data.npy")
print(data)
print(data.shape)
