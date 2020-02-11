import numpy as np
import random
import matplotlib.pyplot as plt


def isContinue(X):
    if np.sum(X[0:4] + X[10:14] + X[20:24]) > 24:
        return False
    if np.sum(X[5:9] + X[15:19] + X[25:29]) > 20:
        return False
    if np.sum(X[30:34] + X[40:44] + X[50:54]) > 24:
        return False
    if np.sum(X[35:39] + X[45:49] + X[55:59])> 20:
        return False
    if np.sum(X[60:64] + X[70:74] + X[80:84]) > 24:
        return False
    if np.sum(X[65:69] + X[75:79] + X[85:89]) > 20:
        return False
    return True

class PSO():
    # PSO's parameters
    # pN:num of particle    dim:dimension   total:the total of iteration
    def __init__(self, pN, dim, total, day):
        self.w = 1.2    #weight
        self.c1 = 0.5     #positive constants c1
        self.c2 = 0.5     #positive constants c2
        self.r1 = 0.5   #random r1
        self.r2 = 0.5   #random r2
        self.pN = pN    # num of particle
        self.dim = dim  # dimension
        self.total = total  # the total of iteration
        self.X = np.zeros((self.pN, self.dim))  # vector of particle's position
        self.V = np.zeros((self.pN, self.dim))  # vector of particle's velocity
        self.pbest = np.zeros((self.pN, self.dim))  # the best particle position
        self.gbest = np.zeros((1, self.dim))        # the best group position
        self.p_fit = np.zeros(self.pN)
        self.fit = 0  # fitness
        self.day = day

    def isContinue(self, X):
        if np.sum(X[0:4] + X[10:14] + X[20:24]) > 24:
            return False
        if np.sum(X[5:9] + X[15:19] + X[25:29]) > 20:
            return False
        if np.sum(X[30:34] + X[40:44] + X[50:54]) > 24:
            return False
        if np.sum(X[35:39] + X[45:49] + X[55:59]) > 20:
            return False
        if np.sum(X[60:64] + X[70:74] + X[80:84]) > 24:
            return False
        if np.sum(X[65:69] + X[75:79] + X[85:89]) > 20:
            return False
        if np.min(X) < 0:
            return False
        return True

    # target function
    def function(self, x):
        # d5 = x[0][4]*11 + x[0][9]*10
        self.day[4] = x[4]*11 + x[9]*10
        # d4 = min(x[2][3]*11 + x[2][8]*10, x[2][23]*7 + x[2][28]*6)
        self.day[3] = min(x[63]*11 + x[68]*10, x[83]*7 + x[88]*6)
        # d3 = min((x[2][2]*11 + x[1][2]*11 + x[1][7]*10)/2, x[2][22]*7 + x[1][22]*7 + x[1][27]*6)
        self.day[2] = min((x[26]*11 + x[32]*11 + x[37]*10)/2, x[82]*7 + x[52]*7 + x[57]*6)
        # d2 = min((x[0][1]*11 + x[1][1]*11 + x[1][6]*10)/2, x[0][11]*11 + x[1][11]*11 + x[1][16]*10, (x[0][21]*7 + x[1][21]*7 + x[1][26]*6)/2)
        # *********
        self.day[1] = min((x[1]*11 + x[6]*10 + x[31]*11 + x[36]*10)/2, x[11]*11 + x[16]*10 + x[41]*11 + x[46]*10, (x[21]*7 + x[26]*6 + x[51]*7 + x[56]*6)/2)
        # d1 = min(x[1][0]*11 + x[1][5]*10, x[1][10]*11 + x[1][15]*10)
        self.day[0] = min(x[30]*11 + x[35]*10, x[40]*11 + x[45]*10)
        return np.sum(self.day)
        # return X ** 4 - 2 * X + 3

    # initialize the particle's position and velocity
    def init_Population(self):
        for i in range(self.pN):        # initialize i particle
            # for j in range(self.dim):   # initialize every dim
                # self.X[i][j] = random.random(0, 1)     #position
                # for k in range(3):
                # self.X[i][j] =
                # self.V[i][j] = random.uniform(0, 1)     #velocity
            # for j in range(self.dim):
            #     self.X[i][j] = random.randint(0, 4)
            self.V[i][4] = 1
            self.V[i][9] = 1
            self.V[i][63] = 1
            self.V[i][68] = 1
            self.V[i][83] = 1

            self.V[i][88] = 1
            self.V[i][26] = 1
            self.V[i][32] = 1
            self.V[i][37] = 1
            self.V[i][82] = 1

            self.V[i][52] = 1
            self.V[i][57] = 1
            self.V[i][1] = 1
            self.V[i][31] = 1
            self.V[i][36] = 1

            self.V[i][11] = 1
            self.V[i][41] = 1
            self.V[i][21] = 1
            self.V[i][51] = 1
            self.V[i][56] = 1

            self.V[i][30] = 1
            self.V[i][56] = 1
            self.V[i][35] = 1
            self.V[i][40] = 1
            self.V[i][45] = 1
            # ******

            # # d5 = x[0][4]*11 + x[0][9]*10
            # self.day[4] = x[4] * 11 + x[9] * 10
            # # d4 = min(x[2][3]*11 + x[2][8]*10, x[2][23]*7 + x[2][28]*6)
            # self.day[3] = min(x[63] * 11 + x[68] * 10, x[83] * 7 + x[88] * 6)
            # # d3 = min((x[2][2]*11 + x[1][2]*11 + x[1][7]*10)/2, x[2][22]*7 + x[1][22]*7 + x[1][27]*6)
            # self.day[2] = min((x[26] * 11 + x[32] * 11 + x[37] * 10) / 2, x[82] * 7 + x[52] * 7 + x[57] * 6)
            # # d2 = min((x[0][1]*11 + x[1][1]*11 + x[1][6]*10)/2, x[0][11]*11 + x[1][11]*11 + x[1][16]*10, (x[0][21]*7 + x[1][21]*7 + x[1][26]*6)/2)
            # # *********
            # self.day[1] = min((x[1] * 11 + x[31] * 11 + x[36] * 10) / 2, x[11] * 11 + x[41] * 11 + x[46] * 10,
            #                   (x[21] * 7 + x[51] * 7 + x[56] * 6) / 2)
            # # d1 = min(x[1][0]*11 + x[1][5]*10, x[1][10]*11 + x[1][15]*10)
            # self.day[0] = min(x[30] * 11 + x[35] * 10, x[40] * 11 + x[45] * 10)

            self.X[i][4] = random.randint(2, 7)
            self.X[i][9] = random.randint(2, 7)
            self.X[i][63] = random.randint(2, 7)
            self.X[i][68] = random.randint(2, 7)
            self.X[i][83] = random.randint(2, 7)

            self.X[i][88] = random.randint(2, 7)
            self.X[i][26] = random.randint(2, 7)
            self.X[i][32] = random.randint(2, 7)
            self.X[i][37] = random.randint(2, 7)
            self.X[i][82] = random.randint(2, 7)

            self.X[i][52] = random.randint(2, 7)
            self.X[i][57] = random.randint(2, 7)
            self.X[i][1] = random.randint(2, 7)
            self.X[i][31] = random.randint(2, 7)
            self.X[i][36] = random.randint(2, 7)

            self.X[i][11] = random.randint(2, 7)
            self.X[i][41] = random.randint(2, 7)
            self.X[i][21] = random.randint(2, 7)
            self.X[i][51] = random.randint(2, 7)
            self.X[i][56] = random.randint(2, 7)

            self.X[i][30] = random.randint(2, 7)
            self.X[i][56] = random.randint(2, 7)
            self.X[i][35] = random.randint(2, 7)
            self.X[i][40] = random.randint(2, 7)
            self.X[i][45] = random.randint(2, 7)

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
                        # print(self.gbest)
                        self.fit = self.p_fit[i]
            for i in range(self.pN):    #update position and velocity
                # self.r1 = random.uniform(0,1)
                # self.r2 = random.uniform(0,1)
                self.V[i] = self.w * self.V[i] + self.c1 * self.r1 * (self.pbest[i] - self.X[i]) + \
                            self.c2 * self.r2 * (self.gbest - self.X[i])
                self.X[i] = np.floor(self.X[i] + self.V[i])
                # while not isContinue(self.X[i]):
                while not self.isContinue(self.X[i]):
                    self.X[i][4] = random.randint(2, 7)
                    self.X[i][9] = random.randint(2, 7)
                    self.X[i][63] = random.randint(2, 7)
                    self.X[i][68] = random.randint(2, 7)
                    self.X[i][83] = random.randint(2, 7)

                    self.X[i][88] = random.randint(2, 7)
                    self.X[i][26] = random.randint(2, 7)
                    self.X[i][32] = random.randint(2, 7)
                    self.X[i][37] = random.randint(2, 7)
                    self.X[i][82] = random.randint(2, 7)

                    self.X[i][52] = random.randint(2, 7)
                    self.X[i][57] = random.randint(2, 7)
                    self.X[i][1] = random.randint(2, 7)
                    self.X[i][31] = random.randint(2, 7)
                    self.X[i][36] = random.randint(2, 7)

                    self.X[i][11] = random.randint(2, 7)
                    self.X[i][41] = random.randint(2, 7)
                    self.X[i][21] = random.randint(2, 7)
                    self.X[i][51] = random.randint(2, 7)
                    self.X[i][56] = random.randint(2, 7)

                    self.X[i][30] = random.randint(2, 7)
                    self.X[i][56] = random.randint(2, 7)
                    self.X[i][35] = random.randint(2, 7)
                    self.X[i][40] = random.randint(2, 7)
                    self.X[i][45] = random.randint(2, 7)
            fitness[t]=self.fit #save the data
            print(self.fit)
            print(self.gbest)
        return fitness

# initialize the target
total = 100
day = np.array([0, 0, 0, 0, 0])
my_pso = PSO(pN=50, dim=90, total=total, day=day)
# print(my_pso.day)
# initialize the particle's position and velocity
my_pso.init_Population()
fitness = my_pso.iterator()
print(my_pso.day)
# print(my_pso.gbest)
# print(my_pso.X[])
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
