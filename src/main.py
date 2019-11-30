import numpy as np
import pandas as pd
from src.algorithm import *

# 文件的名字
FILENAME = "../data.xlsx"
# 禁用科学计数法
pd.set_option('float_format', lambda x: '%.3f' % x)
np.set_printoptions(suppress=True, threshold=np.nan)
# 得到的DataFrame分别为总价、面积、房间、客厅、年份
data = pd.read_excel(FILENAME, header=0, usecols="A,D,H,I,J")
# DataFrame转化为array
DataArray = data.values
Y=DataArray[:,0]
X=DataArray[:,1:4]
print(Y)
print(X)

