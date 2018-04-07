import numpy as np

a = np.arange(3 * 4 * 5).reshape(3, 4, 5)
lidx = [[0], [1]]
aidx = np.array(lidx)
print(a[lidx])
print(a[aidx]) 
temp1 = a[tuple(lidx)]
temp2 = a[aidx,:,:]

i0 = np.array([[1, 2, 1], [0, 1, 0]])
i1 = np.array([[[0]], [[1]]])
i2 = np.array([[[2, 3, 2]]])
b = a[i0, i1, i2]
print(b)
ind0, ind1, ind2 = np.broadcast_arrays(i0, i1, i2)

I, J, K, L = 6, 7, 8, 3
_, _, v = np.mgrid[:I, :J, :K]
idx = np.random.randint(0, K - L, size=(I, J))

idx_k = idx[:, :, None] + np.arange(3)
idx_k.shape