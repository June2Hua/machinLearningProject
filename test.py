import random
r = random.Random(98765)
sumx = 0
count = 0
for rep in range(10000):
    x = 0;
    consechds = 0;
    while True:
        u = r.uniform(0.0,1.0)
        if u < 0.5:
            consechds += 1
        else:
            consechds = 0
        x += 1
        if consechds == 3:
            break
    if x > 6:
        count += 1
    sumx += 1


print(count/sumx)