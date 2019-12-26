# -*- coding: utf-8 -*-
# author = 'IReverser'

import os
import io
import json

import cal_IoU as cI

json_path = 'H:\\data\\train_single\\'

label_len = 0
true = 0
acc = 0

def cal_box_acc(test_box):
    for i in range(len(test_box)):

        img_name = test_box[i]['image_name']
        data_label_len = 8   # 检测的特定的label长度
        m_path = json_path+img_name+'.json'
        file_json = io.open(m_path, 'r', encoding='utf-8')

        json_data = file_json.read()
        data = json.loads(json_data)
        data_label = data['shapes']

        for i in range(0, len(data_label)):
            find_labeling = data_label[i]
            find_label = find_labeling['label']
            if len(find_label) == data_label_len:
                label_len = label_len + 1
                box_real = find_labeling['points']   # 四边形四个点坐标的一维数组表示，[x,y,x,y....]
                box_real[:] = cI.multi_array2array(box_real)
                for j in range(len(test_box[i]['box_list'])):
                    box_detect = test_box[i]['box_list'][j]
                    value = cI.cal_IoU(box_real, box_detect)
                    if value > 0.9:
                        true = true + 1

    print float(true)/label_len


