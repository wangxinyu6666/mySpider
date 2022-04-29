import requests
from bs4 import BeautifulSoup
from mySpiderForBook250 import askURL
import re
baseurl = "https://book.douban.com/top250?start="  #要爬取的网页链接
html = askURL(baseurl)
# 获取我们的HTML解释器
soup = BeautifulSoup(html, 'html.parser')

findImgSrc = re.compile(r'<img src="(.*?)" ', re.S) # <img src="https://img1.doubanio.com/view/subject/s/public/s1070959.jpg"
findTitle1 = re.compile(r'<a href="(.*?)" onclick="(.*?)" title="(.*?)">(.*?)</a>', re.S)
img_name_list = []
img_link_list = []
j = 0
for item in soup.find_all('table'):  # 查找符合要求的字符串
    j = j + 1
    # data = []  # 保存一本书的所有信息
    # 定义储存列表
    item = str(item)
    print(item)   # 获得一本书的内容了
    print("-----------------以下是第" + str(j) + "本书的内容------------------------------------------")
    # 一本书图片的标题
    title1 = re.findall(findTitle1, item)[0][2]
    img_name_list.append(title1.strip())
    print(title1.strip())  # 去掉空格
    # 一本书图片的链接
    linkImgSrc = re.findall(findImgSrc, item)[0]
    img_link_list.append(linkImgSrc)
    print(linkImgSrc)

print("解析完毕")

print("开始获取下载链接")

len_img = len(img_name_list)
# print(len_img)
# 创建循环
for num in range(0, len_img):
    # print(num)
    wallpaper_img = requests.get(img_link_list[num])
    print(img_name_list[num] + "-----访问成功")
    # 获取网页内容
    wallpaper_img = wallpaper_img.content
    # print(type(wallpaper_img))
    # 写入文件
    path = r'D://Projects//Pictures'
    with open(path+ "./" + img_name_list[num] + ".jpg", "wb+") as img_write:
        img_write.write(wallpaper_img)
        print(img_name_list[num] + "-----写入成功")
        img_write.close()
