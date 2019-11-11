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
import time

def align(l1,l2):
    if len(l1)>len(l2):
        l1.pop()
    if len(l1)<len(l2):
        l2.pop()
    print(len(l1),len(l2))

for t in range(1):
    f=open("E:\\yihang\\caffe_sar\\log\\log_info_20190615-153239.13284","r")
    lines = f.readlines()
    
    TrainAcc=[]
    TrainIter=[]
    ValAcc=[]
    TestAcc=[]
    TestIter=[]
    TrainLoss=[]
    TestLoss=[]
    
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
    #    pattern = re.compile(r"Train net output #(\d+): accuracy = (0?.?\d+)")
    #    if re.search(pattern,line):
    #        Acc=re.search(pattern,line)
    #        s2=Acc.group(2)
    #        Acc_num = float(s2)
    #        TrainAcc.append(Acc_num)
    #        continue
        pattern = re.compile(r"Train net output #(\d+): loss = (\d+?.?\d+)")
        if re.search(pattern,line):
            Loss=re.search(pattern,line)
            s3=Loss.group(2)
            Loss_num = float(s3)
            TrainLoss.append(Loss_num)
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
    #    pattern = re.compile(r"Test net output #(\d+): accuracy = (0?.?\d+)")
    #    if re.search(pattern,line):
    #        Acc=re.search(pattern,line)
    #        s2=Acc.group(2)
    #        Acc_num = float(s2)
    #        TestAcc.append(Acc_num)
    #        continue
        pattern = re.compile(r"Test net output #(\d+): loss = (\d+?.?\d+)")
        if re.search(pattern,line):
            Loss=re.search(pattern,line)
            s2=Loss.group(2)
            Loss_num = float(s2)
            TestLoss.append(Loss_num)
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
    # plt.plot(TrainIter,TrainAcc)
    align(TrainIter,TrainLoss)
    align(TestIter,TestLoss)
    plt.figure(s1)    
    plt.ylim(0,100)
    plt.plot(TrainIter,TrainLoss,label="TrainLoss")
    # plt.plot(TestIter,TestAcc)
    plt.plot(TestIter,TestLoss,label="TestLoss")
    plt.show()
    time.sleep(20)
    t = t+1
plt.plot(TrainIter,TrainLoss,label="TrainLoss")
    # plt.plot(TestIter,TestAcc)
plt.plot(TestIter,TestLoss,label="TestLoss")
plt.legend(loc='upper left')
plt.savefig(s1+"Loss_br=-7"+".pdf")
#p=plt.plot(TrainIter,TrainAcc)
#plt.plot(a,b)
#plt.show()
#f.close()