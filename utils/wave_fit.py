import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import mplfinance as mpf

from get_data import set_data


def find_localminmax(X, Y, size=4, offset=0):
    slideX, slideY = get_slice(Y[0, :], size, offset)
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
    extremumX, extremumY = final_fix(X, Y, extremumX, extremumY)
    return final_fix(X, Y, extremumX, extremumY)
    # return rec_delect(extremumX, extremumY)
    # return extremumX, extremumY


def rec_delect(extremumX, extremumY, count=0):
    if len(extremumX) <= 2:
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
    for index in range(0, len(extremumX)):
        # get both maxmin around the index
        if (index != 0) & (index != len(extremumX) - 1):
            tmpY = Y[1:3, extremumX[index - 1] + 1:extremumX[index + 1]]
            tmpX = X[extremumX[index - 1] + 1:extremumX[index + 1]]
        elif index == 0:
            tmpY = Y[1:3, :extremumX[index + 1]]
            tmpX = X[:extremumX[index + 1]]
        elif index == len(extremumX) - 1:
            tmpY = Y[1:3, extremumX[index - 1] + 1:]
            tmpX = X[extremumX[index - 1] + 1:]
        if index < len(extremumX) - 1:
            if extremumY[index + 1] > extremumY[index]:
                extremumY[index] = min(tmpY[1])
                tmp_list = tmpY[1].tolist()
                extremumX[index] = tmpX[tmp_list.index(min(tmpY[1]))]
            else:
                extremumY[index] = max(tmpY[0])
                tmp_list = tmpY[0].tolist()
                extremumX[index] = tmpX[tmp_list.index(max(tmpY[0]))]
        else:
            if extremumY[index - 1] > extremumY[index]:
                extremumY[index] = min(tmpY[1])
                tmp_list = tmpY[1].tolist()
                extremumX[index] = tmpX[tmp_list.index(min(tmpY[1]))]
            else:
                extremumY[index] = max(tmpY[0])
                tmp_list = tmpY[0].tolist()
                extremumX[index] = tmpX[tmp_list.index(max(tmpY[0]))]
    return extremumX, extremumY


def get_tmp(index, X, Y, size):
    resX = X[index - (size // 2):index + (size // 2 + size % 2)]
    rexY = Y[index - (size // 2):index + (size // 2 + size % 2)]
    return resX, rexY


def get_slice(Y, slice_size, offset=0):
    slideX = []
    slideY = []
    count = 0
    for index in Y:
        if count % slice_size == offset:
            slideX.append(count)
            slideY.append(index)
        count += 1
    return slideX, slideY


def convert2line(extX, extY, X, narray=False):
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
            if narray:
                val = float(val)
            result.append(round(val, 2))


def find_all(X, Y, appro_size):
    result_setX = []
    result_setY = []
    for offset in range(0, appro_size):
        # print(f"offset:{offset}")
        extX, extY = find_localminmax(X, Y, appro_size, offset)
        if len(result_setX) == 0:
            print(f"offset:{offset}")
            result_setX.append(extX)
            result_setY.append(extY)
            # print("branch1")
            # print(result_setX[0])
        else:
            # print("branch2")

            flag = False
            for i in range(len(result_setX)):
                result_setX[i] = np.array(result_setX[i])
                result_setY[i] = np.array(result_setY[i])
                extX = np.array(extX)
                extY = np.array(extY)
                # print(result_setX[i])
                # print(extX)
                # print((result_setX[i] == extX))
                # print((result_setX[i] == extX).all())
                if (len(result_setX[i]) != len(extX)):
                    continue
                if (result_setX[i] == extX).all():
                    flag = True
                    break
            if not flag:
                print(f"offset:{offset}")
                result_setX.append(extX)
                result_setY.append(extY)

    return result_setX, result_setY


if __name__ == '__main__':
    size = 2000
    appro_size = 5
    interval = '1h'
    year = '22'
    month = '08'
    day = '01'

    X, Y = set_data(get=False, size=size, interval=interval, year=year, month=month, day=day)

    data = pd.read_csv(f'../data/csv/20{year}-{month}-{day}_{size}_{interval}.csv', index_col=0, parse_dates=True)
    data.index.name = 'Date'

    # --draw one solution
    extX, extY = find_localminmax(X, Y, size=appro_size, offset=2)
    apd = mpf.make_addplot(convert2line(extX, extY, X))
    mpf.plot(data, type='candle', volume=True, addplot=apd)

    # --draw all possible solution
    # extX, extY = find_all(X, Y, appro_size)
    # for i in range(len(extX)):
    #     print(len(convert2line(extX[i], extY[i], X)))
    #     apd = mpf.make_addplot(convert2line(extX[i], extY[i], X))
    #     mpf.plot(data, type='candle', volume=True, addplot=apd)

    print(extX)
    print(extY)

    # extX = np.array([extX, extY])
    # extX = extX.reshape(-1, 2)
    # print(extX)

    # plt.plot(X, Y[0, :], "-")
    # plt.plot(extX, extY, "-o")
    # plt.show()

    # plt.plot(np.arange(0, 542), convert2line(extX[0], extY[0], X), "-")
    # plt.plot(extX[0], extY[0], "-o")
    # plt.show()
