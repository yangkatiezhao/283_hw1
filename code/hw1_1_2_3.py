import numpy as np
from numpy.linalg import cholesky
import matplotlib.pyplot as plt
import math
import tensorflow as tf
from tensorflow.python.framework import ops
ops.reset_default_graph()
import random
import pandas as pd
from numpy import dot
from numpy.linalg import inv

# Create graph
sess = tf.Session()

# =============================================================================
# 1)

sampleNo = 200;

s0 = np.zeros((sampleNo,2))
s1 = np.zeros((sampleNo,2))

mu = np.array([0.,0.])
lambda_1 = 2.
u_1 = np.array([1.,0.])
lambda_2 = 1.
u_2 = np.array([0.,1.])
mean = [0.,0.]
con = [[2.,0.],[0.,1.]]
s0[:,0],s0[:,1] = np.random.multivariate_normal(mean,con,sampleNo).T
plt.plot(s0[:,0],s0[:,1],'+')
plt.show()

piA = 1./3.
muA = np.array([-2.,1.])
lambdaA_1 = 2.
uA_1 = np.array([math.cos(-3.*math.pi/4.),math.sin(-3.*math.pi/4.)])
lambdaA_2 = 1./4.
uA_2 = np.array([-math.sin(-3.*math.pi/4.),math.cos(-3.*math.pi/4.)])
piB = 2./3.
muB = np.array([3.,2.])
lambdaB_1 = 3.
uB_1 = np.array([math.cos(math.pi/4.),math.sin(math.pi/4.)])
lambdaB_2 = 1.
uB_2 = np.array([-math.sin(math.pi/4.),math.cos(math.pi/4.)])

s1_1 = np.zeros((sampleNo,2))
s1_2 = np.zeros((sampleNo,2))

mean_cla = [-2.,1.]
mean_clb = [3.,2.]
con_cla = [[1.125,0.875],[0.875,1.125]]
con_clb = [[2.,1.],[1.,2.]]
s1_1[:,0],s1_1[:,1] = np.random.multivariate_normal(mean_cla,con_cla,sampleNo).T
s1_2[:,0],s1_2[:,1] = np.random.multivariate_normal(mean_clb,con_clb,sampleNo).T

for i in range(sampleNo):
    a = random.randint(0,8)
    if a<3:
        s1[i,0] = s1_1[i,0]
        s1[i,1] = s1_1[i,1]
    else:
        s1[i,0] = s1_2[i,0]
        s1[i,1] = s1_2[i,1]

plt.plot(s0[:,0],s0[:,1],'g+')
plt.plot(s1[:,0],s1[:,1],'rx')
plt.show()

total_xs = np.concatenate((s0,s1))
tmp0 = np.zeros((sampleNo,1))
tmp1 = np.ones((sampleNo,1))
total_ys = np.concatenate((tmp0,tmp1))

# =============================================================================
# 2)

def G(x,m,C):
    de = C[0][0]*C[1][1] - C[0][1]*C[1][0]
    return (math.pi**(-1.)) * de**(-0.5) * math.exp( (-1./2.)*(np.mat(x-m))*inv(C)*((np.mat(x-m)).T) )

h = 0.2
x0_min,x0_max = total_xs[:,0].min()-1, total_xs[:,0].max()+1
x1_min,x1_max = total_xs[:,1].min()-1, total_xs[:,1].max()+1
xx0, xx1 = np.meshgrid(np.arange(x0_min, x0_max, h),
                     np.arange(x1_min, x1_max, h))
i_range,j_range = xx0.shape
zz = np.zeros((i_range,j_range))
for i in range(i_range):
    for j in range(j_range):
#        print(xx0[i,j],xx1[i,j])
        x0_now = xx0[i,j]
        x1_now = xx1[i,j]
        zz[i,j] = (1/3)*G([x0_now,x1_now],muA,con_cla) + (2/3)*G([x0_now,x1_now],muB,con_clb) - G([x0_now,x1_now],mu,con)

plt.contour(xx0,xx1,zz,[0],cmap=plt.cm.Paired)
plt.plot(s0[:,0],s0[:,1],'g+')
plt.plot(s1[:,0],s1[:,1],'rx')
plt.show()
 
# =============================================================================
# 3)

j = 0
for i in range(sampleNo):
    x0_now = total_xs[i,0]
    x1_now = total_xs[i,1]
    if (1./3.)*G([x0_now,x1_now],muA,con_cla) + (2./3.)*G([x0_now,x1_now],muB,con_clb) - G([x0_now,x1_now],mu,con) >=0.:
        j +=1
for i in range(sampleNo):
    x0_now = total_xs[i+sampleNo,0]
    x1_now = total_xs[i+sampleNo,1]
    if (1./3.)*G([x0_now,x1_now],muA,con_cla) + (2./3.)*G([x0_now,x1_now],muB,con_clb) - G([x0_now,x1_now],mu,con) <0.:
        j +=1

error_ratio = (1.0*j)/(2.0*sampleNo)   
print (error_ratio)  

np.save("total_xs_no1.npy",total_xs)
np.save("total_ys_no1.npy",total_ys)