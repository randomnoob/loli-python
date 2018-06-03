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
            if (tmp_path.find('loli') <= -1):
                if (file_extension(tmp_path) != '.txt'):
                    os.remove(tmp_path)
                    print('文件-REMOVED: %s' % tmp_path)
        else:
            print('文件夹：%s' % tmp_path)
            traverse(tmp_path)


def traversee(f):
    fs = os.listdir(f)
    id = 0
    global urlall
    walk = 0
    total = len(fs)
    for f1 in fs:
        walk = walk + 1
        tmp_path = os.path.join(f, f1)
        if not os.path.isdir(tmp_path):
            if (tmp_path.find('opt') <= -1):
                if (file_extension(tmp_path) != '.txt'):
                    os.remove(tmp_path)
                    print('文件-REMOVED: %s' % tmp_path)
        else:
            print('文件夹：%s' % tmp_path)
            traversee(tmp_path)


traverse('pack')
traversee('pack')
