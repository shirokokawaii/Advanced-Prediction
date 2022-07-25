import datetime

import numpy as np


def get_time_from_file(filename='hist_data1', format=''):
    data = np.load("../data/" + filename + ".npy")
    date = data[:, 0]
    datelist = []
    for time in date:
        time = datetime.datetime.fromtimestamp(time / 1000)
        if format != '':
            time = time.strftime(format)
        datelist.append(time)
    print(datelist)
    return datelist


def get_timepoint(filename, point, format='%Y-%m-%d %H:%M:%S'):
    data = np.load("../data/" + filename + ".npy")
    date = data[:, 0]
    if point >= len(date):
        print("Out of range")
        point = len(date)-1
    point = date[point]
    time = datetime.datetime.fromtimestamp(point / 1000)
    time = time.strftime(format)
    print(time)
    return time
