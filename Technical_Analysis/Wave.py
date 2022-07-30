from wave_fit import *

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