import random
import simpy
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

maxA = 10
maxB = 10
passengersWaitTime = np.zeros((maxA,maxB))
utilizationRatio = np.zeros((maxA,maxB))
for serviceA in range(maxA):
    for serviceB in range(maxB):
        #lambda_A_VIP = 58 / (8 * 60 + 44) / serviceA
        lambda_A_VIP = 58 / (8 * 60 + 44) / (serviceA+1)
        mu_A = (7 + 9) / (
                7.5 + 5.3 + 11.1 + 10.0 + 9.1 + 8.8 + 12.6 + 15.4 + 11.9 + 14.6 + 11.8 + 14.8 + 20.4 + 7.7 + 7.5 + 10.9)
        mu_B = 29 / (
                    48 + 45 + 28 + 25 + 22 + 24 + 17 + 33 + 8 + 10 + 26 + 32 + 21 + 37 + 8 + 60 + 40 + 18 + 26 + 8 + 21 + 23 + 28 + 50 + 28 + 48 + 28 + 36 + 27 + 5)

        RANDOM_SEED = 2
        NEW_CUSTOMERS_VIP = 300  # 客户数
        NEW_CUSTOMERS = 150  # 客户数
        INTERVAL_CUSTOMERS = 10.0  # 客户到达的间距时间
        free_time = 0  # 空闲时间

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
                # print("乘客%d到达的间隔为：%7.4f" % (i, t))
                time_in_bank = random.expovariate(mu_A)
                # print("乘客%d所需的服务时间为：%7.4f" % (i, time_in_bank))
                service_array[i] = time_in_bank
                c = customer(env, '乘客%d' % i, counter, time_in_bank, i, wait_array)
                env.process(c)
                yield env.timeout(t)


        def customer(env, name, counter, time_in_bank, i, wait_array):
            """一个客户表达为一个协程, 客户到达, 被服务, 然后离开"""

            arrive = env.now
            # print('%7.4f时刻 %s: 到达' % (arrive, name))
            global sum_array, lastArrive, total_time, num_y

            with counter.request() as req:
                yield req
                wait = env.now - arrive
                wait_array[i] = wait
                if wait == 0:
                    total_time += env.now - lastArrive
                # 到达柜台
                # print('%7.4f %s: 等待时间为 %6.3f' % (env.now, name, wait))
                # tib = random.expovariate(1.0 / time_in_bank)
                yield env.timeout(time_in_bank)
                lastArrive = env.now
                # print('%7.4f %s: 完成了服务' % (env.now, name))
                sum_array[i] = wait + time_in_bank
                num_y -= 1
                # print(num_y)
                lastArrive = env.now


        def source2(env, number, interval, counter, wait_array2, service_array):
            """进程用于生成客户"""
            for i in range(number):
                global num_y
                num_y += 1
                num_Y[i] = num_y
                t = random.expovariate(lambda_B_VIP)
                # print("乘客%d到达的间隔为：%7.4f" % (i, t))
                time_in_bank = random.expovariate(mu_B)
                # print("乘客%d所需的服务时间为：%7.4f" % (i, time_in_bank))
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
                # print('%7.4f %s: 等待时间为 %6.3f' % (env.now, name, wait))
                # tib = random.expovariate(1.0 / time_in_bank)
                yield env.timeout(time_in_bank)
                lastArrive = env.now
                # print('%7.4f %s: 完成了服务' % (env.now, name))
                sum_array[i] = wait + time_in_bank
                num_y -= 1
                # print(num_y)
                lastArrive = env.now


        # Setup and start the simulation
        random.seed(RANDOM_SEED)
        env = simpy.Environment()

        # Start processes and run
        counter = simpy.Resource(env, capacity=1)
        env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter, wait_array, service_array))
        env.run()

        #lambda_B_VIP = 1.0 / (lastArrive / NEW_CUSTOMERS_VIP) * serviceA / serviceB
        lambda_B_VIP = ( NEW_CUSTOMERS_VIP / lastArrive) * (serviceA+1) / (serviceB+1)
        # print("lastArrive", lastArrive)
        # print("lambda_B_VIP", lambda_B_VIP)

        env.process(source2(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter, wait_array2, service_array))
        env.run()
        passengersWaitTime[serviceA][serviceB] = np.mean(wait_array) + np.mean(wait_array2)
        utilizationRatio[serviceA][serviceB] = (lastArrive - total_time) / lastArrive
        '''
        plt.plot(np.array(range(NEW_CUSTOMERS)), wait_array, label="wait time A")
        #print("平均等待时间:", np.mean(wait_array) + np.mean(wait_array2))
        #print("利用率为：", (lastArrive - total_time) / lastArrive)
        
        plt.plot(np.array(range(NEW_CUSTOMERS)), wait_array2, label="wait time B")
        plt.title("wait time-- VIP")
        plt.xlabel("each passenger")
        plt.ylabel("spend time")
        plt.legend(loc="best")
        #plt.show()'''

fig = plt.figure()
ax = Axes3D(fig)
X = np.arange(1, 11, 1)
Y = np.arange(1, 11, 1)
X, Y = np.meshgrid(X, Y)
print(X)
print(Y)
#R = np.sqrt(X**2 + Y**2)
#Z = np.sin(R)

# 具体函数方法可用 help(function) 查看，如：help(ax.plot_surface)
ax.plot_surface(X, Y, utilizationRatio, rstride=1, cstride=1, cmap='rainbow')

print(passengersWaitTime)
print(utilizationRatio)
#plt.show()

passengersWaitTime_N = (passengersWaitTime - passengersWaitTime.min() ) / (passengersWaitTime.max() - passengersWaitTime.min())
utilizationRatio_N = (utilizationRatio - utilizationRatio.min() ) / (utilizationRatio.max() - utilizationRatio.min())


# = [['张三','男','未婚',20],['李四','男','已婚',28],['小红','女','未婚',18],['小芳','女','已婚',25]]
output = open('data2.xls','w',encoding='gbk')
for i in range(len(utilizationRatio_N)):
	for j in range(len(utilizationRatio_N[i])):
		output.write(str(utilizationRatio_N[i][j]))    #write函数不能写int类型的参数，所以使用str()转化
		output.write('\t')   #相当于Tab一下，换一个单元格
	output.write('\n')       #写完一行立马换行
output.close()

sum = (passengersWaitTime_N - utilizationRatio_N)
print( np.argmin(sum ))

sum2 = (2*passengersWaitTime_N - utilizationRatio_N)
print( np.argmin(sum2 ))

sum3 = (passengersWaitTime_N - utilizationRatio_N*2)
print( np.argmin(sum3 ))