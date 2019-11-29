# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import re
import matplotlib.pyplot as plt
import numpy as np

def main():
    file = open('E:\yihang\caffe_sar\log\log_info_20190423-162247.12608','r')
    list = []
    # search the line including accuracy
    for line in file:
        m=re.search('Train-mse', line)
        if m:
            n=re.search('[0]\.[0-9]+', line) # 正则表达式
            if n is not None:
                list.append(n.group()) # 提取精度数字
    file.close()
    plt.plot(list, 'go')
    plt.plot(list, 'r')
    plt.xlabel('count')
    plt.ylabel('accuracy')
    plt.title('Accuracy')
    plt.show()

if __name__ == '__main__':
    main()