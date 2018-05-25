import scipy.io as sio  
import pylab as pl
import numpy as np  
import pywt
import scipy.signal as signal
from scipy import fftpack

sampling_rate = 4000 ##取样频率

matfn=u'Normal_HeartSound_Short.mat'  
data=sio.loadmat(matfn) 
hs=data['data']
len = np.size(hs)
fft_size  =256   #FFT处理的取样长度

t = np.arange(0,len/sampling_rate,1.0/sampling_rate)
xs = hs[:fft_size]# 从波形数据中取样fft_size个点进行运算

hx_real = fftpack.hilbert(xs).real

xf = np.fft.rfft(xs)/fft_size 
freqs = np.linspace(0,sampling_rate/2,fft_size)
xfp = 20*np.log10(np.clip(np.abs(xf),1e-20,1e1000))

pl.figure(figsize=(8,4))
pl.subplot(211)
pl.plot(t[:fft_size], xs)
pl.xlabel(u"时间(秒)")
pl.title(u"The Wave and Spectrum")
pl.subplot(212)
pl.plot(freqs, xfp)
pl.xlabel(u"Hz")
pl.subplots_adjust(hspace=0.4)
pl.show()

pl.plt.close('all')