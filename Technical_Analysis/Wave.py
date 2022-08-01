from random import randint

import joblib
from numpy import hstack
# from cv2 import DIST_L2
from wave_fit import *
from sklearn.neighbors import KNeighborsClassifier
import datetime
# import cv2

# class wave_fit(object):
def wave_fit(year, month, day, size, appro_size, interval):
    X, Y = set_data(get=True, size=size, interval=interval, year=year, month=month, day=day)
    data = []    # data: [0, 3, 9], [1, 4, 10]... [time, lowest, highest]
    for element in X:
        data.append([element, Y[2,element], Y[1,element]])
    extX, extY = find_localminmax(X, Y, appro_size)

    data = pd.read_csv(f'data/csv/20{year}-{month}-{day}_{size}_{interval}.csv', index_col=0, parse_dates=True)
    data.index.name = 'Date'

    apd = mpf.make_addplot(convert2line(extX, extY, X))
    mpf.plot(data, type='candle', volume=True, addplot=apd)
    return extX, extY

def k_predict(range, appro_size, interval, year, month, day):
    # trainer = []
    k = []
    Key_X, Key_Y =wave_fit(year, month, day, range, appro_size, interval)# Key points, X = time, Y = price
    if(len(Key_X) > 3):
        for num1 in (-1, -2, -3, -4):
            # if(Key_Y[num1] > Key_Y[num1-1]):
                # for num2 in range(Key_X[num1-1], Key_X[num1]+1):
                #     trainer.append([num2, data[num2, 1]])
            k.append((Key_Y[num1-1]-Key_Y[num1])/(Key_X[num1-1]-Key_X[num1]))
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
    return k

if __name__ == '__main__':
    now = datetime.datetime.now()
    range = 200
    appro_size = 4
    interval = '1h' #1m, 1h, 1d
    year = now.strftime('%y')
    month = now.strftime('%m')
    day = now.strftime('%d')
    # year = '22'
    # month = '07'
    # day = '29'

    k = k_predict(range, appro_size, interval, year, month, day)
    print(k)

#     # *****************test code：train model data from 2010 to 2020

    # X = []
    # Y = []
    # start = datetime.date(2015,1,1)
    # end = datetime.date(2021,1,1)
    # delta = start.__rsub__(end).days * 24
    # times = delta//1000 + 1
    # range = 1000
    # range_final = delta%1000
    # count = 0
    # while(count <times):
    #     # Key_X_tem, Key_Y_tem = wave_fit(year, month, day, range, appro_size, interval)# Key points, X = time, Y = price
    #     start += datetime.timedelta(hours=1000)
    #     year = start.strftime('%y')
    #     month = start.strftime('%m')
    #     day = start.strftime('%d')
    #     print('year=',year)
    #     if(count == times-1 ):
    #         year = end.strftime('%y')
    #         month = end.strftime('%m')
    #         day = end.strftime('%d')
    #         range = range_final
    #     # X_tem, Y_tem = set_data(get=True, size=range, interval=interval, year=year, month=month, day=day)
    #     Key_X, Key_Y, data = wave_fit(year, month, day, range, appro_size, interval)
    #     data_k = []
    #     note = []
    #     print('training')
    #     count = 50
    #     while(count < len(Key_X)-50):
    #         if(count%300 == 0):
    #             print(count)
    #         train_k = []
    #         num1 = count-1
    #         while (num1 > count-5):
    #             train_k.append((Key_Y[num1-1]-Key_Y[num1])/(Key_X[num1-1]-Key_X[num1]))
    #             num1 -= 1
    #         actual_K = (data[0,Key_X+6] - Key_Y[count]) / (Key_X+6 - Key_X[count])
    #         trend = 0
    #         if(actual_K > 0):
    #             trend = 1
    #         if(actual_K < 0):
    #             trend = -1
    #         count += 1
    #         data_k.append(train_k)
    #         note.append(trend)

    #     wave_fit_model = KNeighborsClassifier()
    #     wave_fit_model.fit(data_k,note)
    #     joblib.dump(wave_fit_model,'model/wave_fit.pkl')
    #     # print('year=',year)
    #     # counter = 0
    #     # while(counter < len(X_tem)):
    #     #     X_tem[counter] += count*range
    #     #     counter += 1
    #     # for element in X_tem:
    #     #     X.append(element)
    #     # print(X)
    #     # print(Y)
    #     # Y = np.append(Y_tem,axis=1)
    #     # count += 1

    # # X = np.load('data/X.npy')
    # # Y = np.load('data/Y.npy')
    # print(Y)


