import cv2
import numpy as np
from random import *
np.set_printoptions(suppress=True)

class Trend(object):
    def __init__(self, data, days):
        data = data[-days:,:]
        self.values = self.calculate_trend(data, days)
        # print('days=',days,': k=',self.values,sep = '')

    def calculate_trend(self,data, days):
        price = []
        xdata = []
        ydata = []

            # Save necessary data into array
        get_Highest_price = data[:,1]
        get_Lowest_price = data[:,2]
        # get_Average_price = (data[:,0]+data[:,3])/2
        get_price = (get_Highest_price + get_Lowest_price)/2

            # Change data into dot type
        count = 0
        for element in get_price:
            xdata.append(count)
            ydata.append(element)
            price.append([count,element])
            count += 1
        count -= 1
        price = np.array(price)
        # print(price)
        output = cv2.fitLine(price, cv2.DIST_L2, 0,  0.01, 0.01)

        k = output[1] / output[0]
        b = output[3] - k * output[2]
        # print(output)
            #draw the graph
        # import matplotlib.pyplot as plt
        # plt.title(days)
        # plt.xlabel('Days')
        # plt.ylabel('Price')
        # plt.plot(xdata, ydata)
        # plt.plot([0,output[2],count], [b,output[3],k*count+b])
        # plt.show()
        return k

class Predict(object):
    def __init__(self, data):
        w1 = 0.3
        w2 = 0.25
        w3 = 0.25
        w4 = 0.2
        k_5 = Trend(data, 5).values
        k_10 = Trend(data, 10).values
        k_20 = Trend(data, 20).values
        k_40 = Trend(data, 40).values
        k_average = k_5*w1 + k_10*w2 + k_20*w3 + k_40*w4
        self.values_K = k_average
        days_average = 5*w1 + 10*w2 + 20+w3 + 40*w4
        self.values_days = days_average
        # print('Average K=', k_average, sep = '')
        # print('Average days=', days_average, sep = '')

# Load data from file
# data = np.load('hist_data.npy')
# Predict(data)

data = np.load('data,180712-190722.npy')
correct_times = 0
total_times = 0
for i in range(10000):
    randomtime = randint(50,1748)
    data_tem = data[randomtime-45:randomtime,:]
    data_tem_next = data[randomtime:randomtime+20,:]
    predict_K = Predict(data_tem).values_K
    actual_K = Trend(data_tem_next, 30).values
    if(predict_K * actual_K > 0):
        correct_times += 1
    total_times += 1
    print(total_times)
print('The correct prediction possibility:', correct_times/total_times, sep = '')



