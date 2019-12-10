# -*-coding:utf-8-*-
#
#  test.py
#  DataTest
#
#  Created by zhoujianwen on 2019/5/1.
#  Copyright © 2019年 Clement. All rights reserved.
#

from PIL import Image
import os
import cPickle
import json
import glob
import io
import shutil
import sys
# from scipy.spatial import distance as dist
import numpy as np
import math

reload(sys)
sys.setdefaultencoding('utf-8')
from matplotlib.path import Path


def format_output():
    res = open(os.path.join('./', 'test.txt'), 'w')
    for i in range(len(lines) - 2):
        res.write(",".join(str(j) for j in lines[i]))
    res.write(",".join(str(i) for i in lines[len(lines) - 1]))
    res.write('\n')
    res.close()


def check_points():
    lines = []
    index = 0
    labelme_json = glob.glob('/media/wyu/software/new_image/300_json/*.json')
    for num, json_file in enumerate(labelme_json):
        with open(json_file, 'r') as fp:
            data = json.load(fp)
            for shapes in data['shapes']:
                if len(shapes['points']) % 2 or not len(shapes['points']) % 6 or not len(shapes['points']) % 8:
                    index = index + 1
                    lines.append(str.format('id:{0},{1}.jpg,坐标数量：{2}\n', index, json_file.split('/')[-1].split('.')[0],
                                            len(shapes['points'])))
    f = open(os.path.join('./', 'error_log.txt'), 'w')
    for i in lines:
        f.write(str(i))
    f.close()


def check_label_len(num):
    lines = []
    index = 0
    path = '/media/wyu/software/new_image/300_json/*.json'  # './data/train/*.json'
    labelme_json = glob.glob(path)
    for num, json_file in enumerate(labelme_json):
        with open(json_file, 'r') as fp:
            data = json.load(fp)
            for shapes in data['shapes']:
                if len(shapes['label']) > 1 and len(shapes['label']) <= 4 or len(
                        shapes['label'].strip()) == 0:  # =1 is char,=0 or =2 is error,>2 is datatime
                    print
                    data['imagePath'], shapes['label']
                    index = index + 1
                    lines.append(str.format('id:{0},{1},{2},标签长度：{3}\n', index, data['imagePath'], shapes['label'],
                                            len(shapes['label'])))

    outpath = './'
    f = open(os.path.join(outpath, 'error_log2.txt'), 'w')
    for i in lines:
        f.write(str(i))
    f.close()


class biaozhu(object):
    def __init__(self, label, points, ds):
        self.label = label
        self.points = points
        self.ds = ds
        self.charbox = []

    def __repr__(self):
        return repr((self.label, self.points, self.ds, self.charbox))


# this function is confined to rectangle
def order_points(pts):
    # sort the points based on their x-coordinates
    xSorted = pts[np.argsort(pts[:, 0]), :]

    # grab the left-most and right-most points from the sorted
    # x-roodinate points
    leftMost = xSorted[:2, :]
    rightMost = xSorted[2:, :]

    # now, sort the left-most coordinates according to their
    # y-coordinates so we can grab the top-left and bottom-left
    # points, respectively
    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    (tl, bl) = leftMost

    # now that we have the top-left coordinate, use it as an
    # anchor to calculate the Euclidean distance between the
    # top-left and right-most points; by the Pythagorean
    # theorem, the point with the largest distance will be
    # our bottom-right point
    D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
    (br, tr) = rightMost[np.argsort(D)[::-1], :]

    # return the coordinates in top-left, top-right,
    # bottom-right, and bottom-left order
    return np.array([tl, tr, br, bl], dtype="float32")


class biaozhubox(object):
    def __init__(self, label, points, ds, ce):
        self.label = label
        self.points = points
        self.ds = ds
        self.charbox = []
        self.ce = ce

    def __repr__(self):
        return repr((self.label, self.points, self.ds, self.charbox, self.ce))


