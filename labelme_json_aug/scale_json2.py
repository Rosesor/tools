# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 10:48:28 2019

@author: 介
"""

# 修改json
import re
import os
import cv2
# scale json file for different resolution ratio.
# when we downsample img, its json file so change too

######config:#######
# dir is origin json storage document, should end with \\
# img_dir is origin img storage document should end with \\
# outdir is new json storage document should end with \\
# count is the first json file you want, and rest file should be named one by one like
# 1.json, 2.json
# not 1.json, 3.json, which exclude 2.json
dir = 'E:\\moudle_8_train\\json\\'
img_dir = 'E:\\moudle_8_train\\alter_pic\\'
outdir = 'E:\\\moudle_8_train\\new_json\\' # should end with \\

def aterpolygon(file, xrate, yrate, outdir):
    with open(file, "r") as f1:
        with open(outdir + file.split('\\')[-1], "w") as f2:
            for line in f1:
                if "points" in line:
                    # skip to number line
                    f2.write(line)
                    line = next(f1)
                    f2.write(line)

                    # read and handle coordinate
                    line = next(f1)
                    # line = "123,"   x1 = 123
                    x1 = float(line.split(',')[0])/xrate
                    x1 = '          ' + str(x1) + ',\n'
                    f2.write(x1)
                    line = next(f1)
                    y1 = float(line) / yrate
                    # print("y1", y1)
                    y1 = '          ' + str(y1) + '\n'
                    f2.write(y1)

                    #as x1 and y1 before
                    line = next(f1)
                    f2.write(line)
                    line = next(f1)
                    f2.write(line)
                    line = next(f1)
                    x2 = float(line.split(',')[0]) / xrate
                    x2 = '          ' + str(x2) + ',\n'
                    f2.write(x2)
                    line = next(f1)
                    y2 = float(line) / yrate
                    y2 = '          ' + str(y2) + '\n'
                    f2.write(y2)

                    line = next(f1)
                    f2.write(line)
                    line = next(f1)
                    f2.write(line)
                    line = next(f1)
                    # print(line)
                    x3 = float(line.split(',')[0]) / xrate
                    x3 = '          ' + str(x3) + ',\n'
                    f2.write(x3)
                    line = next(f1)
                    y3 = float(line) / yrate
                    y3 = '          ' + str(y3) + '\n'
                    f2.write(y3)

                    line = next(f1)
                    f2.write(line)
                    line = next(f1)
                    f2.write(line)
                    line = next(f1)
                    # print(line)
                    x4 = float(line.split(',')[0]) / xrate
                    # print("x4", x4)
                    x4 = '          ' + str(x4) + ',\n'
                    f2.write(x4)
                    line = next(f1)
                    y4 = float(line) / yrate
                    y4 = '          ' + str(y4) + '\n'
                    f2.write(y4)
                elif "imageData" in line:
                    if len(line) > 100:
                        imgData = line.split(':')[0] + ": null\n"
                        f2.write(imgData)
                    else:
                        imgData = line.split(':')[0]+": null,\n"
                        f2.write(imgData)
                elif "imageHeight" in line:
                    imgHeight = float(re.findall(r"\d+\.?\d*", line)[0])/yrate
                    f2.write('  \"imageHeight\": ' + str(int(imgHeight)) + ',\n')
                elif "imageWidth" in line:
                    imgWidth = float(re.findall(r"\d+\.?\d*", line)[0])/xrate
                    f2.write('  \"imageWidth\": ' + str(int(imgWidth)) + '\n')
                else:
                    # as f1
                    f2.write(line)

for root, dirs, files in os.walk(dir):
    for file in files:
        print(img_dir+file.split('.')[0]+'.jpg')
        shape = cv2.imread(img_dir+file.split('.')[0]+'.jpg').shape
        aterpolygon(dir+file, shape[1]/1280, shape[0]/1024, outdir)
        print(img_dir+file, ' :size is ', shape, '\n\t rate is ', shape[1]/1280, shape[0]/1024)

#aterpolygon(f, 2, 'C:\\Users\\植一航\\Desktop\\delect2\\107.json')

