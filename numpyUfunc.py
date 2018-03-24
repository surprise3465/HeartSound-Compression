import numpy as np
import math
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

xl = x[:]
sin_math(x)

xa = np.array(x)
sin_numpy(xa)

xl = x[:]
sin_numpy_loop(x)