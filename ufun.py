import numpy as np
from scipy.signal import butter, filtfilt
from scipy import fftpack
import pywt as pwt
import pylab as pl


def hs_pcm(x, bit):
    maxx = np.max(x)
    minx = np.min(x)
    t = maxx - minx
    quiz = t / (2**bit)
    y = quiz * np.round(x / quiz)
    return y


def hs_prd(x, y):
    t = x - y
    s = np.sum(np.square(t))
    r = np.sum(np.square(x - np.mean(x)))
    snr = 100 * np.sqrt(s / r)
    return snr


def hs_tp(x):
    t = np.unique(x)
    p = []
    for i in t:
        p.append(t.count(i))
    return t, np.array(p, dtype = float)


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


def Rwave_detection(x, fsd):
    fs = 2000
    n = int(fsd / fs)
    xs = x[::n]
    fxs = butter_bandpass_filter(xs, 5, 25, fs, 3)
    dfxs = np.diff(fxs)
    hx = fftpack.hilbert(dfxs.reshape(dfxs.size, 1))
    secg = np.abs(np.square(hx))
    i = 1
    ind1 = []
    while (i < len(secg)):
        if (secg[i] > 1e-4):
            ind1.append(i)
            i = i + 750
        else:
            i = i + 1
    ReInd = (np.array(ind1, dtype=int) * fsd / fs).astype(int)
    return ReInd


def runlength_encode(InputX):
    M = InputX.size
    firstIndex = InputX[0]
    i = 0
    j = 0
    R = []
    R.append(1)
    while (i < M - 1):
        if (InputX[i + 1] == InputX[i]):
            R[j] += 1
        else:
            R.append(1)
            j += 1
        i = i + 1
    y = np.array(R, dtype=int)
    return y, firstIndex


def runlength_decode(InputY, firstIndex):
    S = []
    if (firstIndex == 0):
        SencndIndex = 1
    else:
        SencndIndex = 0

    i = 0
    while (i < InputY.size):
        if (np.mod(i, 2) == 0):
            for j in range(0, InputY[i]):
                S.append(firstIndex)
        else:
            for j in range(0, InputY[i]):
                S.append(SencndIndex)
        i = i + 1
    return np.array(S, dtype=int)


def getKvalue(x, prdvalue):
    flag = 0
    K = 0

    list_MaxI = [1, 2, 3, 4, 5]
    list_MaxV = [1, 2, 3, 4, 5]

    decoeffs = []
    coeffs = pwt.wavedec(x, pwt.Wavelet('db8'), level=4)

    for coef in coeffs:
        decoeffs.append(np.zeros(coef.size))

    while (flag == 0):
        for index in range(len(coeffs)):
            list_MaxI[index] = np.argmax(np.abs(coeffs[index]))
            list_MaxV[index] = np.max(np.abs(coeffs[index]))

        tmpMaxI = np.argmax(np.array(list_MaxV, dtype=float))
        decoeffs[tmpMaxI][list_MaxI[tmpMaxI]] = coeffs[tmpMaxI][list_MaxI[
            tmpMaxI]]
        coeffs[tmpMaxI][list_MaxI[tmpMaxI]] = 0
        z = pwt.waverec(decoeffs, 'db8')
        K = K + 1
        if (hs_prd(x, z[0:x.size]) <= prdvalue):
            flag = 1
    pl.plot(x)
    pl.plot(z, 'r')
    pl.show()
    return K


def chooseKmaxValue(inputData, K):
    maxIndex = []
    tempData = np.zeros(1, inputData.size)
    while (K > 0):
        maxIndex = np.max(np.abs(inputData))
        tempData[maxIndex] = inputData[maxIndex]
        maxIndex.append(maxIndex)
        inputData[maxIndex] = 0
        K = K - 1

    IndexArr = np.array(maxIndex, dtype=int)
    nonZeroData = tempData[IndexArr]

    return nonZeroData, IndexArr


def getPcmInfo(x, bit):
    n = 2**bit
    unit = 1 / (2 * n)
    quiz = np.arange(unit, 1, 1 / n)
    lent = x.size

    EValue = np.zeros(1, lent)
    Qindex = np.zeros(1, lent)

    for i in range(lent):
        Qindex[i] = np.argmin(np.abs(x[i] - quiz))
        EValue[i] = x[i] - quiz(Qindex[i])

    return EValue, Qindex

