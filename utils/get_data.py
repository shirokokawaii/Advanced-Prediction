import json
import time

import pandas as pd
import requests
import numpy as np

DIR = "../data/"


def get_data(interval, size, end, filename=""):
    endpoint = {'1d': 'https://min-api.cryptocompare.com/data/histoday',
                '1h': 'https://min-api.cryptocompare.com/data/v2/histohour',
                '1m': 'https://min-api.cryptocompare.com/data/v2/histominute'}
    Ts = time.mktime(time.strptime(end, "%Y-%m-%d %H:%M:%S"))
    res = requests.get(endpoint[interval] + '?fsym=BTC&tsym=USD&limit=' + str(size) + "&toTs=" + str(int(Ts)))
    if interval != '1d':
        data = json.loads(res.content)['Data']['Data']
    else:
        data = json.loads(res.content)['Data']
    hist = pd.DataFrame(data)
    hist.drop(["conversionType", "conversionSymbol"], axis='columns', inplace=True)
    # hist = hist.set_index('time')
    # hist.index = pd.to_datetime(hist.index, unit='s')

    if filename != "":
        np.save(DIR + filename, hist)
    return hist


if __name__ == "__main__":
    time_interval = '1h'
    data_size = 2000
    year = '22'
    month = '07'
    day = '29'

    end = f"20{year}-{month}-{day} 20:00:00"
    filename = f"20{year}-{month}-{day}_{data_size}_{time_interval}"
    hist = get_data(time_interval, data_size, end, filename)
    data = np.load(DIR + filename + ".npy")
    print(data[0, :])
