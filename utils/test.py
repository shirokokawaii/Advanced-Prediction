import numpy as np
import pandas as pd

from utils.get_data import get_data

DIR="../data/"


end = "2015-07-05 20:00:00"
time_interval = '1d'
data_size = 10
filename = "2015-7_"+str(data_size)+"_"+time_interval

hist = get_data(time_interval, data_size, end, filename)

print(hist.head(5))
print(hist.size)
hist = pd.read_csv(DIR+filename+".csv")
target_col = 'close'
print(hist[target_col])


