import scipy.io as sio  
from pylab import *  
import numpy as np  

matfn=u'HS.mat'  
data=sio.loadmat(matfn) 
xx=data['data']
yy = xx[0:10000]
sio.savemat('normal_HeartSound_Short',{'data': yy})
plot(yy, linewidth=1.0)  
xlabel('x')  
title('Simple plot')  
grid(True)  
savefig("HS.png")  
show()  
plt.close('all')