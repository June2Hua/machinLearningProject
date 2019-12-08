import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# 文件的名字
FILENAME = "../data.xlsx"
# 禁用科学计数法
pd.set_option('float_format', lambda x: '%.3f' % x)
np.set_printoptions(suppress=True, threshold=np.nan)
# 得到的DataFrame分别为总价、面积、房间、客厅、年份
data = pd.read_excel(FILENAME, header=0, usecols="A,D,H,I,J")
# DataFrame转化为array
DataArray = data.values
Y = DataArray[:, 0]
X = DataArray[:, 1:5]
X = np.array(X)#转化为array,自变量
Y = np.array(Y)#转化为array，因变量房价
oneVector = np.ones(np.size(X, 0)).reshape(np.size(X, 0), 1)#全1矩阵x
X = np.concatenate((oneVector, X), axis=1)#矩阵拼接
firstResult = np.dot(np.transpose(X),X)#矩阵X的转置和矩阵X点乘
secondResult = np.dot(np.linalg.inv(firstResult), np.transpose(X))#（矩阵X的转置和矩阵X点乘结果）和(矩阵X的转置)的点乘结果
Theta = np.dot(secondResult, Y)#得出的各个参数
print(Theta)
# 标题显示中文
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
#计算预测值
Y_pre = np.sum(Theta*X,axis=1)
#画图
plt.plot(np.arange(380), Y,"r^")
plt.plot(np.arange(380),Y_pre,"bs")
plt.title("红色为真实值，蓝色为预测值")
plt.show()