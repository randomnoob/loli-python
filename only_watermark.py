from PIL import Image, ImageDraw, ImageFont
import os
import requests
import re
import time
import pymysql


def file_extension(path):
    return os.path.splitext(path)[1]


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
            if (tmp_path.find('loli') <= -1):
                print('文件: %s' % tmp_path)
                id = id + 1
                dir = f
                if (file_extension(tmp_path) == '.txt'):
                    id = id - 1
                else:
                    resultfile = watermark(tmp_path, dir, str(id) + ".jpg")
        else:
            print('文件夹：%s' % tmp_path)
            traverse(tmp_path)




def write(fname, content):
    if os.path.exists(fname):
        os.remove(fname)
    print(fname)
    fobj = open(fname, 'w')
    fobj.write(content)
    fobj.close()


def watermark(file, dir, name):
    im = Image.open(file).convert('RGBA')
    txt = Image.new('RGBA', im.size, (0, 0, 0, 0))
    fnt = ImageFont.truetype("c:/Windows/fonts/Tahoma.ttf", round(txt.size[0] / 16.98))
    d = ImageDraw.Draw(txt)
    d.text((round(txt.size[0] / 1.46), round(txt.size[1] - 250)), "mosaic.com", font=fnt, fill=(254, 67, 101, 200))
    out = Image.alpha_composite(im, txt)
    pa = os.path.join(dir, "loli_" + name)
    if os.path.exists(pa):
        os.remove(pa)
    out = out.convert('RGB')
    out.save(pa)
    return pa


traverse('pack')
