import numpy as np

#重整行列
c = np.array([[1,2,3,4],[5,6,7,8],[7,8,9,10]])
d = c.reshape(4,3)
print(c.shape,c.dtype,d)

#指定数组类型
ai32 = np.array([1,2,3,4],dtype = np.int32)
af = np.array([1,2,3,4],dtype = float)
ac = np.array([1,2,3,4],dtype = complex)

a16 = np.int16(200)#精度有限导致平方溢出
#print(a16*a16)

#数组转换
t1 = af.astype(np.int32)
t2 = ai32.astype(np.complex)

#自动生成数组
ap = np.arange(0,1,0.1)
aline = np.linspace(0,1,10)
alog = np.logspace(1,3,3,base=2,endpoint=True)#指数
print(ap,aline,alog)

#创建预定值数组
azeros = np.zeros(4,np.int)
afull = np.full(4,np.pi)
aempty = np.empty(4,np.int)
aones = np.ones(4,np.int)
print(azeros,afull,aones,aempty)

#zeros_like(),ones_like()等可以创建与参数数组类型相同的数组

#frombuffer fromstring fromfile创建数组
strtmp = "abcdefgh"
arytmp = np.fromstring(strtmp,dtype = np.int8)
print(arytmp)
#fromstring会对字符串的字节序列进行复制，使用frombuffer()创建的数组与原始字符串共享内存
buftmp = np.frombuffer(arytmp,dtype = np.int16)
print(buftmp)

#从函数创造数组
def func(i):
    return i%4+1
    
def func2(i,j):
    return (i+1)*(j+1)


funtmp1 = np.fromfunction(func,(10,))
funtmp2 = np.fromfunction(func2,(9,9))
print(funtmp1,funtmp2)

a = np.arange(10)
a1 = a[3:5]
a2 = a[:5]
a3 = a[:-1]
a4 = a[1:-1:2]
a5 = a[::-1]
a6 = a[5:1:-2]
print(a1,a2,a3,a4,a5,a6,sep = '\n ', end = '\n')
#[3 4] [0 1 2 3 4] [0 1 2 3 4 5 6 7 8] [1 3 5 7] [9 8 7 6 5 4 3 2 1 0] [5 3]

#数组切片获取的是原数组的一个视图。与原数组共享同一块共享空间
x = np.arange(10,1,-1)
a = x[3:7]
#数组用整数列表对数组元素进行存取时，不和原数组共享同一块共享空间
b = x[[3,3,-3,8]]
#布尔数组作为下标存取元素，不和原数组共享内存
x = np.arange(5,0,-1)
c = x[np.array([True,False,True,False,False])]
x = np.random.randint(0,10,6)
d = x[x>5]
print(a,b,c,d, sep = '\n', end = '\n')
#[7 6 5 4][7 7 4 2][5 3][9 7 6 8]

#多维数组的整数和切片查询
m = np.arange(0,60,10).reshape(-1,1)+np.arange(0,6)
m1 = m[0,3:5]
m2 = m[4:,4:]
m3 = m[:,2]
m4 = m[2::2,::2]
mask = np.array([1,0,1,0,0,1],dtype = np.bool)
m5 = m[mask,2]
print(m,m1,m2,m3,m4,m5,sep = '\n', end = '\n')

#所有轴都用形状相同的整数数组作为下标时，得到的数组和下标数组的形状相同
x = np.array([[0,1],[2,3]])#[[0 1] [2 3]]
y = np.array([[-1,-2],[-3,-4]])#[[-1 -2] [-3 -4]]
z = m[x,y]#m[(0,1,2,3),(-1,-2,-3,-4)].reshape(2,2)
print(m[x],x,y,z,sep = '\n')
#[[ 5 14] [23 32]]

palette = np.array([[0,0,0],
                    [255,0,0],
                    [0,255,0],
                    [0,0,255],
                    [255,255,255]])
image = np.array([[0,1,2,3],
                 [0,3,4,0]])
print(palette,image,sep = '\n')
print(palette[image])#三维数组

#结构数组
persontype = np.dtype({
    'names':['name','age','weight'],
    'formats':['S30','i','f']}, align = True)
a = np.array([("Zhang",32,75.5),("Wang",24,65.2)],dtype = persontype)
a[1]["name"] = "Li"
a.tofile("test.bin")
print(a)

#当下标使用整数和切片时，共享存储区域
#当下标使用整数序列，整数数组和布尔数组时，只能对数据进行复制

