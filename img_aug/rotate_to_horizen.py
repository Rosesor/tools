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
from decide_up_or_down import decide_up_or_down
from check_in_box import check_in_box
source_path = 'F:/cocoDataAugment/data/rotate' # 包含json文件及pic
destination_path = 'F:/cocoDataAugment/data/rerotate'#存放json及pic
# source_path = 'F:/cocoDataAugment/data' # 包含json文件及pic
# destination_path = 'F:/cocoDataAugment/rotate'#存放json及pic
angle = [90, 180, 270]

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

def get_degree(point_list, point_o):
    # point_list: n个一维数组，一组八个点，代表一个框 [(x1,y1,x2,y2,...,x8,y8)]
    # point_o: 一个o点的四个坐标,格式与point_list一样
    box_list = []
    for i in range(len(point_list)):
        point = np.array(point_list[i]).reshape((4, 2))
        box_list.append(point)
        p1 = point[0]
        sort = np.argsort(np.sum(np.asarray(p1 - point) ** 2, axis=1))
        p2 = point[sort[2]]
        if p2[0] < p1[0]:
            p1, p2 = p2, p1
        if p2[0] == p1[0]:
            if p1[1] > p2[1]:
                p1,p2 = p2,p1
        # print(p2, p1)
        if i == 0:
            degrees = math.degrees(math.atan2(-p2[1] + p1[1], p2[0] - p1[0]))
            # if degrees == 180.0 or degrees == 360.0:
            if degrees > 90 or degrees < -90:
                degrees = 0
        one_degree = math.degrees(math.atan2(-p2[1] + p1[1], p2[0] - p1[0]))
        if one_degree > 90 or one_degree < -90:
            one_degree = 0
        if i >= 1:
            if abs(degrees-one_degree)>160:
                one_degree = degrees
        degrees = 0.5 * (degrees + one_degree)
    print('origin degree', degrees)
    point_o = np.array(point_o).reshape((4, 2))
    # print(point_o)
    # print(point_o[...,:1])
    # print(point_o[...,1:2])
    # print(sum(point_o[...,:1]))
    # print(sum(point_o[...,1:2]))
    point_o = [sum(point_o[..., :1])/4, sum(point_o[..., 1:2])/4]  # o的中点
    for i in range(len(box_list)):
        if check_in_box(point_o, box_list[i]):
            box_coordinate = box_list[i]
            break
    # sort = np.argsort(np.sum(np.asarray(point_o - box_list) ** 2, axis=1))  # 计算到o点最近的外框点
    # p1 = point[sort[0]]
    # for i in range(len(point_list)):
    #     point = np.array(point_list[i]).reshape((4, 2))
    #     sort = np.argsort(np.sum(np.asarray(p1 - point) ** 2, axis=1))
    #     p2 = point[sort[2]]
    #     p3 = point
    #     if p2[0] < p1[0]:
    #         p1, p2 = p2, p1

    up = 0
    up, left = decide_up_or_down(box_coordinate,point_o)

    if left is True:
        return 360-abs(degrees)
    elif left is False:
        return abs(degrees)
    if degrees > 0:
        return (180-degrees)+up*180
    if degrees < 0:
        if up is True:
            return abs(degrees)
        else:
            return abs(degrees)+180
    else:
        return degrees

def rotation_img(img, angle):
    cols = img.shape[1]
    rows = img.shape[0]
    # print(cols,rows,angle)
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    heightNew = int(cols * math.fabs(math.sin(math.radians(angle))) + rows * math.fabs(math.cos(math.radians(angle))))
    widthNew = int(rows * math.fabs(math.sin(math.radians(angle))) + cols * math.fabs(math.cos(math.radians(angle))))
    M[0, 2] += (widthNew - cols) / 2
    M[1, 2] += (heightNew - rows) / 2
    img = cv2.warpAffine(img, M, (widthNew, heightNew))
    return img, heightNew, widthNew, rows, cols

