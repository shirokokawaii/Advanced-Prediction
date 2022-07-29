import numpy as np


def set_data(size="2000", interval="1d", year="18"):
    DIR = "../../data/"
    filename = f"20{year}-8_{size}_{interval}.npy"

    data = np.load(DIR + filename)
    data = data[:, 3]
    X = np.arange(0, data.size)
    # X = data[:, 0]
    Y = data
    return X, Y
