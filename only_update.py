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
             if (file_extension(tmp_path) != '.txt'):
                 resultfile = tmp_path
                 print(resultfile)
                 url = post_img(resultfile)
                 time.sleep(5)
                 idd = re.sub("\D", "", f)
                 urlall[int(idd)].append(url)
        else:
            print('文件夹：%s' % tmp_path)
            traverse(tmp_path)



def post_img(file):
    url = "https://sm.ms/api/upload"
    files = {'smfile': open(file, 'rb')}
    r = requests.post(url, files=files)
    result = str(r.text)
    print(result)
    urlpos = result.find("url")
    print(urlpos)

    deletepos = result.find("delete")
    print(deletepos)
    get = result[urlpos:deletepos]
    return clean(get)


def clean(get):
    get = get.replace("url", "")
    get = get.replace('"', "")
    get = get.replace(':', "")
    get = get.replace(',', "")
    get = get.replace("https", "")
    get = get.replace("\\", "")
    print(get)
    return get






def update_mysql_work():
    global urlall
    db = pymysql.connect("ip", "name", "password", "database")
    cursor = db.cursor()
    for i in range(len(urlall)):
        allresult = 's'
        if (i != 0):
            print(i, urlall[i])
            for w in range(len(urlall[i])):
                if(allresult=='s'):
                    allresult=urlall[i][w]
                else:
                 allresult = allresult + "|"+urlall[i][w]
            print(allresult)
            if(allresult!='s'):
             sql = "UPDATE article SET imgUrl='" + allresult + "' where id='" + str(i) + "';"
             print(sql)
             cursor.execute(sql)
             db.commit()
    db.close()



traverse('pack')
for i in range(len(urlall)):
    print(i,urlall[i])
update_mysql_work()