import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import mplfinance as mpf

from get_data import set_data


def find_localminmax(X, Y, size=4):
    slideX, slideY = get_slice(Y[0, :], size)
    extremumX = []
    extremumY = []
    # return slideX, slideY
    #
    for count in range(0, len(slideX)):
        index = slideX[count]
        if (count != 0) & (count != len(slideX) - 1):
            tmpx, tmpy = get_tmp(index, X, Y[0, :], size)
        elif count == len(slideX) - 1:
            tmpx = X[index - (size // 2):]
            tmpy = Y[0, :][index - (size // 2):]
        elif count == 0:
            tmpx = X[:index + (size // 2 + size % 2)]
            tmpy = Y[0, :][:index + (size // 2 + size % 2)]
        if count < len(slideX) - 1:
            if slideY[count] >= slideY[count + 1]:
                extY = max(tmpy)
            else:
                extY = min(tmpy)
            list_t = tmpy.tolist()
            extX = tmpx[list_t.index(extY)]
            extremumX.append(extX)
            extremumY.append(extY)
        else:
            extremumX.append(X[-1])
            extremumY.append(Y[0, :][-1])

    extremumX, extremumY = rec_delect(extremumX, extremumY)
    #
    return final_fix(X, Y, extremumX, extremumY)
    # return rec_delect(extremumX, extremumY)
    # return extremumX, extremumY


def rec_delect(extremumX, extremumY, count=0):
    if len(extremumX) <= 3:
        return extremumX, extremumY
    if count < len(extremumX) - 2:
        if extremumY[count] >= extremumY[count + 1]:
            if extremumY[count + 1] >= extremumY[count + 2]:
                extremumX = np.delete(extremumX, count + 1)
                extremumY = np.delete(extremumY, count + 1)
                extremumX, extremumY = rec_delect(extremumX, extremumY, count)
        if extremumY[count] < extremumY[count + 1]:
            if extremumY[count + 1] < extremumY[count + 2]:
                extremumX = np.delete(extremumX, count + 1)
                extremumY = np.delete(extremumY, count + 1)
                extremumX, extremumY = rec_delect(extremumX, extremumY, count)
        count += 1
        extremumX, extremumY = rec_delect(extremumX, extremumY, count)

    return extremumX, extremumY


def final_fix(X, Y, extremumX, extremumY):
    # 所有最大值集合和最小值集合
    maxV = Y[1, :]
    minV = Y[2, :]

    # Y = Y[0, :]
    listMin = minV.tolist()
    listMax = maxV.tolist()

    list = Y.tolist()
    for index in range(0, len(extremumX)):
        # get both maxmin around the index
        if (index != 0) & (index != len(extremumX) - 1):
            # tmpX = X[extremumX[index - 1]:extremumX[index + 1]]
            tmpY = Y[1:3, extremumX[index - 1]+1:extremumX[index + 1]]
        elif index == 0:
            tmpY = Y[1:3, :extremumX[index + 1]]
        elif index == len(extremumX) - 1:
            tmpY = Y[1:3, extremumX[index - 1]+1:]
        if index < len(extremumX) - 1:
            if extremumY[index + 1] > extremumY[index]:
                extremumY[index] = min(tmpY[1])
                extremumX[index] = X[listMin.index(min(tmpY[1]))]
            else:
                extremumY[index] = max(tmpY[0])
                extremumX[index] = X[listMax.index(max(tmpY[0]))]
        else:
            if extremumY[index - 1] > extremumY[index]:
                extremumY[index] = min(tmpY[1])
                extremumX[index] = X[listMin.index(min(tmpY[1]))]
            else:
                extremumY[index] = max(tmpY[0])
                extremumX[index] = X[listMax.index(max(tmpY[0]))]

    return extremumX, extremumY


def get_tmp(index, X, Y, size):
    resX = X[index - (size // 2):index + (size // 2 + size % 2)]
    rexY = Y[index - (size // 2):index + (size // 2 + size % 2)]
    return resX, rexY


def get_slice(Y, slice_size):
    slideX = []
    slideY = []
    count = 0
    for index in Y:
        if count % slice_size == 1:
            slideX.append(count)
            slideY.append(index)
        count += 1
    return slideX, slideY


def convert2line(extX, extY, X):
    result = []
    for count in range(0, len(extX)):
        if count == 0:
            for i in range(0, extX[count]):
                result.append(np.nan)
        if count == len(extX) - 1:
            result.append(extY[count])
            for j in range(extX[count] + 1, len(X)):
                result.append(np.nan)
            return result
        current_point = extY[count]
        next_point = extY[count + 1]
        dis = extX[count + 1] - extX[count]
        dif = (next_point - current_point) / dis
        for k in range(0, dis):
            val = current_point + k * dif
            result.append(round(val, 2))


if __name__ == '__main__':
    size = 150
    interval = '1h'
    year = '22'
    month = '07'
    day = '29'

    X, Y = set_data(get=True, size=size, interval=interval, year=year, month=month, day=day)

    appro_size = 3
    extX, extY = find_localminmax(X, Y, appro_size)
    print(extX)
    print(extY)

    data = pd.read_csv(f'data/csv/20{year}-{month}-{day}_{size}_{interval}.csv', index_col=0, parse_dates=True)
    data.index.name = 'Date'

    apd = mpf.make_addplot(convert2line(extX, extY, X))
    mpf.plot(data, type='candle', volume=True, addplot=apd)

    # mpf.plot(data, type='candle', mav=(3, 6, 9), volume=True)

    # plt.plot(X, Y[0, :], "-")
    # plt.plot(extX, extY, "-o")
    # plt.show()
