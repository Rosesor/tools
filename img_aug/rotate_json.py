# -*- coding: utf-8 -*-
import os
import sys
import json
import io
import random
import re
import cv2
import numpy as np
from random import choice
import math
from PIL import Image

source_path = 'F:/cocoDataAugment/data'
destination_source_path = 'F:/cocoDataAugment/rotate/random'
angle = [10,20,30,40,50,60,70,80,90]

article_info = {}
data_json = json.loads(json.dumps(article_info,indent=4))
print(data_json)
data_json['version'] = '3.16.7'
data_json['flags'] = {}
data_json["lineColor"] = [
    0,
    255,
    0,
    128
]
data_json["fillColor"] = [
    255,
    0,
    0,
    128
]


def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.json':
                L.append(os.path.join(root, file))
        return L

def rotation_point(img, angle, point):
    cols = img.shape[1]
    rows = img.shape[0]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    heightNew = int(cols * math.fabs(math.sin(math.radians(angle))) + rows * math.fabs(math.cos(math.radians(angle))))
    widthNew = int(rows * math.fabs(math.sin(math.radians(angle))) + cols * math.fabs(math.cos(math.radians(angle))))
    M[0, 2] += (widthNew - cols) / 2
    M[1, 2] += (heightNew - rows) / 2
    img = cv2.warpAffine(img, M, (widthNew, heightNew))
    a = M[:, :2]
    b = M[:, 2:]
    b = np.reshape(b, newshape=(1, 2))
    a = np.transpose(a)
    # 将point变成两列（x，y)
    point = np.reshape(point, newshape=(int(len(point) / 2), 2))
    # point旋转
    point = np.dot(point, a) + b
    # point变回一列
    point = np.reshape(point, newshape=(int(len(point) / 4), 8))

    x_rate = img.shape[1]/1280
    y_rate = img.shape[0]/1024
    widthNew=1280
    heightNew=1024

    img = img.resize((1280,1024),Image.BILINEAR)
    point = np.reshape(point, newshape=(int(len(point) / 2), 2))
    # point旋转
    for i in range(0,len(point)):
        point[i][0]=point[i][0]/x_rate
        point[i][1]=point[i][1]/y_rate
    # point变回一列
    point = np.reshape(point, newshape=(int(len(point) / 4), 8))
    return img, point, heightNew, widthNew

# for a in range(len(angle)):
destination_path = destination_source_path #+'/'+str(angle[a])
if not os.path.isdir(destination_path):
    os.mkdir(destination_path)
print(destination_path)
for angle_index in range(len(angle)):
    for name in enumerate(file_name(source_path)):
        shape_json = []
        m_path = name[1]
        dir = os.path.dirname(m_path)
        file_json = io.open(m_path, 'r', encoding='utf-8')
        json_data = file_json.read()
        data = json.loads(json_data)
        data_json['imageData'] = None
        data_name = data['imagePath']
        data_path = dir + '/' + data_name
        angle_item = angle[angle_index]
        object_name = os.path.splitext(data['imagePath'])[0]
        for i in range(len(data['shapes'])):
            point = np.array([])
            assert len(data['shapes'][i]['points']) == 4, object_name+'.jpg has more than 4 points'
            for j in range(0,4):
                point= np.append(point, data['shapes'][i]['points'][j][0])
                point= np.append(point, data['shapes'][i]['points'][j][1])
            m_name_0 = data['shapes'][i]['label']
            data_json_line_color = data['shapes'][i]['line_color']
            data_json_fill_color = data['shapes'][i]['fill_color']
            img = cv2.imread(data_path)
            im_rotate, point, data_json['imageHeight'], data_json['imageWidth'] = rotation_point(img, angle_item, point)
            (filename, extension) = os.path.splitext(data_name)
            data_new_picture_name = destination_path + "/" + str(angle_item) + "/"+filename + "_" + str(angle_item) + ".jpg"
            data_new_json_name = destination_path + "/" + str(angle_item) + "/" + filename + "_" + str(angle_item) + ".json"
            if not os.path.exists(str(destination_path + "/" + str(angle_item) + "/")):
                os.mkdir(str(destination_path + "/" + str(angle_item) + "/"))
            data_json['imagePath'] = filename + "_" + str(angle_item) + ".jpg"
            cv2.imwrite(data_new_picture_name, im_rotate)
            # im_rotate = cv2.imread(data_new_picture_name)
            # data_json['imageWidth'] = im_rotate.shape[1]
            # data_json['imageHeight'] = im_rotate.shape[0]
            shape_json_item = {"label": m_name_0,
                               "line_color": data_json_line_color,
                               "fill_color": data_json_fill_color,
                               "points": [[point[0][0], point[0][1]],
                                          [point[0][2], point[0][3]],
                                          [point[0][4], point[0][5]],
                                          [point[0][6], point[0][7]]]
                               }
            shape_json.append(shape_json_item)
        data_json['shapes'] = shape_json
        data_info = json.dumps(data_json, ensure_ascii=False,indent=2)
        fp = open(data_new_json_name, "w+")
        fp.write(data_info)
        fp.close()