def json2txt():
    file_path = '/media/tyy/TOSHIBA EXT/roation2/*.json'  # 存储.txt的地方
    # file_path = './100/*.json'
    labelme_json = glob.glob(file_path)
    for num, json_file in enumerate(labelme_json):
        with open(json_file, 'r') as fr:
            # print(json_file)
            data = json.load(fr)
            boxs = []
            index = 0
            for shapes in data['shapes']:  # 统计检测框数量，父级检测框boxs
                if len(shapes['label'].strip()) > 1:
                    if len(shapes['points']) == 2:
                        rect = shapes['points']
                        x1_box = rect[1][0] if rect[0][0] > rect[1][0] else rect[0][0]  # min_x
                        y1_box = rect[1][1] if rect[0][1] > rect[1][1] else rect[0][1]  # min_y
                        x3_box = rect[0][0] if rect[0][0] > rect[1][0] else rect[1][0]  # max_x
                        y3_box = rect[0][1] if rect[0][1] > rect[1][1] else rect[1][1]  # max_y
                        x2_box, y2_box = [x3_box, y1_box]
                        x4_box, y4_box = [x1_box, y3_box]
                    else:
                        polygons = order_points(np.array(shapes['points']))
                        point = polygons
                        x1_box, y1_box = point[0]
                        x2_box, y2_box = point[1]
                        x3_box, y3_box = point[2]
                        x4_box, y4_box = point[3]

                    ds = np.sqrt(np.square(0 - x1_box) + np.square(0 - y1_box))
                    ce_x = (x1_box + x3_box) / 2
                    ce_y = (y1_box + y3_box) / 2
                    label = shapes['label'].replace(' ', '')
                    boxs.append(
                        biaozhubox(label, [[x1_box, y1_box], [x2_box, y2_box], [x3_box, y3_box], [x4_box, y4_box]], ds,
                                   [ce_x, ce_y]))

            for box in boxs:  # 父级检测框关联字符框boxs
                # 获取父级检测框的坐标
                x1_box, y1_box = [float(i) for i in box.points[0]]
                x2_box, y2_box = [float(i) for i in box.points[1]]
                x3_box, y3_box = [float(i) for i in box.points[2]]
                x4_box, y4_box = [float(i) for i in box.points[3]]
                for shapes in data['shapes']:  # 添加字符框char
                    label = shapes['label'].replace(' ', '')
                    if len(label) > 1:
                        continue
                    if len(shapes['points']) == 2:
                        rect = shapes['points']
                        x1 = rect[1][0] if rect[0][0] > rect[1][0] else rect[0][0]  # min_x
                        y1 = rect[1][1] if rect[0][1] > rect[1][1] else rect[0][1]  # min_y
                        x3 = rect[0][0] if rect[0][0] > rect[1][0] else rect[1][0]  # max_x
                        y3 = rect[0][1] if rect[0][1] > rect[1][1] else rect[1][1]  # max_y
                        x2, y2 = [x3, y1]
                        x4, y4 = [x1, y3]
                    else:
                        # print data['imagePath']
                        polygons = order_points(np.array(shapes['points']))
                        point = polygons.astype(np.float)
                        x1, y1 = point[0]
                        x2, y2 = point[1]
                        x3, y3 = point[2]
                        x4, y4 = point[3]
                    ds = np.sqrt(np.square(x1_box - x1) + np.square(y1_box - y1))
                    ce_x = (x1 + x3) / 2
                    ce_y = (y1 + y3) / 2
                    # ds = format((x1+y1+x2+y2+x3+y3+x4+y4)/8,'.2f')
                    points = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
                    if len(boxs) == 1:
                        box.charbox.append(biaozhubox(label, points, ds, [ce_x, ce_y]))
                    else:  # 图片超过1个父级标签就执行下面语句
                        if (
                        Path([(x1_box, y1_box), (x2_box, y2_box), (x3_box, y3_box), (x4_box, y4_box)]).contains_points(
                                [(ce_x, ce_y)])):
                            box.charbox.append(biaozhubox(label, points, ds, [ce_x, ce_y]))
                        # else:
                        #     print data['imagePath']  #输出漏检的字符框

                box.charbox = sorted(box.charbox, key=lambda biaozhubox: biaozhubox.ds)
            # 父级标签和子级标签关联完就按照指定格式输出到txt文件
            (filepath, tempfilename) = os.path.split(file_path)
            # print(filepath)
            # (filename, extension) = os.path.splitext(tempfilename)
            with open(os.path.join(filepath + '/', str.format('{0}.txt', data['imagePath'])),
                      'w') as fw:  # 把相关数据写入.txt文件
                for box in boxs:
                    x1_box, y1_box = box.points[0]
                    x2_box, y2_box = box.points[1]
                    x3_box, y3_box = box.points[2]
                    x4_box, y4_box = box.points[3]
                    if box.label.find('合') >= 0 or box.label.find('格') >= 0:
                        box.label = box.label.replace('合', '').replace('格', '')
                    fw.write(
                        str.format('{0},{1},{2},{3},{4},{5},{6},{7},{8},', x1_box, y1_box, x2_box, y2_box, x3_box,
                                   y3_box, x4_box, y4_box, box.label))
                    for j in range(len(box.charbox) - 1):
                        # if box.charbox[j].label.find('合')>=0 or box.charbox[j].label.find('格')>=0:
                        #      continue
                        point = box.charbox[j].points
                        x1, y1 = [float(i) for i in point[0]]
                        x2, y2 = [float(i) for i in point[1]]
                        x3, y3 = [float(i) for i in point[2]]
                        x4, y4 = [float(i) for i in point[3]]
                        fw.write(
                            str.format('{0},{1},{2},{3},{4},{5},{6},{7},{8},', x1, y1, x2, y2, x3, y3, x4, y4,
                                       box.charbox[j].label))
                    if len(box.charbox) < 1:
                        print(data['imagePath'], shapes['label'])
                        continue
                    point = box.charbox[len(box.charbox) - 1].points
                    x1, y1 = [float(i) for i in point[0]]
                    x2, y2 = [float(i) for i in point[1]]
                    x3, y3 = [float(i) for i in point[2]]
                    x4, y4 = [float(i) for i in point[3]]
                    fw.write(str.format('{0},{1},{2},{3},{4},{5},{6},{7},{8}\r\n', x1, y1, x2, y2, x3, y3, x4, y4,
                                        box.charbox[len(box.charbox) - 1].label))
                    # fw.write('\r\n')
            fw.close()
        fr.close()


