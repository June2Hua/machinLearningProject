import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import math
#紧急医疗包  医疗包，存放在无人机中的，长度单位为英寸
MED1_weight = 2  #2磅
MED2_weight = 2  #2磅
MED3_weight = 3  #3磅
MED1_L = 14
MED2_L = 5
MED3_L = 12
MED1_W = 7
MED2_W = 8
MED3_W = 7
MED1_H = 5
MED2_H = 5
MED3_H = 4
#无人机运输集装箱尺寸，长度单位为英寸
drone_A_L = 45
drone_A_W = 45
drone_A_H = 25

drone_B_L = 30
drone_B_W = 30
drone_B_H = 22

drone_C_L = 60
drone_C_W = 50
drone_C_H = 30

drone_D_L = 25
drone_D_W = 20
drone_D_H = 25

drone_E_L = 25
drone_E_W = 20
drone_E_H = 27

drone_F_L = 40
drone_F_W = 40
drone_F_H = 25

drone_G_L = 32
drone_G_W = 32
drone_G_H = 17

drone_H_L = 65
drone_H_W = 75
drone_H_H = 41
drone_dim = np.array([[45, 45, 25],
                     [30, 30, 22],
                     [60, 50, 30],
                     [25, 20, 25],
                     [25, 20, 27],
                     [40, 40, 25],
                     [32, 32, 17]])

#ISO容器尺寸，单位为英尺
ISO_container_L = 19*12+3
ISO_container_W = 7*12+8
ISO_container_H = 7*12+10
ISO_container = np.array([19*12+3, 7*12+8, 7*12+10])

#无人机速度,单位km每小时
drone_A_v = 40
drone_B_v = 79
drone_C_v = 64
drone_D_v = 60
drone_E_v = 60
drone_F_v = 79
drone_G_v = 64
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
# print(N_drone)
W_max = N_drone * Payload_Capability
# print(W_max)
D_max = drone_v * drone_time
# print(D_max)

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
r1 = 0.2
r2 = 0.5
r3 = 0.3
maxReturn = r1*W_max + r2*D_max + r3*M
print(maxReturn)