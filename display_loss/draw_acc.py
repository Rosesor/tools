#!/usr/bin/env python
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import math
import re
import pylab
from pylab import figure, show, legend
from mpl_toolkits.axes_grid1 import host_subplot
 
def align(l1,l2):
    if len(l1)>len(l2):
        l1.pop()
    if len(l1)<len(l2):
        l2.pop()
    print(len(l1),len(l2))
    
f=open("E:\\yihang\\caffe_sar\\log\\log_info_20190615-153239.13284","r")
lines = f.readlines()
print("open")
TrainAcc=[]
TrainIter=[]
ValAcc=[]
TestAcc=[]
TestIter=[]

for line in lines:
    #print(line)
    pattern = re.compile(r"Iteration \d+, loss")
    if re.search("Iteration \d+, loss",line):
        Iter=re.search(pattern,line)
        # num = re.findall(r"0\.\d*",line)
        # print(Iter.group(0))
        s1=Iter.group(0)
        pattern = re.compile(r"\d+")
        Iter_num=re.search(pattern,s1)
        #print(type(Iter_num.group(0)))
        Iter_num=int(Iter_num.group(0))
        TrainIter.append(Iter_num)
        continue
    pattern = re.compile(r"Train net output #(\d+): accuracy = (0?.?\d+)")
    if re.search(pattern,line):
        Acc=re.search(pattern,line)
        s2=Acc.group(2)
        Acc_num = float(s2)
        TrainAcc.append(Acc_num)
        continue
    pattern = re.compile(r"Iteration \d+, Testing net")
    if re.search(pattern,line):
        Iter=re.search(pattern,line)
        # num = re.findall(r"0\.\d*",line)
        # print(Iter.group(0))
        s1=Iter.group(0)
        pattern = re.compile(r"\d+")
        Iter_num=re.search(pattern,s1)
        #print(type(Iter_num.group(0)))
        Iter_num=int(Iter_num.group(0))
        TestIter.append(Iter_num)
        continue
    pattern = re.compile(r"Test net output #(\d+): accuracy = (0?.?\d+)")
    if re.search(pattern,line):
        Acc=re.search(pattern,line)
        s2=Acc.group(2)
        Acc_num = float(s2)
        TestAcc.append(Acc_num)
        continue
        #TrainIter.append(int(Iter_num.group(0)))
        #TrainIter.append(int(re.findall("\d+",Iter)))

#        if len(num) != 0:
#            TrainAcc.append(float(num))
#        else:
#            TrainAcc.append(float(1))
        #TrainAcc.append(re.findall)
#print(TrainAcc,TrainIter)
s1 = f.name
align(TrainIter,TrainAcc)
align(TestIter,TestAcc)
plt.plot(TrainIter,TrainAcc,label="TrainAcc")
plt.plot(TestIter,TestAcc,label="TestAcc")
plt.yticks([0,0.8,0.85,0.9,0.95,1])
plt.grid()
plt.legend(loc='upper left')
plt.savefig(s1+"Acc"+".pdf")
plt.show()


#p=plt.plot(TrainIter,TrainAcc)
#plt.plot(a,b)
#plt.show()
#f.close()