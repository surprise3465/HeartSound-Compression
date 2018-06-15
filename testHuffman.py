import numpy as np
from huffman import *

test1 =np.array([1,2,3,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,1,1,2,3,3,1],dtype = float)
code1, str1 = compress(test1)
test2 = decompress(code1,str1)
print(test1)
print(test2)