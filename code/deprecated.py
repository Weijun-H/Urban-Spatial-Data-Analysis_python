# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 21:38:33 2020

@author: richie
"""

'''01'''
import numpy as np
import math
mu_list=[0,0,0,-2,2]
sigmaSquare_list=[0.2,1.0,5.0,0.5,1.0]
normalDistr_paras=zip(mu_list,[math.sqrt(sig2) for sig2 in sigmaSquare_list])#配置多个平均值和标准差对
s_list=[np.random.normal(para[0], para[1], 1000) for para in normalDistr_paras]
n=0
for s in s_list:
    sns.kdeplot(s,label="μ=%s, σ2=%s"%(mu_list[n],sigmaSquare_list[n]))
    n+=1    
plt.legend()   



### 1.2 卡方分布
#### 1.1.1 卡方分布
def n_ND(n=5,size=1000):    
    from scipy import stats
    import numpy as np
    import seaborn as sns
    '''
    function-生成n个服从标准正态分布相互独立的随机变量,均值和平方差累积增加
    
    Params:
    n - 生成的变量数
    size - 随机数数量
    '''
    locs=np.array([[val*10 for val in list(range(n))]]).cumsum()
    scales=np.array([[val*1 for val in list(range(n))]]).cumsum()
    x_lst=[]
    for i in range(n):
        x=stats.norm.rvs(loc=locs[i],scale=scales[i],size=1000)
        x_zscore=stats.zscore(c)
        kstest_test=stats.kstest(x_zscore,cdf='norm')
        if kstest_test.pvalue>0.05:
            x_lst.append(x)
        else:
            print("%d-x is not normally distribted."%i)
    x_array=np.array(x_lst)

    i=0
    for x_ in x_array:
        sns.distplot(x_,bins=30,hist=False,label="%.1f,%.1f"%(x_.mean(),np.std(x_)))
        i+=1
    return x_array

x_array=n_ND(n=3,size=1000)
x_quadraticSum=np.square(x_array).sum(axis=0)

import matplotlib.pyplot as plt
plt.figure()
sns.distplot(x_quadraticSum,bins=30,hist=False,label="")





