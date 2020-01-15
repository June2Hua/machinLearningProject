lambda_A = 47 / (9 * 60 + 56) / 5
print(lambda_A)
lambda_A_VIP = 58 / (8 * 60 + 44)
print("lambda_A_VIP", lambda_A_VIP)
lambda_B = 1.0 / 63.99 * 5 /3
print("lambda_B", lambda_B)
lambda_B_VIP = 1.0 / 17.9 * 2
print("lambda_B_VIP", lambda_B_VIP)

# print("lambda_A", lambda_A)

mu_A = (7 + 9) / (
        7.5 + 5.3 + 11.1 + 10.0 + 9.1 + 8.8 + 12.6 + 15.4 + 11.9 + 14.6 + 11.8 + 14.8 + 20.4 + 7.7 + 7.5 + 10.9)

mu_A = mu_A * 0.9

mu_B = 29 / (48+45+28+25+22+24+17+33+8+10+26+32+21+37+8+60+40+18+26+8+21+23+28+50+28+48+28+36+27+5)
print("mu_A", mu_A)

L_s_A = lambda_A / (mu_A - lambda_A)
L_q_A = lambda_A ** 2 / (mu_A * (mu_A - lambda_A))
W_s_A = 1 / (mu_A - lambda_A)
W_q_A = lambda_A / (mu_A * (mu_A - lambda_A))
'''
print(L_s_A)
print(L_q_A)
print(W_s_A)
print(W_q_A)
'''
millimeter_mean = (7 * 60 + 42.6) / 40
X_ray_mean = (1 * 60 + 18.0 + 11.0) / (11 + 4)
time_belt_mean = 28.37
# print(millimeter_mean+X_ray_mean)


import random
import simpy
import numpy as np
from matplotlib import pyplot as plt

RANDOM_SEED = 2
NEW_CUSTOMERS_VIP = 300  # 客户数
NEW_CUSTOMERS = 150 # 客户数
INTERVAL_CUSTOMERS = 10.0  # 客户到达的间距时间
MIN_PATIENCE = 1  # 客户等待时间, 最小
MAX_PATIENCE = 3  # 客户等待时间, 最大
free_time = 0   #空闲时间

time_x = 0
num_y = 0
num_Y = np.zeros((NEW_CUSTOMERS, 1))

wait_array = np.zeros((NEW_CUSTOMERS, 1))
wait_array2 = np.zeros((NEW_CUSTOMERS, 1))
sum_array = np.zeros((NEW_CUSTOMERS, 1))
service_array = np.zeros((NEW_CUSTOMERS, 1))
lastArrive = 0
total_time = 0

def source(env, number, interval, counter, wait_array, service_array):
    """进程用于生成客户"""
    for i in range(number):
        global num_y
        num_y += 1
        num_Y[i] = num_y
        t = random.expovariate(lambda_A_VIP)
        print("乘客%d到达的间隔为：%7.4f" % (i, t))
        time_in_bank = random.expovariate(mu_A)
        print("乘客%d所需的服务时间为：%7.4f" % (i, time_in_bank))
        service_array[i] = time_in_bank
        c = customer(env, '乘客%d' % i, counter, time_in_bank, i, wait_array)
        env.process(c)
        yield env.timeout(t)


def customer(env, name, counter, time_in_bank, i, wait_array):
    """一个客户表达为一个协程, 客户到达, 被服务, 然后离开"""

    arrive = env.now
    print('%7.4f时刻 %s: 到达' % (arrive, name))
    global sum_array, lastArrive, total_time, num_y

    with counter.request() as req:
        yield req
        wait = env.now - arrive
        wait_array[i] = wait
        if wait == 0:
            total_time += env.now - lastArrive
        # 到达柜台
        print('%7.4f %s: 等待时间为 %6.3f' % (env.now, name, wait))
        # tib = random.expovariate(1.0 / time_in_bank)
        yield env.timeout(time_in_bank)
        lastArrive = env.now
        print('%7.4f %s: 完成了服务' % (env.now, name))
        sum_array[i] = wait + time_in_bank
        num_y -= 1
        print(num_y)
        lastArrive = env.now



