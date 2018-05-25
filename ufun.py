import numpy as np
from scipy.signal import butter, lfilter

def hs_pcm(x, maxx, minx, bit):
    t=maxx-minx
    quiz=t/(2^bit)
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
    y = lfilter(b, a, data)
    return y
  

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandpass')
    return b, a

def Rwave_detection(x,fsd):
    fs=2000
    n = fsd/fs
    xs = x[1::n]
    ecg=resample(x,fs,fsd)
    [b,a]=butter(5,[10/fs 50/fs])# 滤波，带宽介于5-25Hz
    Delay=50;
    b=fir1(Delay,[10/fs 50/fs]);a=1;
    fecg=filter(b,a,ecg);
    clear b a;
    decg=diff(fecg);
    hecg=hilbert(decg);
    secg=abs(hecg.^2);
    i=1
    j=1
    ind1=np.array.zeros(length(secg))
    while(i<=length(secg)):
        if(secg(i)>1e-4):
            ind1(j)=i
            i=i+750
            j=j+1
        else
            i=i+1
        end
    end
    I=find(ind1~=0)
    return ind=ind1(I)*fsd/fs

ecg=resample(x,fs,fsd)
[b,a]=butter(5,[10/fs 50/fs]); % 滤波，带宽介于5-25Hz
Delay=50;
b=fir1(Delay,[10/fs 50/fs]);a=1;
fecg=filter(b,a,ecg);
clear b a;

decg=diff(fecg);
hecg=hilbert(decg);
secg=abs(hecg.^2);
i=1;j=1;ind1=zeros(1,length(secg))
while(i<=length(secg))
    if(secg(i)>1e-4)
        ind1(j)=i;
        i=i+750;
        j=j+1;
    else
        i=i+1;
    end
end
I=find(ind1~=0);
ind=ind1(I)*fsd/fs;