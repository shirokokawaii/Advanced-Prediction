import numpy as np
import pylab as pl
from matplotlib import pyplot as plt
from scipy import optimize


# def find_localminmax(window):
from utils.get_data import set_data


def segments_fit(X, Y, count):
    xmin = X.min()
    xmax = X.max()

    seg = np.full(count - 1, (xmax - xmin) / count)

    px_init = np.r_[np.r_[xmin, seg].cumsum(), xmax]
    py_init = np.array([Y[np.abs(X - x) < (xmax - xmin) * 0.01].mean() for x in px_init])

    def func(p):
        seg = p[:count - 1]
        py = p[count - 1:]
        px = np.r_[np.r_[xmin, seg].cumsum(), xmax]
        return px, py

    def err(p):
        px, py = func(p)
        Y2 = np.interp(X, px, py)
        return np.mean((Y - Y2) ** 2)

    r = optimize.minimize(err, x0=np.r_[seg, py_init], method='Nelder-Mead')
    return func(r.x)


if __name__ == '__main__':
    X, Y = set_data(size='200', interval='1d')

    sunX = []
    sunY = []
    wenX = []
    wenY = []
    count = 0
    for ind in Y:
        if count % 7 == 4:
            sunX.append(count)
            sunY.append(ind)
        if count % 7 == 1:
            wenX.append(count)
            wenY.append(ind)
        count+=1

    print(wenY)
    print(wenX)
    print(sunY)
    print(sunX)

    # px, py = segments_fit(X, Y, 21)

    plt.plot(X, Y, "-")
    # plt.plot(px, py, "-or")
    plt.plot(sunX, sunY, label='sun')
    plt.plot(wenX, wenX, label='wen')

    pl.show()
