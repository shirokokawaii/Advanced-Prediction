import datetime
import time

# import numpy as np
# # 导入数组工具
# import numpy as np
# # 导入数据集生成器
# from sklearn.datasets import make_blobs
# # 导入KNN 分类器
# from sklearn.neighbors import KNeighborsClassifier
# import joblib
# # 生成样本数为200，分类数为2的数据集
# data=make_blobs(n_samples=200, n_features=2,centers=2, cluster_std=1.0, random_state=8)
# X,Y=data
# print(X)
# print(Y)
# clf = KNeighborsClassifier()
# clf.fit(X,Y)
# res = clf.predict([[6.75,9.82]])
# print(res)
# joblib.dump(clf,'model/rfc.pkl')
# #读取模型
# clf_new = joblib.load('model/rfc.pkl')
# res = clf_new.predict([[6.75,9.82]])
data = [1,2,3,4]
print(data[1:])

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(1659513600)))