# -*- coding: utf-8 -*-
"""
Created on Mon May 20 09:43:48 2019

@author: AUSU
"""

import lmdb

env = lmdb.open("E:\\yihang\\database-sar\\sar10_rotate\\lmdb_train",readonly=True)
txn = env.begin()
cur = txn.cursor()
count = 0
for key,value in cur:
    print('key:',key)
    print(str(value[0:10]))
    print('...'+value[-5:])
    count = count + 1
    if count>20:
        break
env.close()