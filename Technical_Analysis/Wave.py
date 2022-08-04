import datetime
import wave
# import cv2
import joblib
import numpy as np
import pandas as pd
from random import randint
import mplfinance as mpf
# from cv2 import DIST_L2
from wave_fit import find_localminmax, convert2line
from get import get_data, set_data
from sklearn.neighbors import KNeighborsClassifier


# class wave_fit(object):
def wave_fit(start_date:datetime, end_date:datetime, interval:str, appro_size:int):
    data_raw = get_data(start_date, end_date, interval)
    X, Y = set_data(data_raw)
    data = []    # data: [0, 3, 9], [1, 4, 10]... [time, lowest, highest]
    for element in X:
        data.append([element, Y[2,element], Y[1,element]])
    extX, extY = find_localminmax(X, Y, appro_size)
    data = np.array(data)
    return extX, extY, data

def k_predict(start_date:datetime, end_date:datetime, interval:str, appro_size:int):
    k = []
    Key_X, Key_Y, data =wave_fit(start_date, end_date, interval, appro_size)# Key points, X = time, Y = price
    if(len(Key_X) > 3):
        diff = 0
        for num1 in (-1, -2, -3, -4):
            # if(Key_Y[num1] > Key_Y[num1-1]):
                # for num2 in range(Key_X[num1-1], Key_X[num1]+1):
                #     trainer.append([num2, data[num2, 1]])
            k.append((Key_Y[num1-1]-Key_Y[num1])/(Key_X[num1-1]-Key_X[num1]))
            diff += abs(Key_X[num1-1]-Key_X[num1])
            # else:
                # for num2 in range(Key_X[num1-1], Key_X[num1]+1):
                #     trainer.append([num2, data[num2, 0]])
            # print(trainer)
            # trainer = np.array(trainer)
            # output = cv2.fitLine(trainer, DIST_L2, 0, 0.01, 0.01)
            # k_tem = output[1]/output[0]
            # b = output[3] - k * output[2]
            # plt.plot(X, Y)
            # plt.plot([0,output[2]], [b,output[3]])
            # plt.show()
            # print(k)
            # k.append(k_tem)
    else:
        print('Not enourgh data length')
    diff = diff/4
    knn = joblib.load('model/knn_predict_trend.pkl')
    k = np.array(k).reshape(1, -1)
    res = knn.predict(k)
    return res, diff

def train_model(start:datetime, end:datetime, interval:str, appro_size:int):
    X, Y, data = wave_fit(start, end, interval, appro_size)
    size = len(X)
    k = []
    note = []
    diff = 0
    print('training model')
    for i in range(5, size-5):
        k_tem = []
        for num1 in (i-1, i-2, i-3, i-4):
            k_tem.append((Y[num1-1]-Y[num1])/(X[num1-1]-X[num1]))
            diff += abs(X[num1-1]-X[num1])
        k.append(k_tem)
        diff = int(diff/4)
        y = (data[X[i],1]+data[X[i],2])/2
        x = X[i]
        y_next = (data[X[i]+diff,1]+data[X[i]+diff,2])/2
        x_next = x+diff
        actual_k = (y_next -y)/(x_next - x)
        trend = 0
        if(actual_k > 0):
            trend = 1
        if(actual_k < 0):
            trend = -1
        note.append(trend)
    # print(k)
    # print(note)
    knn = KNeighborsClassifier()
    knn.fit(k,note)
    joblib.dump(knn,'model/knn_predict_trend.pkl')
    print('model saved')

def test_model(start:datetime, end:datetime, interval:str, appro_size:int):
    X, Y, data = wave_fit(start, end, interval, appro_size)
    size = len(X)
    k = []
    note = []
    diff = 0
    knn = joblib.load('model/knn_predict_trend.pkl')
    for i in range(5, size-5):
        k_tem = []
        for num1 in (i-1, i-2, i-3, i-4):
            k_tem.append((Y[num1-1]-Y[num1])/(X[num1-1]-X[num1]))
            diff += abs(X[num1-1]-X[num1])
        k.append(k_tem)
        diff = int(diff/4)
        y = (data[X[i],1]+data[X[i],2])/2
        x = X[i]
        y_next = (data[X[i]+diff,1]+data[X[i]+diff,2])/2
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
    appro_size = 4
    interval = '1d' #1h, 4h, 1d

    # k, days = k_predict(start, end, interval, appro_size)
    # print(k,'for',days,'days')

    start = datetime.datetime(2010,1,12)
    end = datetime.datetime(2022,1,12)
    # train_model(start, end, interval, appro_size)
    start = datetime.datetime(2022,1,12)
    end = datetime.datetime(2022,7,12)
    # test_model(start, end, interval, appro_size)

