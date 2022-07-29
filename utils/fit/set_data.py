import numpy as np


def set_data(size="2000", interval="1d", year="18", month='07', day='28'):
    DIR = "../../data/"
    filename = f"20{year}-{month}-{day}_{size}_{interval}.npy"

    data = np.load(DIR + filename)
    v = data[:, 5]
    close = data[:, 3]
    X = np.arange(0, close.size)
    # X = data[:, 0]
    Y = close
    return X, Y
