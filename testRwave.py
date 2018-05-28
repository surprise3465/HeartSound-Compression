import scipy.io as sio  
import pylab as pl
from ufun import *

fsd = 4000
matfn=u'ECG.mat'  
data=sio.loadmat(matfn) 
RawECGData=data['AA']
shortEcgData = RawECGData[0:80000]
ReshapeEcgData = shortEcgData.reshape(1,shortEcgData.size)[0]
QcpEcgData = hs_pcm(ReshapeEcgData,12)
tind=Rwave_detection(QcpEcgData,fsd)

pl.plot(QcpEcgData, linewidth=1.0)  
pl.plot(tind, QcpEcgData[tind], 'r*')
pl.show()
pl.allclose
a = hs_prd(QcpEcgData,ReshapeEcgData)
print(a)