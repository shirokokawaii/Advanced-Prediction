import numpy as np
np.set_printoptions(suppress=True)

# predict_K = 10000
# actual_K = -1
# if((predict_K * actual_K) > 0):
#     print('ture')
# else:
#     print('false')
data = np.load('data/hist_data.npy')
print(data.shape)
print(data)