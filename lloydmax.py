import numpy as np

def lloydmax_sig(Signal, bit, tol):
    minx = np.min(Signal)
    maxx = np.max(Signal)
    n = 2**bit
    quiz = (maxx-minx)/n
    Initial = np.arange(minx+quiz/2,maxx,quiz)
    L = Initial.size         # Number of quantization levels 
    breakpoints = np.zeros(L-1)    # Breakpoints for levels 
    Old_Sum = 1        # Old Sum for iterations 
    New_Sum = 0
    ############################### 
    # Max - Lloyd Algorithm # 
    while (abs(Old_Sum-New_Sum) > tol ):
        # Updating breakpoints # 
        breakpoints = 0.5*(Initial[0:L-1]+Initial[1:L])
        
        # Updating levels 
        Old_Sum = New_Sum
        New_Sum = 0    
        # Avoid getting zero # 
        if (np.sum(np.where(Signal < breakpoints[0]) )>=1 ):
            Initial[0] = np.mean(Signal[np.where(Signal < breakpoints[0])])
            New_Sum += np.sum(np.linalg.norm(Signal[np.where(Signal < breakpoints[0])]-Initial[0]))                                
        for i in range(1,L-1): 
            if (np.sum( np.logical_and(Signal>breakpoints[i-1],Signal<breakpoints[i]))>=1) :
                Initial[i] = np.mean(Signal[np.logical_and(Signal>breakpoints[i-1],Signal<breakpoints[i])])
                New_Sum += np.sum(np.linalg.norm(Signal[np.logical_and(Signal>breakpoints[i-1],Signal<breakpoints[i])]-Initial[i])) 
        if (np.sum(np.where(Signal>breakpoints[L-2])) >= 1 ):
            Initial[L-1] = np.mean(Signal[np.where(Signal>breakpoints[L-2])])
            New_Sum += np.sum(np.linalg.norm(Signal[np.where(Signal>breakpoints[L-2])]-Initial[L-1]))

    return Initial


def hs_Qlmax(InputX, Centers):
    z = []
    for i in range(len(InputX)):
       index = np.argmin(np.abs(InputX[i]-Centers))
       z.append(Centers[index])

    return np.array(z, dtype = float)