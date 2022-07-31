from random import randint
from cv2 import DIST_L2
from wave_fit import *
from sklearn.neighbors import KNeighborsClassifier
import datetime
import cv2

# class wave_fit(object):
def wave_fit(year, month, day, size, appro_size, interval):
    X, Y = set_data(get=True, size=size, interval=interval, year=year, month=month, day=day)
    extX, extY = find_localminmax(X, Y, appro_size)

    data = pd.read_csv(f'data/csv/20{year}-{month}-{day}_{size}_{interval}.csv', index_col=0, parse_dates=True)
    data.index.name = 'Date'

    apd = mpf.make_addplot(convert2line(extX, extY, X))
    mpf.plot(data, type='candle', volume=True, addplot=apd)
    return extX, extY, data_1

def k_predict(range, appro_size, interval, year, month, day):
    trainer = []
    k = []
    # ********data should get the highest and lowest price
    # data: [0, 3, 9], [1, 4, 10]...
    Key_X, Key_Y, data =wave_fit(year, month, day, range, appro_size, interval)# Key points, X = time, Y = price
    if(len(Key_X) > 3):
        for num1 in (-1, -2, -3, -4, -5):
            if(Key_Y[num1] > Key_Y[num1-1]):
                for num2 in range(Key_X[num1-1], Key_X[num1]+1):
                    trainer.append([num2, data[num2, 1]])
            else:
                for num2 in range(Key_X[num1-1], Key_X[num1]+1):
                    trainer.append([num2, data[num2, 0]])
            print(trainer)
            trainer = np.array(trainer)
            output = cv2.fitLine(trainer, DIST_L2, 0, 0.01, 0.01)
            k_tem = output[1]/output[0]
            # b = output[3] - k * output[2]
            # plt.plot(X, Y)
            # plt.plot([0,output[2]], [b,output[3]])
            # plt.show()
            # print(k)
            k.append(k_tem)
    else:
        print('Not enourgh data length')
    return k

if __name__ == '__main__':
    now = datetime.datetime.now()

    range = 50
    appro_size = 4
    interval = '1d'
    year = now.strftime('%y')
    month = now.strftime('%m')
    day = now.strftime('%d')
    # year = '22'
    # month = '07'
    # day = '29'
    total_train_time = 3000

    data_k = []
    for i in range(total_train_time):
        randomtime = randint(range,len(data-50))
        # randomtime to time************************************
        k = k_predict(range, appro_size, interval, year, month, day)
    print(k)

