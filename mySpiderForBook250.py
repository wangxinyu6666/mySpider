# -*- codeing = utf-8 -*-
import requests
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作

# 创建正则表达式对象详情链接的规则
findLink = re.compile(r'<a href="(.*?)" ')
findImgSrc = re.compile(r'<img src="(.*?)" ', re.S) # <img src="https://img1.doubanio.com/view/subject/s/public/s1070959.jpg"
findTitle1 = re.compile(r'<a href="(.*?)" onclick="(.*?)" title="(.*?)">(.*?)</a>', re.S)
findTitle2 = re.compile(r'<span style="font-size:12px;">(.*)</span>') # <span style="font-size:12px;">Cien años de soledad</span>
findRating = re.compile(r'<span class="rating_nums">(.*)</span>')
findJudge = re.compile(r'<span class="pl">(.*?)</span>', re.S)
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="pl">(.*?)</p>', re.S)

def main():
    baseurl = "https://book.douban.com/top250?start="  #要爬取的网页链接
    # 1.爬取网页
    datalist = getData(baseurl)

    savepath = "豆瓣读书Top250.xls"    #当前目录新建XLS，存储进去
    # dbpath = "book.db"              #当前目录新建数据库，存储进去
    # 3.保存数据
    saveData(datalist, savepath)      #2种存储方式可以只选择一种
    # saveData2DB(datalist,dbpath)

# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

# 解析网页
def getData(baseurl):
    datalist = []  #用来存储爬取的网页信息
    img_name_list = []
    img_link_list = []
    for i in range(0, 10):  # 调用获取页面信息的函数，10次
        # 第i页URL
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页源码
        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        j = 0
        for item in soup.find_all('table'):  # 查找符合要求的字符串
            j = j + 1
            sum = i*25 + j
            data = []  # 保存一本书的所有信息
            # 下面两个列表，因为需要下载书的封面，额外又定义了两个，方面操作
            img_name_list = []
            img_link_list = []

            item = str(item)
            # print(item)   # 获得一本书的内容了
            print( "-----------------以下是第"+ str(sum) +"本书的内容------------------------------------------")

            # 一本书的标题1
            title1 = re.findall(findTitle1, item)[0][2]
            data.append(title1.strip())
            img_name_list.append(title1.strip())

            print(title1.strip()) #去掉空格
            # 一本书的标题2
            title2 = re.findall(findTitle2, item)
            # print(type(title2))
            # print(title2)
            if len(title2) != 0:
                if len(title2) == 1: # 说明是例如 《三体：地球往事》这一类的书名
                    # 去掉前面的冒号
                    title = title2[0].replace(":", "")  # 消除转义字符

                    data.append(title.strip())
                else:
                    data.append(title2[1])
                    # print(title2[1])
            else:
                data.append(" ")
                # print("--------------------没有标题2----------------------")
            # 一本书的评分
            linkRating = re.findall(findRating, item)[0]
            data.append(linkRating)
            # print(linkRating)

            # 一本书有多少人评分
            judgeNum = re.findall(findJudge, item)[0]
            judgeNum1 = judgeNum.replace("/n", " ")
            judgeNum = judgeNum1.replace("(", " ")
            judgeNum = judgeNum.replace(")", " ")
            data.append(judgeNum.strip())
            # print(judgeNum.strip())
            # 一本书的相关信息(可能有的书没有)
            inq = re.findall(findInq, item)
            # print(type(inq))
            if len(inq) != 0:
                data.append(inq)
                # print(inq)
            else:
                data.append(" ")
            # 本书出版信息
            linkBd = re.findall(findBd, item)[0]
            data.append(linkBd)
            # print(linkBd)
            # 一本书的链接
            linkInfor = re.findall(findLink, item)[0]
            data.append(linkInfor)
            # print(linkInfor)

            # 一本书图片的链接
            linkImgSrc = re.findall(findImgSrc, item)[0]
            data.append(linkImgSrc)
            img_link_list.append(linkImgSrc)
            # print(linkImgSrc)
            # 图片保存到本地
            getImgData(img_name_list, img_link_list)
            datalist.append(data) # 一个data就是一本的书的信息，所以每次添加到总共datalist里面

            print(data)
    return datalist

# 保存图片到本地
def getImgData(img_name_list, img_link_list):
    len_img = len(img_name_list)
    # print(len_img)
    # 创建循环
    for num in range(0, len_img):
        # print(num)
        wallpaper_img = requests.get(img_link_list[num])
        # print(img_name_list[num] + "-----访问成功")
        # 获取网页内容
        wallpaper_img = wallpaper_img.content
        # 写入文件
        path = r'D://Projects//Pictures//BooksImg'
        with open(path + "./" + img_name_list[num] + ".jpg", "wb+") as img_write:
            img_write.write(wallpaper_img)
            print(img_name_list[num] + "-----写入成功")
            img_write.close()

# 保存数据
def saveData(datalist, savepath):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('豆瓣读书Top250', cell_overwrite_ok=True)
    col = ( "书名1", "书名2", "评分", "评价数", "概况", "相关信息", "书籍详情链接", "书籍图片链接",)
    sheet.col(0).width = 8000
    sheet.col(1).width = 8000
    sheet.col(2).width = 2000
    sheet.col(3).width = 4000
    sheet.col(4).width = 13000
    sheet.col(5).width = 20000
    sheet.col(6).width = 8000
    sheet.col(7).width = 13000

    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(0, 250):
        print("第%d本书信息存储完毕"%(i+1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i+1, j, data[j])
    book.save(savepath)

if __name__ == "__main__":  # 当程序执行时
    # 调用函数
     main()
    # init_db("movietest.db")
     print("爬取完毕！")