def divide():
    # coding=utf-8

    import os
    import os.path
    import shutil

    import numpy as np

    source_dir = '/media/tyy/TOSHIBA EXT/roation2/'  # 图片存储的文件夹名称
    # 30%的数据生成验证集
    val_dir = '/home/tyy/Desktop/Product_date/masktext/lib/datasets/data/moulde_val/val_images/'
    # 70%的数据生成训练集
    train_dir = '/home/tyy/Desktop/Product_date/masktext/lib/datasets/data/moulde_train/train_images/'
    # 70%的数据生成训练集
    test_dir = '/home/tyy/Desktop/Product_date/masktext/lib/datasets/data/moulde_test/test_images/'
    source_dir = 'G:/roation2/'  # 图片存储的文件夹名称
    # 30%的数据生成验证集
    val_dir = 'F:/cocoDataAugment/data/1-10/val_images/'
    # 70%的数据生成训练集
    train_dir = 'F:/cocoDataAugment/data/1-10/train_images/'
    # 70%的数据生成训练集
    test_dir = 'F:/cocoDataAugment/data/1-10/test_images/'
    n = 793  # 图片的数量
    start_iter = 72 # start
    angle = 36 #最后的角度 35+1

    f1 = file(val_dir + "val_list.txt", "a+")
    f2 = file(train_dir + "train_list.txt", "a+")
    f3 = file(test_dir + "test_list.txt", "a+")
    array = start_iter + np.arange(n)  # 产生长度为n的序列\
    np.random.shuffle(array)  # 将arrray序列随机排列

    i = 1 # 文件数量计算
    for file_single in range(0, n):
        if i in range(1,int(n*0.6+1)):
                # 0-0.6  20%
                # jpg file
                # json file
            for j in range(1, angle):
                shutil.copy(source_dir + str(array[i-1]) + '_' + str(int(j * 10)) + '.jpg', train_dir)
                # shutil.copy(source_dir + file_single.split('.')[0] + '.json', train_dir)
                shutil.copy(source_dir + str(array[i-1]) + '_' + str(int(j * 10)) + '.jpg.txt', train_dir)
                f2.write(str(array[i-1]) + '_' + str(int(j * 10)) + '.jpg' + '\n')
        elif i in range(int(n*0.6+1) + 1,int(n*0.8+1)):
                # 0.6-0.8  20%
                # jpg file
                # json file
            for j in range(1, angle):
                shutil.copy(source_dir + str(array[i-1]) + '_' + str(int(j * 10)) + '.jpg', val_dir)
                # shutil.copy(source_dir + file_single.split('.')[0] + '.json', val_dir)
                shutil.copy(source_dir + str(array[i-1]) + '_' + str(int(j * 10)) + '.jpg.txt', val_dir)
                f1.write(str(array[i-1]) + '_' + str(int(j * 10)) + '.jpg' + '\n')
        else:
                # 0.8-1.0 20%
            for j in range(1, angle):
                shutil.copy(source_dir + str(array[i-1]) + '_' + str(int(j * 10)) + '.jpg', test_dir)
                # shutil.copy(source_dir + file_single.split('.')[0] + '.json', test_dir)
                shutil.copy(source_dir + str(array[i-1]) + '_' + str(int(j * 10)) + '.jpg.txt', test_dir)
                f3.write(str(array[i-1]) + '_' + str(int(j * 10)) + '.jpg' + '\n')
        print('n pic', i)
        i = i + 1
    f1.close()
    f2.close()
    f3.close()
        # for root, dirs, files in os.walk(source_dir):
        #     l = len(files) / 3
        # for file_single in files:
        #     if 'txt' not in file_single and 'json' not in file_single:
        #         for j in range(0, 36):
        #             if i < int(l * 0.6):
        #                 # 0-0.6  20%
        #                 # jpg file
        #                 # json file
        #                 shutil.copy(source_dir + file_single.split('.')[0] + '_' + int(j*10) + '.jpg', train_dir)
        #                 # shutil.copy(source_dir + file_single.split('.')[0] + '.json', train_dir)
        #                 shutil.copy(source_dir + file_single.split('.')[0] + '_' + int(j*10) + '.jpg.txt', train_dir)
        #                 f2.write(file_single + '\n')
        #                 i = i + 1
        #             elif i < int(l * 0.8) and i >= math.ceil(l * 0.6):
        #                 # 0.6-0.8  20%
        #                 # jpg file
        #                 # json file
        #                 shutil.copy(source_dir + file_single.split('.')[0] + '_' + int(j*10) + '.jpg', val_dir)
        #                 # shutil.copy(source_dir + file_single.split('.')[0] + '.json', val_dir)
        #                 shutil.copy(source_dir + file_single.split('.')[0] + '_' + int(j*10) + '.jpg.txt', val_dir)
        #                 f1.write(file_single + '\n')
        #                 i = i + 1
        #             else:
        #                 # 0.8-1.0 20%
        #                 shutil.copy(source_dir + file_single.split('.')[0] + '_' + int(j*10) + '.jpg', test_dir)
        #                 # shutil.copy(source_dir + file_single.split('.')[0] + '.json', test_dir)
        #                 shutil.copy(source_dir + file_single.split('.')[0] + '_' + int(j*10) + '.jpg.txt', test_dir)
        #                 f3.write(file_single + '\n')
        #                 i = i + 1
        #     else:
        #         continue
        # f1.close()
        # f2.close()
        # f3.close()


if __name__ == '__main__':
    print('reading......')
    # json2txt()
    divide()

'''
python 两个list 求交集，并集，差集

listA = [1,3,65,2,7]
listB = [3,2,5,4]

c = [x for x in listA if x in listB]
d = [y for y in (listA+listB) if y not in c]

print(c)
print(d)

def diff(listA,listB):
    #求交集的两种方式
    retA = [i for i in listA if i in listB]
    retB = list(set(listA).intersection(set(listB)))

    print "retA is: ",retA
    print "retB is: ",retB

    #求并集
    retC = list(set(listA).union(set(listB)))
    print "retC1 is: ",retC

    #求差集，在B中但不在A中
    retD = list(set(listB).difference(set(listA)))
    print "retD is: ",retD
'''
