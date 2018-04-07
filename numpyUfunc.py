import numpy as np
import math

from mpl_toolkits.mplot3d.axes3d import Axes3D
import pylab as pl
#ufnunc 泛用函数

x = np.linspace(0, 2*np.pi, 10)
y = np.sin(x)
print(y)

x = [i * 0.001 for i in range(1000000)]

def sin_math(x):
    for i, t in enumerate(x):
        x[i] = math.sin(t)

def sin_numpy(x):
    np.sin(x, x)#时间最短

def sin_numpy_loop(x):
    for i, t in enumerate(x):
        x[i] = np.sin(t)
'''
xl = x[:]
sin_math(x)

xa = np.array(x)
sin_numpy(xa)

xl = x[:]
sin_numpy_loop(x)
'''
#矩阵加法
a = np.arange(0, 4)
b = np.arange(1, 5)
print(np.add(a, b, a)) #out-a#[ 2  5  8 11]
#add(x1,x2,out)+/subtract-/mutiply/divide/true_devide/floor_devide///negative-/power**/remainder,mod%

#比较运算
print(np.array([1, 2, 3]) < np.array([3, 2, 1]))#[ True False False]
#布尔运算
a = np.arange(5)#01234
b = np.arange(4, -1, -1)#43210
print(a == b)
print(a > b)
print(np.logical_or(a == b, a > b))  # 和 a>=b 相同
print(~ np.arange(5))
print(~np.arange(5,dtype = np.uint8))

#自定义ufunc
def triangle_wave(x, c, c0, hc):
    x = x - int(x) # 三角波的周期为1，因此只取x坐标的小数部分进行计算
    if x >= c: r = 0.0
    elif x < c0: r = x / c0 * hc
    else: r = (c-x) / (c-c0) * hc
    return r

x = np.linspace(0, 2, 1000)
y1 = np.array([triangle_wave(t, 0.6, 0.4, 1.0) for t in x])

triangle_ufunc1 = np.frompyfunc(triangle_wave, 4, 1)
y2 = triangle_ufunc1(x, 0.6, 0.4, 1.0)

#print(y1==y2)
#frompyfunc将计算单个元素的函数转换成ufunc函数，对数组进行计算
'''
#当时用ufunc进行计算时，如果数组形状不同，会进行如下处理
a = np.arange(0, 60, 10).reshape(-1, 1)
b = np.arange(0, 5)
c = a + b
b = b.repeat(6, axis=0)
a = a.repeat(5, axis=1)
x, y = np.mgrid[:5, :5]
x, y = np.ogrid[:5, :5]
x, y = np.ogrid[:1:4j, :1:3j]
x, y = np.ogrid[-2:2:20j, -2:2:20j]
z = x * np.exp( - x**2 - y**2)

fig = pl.figure(figsize=(15, 5))
ax = fig.add_subplot(1, 1, 1, projection='3d')
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap="coolwarm", linewidth=0.2)
pl.show()
'''
#reduce
r1 = np.add.reduce([1, 2, 3])  # 1 + 2 + 3
r2 = np.add.reduce([[1, 2, 3], [4, 5, 6]], axis=1)  # (1+2+3),(4+5+6)
a1 = np.add.accumulate([1, 2, 3])
a2 = np.add.accumulate([[1, 2, 3], [4, 5, 6]], axis=1)

a = np.array([1, 2, 3, 4])
result = np.add.reduceat(a, indices=[0, 1, 0, 2, 0, 3, 0])

np.multiply.outer([1, 2, 3, 4, 5], [2, 3, 4])
'''
array([[ 2,  3,  4],
       [ 4,  6,  8],
       [ 6,  9, 12],
       [ 8, 12, 16],
       [10, 15, 20]])
'''
