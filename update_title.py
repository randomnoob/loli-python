import urllib
from bs4 import BeautifulSoup
import lxml
import re
from urllib.parse import urlparse
import urllib
import urllib.request
import urllib.parse
import http.cookiejar
import os
import operate_txt
import pymysql

global title
global downloadurl
global baidu_ver
global tagall
global pwd


def get_content(url):
    global title
    global downloadurl
    global baidu_ver
    global tagall
    global pwd
    content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content, "lxml")
    content1 = str(soup.find(name='blockquote', attrs={}))

    if (len(content1) < 100 or content1.find('点击下载') <= -1):
        # print(content1)
        print('retry', url + '/2')
        return get_content(url + '/2')
    else:

        title = str(soup.find('title'))
        title = title.replace("<title>", "")
        title = title.replace("</title>", "")
        title = title.replace("百度云下载", "")
        title = title.replace("-第2页", "")

        tag = soup.find_all(name='a', attrs={"rel": "tag"})
        print(tag)
        tagall = 'nope'
        for i in range(len(tag)):
            tagnow = tag[i].get_text()
            if (tagall == 'nope'):
                tagall = tagnow
            else:
                tagall = tagall + '|' + tagnow

        return content1


def log_in():
    hosturl = 'http://mosaic/wp-login.php'
    posturl = 'http://mosaic/wp-login.php'
    cj = http.cookiejar.LWPCookieJar()
    cookie_support = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    h = urllib.request.urlopen(hosturl)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
               'Referer': '******'}
    postData = {"log": "name",
                "pwd": "password",
                "remember": "forever",
                "wp-submit": "%E7%99%BB%E5%BD%95&",
                "redirect_to": "http://mosaic"
                }
    postData = urllib.parse.urlencode(postData).encode('utf-8')
    request = urllib.request.Request(posturl, postData, headers)
    print(request)
    response = urllib.request.urlopen(request)
    text = response.read()
    print(text)


def txt_wrapp(start_str, end, html):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            result = html[start:end].strip()
            return str(result)


def get_link(url):
    global title
    global downloadurl
    global baidu_ver
    global tagall
    global pwd
    content1 = get_content(url)
    print(content1)
    downloadurl = txt_wrapp('href', 'rel', content1)
    downloadurl = downloadurl.replace('"', "")
    downloadurl = downloadurl.replace(' ', "")
    downloadurl = downloadurl.replace('=', "")

    soup = BeautifulSoup(content1, "lxml")
    baidu_ver = soup.find(name='span', attrs={})
    baidu_ver = baidu_ver.get_text()

    pwd = txt_wrapp('密码：', '<', content1)




import time
def update_mysql_work(id):
    global title
    global downloadurl
    global baidu_ver
    global tagall
    global pwd
    db = pymysql.connect("ip", "name", "password", "database",use_unicode=True, charset="utf8")
    cursor = db.cursor()
    sql = "UPDATE article SET downloadUrl='" + str(downloadurl) + "' where id='" + str(id) + "';"
    cursor.execute(sql)
    sql = "UPDATE article SET name='" + str(title) + "' where id='" + str(id) + "';"
    cursor.execute(sql)
    sql = "UPDATE article SET type='" + str(tagall) + "' where id='" + str(id) + "';"
    cursor.execute(sql)
    now = time.strftime('%m-%d',time.localtime(time.time()))
    sql = "UPDATE article SET date='" + str(now) + "' where id='" + str(id) + "';"
    cursor.execute(sql)
    db.commit()
    db.close()




def file_extension(path):
    return os.path.splitext(path)[1]


def traverse(f):
    fs = os.listdir(f)
    for f1 in fs:
        tmp_path = os.path.join(f, f1)
        if not os.path.isdir(tmp_path):

            if (file_extension(tmp_path) == '.txt'):
                if (tmp_path.find('count.txt') <= -1):
                    print('处理文件: %s' % tmp_path)
                    idd = re.sub("\D", "", f)
                    text = str(operate_txt.read_txt(tmp_path))
                    text = text.replace("\n", "")
                    text = text.replace(" ", "")
                    print(idd, text)
                    handle(text,idd)
        else:
            print()
            print('文件夹：%s' % tmp_path)
            traverse(tmp_path)


def handle(url,id):
    global title
    global downloadurl
    global baidu_ver
    global tagall
    global pwd
    get_link(url)

    downloadurl = downloadurl + "|" + baidu_ver + "|" + pwd
    print("链接：", url)
    print("标题：", title)
    print("下载链接|提取码|解压密码：", downloadurl)
    print('标签：', tagall)
    update_mysql_work(id)

log_in()
traverse('TITLE')
