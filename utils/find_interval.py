import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from scipy import optimize
from utils.get_data import set_data, set_from_file
from utils.wave_fit import find_all, convert2line, find_localminmax


def split_interval(extX, extY, float_range):
    interval_set = []
    point_set = []
    for i in range(len(extX)):
        point_set.append([extX[i], extY[i]])
    # print(point_set)
    interval_tmpX = []
    interval_tmpY = []

    def cal_scale(i):
        scale = abs(point_set[i][1] - point_set[i + 1][1])
        scale_next = abs(point_set[i + 2][1] - point_set[i + 3][1])
        scale_h = abs(point_set[i + 1][1] - point_set[i + 2][1])
        scale_h_next = abs(point_set[i + 3][1] - point_set[i + 4][1])
        return scale, scale_next, scale_h, scale_h_next

    for i in range(len(point_set) - 4):
        scale, scale_next, scale_h, scale_h_next = cal_scale(i)
        # print(scale,scale_next,scale_h,scale_h_next)
        if (scale_next > (1 - float_range) * scale) & (scale_next < (1 + float_range) * scale):
            if (scale_h_next > (1 - float_range) * scale_h) & (scale_h_next < (1 + float_range) * scale_h):
                if len(interval_tmpX) == 0:
                    interval_tmpX.extend([point_set[i][0], point_set[i + 1][0], point_set[i + 2][0],
                                          point_set[i + 3][0], point_set[i + 4][0]])
                    interval_tmpY.extend([point_set[i][1], point_set[i + 1][1], point_set[i + 2][1],
                                          point_set[i + 3][1], point_set[i + 4][1]])
                else:
                    interval_tmpX.append(point_set[i + 4][0])
                    interval_tmpY.append(point_set[i + 4][1])
        else:
            if len(interval_tmpX) != 0:
                interval_set.append([interval_tmpX, interval_tmpY])
                interval_tmpX = []
                interval_tmpY = []

    if len(interval_tmpX) != 0:
        interval_set.append([interval_tmpX, interval_tmpY])
    interval_set = merge(interval_set)
    print(interval_set)
    return interval_set


def bisect(interval_set):
    max_set = []
    min_set = []
    for i in range(len(interval_set)):
        if interval_set[i][1][0] < interval_set[i][1][1]:
            off_set = 1
        else:
            off_set = 0
        max_setT = []
        min_setT = []
        for j in range(len(interval_set[i][0])):
            if j % 2 == off_set:
                max_setT.append([interval_set[i][0][j], interval_set[i][1][j]])
                # print(interval_set[i][0][j])
            else:
                min_setT.append([interval_set[i][0][j], interval_set[i][1][j]])
        max_set.append(max_setT)
        min_set.append(min_setT)
    # print(max_set)
    return max_set, min_set


def merge(sets):
    i = 0
    while i < len(sets) - 1:
        l = np.size(sets[i][0])
        for k in range(1, 3):
            if sets[i][0][l - k] == sets[i + 1][0][0]:
                for j in range(k, len(sets[i + 1][0])):
                    sets[i][0].append(sets[i + 1][0][j])
                    sets[i][1].append(sets[i + 1][1][j])
                sets.pop(i + 1)
            continue
        # elif sets[i][0][l-1] == sets[i+1][0][0]:
        #     for j in range(1, len(sets[i + 1][0])):
        #         sets[i][0].append(sets[i + 1][0][j])
        #         sets[i][1].append(sets[i + 1][1][j])
        #     sets.pop(i+1)
        i += 1
    return sets


def get_points(points):
    x = []
    y = []
    for i in range(len(points)):
        x.append(points[i][0])
        y.append(points[i][1])
    return x, y


def fit_line(set):
    k = []
    b = []
    for i in range(len(set)):
        points = set[i]
        points = np.array(points)
        x, y = get_points(points)
        k1, b1 = optimize.curve_fit(f_1, x, y)[0]
        k.append(k1)
        b.append(b1)

    return k, b


# def line_conf(k, b):
#     def line(x):
#         return k * x + b
#
#     return line

def f_1(x, A, B):
    return A * x + B


def line(k, b, x):
    return k * x + b


if __name__ == '__main__':
    size = 300
    appro_size = 3
    interval = '1d'
    year = '22'
    month = '07'
    day = '29'
    DIR = "../data/"
    filename = f"20{year}-{month}-{day}_{size}_{interval}"

    tmp_size = 130
    X, Y = set_from_file(DIR, filename, tmp_size)
    # X, Y = set_data(get=True, size=size, interval=interval, year=year, month=month, day=day)

    data = pd.read_csv(f'../data/csv/20{year}-{month}-{day}_{size}_{interval}.csv', index_col=0, parse_dates=True)
    data.index.name = 'Date'
    data = data.iloc[-tmp_size:]

    # --draw one solution
    extX, extY = find_localminmax(X, Y, size=appro_size, offset=0)

    # find value range
    float_range = 0.7
    setMax, setMin = bisect(split_interval(extX, extY, float_range))
    k1, b1 = fit_line(setMax)
    k2, b2 = fit_line(setMin)

    plt.plot(X, Y[0, :], "-")
    plt.plot(extX, extY, "-o")

    apds = [mpf.make_addplot(convert2line(extX, extY, X))]
    for i in range(len(setMax)):
        plt.plot([setMax[i][0][0], setMax[i][-1][0]],
                 [line(k1[i], b1[i], setMax[i][0][0]), line(k1[i], b1[i], setMax[i][-1][0])], "-")
        plt.plot([setMin[i][0][0], setMin[i][-1][0]],
                 [line(k2[i], b2[i], setMin[i][0][0]), line(k2[i], b2[i], setMin[i][-1][0])], "-")
        apds.append(mpf.make_addplot(convert2line([setMax[i][0][0], setMax[i][-1][0]],
                                                  [line(k1[i], b1[i], setMax[i][0][0]),
                                                   line(k1[i], b1[i], setMax[i][-1][0])], X, True)))
        apds.append(mpf.make_addplot(convert2line([setMin[i][0][0], setMin[i][-1][0]],
                                                  [line(k2[i], b2[i], setMin[i][0][0]),
                                                   line(k2[i], b2[i], setMin[i][-1][0])], X, True)))

    plt.show()
    mpf.plot(data, type='candle', volume=True, addplot=apds)
