import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize


def innerdef():
    var2 = "6asdsa"
    def pr():
        print(var2)

    pr()


def f_1(x, A, B):
    return A*x + B


def leastSquare(x, y):
    if len(x) == 2:
        # 此时x为自然序列
        sx = 0.5 * (x[1] - x[0] + 1) * (x[1] + x[0])
        ex = sx / (x[1] - x[0] + 1)
        sx2 = ((x[1] * (x[1] + 1) * (2 * x[1] + 1))
               - (x[0] * (x[0] - 1) * (2 * x[0] - 1))) / 6
        x = np.array(range(int(x[0]), int(x[1] + 1)))
    else:
        sx = sum(x)
        ex = sx / len(x)
        sx2 = sum(x ** 2)

    sxy = sum(x * y)
    ey = np.mean(y)

    a = (sxy - ey * sx) / (sx2 - ex * sx)
    b = (ey * sx2 - sxy * ex) / (sx2 - ex * sx)
    return a, b


if __name__ == '__main__':
    innerdef()

    plt.figure()

    # 拟合点
    x0 = [1, 2, 3, 4, 5]
    y0 = [1, 3, 8, 18, 36]

    # 绘制散点
    plt.scatter(x0[:], y0[:], 25, "red")

    # 直线拟合与绘制
    A1, B1 = optimize.curve_fit(f_1, x0, y0)[0]
    print(A1, B1)
    x1 = np.arange(0, 6, 0.01)
    y1 = A1 * x1 + B1
    plt.plot(x1, y1, "blue")
    plt.show()


