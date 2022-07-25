import os

from binance.client import Client
import numpy as np

DIR = "../data/hist_data"


def get_data(start, end, intervals='1d', override=False, trading_pair='BTCUSDT'):
    keys = open('key.txt').readline()
    print('Connecting to Client...')
    api = Client(keys[0], keys[1])
    print('Fetching data (may take multiple API requests)')
    hist = api.get_historical_klines(trading_pair, intervals, start, end)
    print('Finished.')
    hist = np.array(hist, dtype=np.float32)
    hist = hist[:, 0:6]
    print("\nDatapoints:  {0}".format(hist.shape[0]))
    print("Memory:      {0:.2f} Mb\n".format((hist.nbytes) / 1000000))
    save_file(hist, 1, override)


def save_file(data, count=1, override=False):
    if override:
        np.save(DIR, data)
    else:
        if os.path.exists(DIR + str(count) + ".npy"):
            count += 1
            save_file(data, count)
        else:
            np.save(DIR + str(count), data)
            datas = np.load(DIR + str(count) + ".npy")
            print('Results------')
            print(datas)
