import pandas as pd
import mplfinance as mpf

from utils.get_data import set_data, set_from_file
from utils.wave_fit import find_all, convert2line, find_localminmax

if __name__ == '__main__':
    size = 100
    appro_size = 3
    interval = '1d'
    year = '21'
    month = '05'
    day = '26'
    DIR = "../data/"
    filename = f"20{year}-{month}-{day}_{size}_{interval}"

    X, Y = set_from_file(DIR, filename, 10)
    # X, Y = set_data(get=False, size=size, interval=interval, year=year, month=month, day=day)
    # data = pd.read_csv(f'../data/csv/20{year}-{month}-{day}_{size}_{interval}.csv', index_col=0, parse_dates=True)
    # data.index.name = 'Date'
    #
    # --draw one solution
    extX, extY = find_localminmax(X, Y, size=appro_size, offset=2)
    # apd = mpf.make_addplot(convert2line(extX, extY, X))
    # mpf.plot(data, type='candle', volume=True, addplot=apd)

    # --draw all possible solution
    # extX, extY = find_all(X, Y, appro_size)
    # for i in range(len(extX)):
    #     print(len(convert2line(extX[i], extY[i], X)))
    #     apd = mpf.make_addplot(convert2line(extX[i], extY[i], X))
    #     mpf.plot(data, type='candle', volume=True, addplot=apd)

    print(extX)
    print(extY)

    for i in zip(extX, extY):
        arraydata = [extX, extY]

    print(arraydata)
    # extX = np.array([extX, extY])
    # extX = extX.reshape(-1, 2)
    # print(extX)

    # plt.plot(X, Y[0, :], "-")
    # plt.plot(extX, extY, "-o")
    # plt.show()

    # plt.plot(np.arange(0, 542), convert2line(extX[0], extY[0], X), "-")
    # plt.plot(extX[0], extY[0], "-o")
    # plt.show()
