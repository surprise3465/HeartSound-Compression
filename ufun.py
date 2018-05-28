import numpy as np
from scipy.signal import butter, lfilter,filtfilt
from scipy import fftpack

def hs_pcm(x,bit):
    maxx = np.max(x)
    minx = np.min(x)
    t=maxx-minx
    quiz=t/(2**bit)
    y=quiz*np.round(x/quiz)
    return y   


def hs_prd(x,y):
    t = x-y
    s=np.sum(np.square(t))
    r = np.sum(np.square(x-np.mean(x)))
    snr = 100*np.sqrt(s/r)
    return snr

def hs_tp(x):
    t=np.unique(x)
    p = []
    for i in t :
        p.append(t.count(i))
    return t,p

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y
  

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandpass')
    return b, a

def Rwave_detection(x,fsd):
    fs=2000
    n = int(fsd/fs)
    xs = x[::n]
    fxs = butter_bandpass_filter(xs,5,25,fs,3)
    dfxs = np.diff(fxs)
    hx = fftpack.hilbert(dfxs.reshape(dfxs.size,1))
    secg = np.abs(np.square(hx))
    i=1
    ind1=[]
    while(i<len(secg)):
        if(secg[i]>1e-4):
            ind1.append(i)
            i=i+750
        else:
            i=i+1
    ReInd=(np.array(ind1, dtype = int)*fsd/fs).astype(int)
    return ReInd