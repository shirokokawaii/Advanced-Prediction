import datetime
import cv2
import mplfinance as mpf
import numpy as np
from get import get_data
from get_data import convert2csv

if(__name__ == '__main__'):
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=50)
    interval = '1d' #1h, 4h, 1d
    data_raw = get_data(start, end, interval)
    points = []
    for i in (1,2,3,6):
        count = 0
        for element in data_raw[i]:
            points.append([count, element])
            count += 1
    points = np.array(points, dtype=np.float32)
    minRect = cv2.minAreaRect(points)
    print(minRect)
    # mpf.plot(convert2csv(data_raw), type='candle', volume=True, addplot = add_plot)

