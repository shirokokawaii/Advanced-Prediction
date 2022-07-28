import numpy as np
import pwlf
from GPyOpt.methods import BayesianOptimization  # initialize piecewise linear fit with your x and y data
from matplotlib import pyplot as plt

data = np.load("../../data/hist_data.npy")
data = data[:, 1]
x = np.arange(0, data.size)
y = data

my_pwlf = pwlf.PiecewiseLinFit(x, y)

# fit the data for four line segments
# this performs 3 multi-start optimizations
res = my_pwlf.fitfast(4, pop=5)

# predict for the determined points
xHat = np.linspace(min(x), max(x), num=10000)
yHat = my_pwlf.predict(xHat)

# plot the results
plt.figure()
plt.plot(x, y, label='origin')
plt.plot(xHat, yHat, '-')
plt.show()