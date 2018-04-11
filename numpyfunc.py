import numpy as np
from numpy import random as nr
np.set_printoptions(precision=2) # 为了节省篇幅，只显示小数点后两位数字
r1 = nr.rand(4, 3)#0-1分布
r2 = nr.randn(4, 3)#标准正态分布
r3 = nr.randint(0, 10, (4, 3))#整数随机分布
print(r1,r2,r3)

r4 = nr.normal(100, 10, (4, 3))
r5 = nr.uniform(10, 20, (4, 3))
r6 = nr.poisson(2.0, (4, 3))
print(r4,r5,r6)

a = np.array([1, 10, 20, 30, 40])
print(nr.permutation(10))#[2 4 3 5 6 8 0 1 9 7]
print(nr.permutation(a))#[40  1 10 20 30]
nr.shuffle(a)
print(a)

b = np.arange(10, 25, dtype=float)
c1 = nr.choice(b, size=(4, 3))
c2 = nr.choice(b, size=(4, 3), replace=False)
c3 = nr.choice(b, size=(4, 3), p=b/np.sum(b))

r11 = nr.randint(0, 100, 3)
r21= nr.randint(0, 100, 3)
nr.seed(42)
r31 = nr.randint(0, 100, 3)
nr.seed(42)
r41 = nr.randint(0, 100, 3)

np.random.seed(42)
d = np.random.randint(0,10,size=(4,5))
dnum = np.sum(d)
print(dnum, np.sum(d, axis=1), np.sum(d, axis=0))
np.sum(np.ones((2, 3, 4)), axis=(0, 2))#1-3轴相加，得到第二维度array([ 8.,  8.,  8.])

np.sum(d, 1, keepdims=True) #保持维度相加
np.sum(d, 0, keepdims=True)
'''
[[26],                       [[22, 13, 27, 18, 16]]     
 [28],                                                  
 [24],                                                  
 [18]] 
 '''                
pa = d/np.sum(d, 1, dtype=float, keepdims=True) * 100
print(pa,pa.sum(1, keepdims=True),sep = '\n',end = '\n')

np.mean(d, axis=1) # 整数数组使用双精度浮点数进行计算
print(np.mean(d, axis=1))
'''
np.set_printoptions(precision=8)
b = np.full(1000000, 1.1, dtype=np.float32) # 创建一个很大的单精度浮点数数组
b # 1.1无法使用浮点数精确表示，存在一些误差
'''

score = np.array([83, 72, 79])
number = np.array([20, 15, 30])
#print(np.average(score, weights=number))
#print(np.sum(score*number)/np.sum(number, dtype=float))

a = nr.normal(0, 2.0, (100000, 10)) 
v1 = np.var(a, axis=1, ddof=0) #可以省略ddof=0
v2 = np.var(a, axis=1, ddof=1)

print(np.mean(v1),np.mean(v2))

def normal_pdf(mean, var, x):
    return 1 / np.sqrt(2 * np.pi * var) * np.exp(-(x - mean) ** 2 / (2 * var))

nr.seed(42)
data = nr.normal(0, 2.0, size=10)                         #❶
mean, var = np.mean(data), np.var(data)                   #❷
var_range = np.linspace(max(var - 4, 0.1), var + 4, 100)  #❸

p = normal_pdf(mean, var_range[:, None], data)            #❹
p = np.product(p, axis=1)                                 #❺

import pylab as pl
pl.plot(var_range, p)
pl.axvline(var, 0, 1, c="r")
pl.show()