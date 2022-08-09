import datetime
import joblib
import numpy as np
import mplfinance as mpf
from wave_fit import find_localminmax
from get_data import convert2csv
from get import get_data, set_data
from sklearn.neighbors import KNeighborsClassifier


# class wave_fit(object):
def wave_fit(start_date:datetime, end_date:datetime, interval:str, appro_size:int, print_data = bool(False)):
    data_raw = get_data(start_date, end_date, interval)
    X, Y = set_data(data_raw)
    data = []    # data: [0, 3, 9], [1, 4, 10]... [time, lowest, highest]
    for element in X:
        data.append([element, Y[2,element], Y[1,element]])
    extX, extY = find_localminmax(X, Y, appro_size)
    data = np.array(data)
    if(print_data):
        mpf.plot(convert2csv(data_raw), type='candle', volume=True)
    return extX, extY, data

def find_minmax_for_train(data_raw, start:int, end:int):
    X, Y = set_data(data_raw[start:end])
    data = []    # data: [0, 3, 9], [1, 4, 10]... [time, lowest, highest]
    for element in X:
        data.append([element, Y[2,element], Y[1,element]])
    extX, extY = find_localminmax(X, Y, appro_size)
    data = np.array(data)
    return extX, extY, data

def k_predict(start_date:datetime, end_date:datetime, interval:str, appro_size:int, print_data:bool):
    k = []
    delta = {'1d':datetime.timedelta(days=1),
             '4h':datetime.timedelta(hours=4), 
             '1h':datetime.timedelta(hours=1)}
    Key_X, Key_Y, data =wave_fit(start_date, end_date, interval, appro_size, print_data)# Key points, X = time, Y = price
    if(len(Key_X) > 4):
        diff = 0
        for num1 in (-1, -2, -3, -4):
            k.append((Key_Y[num1-1]-Key_Y[num1])/(Key_X[num1-1]-Key_X[num1]))
            diff += abs(Key_X[num1-1]-Key_X[num1])
    else:
        print('Not enourgh data')
        return -1, -1, datetime.datetime.now(), datetime.datetime.now()
    diff = diff/4
    begin = datetime.datetime.now() - (len(data) - Key_X[-1])*delta[interval]
    target = begin + diff*delta[interval]
    knn = joblib.load('model/knn_predict_trend.pkl')
    k = np.array(k).reshape(1, -1)
    res = knn.predict(k)
    return res, diff, begin, target

def train_model(start:datetime, end:datetime, interval:str, appro_size:int):
    # X, Y, data = wave_fit(start, end, interval, appro_size)
    data_raw = get_data(start, end, interval)
    size = len(data_raw)
    k = []
    note = []
    diff = 0
    print('Train size:',size)
    print('Training model')
    for i in range(50, size-10):

        X, Y, data = find_minmax_for_train(data_raw, i-50, i)
        if(len(X) > 4):
            k_tem = []
            for j in (-1, -2, -3, -4):
                k_tem.append((Y[j-1]-Y[j])/(X[j-1]-X[j]))
                diff += abs(X[j-1]-X[j])
            k.append(k_tem)
            diff = int(diff/4)

            x, y, data = find_minmax_for_train(data_raw, i-50, i+diff)

            y = (data[X[-1],1]+data[X[-1],2])/2
            x = X[-1]
            y_next = (data[X[-1]+diff,1]+data[X[-1]+diff,2])/2
            x_next = x+diff
            actual_k = (y_next -y)/(x_next - x)
            trend = 0
            if(actual_k > 0):
                trend = 1
            if(actual_k < 0):
                trend = -1
            note.append(trend)
    knn = KNeighborsClassifier()
    knn.fit(k,note)
    joblib.dump(knn,'model/knn_predict_trend.pkl')
    print('Model saved')

def test_model(start:datetime, end:datetime, interval:str, appro_size:int):
    data_raw = get_data(start, end, interval)
    size = len(data_raw)
    k = []
    note = []
    diff = 0
    print('Test size:',size)
    knn = joblib.load('model/knn_predict_trend.pkl')
    for i in range(50, size-10):

        X, Y, data = find_minmax_for_train(data_raw, i-50, i)
        if(len(X) > 4):
            k_tem = []
            for j in (-1, -2, -3, -4):
                k_tem.append((Y[j-1]-Y[j])/(X[j-1]-X[j]))
                diff += abs(X[j-1]-X[j])
            k.append(k_tem)
            diff = int(diff/4)

            x, y, data = find_minmax_for_train(data_raw, i-50, i+diff)

            y = (data[X[-1],1]+data[X[-1],2])/2
            x = X[-1]
            y_next = (data[X[-1]+diff,1]+data[X[-1]+diff,2])/2
            x_next = x+diff
            actual_k = (y_next -y)/(x_next - x)
            trend = 0
            if(actual_k > 0):
                trend = 1
            if(actual_k < 0):
                trend = -1
            note.append(trend)
    print('Test score:{:.2f}'.format(knn.score(k,note)))

if __name__ == '__main__':
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=50)
    # start = datetime.datetime(2021,1,12)
    # end = datetime.datetime(2021,3,12)
    appro_size = 4
    interval = '1d' #1h, 4h, 1d
    print_data = bool(False)

    k, days, begin, target = k_predict(start, end, interval, appro_size, print_data)
    print(k,'from', begin, 'to', target)

# model training code
    start = datetime.datetime(2010,1,12)
    end = datetime.datetime(2022,1,12)
    # train_model(start, end, interval, appro_size)
    start = datetime.datetime(2022,1,13)
    end = datetime.datetime(2022,7,12)
    # test_model(start, end, interval, appro_size)

