# 导入数组工具
import numpy as np
# 导入数据集生成器
from sklearn.datasets import make_blobs
# 导入KNN 分类器
from sklearn.neighbors import KNeighborsClassifier
# 生成样本数为200，分类数为2的数据集
data=make_blobs(n_samples=200, n_features=2,centers=2, cluster_std=1.0, random_state=8)
X,Y=data
clf = KNeighborsClassifier()
clf.fit(X,Y)
res = clf.predict([[6.75,9.82]])
print(res)