
from PIL import Image
import os.path
import glob
def convertjpg(jpgfile,outdir):
    img=Image.open(jpgfile)
    width=int(img.size[0]/3)   #按比例
    height=int(img.size[1]/3)
    new_img=img.resize((width,height),Image.BILINEAR)  
    new_img.save(os.path.join(outdir,os.path.basename(jpgfile)))

for jpgfile in glob.glob("G:\\newtop\\test1\\*.jpg"):   #图片路径
    convertjpg(jpgfile,"G:\\newtop\\test2")  #保存路径