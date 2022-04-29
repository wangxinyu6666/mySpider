# -*- codeing = utf-8 -*-
import socket
import time
import requests
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
#import sqlite3  # 进行SQLite数据库操作

# 创建正则表达式对象详情链接的规则
findLink = re.compile(r'<a href="(.*?)" ')
findTitle = re.compile(r'<a href="(.*?)" ')

def main():
    baseurl = "https://www.xxdx.xyz/list.php?class=guochan"  #要爬取的网页链接
    # baseurl = "https://www.xxdm.xyz"  # 要爬取的网页链接
    # 1.爬取网页
    datalist = getData(baseurl)
    savepath = "国产.xls"    #当前目录新建XLS，存储进去
    # dbpath = "book.db"              #当前目录新建数据库，存储进去
    # 3.保存数据
    saveData(datalist, savepath)      #2种存储方式可以只选择一种
    # saveData2DB(datalist,dbpath)

# 爬取网页
def getData(baseurl):
    datalist = []  #用来存储爬取的网页信息
    for i in range(0, 1):  # 调用获取页面信息的函数，10次
        # 第i页URL
        url = baseurl
        html = askURL(url)  # 保存获取到的网页源码
        # 2.逐一解析数据
        # soup = BeautifulSoup(html, "html.parser")
        # print(soup)
        print(html)
        j = 0
        for item in soup.find_all(class_="list"):  # 查找符合要求的字符串
            j = j + 1
            sum = i*50 + j
            data = []  # 保存一个小视频的标题
            item = str(item)
            print(item)
            print( "-----------------以下是第"+str(i)+"页,第 "+str(sum) +"个链接------------------------------------------")

    return datalist

# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 98.0.4758.136  Safari / 537.36"
       }
    # 用户代理，表示告诉服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
    # request = urllib.request.Request(url, headers=head)

    html = ""
    i = 1
    while i == 1:
        i = 0
        try:
            # response = urllib.request.urlopen(request, timeout=100)
            # html = response.read().decode("utf-8")
            # response.close()
            html = requests.get("https://www.xxdx.xyz/list.php?class=guochan", headers=head)
            print(html.content)
        except urllib.error.URLError as e:
            i = 1
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
    return html

# 保存数据
def saveData(datalist, savepath):
    print("save.......")

if __name__ == "__main__":  # 当程序执行时
    # 调用函数
     main()
    # init_db("movietest.db")
     print("爬取完毕！")

