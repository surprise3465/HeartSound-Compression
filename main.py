import scipy.io as sio  
import pylab as pl
from ufun import *

matfn=u'ECG.mat'  
data1=sio.loadmat(matfn) 
RawECGData=data1['AA']
EcgData = RawECGData.reshape(1,RawECGData.size)[0]
matfn=u'HS.mat'  
data2=sio.loadmat(matfn) 
RawHsData=data2['data']
HsData=RawHsData.reshape(1,RawHsData.size)[0]
HS=hs_pcm(HsData,16)

fs = 4000
prdc=10#%预设失真度
p=5#%一级量化位数
CN=256#%码数大小
k=8#%矢量量化数
k1=3#%关联周期数
R=48#%单次处理周期数
start=1#%起始周期

tind=Rwave_detection(EcgData,fs)#%心音分段
tlen=np.diff(tind[start:start+R])#
meanh=np.mean(HS[tind[start]:tind[start+R]-1])#
HS[tind[start]:tind[start+R]-1]=HS[tind[start]:tind[start+R]-1]-meanh#
indr=np.argmax(tlen)#
HStrain=HS[tind[start+indr-1]:tind[start+indr]-1]
K=getKvalue(HStrain,prdc)#%获取稀疏度Kmax

#获取非零系数，拆分为位置流，幅度流，和残差流
WK=np.zeros(R,K)
WS=np.zeros(R,K)
indamp=np.zeros(R,K)
Evalue=np.zeros(R,K)
xlen=0

for i in range(R):
"""
    [WC, infor(i).CL]=wavedec(HS(tind(start+i-1):tind(start+i)-1),4,'db8')#%四层小波变换
    [WK(i,:), indone]=kchoose(WC,K)#%获取非零系数和位置流
    [rlc, s(i)]=rlencode(indone)#%位置流游程编码
    infor(i).len=length(rlc)#
    [infor(i).t1, infor(i).yc1, infor(i).Htree1]=hfencode(rlc)#%位置流霍夫曼编码
    xlen=xlen+length(infor(i).yc1)#%记录位置流码长
    maxamp(i)=max(WK(i,:))#minamp(i)=min(WK(i,:))# %归一化
    WS(i,:)=(WK(i,:)-minamp(i))/(maxamp(i)-minamp(i))#
    [Evalue(i,:),indamp(i,:)]=getamp(WS(i,:), p)#%一级量化，获取残差系数和幅度下标
    """
