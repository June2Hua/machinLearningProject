import numpy as np
import random
import matplotlib.pyplot as plt

class PSO():
    # PSO's parameters
    # pN:num of particle    dim:dimension   total:the total of iteration
    def __init__(self, pN, dim, total):
        self.w = 0.8    #weight
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
        self.fit = 1e10  # fitness

    # target function
    def function(self, X):
        return X ** 4 - 2 * X + 3

    # initialize the particle's position and velocity
    def init_Population(self):
        for i in range(self.pN):        # initialize i particle
            for j in range(self.dim):   # initialize every dim
                self.X[i][j] = random.uniform(0, 1)     #position
                self.V[i][j] = random.uniform(0, 1)     #velocity
            self.pbest[i] = self.X[i]  # each particle's best position
            tmp = self.function(self.X[i])  # obtain the present best
            self.p_fit[i] = tmp     #initialize the present best
           # update the gobal best
            if tmp < self.fit:
                self.fit = tmp
                self.gbest = self.X[i]

    # update position
    def iterator(self):
        fitness = np.zeros([self.total,1])
        for t in range(self.total):
            for i in range(self.pN):    # update pbest and gbest
                temp = self.function(self.X[i])
                if temp < self.p_fit[i]:  # update pbest
                    self.p_fit[i] = temp
                    self.pbest[i] = self.X[i]
                    if self.p_fit[i] < self.fit:  # update gbest
                        self.gbest = self.X[i]
                        self.fit = self.p_fit[i]
            for i in range(self.pN):    #update position and velocity
                self.V[i] = self.w * self.V[i] + self.c1 * self.r1 * (self.pbest[i] - self.X[i]) + \
                            self.c2 * self.r2 * (self.gbest - self.X[i])
                self.X[i] = self.X[i] + self.V[i]
            fitness[t]=self.fit #save the data
            print(self.fit)
        return fitness

# initialize the target
total = 100
my_pso = PSO(pN=30, dim=1, total=total)
# initialize the particle's position and velocity
my_pso.init_Population()
fitness = my_pso.iterator()
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
