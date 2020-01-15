import random

#坐标值
a = 0
b = 0
count = 0   #命中总次数
N = 10000   #总次数
r = 1   #半径
for i in range(N):
    xRandom = random.uniform(a-r, a+r)
    yRandom = random.uniform(b-r, b+r)
    if xRandom**2 + yRandom**2 <= r**2:
        count += 1
print((count / float(N)) * 4)