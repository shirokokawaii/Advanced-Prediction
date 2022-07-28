import cv2
import numpy as np
import pandas as pd
from random import *
np.set_printoptions(suppress=True)

#time,high,low,open,volumefrom,volumeto,close

class Trend(object):
    def __init__(self, data, days):
        data = data.iloc[-days:,:]
        self.values = self.calculate_trend(data, days)
        # print('days=',days,': k=',self.values,sep = '')

    def calculate_trend(self,data, days):
        price = []
        xdata = []
        ydata = []

            # Save necessary data into array
        get_Highest_price = data.iloc[:,1]
        get_Lowest_price = data.iloc[:,2]
        # get_Average_price = (data[:,3]+data[:,6])/2
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
        w1 = 0.25
        w2 = 0.25
        w3 = 0.25
        w4 = 0.25
        k_1 = Trend(data, 6).values
        k_2 = Trend(data, 18).values
        k_3 = Trend(data, 25).values
        k_4 = Trend(data, 44).values
        k_average = k_1*w1 + k_2*w2 + k_3*w3 + k_4*w4
        self.values_K = k_average
        # days_average = 5*w1 + 10*w2 + 20+w3 + 40*w4
        # self.values_days = days_average
        # print('Average K=', k_average, sep = '')
        # print('Average days=', days_average, sep = '')


# Load data from file
# data = np.load('hist_data.npy')
# Predict(data)

# Test Code: reliability of 5,10,15 and 20 days prediction
data = pd.read_csv('data/2022-7_4000_1d.csv')
correct_times_1 = 0
correct_times_2 = 0
correct_times_3 = 0
correct_times_4 = 0

total_times = 10000
len = len(data) - 44

for i in range(total_times):
    randomtime = randint(44,len-20)
    data_tem = data.iloc[randomtime-44:randomtime,:]
    data_tem_next_1 = data.iloc[randomtime:randomtime+5,:]
    data_tem_next_2 = data.iloc[randomtime:randomtime+10,:]
    data_tem_next_3 = data.iloc[randomtime:randomtime+15,:]
    data_tem_next_4 = data.iloc[randomtime:randomtime+20,:]
    predict_K = Predict(data_tem).values_K
    actual_K_1 = Trend(data_tem_next_1, 5).values
    actual_K_2 = Trend(data_tem_next_2, 10).values
    actual_K_3 = Trend(data_tem_next_3, 15).values
    actual_K_4 = Trend(data_tem_next_4, 20).values

    if((predict_K * actual_K_1) >= 0):
        correct_times_1 += 1
    if((predict_K * actual_K_2) >= 0):
        correct_times_2 += 1
    if((predict_K * actual_K_3) >= 0):
        correct_times_3 += 1
    if((predict_K * actual_K_4) >= 0):
        correct_times_4 += 1
    if(i%1000==0):
        print(i)
print('The correct prediction possibility of 05 days:', correct_times_1/total_times, sep = '')
print('The correct prediction possibility of 10 days:', correct_times_2/total_times, sep = '')
print('The correct prediction possibility of 15 days:', correct_times_3/total_times, sep = '')
print('The correct prediction possibility of 20 days:', correct_times_4/total_times, sep = '')