import numpy as np;

# 计算残差
def error_function(Theta, X, Y):
    # 计算y’-y,得到列向量
    diff = Theta * X - Y
    # 计算损失总值
    error = (1 / (2 * Theta.size)) * np.dot(np.transpose(diff), diff)
    return error


# 计算梯度
def gradient_function(Theta, X, Y):
    diff = X * Theta - Y
    result = (1 / Theta.size) * np.dot(np.transpose(X), diff)
    return result


def gradient_descent(X, Y, a):
    # 初始化θ的值为0的列向量
    Theta = np.array([0, 0, 0, 0, 0]).reshape(5, 1)
    # 计算梯度
    gradient = gradient_function(Theta, X, Y)
    # 寻找200次
    for i in range(1, 200):
        Theta = Theta - a * gradient
        gradient = gradient_function(Theta, X, Y)
    return Theta
