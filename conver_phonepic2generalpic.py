import cv2 as cv
import os, re

# In project, I meet an issue when read img size via Image.open().size
# img that take by different phone have different argues
# which lead to worry output by Image.open().size like mix (h,w) and (w,h)
# so before training neuron net work, we need to convert img.

# shape=(height, width, channel)
img_dir = 'E:\\moudle_8_train\\origin\\'
outdir = 'E:\\moudle_8_train\\alter_pic\\'  # should end with \\
for root, dirs, files in os.walk(img_dir):
    for file in files:
        print(file)
        img = cv.imread(img_dir+file)
        exit()
        print(outdir+file)
        cv.imwrite(outdir+file, img)
# save
