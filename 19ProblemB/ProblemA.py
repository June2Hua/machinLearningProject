import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import math
#紧急医疗包  医疗包，存放在无人机中的，长度单位为英寸
MED1_weight = 2  #2磅
MED2_weight = 2  #2磅
MED3_weight = 3  #3磅

#分别代表医疗包的长宽高
MED_dim = np.array([[14, 7, 5],
                   [5, 8, 5],
                   [12, 7, 4]])
#分别代表长宽高
drone_dim = np.array([[45, 45, 25],
                     [30, 30, 22],
                     [60, 50, 30],
                     [25, 20, 25],
                     [25, 20, 27],
                     [40, 40, 25],
                     [32, 32, 17]])

#ISO容器尺寸，单位为英尺
ISO_container = np.array([19*12+3, 7*12+8, 7*12+10])

#无人机速度,单位km每小时
drone_v = np.array([40, 79, 64, 60, 60, 79, 64])

#无人机飞行时间
drone_time = np.array([35, 40, 35, 18, 15, 24, 16])/60

#无人机的装载盒子
drone_top_cargo = np.array([[8, 10, 14], [24, 20, 20]])
drone_top_cargo1 = 8*10*14*1.0
drone_top_cargo2 = 24*20*20*1.0

#无人机的有效负载能力
Payload_Capability = np.array([3.5, 8, 14, 11, 15, 22, 20])

#计算
N_drone = np.floor((ISO_container/drone_dim))[:, 0] * np.floor((ISO_container/drone_dim))[:, 1] * np.floor((ISO_container/drone_dim))[:, 2]
# print("",N_drone)
W_max = Payload_Capability
# print("负载能力", W_max)
D_max = drone_v * drone_time
# print("负载能力", W_max)
# print("续航能力", D_max)

#计算体积
volume = drone_dim[:, 0]*drone_dim[:, 1]*drone_dim[:, 2]
type = np.array([1, 1, 2, 1, 2, 2, 2])   #*******
M = np.arange(7) * 1.0
for i in range(7):
    if(type[i] == 1):
        M[i] = drone_top_cargo1 / volume[i]
    else:
        M[i] = drone_top_cargo2 / volume[i]

#权重r1,r2,r3
r1 = 2
r2 = 2
r3 = 1
print("续航能力", D_max)
W_max = (W_max - np.min(W_max)) / (np.max(W_max) - np.min(W_max))
D_max = (D_max - np.min(D_max)) / (np.max(D_max) - np.min(D_max))
M = (M - np.min(M)) / (np.max(M) - np.min(M))
print("负载能力", W_max)
print("续航能力", D_max)
print("利用率", M)
maxReturn = r1*W_max + r2*D_max + r3*M
print("权重2：2；1", maxReturn)


#计算第二部分
# n = np.floor(ISO_container_W / MED_dim[:, 1])*np.floor(ISO_container_L / MED_dim[:, 0])*


