from PIL import Image, ImageDraw, ImageFont
import os
import requests
import re
import time
import pymysql


def file_extension(path):
    return os.path.splitext(path)[1]


urlall = [[] for i in range(50)]


def traverse(f):
    fs = os.listdir(f)
    id = 0
    global urlall
    walk = 0
    total = len(fs)
    for f1 in fs:
        walk = walk + 1
        tmp_path = os.path.join(f, f1)
        if not os.path.isdir(tmp_path):
            if(tmp_path.find('loli') > -1):
             print('文件: %s' % tmp_path)
             dir=f
             if (file_extension(tmp_path) != '.txt'):
                 watermark(tmp_path)
        else:
            print('文件夹：%s' % tmp_path)
            traverse(tmp_path)


def watermark(file):
    pri_image = Image.open(file)
    finame = file.replace('loli','loli_opt')
    if os.path.exists(finame):
        os.remove(finame)
    if(pri_image.size[0]>1000 or pri_image.size[1]>1000):
     pri_image.resize((round(pri_image.size[0]/2.1), round(pri_image.size[1]/2.1)), Image.ANTIALIAS).save(finame)

    else:
     pri_image.save(finame)



traverse('pack')