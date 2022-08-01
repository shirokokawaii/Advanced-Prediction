import datetime
import json
import time
import mplfinance as mpf

import pandas as pd
import requests
import numpy as np

DIR = "../MEGA/"


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
    if filename != "":
        np.save(DIR + filename, hist)
    hist = np.load(DIR + filename + ".npy")
    return hist


def convert2csv(hist_data, save=False, filename=""):
    np_to_csv = pd.DataFrame(data=hist_data)
    np_to_csv.to_csv(f"../MEGA/DATA.csv")
    index = [0, 3, 1, 2, 6, 4]
    np_to_csv = np_to_csv[index]
    np_to_csv = np_to_csv.rename(columns={0: 'Date', 3: 'Open', 1: 'High', 2: 'Low', 6: 'Close',
                                          4: 'Volume'})
    np_to_csv['Date'] = pd.to_datetime(np_to_csv['Date'], unit='s')
    np_to_csv = np_to_csv.set_index('Date')
    if save:
        np_to_csv.to_csv(f"../MEGA/{filename}.csv")
    return np_to_csv


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


if __name__ == "__main__":
    size = 2000
    # appro_size = 5
    interval = '1h'
    year = '22'
    month = '08'
    day = '01'
    # end_hour = '12:00:00'
    # filename = f"20{year}-{month}-{day}_{size}_{interval}"
    # end = f"20{year}-{month}-{day} {end_hour}"

    # hist = get_data(interval, size, end, filename)
    # hist = np.load(DIR + filename + ".npy")
    # csv_data = convert2csv(hist, True, filename=filename)

    # start_time = csv_data[0: 1].index
    # current_hour = start_time.strftime('%Y-%m-%d %H:%M:%S').tolist()[0]
    # print(current_hour)
    # print(i)

    n = 50

    for i in range(0, n):
        i = n - i
        if i == n:
            end = "2022-08-01 00:00:00"
        hist = get_data(interval, size, end, str(i))
        print(i)
        csv_data = convert2csv(hist, True, filename=str(i))

        # set next time
        start_time = csv_data[0: 1].index
        print(f"start_time:{start_time}")
        start_time = start_time-datetime.timedelta(hours=-7)

        print(f"after:{start_time}")
        current_hour = start_time.strftime('%Y-%m-%d %H:%M:%S').tolist()[0]
        end = current_hour
        filename = f"{i}_{size}_{interval}"
        print(end)


    for i in range(1, n):
        print(f"{i}base")
        if i == 1:
            base = np.load(f'{DIR}{i}.npy')
        print(base)
        append_data = np.load(f'{DIR}{i+1}.npy')
        base = np.append(base, append_data)
        print(f"----baseshape After append:{len(base)}")
        print(base)

        base = base.reshape(-1, 7)

        print(f"----base After after reshape")
        csv_data = convert2csv(base, True, filename="conv")
        print(base)

    np.save("../MEGA/Conv", base)
    # print("a")
    # print(a)
    # print("b")
    # print(b)
    # print("c")
    # print(c)
    # c = c.reshape(7, int(len(c)/7))
    # print("cAfter")
    # print(c)

    # print(f"{int(start_time.hour)}:00:00")

    # mpf.plot(csv_data, type='candle', volume=True)

    # X, Y = set_data(get=True, size=size, interval=interval, year=year, month=month, day=day)

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
