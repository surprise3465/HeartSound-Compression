import scipy.io as sio
import pylab as pl
from ufun import *

fsd = 4000
matfn = u'ECG.mat'
data = sio.loadmat(matfn)
RawECGData = data['AA']
shortEcgData = RawECGData[0:80000]
ReshapeEcgData = shortEcgData.reshape(1, shortEcgData.size)[0]
tind = Rwave_detection(ReshapeEcgData, fsd)
pl.plot(ReshapeEcgData, linewidth=1.0)
pl.plot(tind, ReshapeEcgData[tind], 'r*')
pl.show()
