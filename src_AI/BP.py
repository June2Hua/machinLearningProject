import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def sigmoid(x):
    # 第一层到第二层的激活函数
    return 1 / (1 + np.exp(-x))


def deriv_sigmoid(x):
    # 第一层到第二层的激活函数的求导函数
    fx = sigmoid(x)
    return fx * (1 - fx)


def mse_loss(y_true, y_pred):
    # 使用方差作为损失函数
    return ((y_true - y_pred) ** 2).mean()


class OurNeuralNetwork:

    def __init__(self):
        # 第一层到第二层的函数
        self.w11 = np.random.normal()
        self.w12 = np.random.normal()
        self.w13 = np.random.normal()
        self.w14 = np.random.normal()
        self.w21 = np.random.normal()
        self.w22 = np.random.normal()
        self.w23 = np.random.normal()
        self.w24 = np.random.normal()
        # 第二层到第三层的函数
        self.w1 = np.random.normal()
        self.w2 = np.random.normal()
        # 截距项，Biases
        self.b1 = np.random.normal()
        self.b2 = np.random.normal()
        self.b3 = np.random.normal()

    def feedforward(self, x):
        # 前向传播学习
        h1 = sigmoid(self.w11 * x[0] + self.w12 * x[1] + self.w13 * x[2] + self.w14 * x[3] + self.b1)
        h2 = sigmoid(self.w21 * x[0] + self.w22 * x[1] + self.w23 * x[2] + self.w24 * x[3] + self.b1)
        o1 = self.w1 * h1 + self.w2 * h2 + self.b3
        return o1
    #训练函数
    def train(self, data, all_y_trues):
        learn_rate = 0.01  # 学习率
        epochs = 1000  # 训练的次数
        # 画图数据
        self.loss = np.zeros(100)
        self.sum = 0;
        # 开始训练
        for epoch in range(epochs):
            for x, y_true in zip(data, all_y_trues):
                # 计算h1
                h1 = sigmoid(self.w11 * x[0] + self.w12 * x[1] + self.w13 * x[2] + self.w14 * x[3] + self.b1)
                # 计算h2
                h2 = sigmoid(self.w21 * x[0] + self.w22 * x[1] + self.w23 * x[2] + self.w24 * x[3] + self.b2)
                #计算输出节点
                y_pred = self.w1 * h1 + self.w2 * h2 + self.b3
                # 反向传播计算导数
                d_L_d_ypred = -2 * (y_true - y_pred)
                d_ypred_d_w1 = h1
                d_ypred_d_w2 = h2
                d_ypred_d_b3 = 0
                d_ypred_d_h1 = self.w1
                d_ypred_d_h2 = self.w2
                sum_1=self.w11 * x[0] + self.w12 * x[1] + self.w13 * x[2] + self.w14 * x[3] + self.b1
                d_h1_d_w11 = x[0] * deriv_sigmoid(sum_1)
                d_h1_d_w12 = x[1] * deriv_sigmoid(sum_1)
                d_h1_d_w13 = x[2] * deriv_sigmoid(sum_1)
                d_h1_d_w14 = x[3] * deriv_sigmoid(sum_1)
                d_h1_d_b1 = deriv_sigmoid(sum_1)
                sum_2 = self.w21 * x[0] + self.w22 * x[1] + self.w23 * x[2] + self.w24 * x[3] + self.b2
                d_h1_d_w21 = x[0] * deriv_sigmoid(sum_2)
                d_h1_d_w22 = x[1] * deriv_sigmoid(sum_2)
                d_h1_d_w23 = x[2] * deriv_sigmoid(sum_2)
                d_h1_d_w24 = x[3] * deriv_sigmoid(sum_2)
                d_h1_d_b2 = deriv_sigmoid(sum_2)

                # 梯度下降法
                self.w11 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_w11
                self.w12 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_w12
                self.w13 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_w13
                self.w14 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_w14
                self.b1 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_b1
                self.w21 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h1_d_w21
                self.w22 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h1_d_w22
                self.w23 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h1_d_w23
                self.w24 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h1_d_w24
                self.b2 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h1_d_b2
                self.w1 -= learn_rate * d_L_d_ypred * d_ypred_d_w1
                self.w1 -= learn_rate * d_L_d_ypred * d_ypred_d_w2
                self.b3 -= learn_rate * d_L_d_ypred * d_ypred_d_b3

            if epoch % 10 == 0:
                y_preds = np.apply_along_axis(self.feedforward, 1, data)
                loss = mse_loss(all_y_trues, y_preds)
                print("Epoch %d loss: %.3f" % (epoch, loss))
                self.loss[self.sum] = loss
                self.sum = self.sum + 1

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
# 处理数据
data = np.array(X)
data_mean = np.sum(data, axis=0) / np.size(data, 0)
data = (data - data_mean) / np.max(data)
all_y_trues = np.array(Y)
all_y_trues_mean = np.sum(all_y_trues) / np.size(all_y_trues)
all_y_trues = (all_y_trues - all_y_trues_mean) / np.max(all_y_trues)
# 训练数据
network = OurNeuralNetwork()
network.train(data, all_y_trues)
# 输出神经网络参数
print("w11-->%.3f" % network.w11)
print("w12-->%.3f" % network.w12)
print("w13-->%.3f" % network.w13)
print("w14-->%.3f" % network.w14)
print("w21-->%.3f" % network.w21)
print("w22-->%.3f" % network.w22)
print("w23-->%.3f" % network.w23)
print("w24-->%.3f" % network.w24)
print("w1-->%.3f" % network.w1)
print("w2-->%.3f" % network.w2)
print("b1-->%.3f" % network.b1)
print("b2-->%.3f" % network.b2)
print("b3-->%.3f" % network.b3)
# 标题显示中文
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 测试数据
testData = np.array([99, 3, 2, 2014])
testPrice = network.feedforward(testData)
# 损失函数曲线图
plt.plot(np.arange(100), network.loss)
plt.show()
# 真实值与预测值对比
y_preds = np.apply_along_axis(network.feedforward, 1, data)
plt.plot(np.arange(380), all_y_trues,"r^")
plt.plot(np.arange(380),y_preds,"bs")
plt.title("红色为真实值，蓝色为预测值")
plt.show()
