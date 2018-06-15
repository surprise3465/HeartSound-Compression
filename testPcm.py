import scipy.io as sio
import numpy as np
import pylab as pl
from ufun import *
from lloydmax import *
from huffman import *
StartPer = 0 # %起始周期
fs = 4000
R = 48  # %单次处理周期数
qbit = 6

matfn = u'ECG.mat'
data1 = sio.loadmat(matfn)
RawECGData = data1['AA']
EcgData = RawECGData.reshape(1, RawECGData.size)[0]
matfn = u'HS.mat'
data2 = sio.loadmat(matfn)
RawHsData = data2['data']
HsData = RawHsData.reshape(1, RawHsData.size)[0]
HS = hs_pcm(HsData,2,-2, 16)

tind = Rwave_detection(EcgData, fs)  # %心音分段
tlen = np.diff(tind[StartPer:StartPer + R])
meanh = np.mean(HS[tind[StartPer]:tind[StartPer + R] - 1])
HS[tind[StartPer]:tind[StartPer + R] -
   1] = HS[tind[StartPer]:tind[StartPer + R] - 1] - meanh


HS_Qpcm = hs_spcm(HS,qbit)
centers = lloydmax_sig(HS,qbit,0.000001)
HS_Lpcm = hs_Qlmax(HS,centers)

indr = np.argmax(tlen)
HStrain = HS[tind[StartPer + indr - 1]:tind[StartPer + indr] - 1]
HSQtrain = HS_Qpcm[tind[StartPer + indr - 1]:tind[StartPer + indr] - 1]
HSLtrain = HS_Lpcm[tind[StartPer + indr - 1]:tind[StartPer + indr] - 1]

prd1 = hs_prd(HStrain,HSQtrain)
print("标量量化PRD=%f" %prd1)
pl.subplot(211)
pl.plot(HStrain)
pl.plot(HSQtrain,'r')

prd2 = hs_prd(HStrain,HSLtrain)
print("Lloyd量化PRD=%f" %prd2)
pl.subplot(212)
pl.plot(HStrain)
pl.plot(HSLtrain,'r')

pl.show()