def source2(env, number, interval, counter, wait_array2, service_array):
    """进程用于生成客户"""
    for i in range(number):
        global num_y
        num_y += 1
        num_Y[i] = num_y
        t = random.expovariate(lambda_B_VIP)
        print("乘客%d到达的间隔为：%7.4f" % (i, t))
        time_in_bank = random.expovariate(mu_B)
        print("乘客%d所需的服务时间为：%7.4f" % (i, time_in_bank))
        service_array[i] = time_in_bank
        c = customer(env, '乘客%d' % i, counter, time_in_bank, i, wait_array2)
        env.process(c)
        yield env.timeout(t)


def customer2(env, name, counter, time_in_bank, i, wait_array2):
    """一个客户表达为一个协程, 客户到达, 被服务, 然后离开"""

    arrive = env.now
    print('%7.4f时刻 %s: 到达' % (arrive, name))
    global sum_array, lastArrive, total_time, num_y

    with counter.request() as req:
        yield req
        wait = env.now - arrive
        wait_array2[i] = wait
        if wait == 0:
            total_time += env.now - lastArrive
        # 到达柜台
        print('%7.4f %s: 等待时间为 %6.3f' % (env.now, name, wait))
        # tib = random.expovariate(1.0 / time_in_bank)
        yield env.timeout(time_in_bank)
        lastArrive = env.now
        print('%7.4f %s: 完成了服务' % (env.now, name))
        sum_array[i] = wait + time_in_bank
        num_y -= 1
        print(num_y)
        lastArrive = env.now

# Setup and start the simulation
print('Bank renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Start processes and run
counter = simpy.Resource(env, capacity=1)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter, wait_array, service_array))
env.run()

env.process(source2(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter, wait_array2, service_array))
env.run()

''''''
plt.plot(np.array(range(NEW_CUSTOMERS)), wait_array, label="wait time A")
plt.plot(np.array(range(NEW_CUSTOMERS)), wait_array2, label="wait time B")
plt.title("wait time-- VIP")
plt.xlabel("each passenger")
plt.ylabel("spend time")
plt.legend(loc="best")

'''
plt.plot(np.array(range(NEW_CUSTOMERS)), num_Y)
plt.title("The number of line")
'''
#print(lastArrive / NEW_CUSTOMERS)
#print("total_time/lastArrive", total_time/lastArrive)
plt.show()














'''zoneB'''

lambda_B_VIP = (lastArrive / NEW_CUSTOMERS)
print(lambda_B_VIP)
num_y_B = 0
time_x_B = 0
num_Y_B = np.zeros((NEW_CUSTOMERS, 1))

wait_array_B = np.zeros((NEW_CUSTOMERS, 1))
sum_array_B = np.zeros((NEW_CUSTOMERS, 1))
service_array_B = np.zeros((NEW_CUSTOMERS, 1))
def sourceB(env, number, interval, counter, wait_array, service_array):
    """进程用于生成客户"""
    for i in range(number):
        global num_y_B
        num_y_B += 1
        num_Y_B[i] = num_y_B
        t = random.expovariate(lambda_B_VIP)
        print("乘客%d到达B的间隔为：%7.4f" % (i, t))
        time_in_bank = random.expovariate(mu_A)
        print("乘客%d所需的服务时间为：%7.4f" % (i, time_in_bank))
        service_array_B[i] = time_in_bank
        c = customerB(env, '乘客%d' % i, counter, time_in_bank, i, wait_array_B)
        env.process(c)
        yield env.timeout(t)


def customerB(env, name, counter, time_in_bank, i, wait_array):
    """一个客户表达为一个协程, 客户到达, 被服务, 然后离开"""

    arrive = env.now
    print('%7.4f时刻 %s: 到达' % (arrive, name))
    global sum_array_B

    with counter.request() as req:
        yield req
        wait = env.now - arrive
        wait_array_B[i] = wait
        # 到达柜台
        print('%7.4f %s: 等待时间为 %6.3f' % (env.now, name, wait))
        # tib = random.expovariate(1.0 / time_in_bank)
        yield env.timeout(time_in_bank)
        print('%7.4f %s: 完成了服务' % (env.now, name))
        sum_array_B[i] = wait + time_in_bank
        global num_y_B, lastArrive
        num_y_B -= 1
        print(num_y_B)
        lastArrive = env.now

env2 = simpy.Environment()
'''
# Start processes and run
counter = simpy.Resource(env, capacity=1)
env2.process(sourceB(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter, wait_array, service_array))
env2.run()'''