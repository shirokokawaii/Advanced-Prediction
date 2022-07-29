import numpy as np
import pylab as pl
from matplotlib import pyplot as plt
import mplfinance as mpf

from utils.fit.set_data import set_data


def find_localminmax(X, Y, size=4):
    slideX, slideY = get_sun(Y, size)
    extremumX = []
    extremumY = []
    for count in range(0, len(slideX)):
        if (count != 0) & (count != len(slideX) - 1):
            index = slideX[count]
            tmpx, tmpy = get_tmp(index, X, Y, size)
            if slideY[count] >= slideY[count + 1]:
                extY = max(tmpy)
            else:
                extY = min(tmpy)

            list_t = tmpy.tolist()
            extX = tmpx[list_t.index(extY)]
            extremumX.append(extX)
            extremumY.append(extY)
        # elif count == len(slideX)-1:
        #     extremumX.append()
        #     extremumY.append()
        # elif count == 0:
        #     extremumX.append()
        #     extremumY.append()

    extremumX, extremumY = rec_delect(extremumX, extremumY)

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
    list = Y.tolist()
    for index in range(0, len(extremumX)):
        if (index != 0) & (index != len(extremumX) - 1):
            tmpX = X[extremumX[index - 1]:extremumX[index + 1]]
            tmpY = Y[extremumX[index - 1]:extremumX[index + 1]]
            if extremumY[index - 1] > extremumY[index]:
                extremumY[index] = min(tmpY)
                extremumX[index] = X[list.index(min(tmpY))]
            else:
                extremumY[index] = max(tmpY)
                extremumX[index] = X[list.index(max(tmpY))]

    return extremumX, extremumY


def get_tmp(index, X, Y, size):
    resX = X[index - (size // 2):index + (size // 2 + size % 2)]
    rexY = Y[index - (size // 2):index + (size // 2 + size % 2)]
    return resX, rexY


def get_sun(Y, day=4):
    slideX = []
    slideY = []
    count = 0
    for index in Y:
        if count % day == 1:
            slideX.append(count)
            slideY.append(index)
        count += 1
    return slideX, slideY


if __name__ == '__main__':
    X, Y = set_data(size='100', interval='1h', year="22", month='07', day='29')

    window_size = 3

    slideX, slideY = find_localminmax(X, Y, window_size)

    print(slideX)
    print(slideY)

    plt.plot(X, Y, "-")
    plt.plot(slideX, slideY, label='sun')

    pl.show()
