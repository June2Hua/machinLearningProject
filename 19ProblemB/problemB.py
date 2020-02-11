import numpy as np
import random
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt

def isTrue(x):
    d = 17.07
    D = 31.60
    position = np.array([[18.44, -66.07],
                         [18.40, -66.16],
                         [18.22, -66.03],
                         [18.33, -65.65],
                         [18.47, -66.73]])
    # if (x[0]-position[0][0])**2 + (x[1]-position[0][1])**2 > d:
    if haversine(x[0], x[1], position[0][0], position[0][1]) > d:
        return False

    # if (x[0]-position[1][0])**2 + (x[1]-position[1][1])**2 > d:
    if haversine(x[0], x[1], position[1][0], position[1][1]) > d:
        return False

    # if (x[0]-position[2][0])**2 + (x[1]-position[2][1])**2 > d:
    if haversine(x[0], x[1], position[2][0], position[2][1]) > d:
        return False

    # if (x[2]-position[2][0])**2 + (x[3]-position[2][1])**2 > D:
    if haversine(x[2], x[3], position[2][0], position[2][1]) > D:
        return False

    # if (x[2]-position[3][0]) ** 2 + (x[3]-position[3][1]) ** 2 > d:
    if haversine(x[2], x[3], position[3][0], position[3][1]) > d:
        return False

    # if (x[4]-position[4][0])**2 + (x[5]-position[4][1])**2 > D:
    if haversine(x[4], x[5], position[4][0], position[4][1]) > D:
        return False

    # if (x[4]-position[1][0])**2 + (x[5]-position[1][1])**2 > D:
    if haversine(x[4], x[5], position[1][0], position[1][1]) > D:
        return False

    return True

def haversine(lat1, lon1, lat2, lon2):

    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r


#粒子群算法
class PSO():
    # PSO's parameters
    # pN:num of particle    dim:dimension   total:the total of iteration
    def __init__(self, pN, dim, total):
        self.w = 0.8    #weight
        self.maxW = 0.8
        self.minW = 0.2
        self.c1 = 1.2     #positive constants c1
        self.c2 = 1.2     #positive constants c2
        self.r1 = 0.3   #random r1
        self.r2 = 0.3   #random r2
        self.pN = pN    # num of particle
        self.dim = dim  # dimension
        self.total = total  # the total of iteration
        self.X = np.zeros((self.pN, self.dim))  # vector of particle's position
        self.V = np.zeros((self.pN, self.dim))  # vector of particle's velocity
        self.pbest = np.zeros((self.pN, self.dim))  # the best particle position
        self.gbest = np.zeros((1, self.dim))        # the best group position
        self.p_fit = np.zeros(self.pN)
        self.fit = 0  # fitness
        self.scope = 0.2

    # target function
    def function(self, X):
        # return (X[0]-X[2]) ** 2 + (X[0]-X[4]) ** 2 +(X[1]-X[3]) ** 2 + (X[1]-X[5]) ** 2
        return haversine(X[0], X[1], X[2], X[3]) + haversine(X[0], X[1], X[4], X[5]);

    # initialize the particle's position and velocity
    def init_Population(self):
        for i in range(self.pN):        # initialize i particle
            # for j in range(self.dim):   # initialize every dim
                # position
                # if j%2 == 0:
                #     self.X[i][j] = random.uniform(0, 1)*0.25 + 18.22
                # else:
                #     self.X[i][j] = random.uniform(0, 1)*(-1.08) - 65.65

            self.X[i][0] = random.uniform(0, 1)*self.scope + 18.34
            self.X[i][1] = random.uniform(0, 1)*(-self.scope) - 66.06

            self.X[i][2] = random.uniform(0, 1) * self.scope + 18.28
            self.X[i][3] = random.uniform(0, 1) * (-self.scope) - 65.75

            self.X[i][4] = random.uniform(0, 1) * self.scope + 18.415
            self.X[i][5] = random.uniform(0, 1) * (-self.scope) - 66.417

            self.V[i][:] = random.uniform(0, 1)*0.0001    #velocity
            while not isTrue(self.X[i]):
                self.X[i][0] = random.uniform(0, 1) * self.scope + 18.34
                self.X[i][1] = random.uniform(0, 1) * (-self.scope) - 66.06

                self.X[i][2] = random.uniform(0, 1) * self.scope + 18.28
                self.X[i][3] = random.uniform(0, 1) * (-self.scope) - 65.75

                self.X[i][4] = random.uniform(0, 1) * self.scope + 18.415
                self.X[i][5] = random.uniform(0, 1) * (-self.scope) - 66.417
            self.pbest[i] = self.X[i]  # each particle's best position
            tmp = self.function(self.X[i])  # obtain the present best
            self.p_fit[i] = tmp     #initialize the present best
           # update the gobal best
            if tmp > self.fit:
                self.fit = tmp
                self.gbest = self.X[i]

    # update position
    def iterator(self):
        fitness = np.zeros([self.total,1])
        for t in range(self.total):
            for i in range(self.pN):    # update pbest and gbest
                temp = self.function(self.X[i])
                if temp > self.p_fit[i]:  # update pbest
                    self.p_fit[i] = temp
                    self.pbest[i] = self.X[i]
                    if self.p_fit[i] > self.fit:  # update gbest
                        self.gbest = self.X[i]
                        self.fit = self.p_fit[i]
            for i in range(self.pN):    #update position and velocity
                self.w = self.maxW - (self.maxW - self.minW)*(t / self.total)
                self.V[i] = self.w * self.V[i] + self.c1 * self.r1 * (self.pbest[i] - self.X[i]) + \
                            self.c2 * self.r2 * (self.gbest - self.X[i])
                self.X[i] = self.X[i] + self.V[i]
                while not isTrue(self.X[i]):
                    self.X[i][0] = random.uniform(0, 1) * self.scope + 18.34
                    self.X[i][1] = random.uniform(0, 1) * (-self.scope) - 66.06

                    self.X[i][2] = random.uniform(0, 1) * self.scope + 18.28
                    self.X[i][3] = random.uniform(0, 1) * (-self.scope) - 65.75

                    self.X[i][4] = random.uniform(0, 1) * self.scope + 18.415
                    self.X[i][5] = random.uniform(0, 1) * (-self.scope) - 66.417
            fitness[t]=self.fit #save the data
            print(self.fit)
        return fitness



# initialize the target
# print(haversine(18.47, -66.73, 18.40, -66.16))

position = np.array([[18.44, -66.07],
                     [18.40, -66.16],
                     [18.22, -66.03],
                     [18.33, -65.65],
                     [18.47, -66.73]])
total = 100
my_pso = PSO(pN=30, dim=6, total=total)
# initialize the particle's position and velocity
my_pso.init_Population()
fitness = my_pso.iterator()
print(my_pso.gbest)
# show
plt.figure(1)
plt.title("PSO")
plt.xlabel("iterators")
plt.ylabel("fitness")
t = np.array([t for t in range(0, total)])
#fitness = np.array(fitness)
plt.plot(t, fitness, color='b', linewidth=3)
print(t.shape)
print(fitness.shape)
plt.show()
#18.47 -66.73
#18.40 -66.16