def rotation_point(w, h , angle, point):
    cols = w
    rows = h
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    heightNew = int(cols * math.fabs(math.sin(math.radians(angle))) + rows * math.fabs(math.cos(math.radians(angle))))
    widthNew = int(rows * math.fabs(math.sin(math.radians(angle))) + cols * math.fabs(math.cos(math.radians(angle))))
    M[0, 2] += (widthNew - cols) / 2
    M[1, 2] += (heightNew - rows) / 2
    a = M[:, :2]
    b = M[:, 2:]
    b = np.reshape(b, newshape=(1, 2))
    a = np.transpose(a)
    # 将point变成两列（x，y)
    point = np.reshape(point, newshape=(int(len(point) / 2), 2))
    # point旋转
    point = np.dot(point, a) + b
    # print(point)
    # point变回一列
    point = np.reshape(point, newshape=(int(len(point) / 4), 8))
    return point

for name in enumerate(file_name(source_path)):
    print(name)
    shape_json = []
    m_path = name[1]
    dir = os.path.dirname(m_path)
    file_json = io.open(m_path, 'r', encoding='utf-8')
    json_data = file_json.read()
    data = json.loads(json_data)
    data_json['imageData'] = None
    data_name = data['imagePath']
    data_path = dir + '/' + data_name
    object_name = os.path.splitext(data['imagePath'])[0]
    point_list = []
    o = np.array([])
    for i in range(len(data['shapes'])):
        point = np.array([])
        assert len(data['shapes'][i]['points']) == 4, object_name+'.jpg has more than 4 points'
        if len(data['shapes'][i]['label']) == 8:
            print(data['shapes'][i]['label'])
            for j in range(0,4):
                point= np.append(point, data['shapes'][i]['points'][j][0])
                point= np.append(point, data['shapes'][i]['points'][j][1])
            point_list.append(point)
        elif data['shapes'][i]['label']=='o' and len(o)==0:
            for j in range(0, 4):
                o = np.append(o, data['shapes'][i]['points'][j][0])
                o = np.append(o, data['shapes'][i]['points'][j][1])

    angle_item = get_degree(point_list, o)
    print('rotate_angel', angle_item)
    img = cv2.imread(data_path)
    im_rotate, newH, newW, orginH, orginW = rotation_img(img, angle_item)
    (filename, extension) = os.path.splitext(data_name)
    data_new_picture_name = destination_path + "/" + filename + "_0" + ".jpg"

    data_new_json_name = destination_path + "/" + filename + "_0" + ".json"
    data_json['imagePath'] = filename + "_0" + ".jpg"
    cv2.imwrite(data_new_picture_name, im_rotate)
    data_json['imageWidth'] = newW
    data_json['imageHeight'] = newH

    for i in range(len(data['shapes'])):
        point = np.array([])
        assert len(data['shapes'][i]['points']) == 4, object_name+'.jpg has more than 4 points'
        for j in range(0, 4):
            point= np.append(point, data['shapes'][i]['points'][j][0])
            point= np.append(point, data['shapes'][i]['points'][j][1])
        m_name_0 = data['shapes'][i]['label']
        data_json_line_color = data['shapes'][i]['line_color']
        data_json_fill_color = data['shapes'][i]['fill_color']
        # data_json_rec = data['shapes'][i]['shape_type']
        data_json_rec = "polygon"
        # print(point)
        point = rotation_point(orginW, orginH, angle_item, point)
        # print(point)
        # img = cv2.imread(data_path)
        # im_rotate, point = rotation_point(img, angle_item, point)
        # (filename, extension) = os.path.splitext(data_name)
        # data_new_picture_name = destination_path + "/" + filename + "_rotate" + ".jpg"
        # print(data_new_picture_name)
        # data_new_json_name = destination_path + "/" + filename + "_rotate" + ".json"
        # data_json['imagePath'] = filename + "_rotate" + ".jpg"
        # cv2.imwrite(data_new_picture_name, im_rotate)
        # im_rotate = cv2.imread(data_new_picture_name)
        # data_json['imageWidth'] = im_rotate.shape[1]
        # data_json['imageHeight'] = im_rotate.shape[0]
        shape_json_item = {"label": m_name_0,
                           "line_color": data_json_line_color,
                           "fill_color": data_json_fill_color,
                           "points": [[point[0][0], point[0][1]],
                                      [point[0][2], point[0][3]],
                                      [point[0][4], point[0][5]],
                                      [point[0][6], point[0][7]]],
                           "shape_type": data_json_rec}
        shape_json.append(shape_json_item)
    data_json['shapes'] = shape_json
    data_info = json.dumps(data_json, ensure_ascii=False,indent=2)
    fp = open(data_new_json_name, "w+")
    fp.write(data_info)
    fp.close()