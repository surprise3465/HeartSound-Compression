import scipy.io as sio
import numpy as np
import pylab as pl
from ufun import *

matfn = u'ECG.mat'
data1 = sio.loadmat(matfn)
RawECGData = data1['AA']
EcgData = RawECGData.reshape(1, RawECGData.size)[0]
matfn = u'HS.mat'
data2 = sio.loadmat(matfn)
RawHsData = data2['data']
HsData = RawHsData.reshape(1, RawHsData.size)[0]
HS = hs_pcm(HsData, 16)

fs = 4000
prdc = 10  # %预设失真度
p = 5  # %一级量化位数
CN = 256  # %码数大小
k = 8  # %矢量量化数
Kper = 3  # %关联周期数
R = 48  # %单次处理周期数
StartPer = 1  # %起始周期

tind = Rwave_detection(EcgData, fs)  # %心音分段
tlen = np.diff(tind[StartPer:StartPer + R])
meanh = np.mean(HS[tind[StartPer]:tind[StartPer + R] - 1])
HS[tind[StartPer]:tind[StartPer + R] -
   1] = HS[tind[StartPer]:tind[StartPer + R] - 1] - meanh
indr = np.argmax(tlen)
HStrain = HS[tind[StartPer + indr - 1]:tind[StartPer + indr] - 1]
K = getKvalue(HStrain, prdc)  # %获取稀疏度Kmax

# 获取非零系数，拆分为位置流，幅度流，和残差流
WK = np.zeros(R, K)
WS = np.zeros(R, K)
indamp = np.zeros(R, K)
Evalue = np.zeros(R, K)
xlen = 0
