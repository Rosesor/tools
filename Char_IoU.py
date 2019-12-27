# -*- coding: utf-8 -*-
# author = 'jie'


import os
import io
import json
import re

import cal_IoU as cI

label_txt_path = '/home/jie/Desktop/product_date/masktext/lib/datasets/data/moudle_8_test/test_gts/'


def cal_box_acc(test_box):
    true = 0
    label_len = 0
    extra = 0
    miss = 0
    for i in range(len(test_box)):
        label = get_one_box(label_txt_path,test_box[i]['image_name'])
        label_len = label_len + len(label['box_list'])
        if len(label['box_list'])>=len(test_box[i]['box_list']):
            for j in range(len(label['box_list'])):
                flag = 0
                for k in range(len(test_box[i]['box_list'])):
                    value = cI.cal_IoU(label['box_list'][j], test_box[i]['box_list'][k])
                    if value > 0:
                        true = true + 1
                        flag = 1
                        break
                if flag == 0:
                    print(label['image_name'])
            miss = miss+len(label['box_list'])-len(test_box[i]['box_list'])
        else:
            for j in range(len(label['box_list'])):
                flag = 0
                for k in range(len(test_box[i]['box_list'])):
                    value = cI.cal_IoU(label['box_list'][j], test_box[i]['box_list'][k])
                    if value > 0:
                        true = true + 1
                        flag = 1
                        break
                if flag == 0:
                    print(label['image_name'])
                # if flag == 1:
                #     break

            extra = extra + len(test_box[i]['box_list']) - len(label['box_list'])
    print(true)
    print(label_len)
    return float(true)/label_len, extra, miss

def get_test_box(path):
    dirs = os.listdir(path)
    files = []
    test_box = []

    for i in dirs:
        if 'char' in i and 'txt' in i:  # 筛选txt文件
            files.append(path+i)

    for file in files: # 遍历文件夹
        # print(file)
        t = {}
        t['box_list'] = []
        t['image_name'] = file.split('char_')[-1].split('.')[0]
        f = open(file)  # 打开文件
        iter_f = iter(f)  # 创建迭代器
        for line in iter_f:  # 遍历文件，一行行遍历，读取文本
            box_coordinate = re.findall(r'［(.*)］;',line)
            box_coordinate = box_coordinate[0]
            box_coordinate = box_coordinate.split(',')
            box_coordinate = [int(x) for x in box_coordinate]
            t['box_list'].append(box_coordinate)
        test_box.append(t)
    return test_box

def get_one_box(label_txt_path,name):
    label = {}
    label['image_name'] = name
    f = open(label_txt_path+name+'.jpg.txt')  # 打开文件
    iter_f = iter(f)  # 创建迭代器
    label['box_list'] = []
    for line in iter_f:  # 遍历文件，一行行遍历，读取文本
        box_coordinate = re.findall(r',\d,',line)
        if len(box_coordinate) < 1:
            print(name)
        box_coordinate = box_coordinate[0]
        box_coordinate = box_coordinate.split(',')
        box_coordinate = map(float, box_coordinate)
        label['box_list'].append(box_coordinate)
    return label

t_box = get_test_box('/home/jie/Desktop/product_date/masktext/results/train/rotate_train/moudle_8_test/model_final.pkl_results/result_final/')
# t_box = get_test_box('/home/jie/Desktop/product_date/masktext/results/train/rotate_train/moudle_8_test/model_final.pkl_results/test/')

print(cal_box_acc(t_box))