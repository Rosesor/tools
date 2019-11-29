# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
#所有json文件的存储目录  json_dir = "C:\\Users\\ASUS\\Desktop\\a"  or something like that
#注意是斜杠是双斜杠
json_dir = "C:\\Users\\ASUS\\Desktop\\a"
count = os.listdir(json_dir)
count.sort(key=lambda x:int(x[:-5]))

#共同头部和尾部里面的"要用\"代替
head = "\"_via_img_metadata\":{"
tail = "},\"_via_attributes\":"

def divide_head(s):
    return s.split(head)[1]
    
def divide_tail(s):
    return s.split(tail)[0]

sum = ""
for j in range(0,len(count)):
    f = open(os.path.join(json_dir,count[j]))
    temp = f.read();
    if (j == 0):
        temp = divide_tail(temp)
        temp += ","
    elif (j == len(count)-1):
        temp = divide_head(temp)
    else :
        temp = divide_head(temp)
        temp = divide_tail(temp)
        temp += ","
    sum += temp
    f.close()
    
print(sum)
fsave = open("sum.json","w")
fsave.write(sum)
fsave.close()
#s = "wo jiao zhiyihang, ni jiao shen me?"
#print(s)
#a = s.split("jiao",1)[0]
#print(a)
