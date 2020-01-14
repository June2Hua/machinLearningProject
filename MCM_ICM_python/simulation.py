#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
from matplotlib.animation import HTMLWriter
import seaborn as sns

sns.set_style("whitegrid")
np.random.seed(1)

#用于判断概率
def func1(probability):
    if np.random.random() < probability:
        return 1
    else:
        return 0

A, B = 5, 12
situ = {'s':'A','l':'B'}
r = range(100) #迭代次数

#定义每次迭代的函数
def iteration(A,B):
    #门外人加入排队
    R1 = func1(0.63)
    A += R1
    R1 = func1(0.63)
    B += R1
    #队伍转移
    if max(A,B)>=3: #2人内不发生转移
        #队伍转移,目前只设置为转移一个
        C = func1(0.2)
        if A <= B:
            A += C
            B -= C
        else:
            A -= C
            B += C
    #办理
    R2 = func1(0.713)
    A -= R2
    if A < 0:
        situ['S'] = 0
    R2 = func1(0.713)
    B -= R2
    if B < 0:
        B = 0
    return A,B

l_A, l_B = [], []
for i in r:
    A, B = iteration(A, B)
    l_A.append(A)
    l_B.append(B)


fig, ax = plt.subplots(figsize=(14,6))
xdata_A, ydata_A = [], []
xdata_B, ydata_B = [], []
ln_A, = plt.plot([], [], 'ro')
ln_B, = plt.plot([], [], 'bo')

def init():
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 20)
    return ln_A,ln_B

def update(frame):
    xdata_A.append(frame)
    ydata_A.append(l_A[frame])
    ln_A.set_data(xdata_A, ydata_A)
    xdata_B.append(frame)
    ydata_B.append(l_B[frame])
    ln_B.set_data(xdata_B, ydata_B)
    return ln_A, ln_B

ani = FuncAnimation(fig, update, frames=range(100),
                    init_func=init, blit=True)
plt.legend([ln_A,ln_B],['A','B'],loc='upper right')
plt.show()

