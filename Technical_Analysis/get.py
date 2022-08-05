import datetime
import json
import time
import os
from imageio import save
import pandas as pd
import requests
import numpy as np


def get_data(start:datetime.date, end:datetime.date, interval:str, save_file=bool(True)):
    # set api and argument
    endpoint =  {'1d': 'https://min-api.cryptocompare.com/data/v2/histoday?',
                '1h': 'https://min-api.cryptocompare.com/data/v2/histohour?',
                '4h': 'https://min-api.cryptocompare.com/data/v2/histohour?aggregate=4&',}
    intdelta =  {'1d': start.__rsub__(end).days,
                '1h': start.__rsub__(end).days*24,
                '4h': start.__rsub__(end).days*6}
    timedelta = {'1d': datetime.timedelta(days=2000),
                '1h': datetime.timedelta(hours=2000),
                '4h': datetime.timedelta(hours=2000)}

    DIR = "data/"
    start_year = start.strftime('%y')
    start_month = start.strftime('%m')
    start_day = start.strftime('%d')
    start_hour = start.strftime('%H')

    end_year = end.strftime('%y')
    end_month = end.strftime('%m')
    end_day = end.strftime('%d')
    end_hour = end.strftime('%H')

    start_time = str(start_year + start_month+'-'+start_day+start_hour)
    end_time = str(end_year + end_month+'-'+end_day+end_hour)

    size = 2000
    times = intdelta[interval]//2000 + 1
    final_range = intdelta[interval]%2000
    if(interval == '4h'):
        size = 500
        times = intdelta[interval]//500 + 1
        final_range = intdelta[interval]%500
    data = []

    # check if data existed
    if(os.path.exists(DIR + start_time + '_' + interval + '_' + end_time + '.npy')):
        print('Data already exist')
        data = np.load(DIR + start_time + '_' + interval + '_' + end_time + '.npy')
        data = pd.DataFrame(data)
        return(data)

    # get data from api
    print('Requesting data')
    for i in range(times):
        start += timedelta[interval]
        Ts = time.mktime(time.strptime(f"{start.strftime('20%y-%m-%d %H:%M:%S')}", "%Y-%m-%d %H:%M:%S"))
        if(i+1 == times):
            res = requests.get(endpoint[interval] + 'fsym=ETH&tsym=USD&limit=' + str(final_range) + "&toTs=" + str(int(Ts)))
            data_tem = json.loads(res.content)['Data']['Data']
            data += data_tem[1:]
            break
        res = requests.get(endpoint[interval] + 'fsym=ETH&tsym=USD&limit=' + str(size) + '&toTs=' + str(int(Ts)))
        res = requests.get(endpoint[interval] + 'fsym=ETH&tsym=USD&limit=' + str(final_range) + "&toTs=" + str(int(Ts)))
        data_tem = json.loads(res.content)['Data']['Data']
        data += data_tem[1:]

    # save data into file
    hist = pd.DataFrame(data)
    hist.drop(["conversionType", "conversionSymbol"], axis='columns', inplace=True)
    np.save(DIR + start_time + '_' + interval + '_' + end_time, hist)
    data = np.load(DIR + start_time + '_' + interval + '_' + end_time + '.npy')
    if(save_file == bool(False)):
        os.remove(DIR + start_time + '_' + interval + '_' + end_time + '.npy')
    data = pd.DataFrame(data)
    print('Finished')
    return(data)

def set_data(data):
    close = data[3].values
    X = np.arange(0, close.size)
    Y = np.concatenate((data[3].values, data[1].values, data[2].values), axis=0)
    Y = Y.reshape(3, int((len(Y) + 2) / 3))
    return X, Y

# test code
if __name__ == '__main__':
    start = datetime.datetime(2021,1,12)# 2021-01-12 12:00
    end = datetime.datetime(2021,1,20)# 2021-01-15 12:00
    data = get_data(start, end, '1d', bool(False))
    data = data[:3]
    print(data)
    print(len(data))
    X,Y = set_data(data)
    print(X, Y)

#return example:
# hist = Object{
#   0:time: 1658707200
#   1:high: 22660.92
#   2:low: 21268.28
#   3:open: 22585.4
#   4:volumefrom: 42928.78
#   5:volumeto: 940453686.83
#   6:close: 21305.59}

#file example:
# 19-01-1212_1d_19-05-2712.npy
# {19:start_year - 01:start_month - 12:start_day 21:start_hour _
# 1d:interval _ 19:end_year - 05:end_month - 27:end_day 21:end_hour}
