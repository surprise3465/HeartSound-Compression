import scipy.io as sio
import numpy as np
import pylab as pl
from ufun import *
from huffman import*

matfn = u'ECG.mat'
data1 = sio.loadmat(matfn)
RawECGData = data1['AA']
EcgData = RawECGData.reshape(1, RawECGData.size)[0]
matfn = u'HS.mat'
data2 = sio.loadmat(matfn)
RawHsData = data2['data']
HsData = RawHsData.reshape(1, RawHsData.size)[0]
HS = hs_spcm(HsData, 16)

fs = 4000
prdc = 10  
R = 8 
StartPer = 1 
qbit = 10

tind = Rwave_detection(EcgData, fs)  
tlen = np.diff(tind[StartPer:StartPer + R])
meanh = np.mean(HS[tind[StartPer]:tind[StartPer + R]])
HS[tind[StartPer]:tind[StartPer + R]] = HS[tind[StartPer]:tind[StartPer + R]] - meanh
indmax = np.argmax(tlen)
HStrain = HS[tind[StartPer + indmax - 1]:tind[StartPer + indmax]]
K = getKvalue(HStrain, prdc)

HSForTest = HS[tind[StartPer]:tind[StartPer + R]]
HSReTest = np.zeros(HS.size)

xlen = 0
ylen = 0

WS = np.zeros((R,K))
WL = np.zeros((R,5),dtype = int)
inforL = []
AllIndex = []

for ind in range(0,R):
    HStemp = HS[tind[StartPer + ind]:tind[StartPer + ind +1]]
    WaveC,WaveL = SingalToWaveArray(HStemp)
    for i in range(len(WaveL)):
        WL[ind,i] = WaveL[i]
    inforL.append(WaveC.size)
    WS[ind,:], tempI = chooseKmaxValue(WaveC, K)
    for i in range(tempI.size):
        AllIndex.append(tempI[i].tolist())

WE = np.reshape(WS,(R*K))
QWC = hs_spcm(WE,qbit)
code1, str1 = compress(QWC)
DWE = decompress(code1, str1)
RWS = np.reshape(DWE,(R,K))

WI = np.array(AllIndex, dtype = int)
QWI,first_s = runlength_encode(WI)
code2, str2  = compress(QWI)
DWI = decompress(code2, str2 )
RWI = runlength_decode(DWI.astype(np.int),first_s)

CR = HSForTest.size*16/(len(str2)+len(str1))
start = 0
for ind in range(0,R):
    HStemp = HSReTest[tind[StartPer + ind]:tind[StartPer + ind +1]]
    RWaveC = np.zeros(inforL[ind])
    RWaveC[RWI[start:start+inforL[ind]]==1] = RWS[ind,:]
    start += inforL[ind]
    HSReTest[tind[StartPer + ind]:tind[StartPer + ind + 1]] = WaveArrayToSignal(RWaveC,WL[ind,:])[0:HStemp.size]

HSdetrain = HSReTest[tind[StartPer + indmax - 1]:tind[StartPer + indmax]]
pl.plot(HStrain)
pl.plot(HSdetrain,'r')
prd1 =hs_prd(HStrain, HSdetrain)
pl.show()
print(prd1)
print(CR)