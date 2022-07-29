from random import randint

import numpy as np
from bayes_opt import BayesianOptimization

from utils.predict import Predict, Trend


def valid(w1, w2, w3, w4, r1, r2, r3, r4):
    r1 = int(r1)
    r2 = int(r2)
    r3 = int(r3)
    r4 = int(r4)
    data = np.load('../data/2022-8_2000_1h.npy')
    total_times = 4000
    correct_times_1 = 0
    correct_times_2 = 0
    correct_times_3 = 0
    correct_times_4 = 0
    length = len(data)
    for i in range(total_times):
        randomtime = randint(r4, length - 20)
        data_tem = data[randomtime - r4:randomtime]
        data_tem_next_1 = data[randomtime:randomtime + 5]
        data_tem_next_2 = data[randomtime:randomtime + 10]
        data_tem_next_3 = data[randomtime:randomtime + 15]
        data_tem_next_4 = data[randomtime:randomtime + 20]
        predict_K = Predict(data_tem, w1, w2, w3, w4, r1, r2, r3, r4).values_K
        actual_K_1 = Trend(data_tem_next_1, 5).values
        actual_K_2 = Trend(data_tem_next_2, 10).values
        actual_K_3 = Trend(data_tem_next_3, 15).values
        actual_K_4 = Trend(data_tem_next_4, 20).values
        if (predict_K * actual_K_1) > 0:
            correct_times_1 += 1
        if (predict_K * actual_K_2) > 0:
            correct_times_2 += 1
        if (predict_K * actual_K_3) > 0:
            correct_times_3 += 1
        if (predict_K * actual_K_4) > 0:
            correct_times_4 += 1
    return (correct_times_1 + correct_times_2 + correct_times_3 + correct_times_4) / (4 * total_times)


if __name__ == "__main__":
    bo = BayesianOptimization(
        valid,
        {'w1': (0, 1),
         'w2': (0, 1),
         'w3': (0, 1),
         'w4': (0, 1),
         'r1': (1, 10),
         'r2': (3, 20),
         'r3': (10, 40),
         'r4': (20, 50), }
    )

    bo = BayesianOptimization(
        valid,
        {'w1': [0],
         'w2': [0],
         'w3': [0],
         'w4': (0, 1),
         'r1': (1, 10),
         'r2': (3, 20),
         'r3': (10, 40),
         'r4': (20, 50), }
    )

    bo.maximize()
