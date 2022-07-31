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
        print(res.content)
        data = json.loads(res.content)['Data']['Data']
    else:
        data = json.loads(res.content)['Data']
    hist = pd.DataFrame(data)
    hist.drop(["conversionType", "conversionSymbol"], axis='columns', inplace=True)
    if filename != "":
        np.save(DIR + filename, hist)

    # for new plt compatibility
    hist['time'] = pd.to_datetime(hist['time'], unit='s')
    head_key = ['time', 'open', 'high', 'low', 'close', 'volumefrom']
    hist = hist[head_key]
    hist = hist.rename(columns={'time': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close',
                                'volumefrom': 'Volume'})
    hist = hist.set_index('Date')
    hist.to_csv(f"{DIR}csv/{filename}.csv")
    return hist


def set_from_file(DIR, filename, size):
    data = np.load(DIR + filename + '.npy')
    close = data[-size:, 3]
    X = np.arange(0, close.size)
    Y = np.concatenate((data[-size:, 3], data[-size:, 1], data[-size:, 2]), axis=0)
    Y = Y.reshape(3, int((len(Y) + 2) / 3))
    return X, Y


def set_data(get=False, size="2000", interval="1d", year="18", month='07', day='28'):
    DIR = "../data/"
    filename = f"20{year}-{month}-{day}_{size}_{interval}"
    end = f"20{year}-{month}-{day} 20:00:00"

    if get:
        get_data(interval, size, end, filename)

    data = np.load(DIR + filename + '.npy')
    close = data[:, 3]
    X = np.arange(0, close.size)
    # Y = np.append(close, data[:, 1], data[:, 2], axis=0)
    Y = np.concatenate((data[:, 3], data[:, 1], data[:, 2]), axis=0)
    Y = Y.reshape(3, int((len(Y) + 2) / 3))
    # print(type(Y))
    return X, Y


def set_data_1D(get=False, size="2000", interval="1d", year="18", month='07', day='28'):
    DIR = "../data/"
    filename = f"20{year}-{month}-{day}_{size}_{interval}"
    end = f"20{year}-{month}-{day} 20:00:00"

    if get:
        get_data(interval, size, end, filename)

    data = np.load(DIR + filename + '.npy')
    print(data)
    close = data[:, 3]
    X = np.arange(0, close.size)
    Y = close
    return X, Y


if __name__ == "__main__":
    size = 10
    interval = '1h'
    year = '22'
    month = '06'
    day = '19'

    X, Y = set_data(get=True, size=size, interval=interval, year=year, month=month, day=day)
    X1, Y1 = set_data_1D(get=True, size=size, interval=interval, year=year, month=month, day=day)
    print(Y)
    print(Y1)
    print(Y[1, :])
    print(Y[1:3, 1])

    # time_interval = '1h'
    # data_size = 20
    # year = '22'
    # month = '07'
    # day = '29'
    #
    # end = f"20{year}-{month}-{day} 20:00:00"
    # filename = f"20{year}-{month}-{day}_{data_size}_{time_interval}"
    # hist = get_data(time_interval, data_size, end, filename)
    # # data = np.load(DIR + filename + ".npy")
    # print(hist)
