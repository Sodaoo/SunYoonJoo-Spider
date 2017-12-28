#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# http://tieba.baidu.com/f?kw=%E5%AD%99%E5%85%81%E7%8F%A0&ie=utf-8&pn=8300
# 抓下来的有一些广告页面  需要遍历目录去掉大小 <100kb 的图片 .
from bs4 import BeautifulSoup
import requests
import re
import os
from urllib.parse import quote
# Following are MyPackages
import myproxy
#import TravelTheFile
headers = myproxy.headers

# 贴吧主站每一页的URL
def MainStation_EveryPage():
    url = "http://tieba.baidu.com/f?kw=%E5%AD%99%E5%85%81%E7%8F%A0&ie=utf-8&pn="
    urllist = list()
    l = [x*50 for x in range(0,175)] # 贴吧的结构还有点奇葩啊.......
    for i in l:
        urllist.append(url+str(i))
    return urllist

# 对每一页的每一篇文章的URL进行提取 :
def SingleForumPage_Everyforum(urllist):
    urls = []
    for url in urllist:
        try:
            res = requests.get(url,headers=headers)
            soup = BeautifulSoup(res.content,'lxml')
        except ConnectionError as e:
            with open('D:/FailedForumURL','a') as ff:
                ff.write(url+'\n')
            continue

        for u in soup.find_all('a',attrs={'target':'_blank','rel':'noreferrer','class':'j_th_tit'}):
            if "▼SonYoonJoo▲" not in u['title']: continue
            urls.append('http://tieba.baidu.com'+u['href'])
#    print(len(urls))
    with open('D:/SunYoonJoo.txt','a') as f:
        for i in urls:
            f.write(i+'\n')


# 对每一篇帖子的里的图片进行抓取 .
# 此时我们已经制作好了所有图片"帖子"的URL , 都在 SunYoonJoo.txt 这个文本里面.

def Run():  # 主要的函数逻辑都会在这里实现 .
    urls = ReadSingleForumFromFile()  # 从制作好的文件中读取每一个帖子的URL , 进行图片抓取操作 .
                                         # urls 中保存的就是每个帖子的URL .
    
    while len(urls) > 0: # 从最后一个开始读.抓取成功后就 pop()掉:
        single_url = urls[len(urls) - 1] # 读取最后一个URL .方便pop()
        pics , filename,urls = PictureScrape(single_url,urls)   # 对单个帖子里的图片进行抓取.
        if pics == None and filename == None: continue  # 没有抓到图片 ,说明是视频网页, 则写入FailedURL.txt

        picture = MadeEveryPictureURL(pics)  # 高清图片URL制作到 picture 列表
        PathCreate(picture,filename)  # == None: urls.pop();continue  # 文件夹创建

        SavePictureToDisk(picture,filename) # 保存图片到硬盘 ~~~ 哦也

        SuccessInFile(urls[len(urls)-1])  # 把爬取成功的URL保存到success.txt
        urls.pop()  # 考虑到抓取的速度较慢 .设置重读文件功能 . 

        RewriteSingleForumToOriginal(urls) # 将还剩下的未爬取的 URL 重新写入覆盖文件 .

def ReadSingleForumFromFile():
    urls , pics  = [],[]
    with open('D:/SunYoonJoo.txt') as f: # open('D:/galgame/SunYoonJoo.txt')
        urls = f.readlines() ;
    # 去掉URL 里的 \n
    for i in range(0,len(urls)): urls[i] = urls[i].strip('\n')   # print(urls):
    return urls

def PictureScrape(single_url,urls):  # 对单个帖子里的图片进行抓取. 但是抓到的不是高清 .
    pics = []
    try:
        res = requests.get(single_url,headers=headers)
        soup = BeautifulSoup(res.content,'lxml')
    except: 
        print(single_url,"请求失败")
        urls.pop()
        with open("D:/FailedURL.txt",'a') as f:
            f.write(single_url+'\n')
        return None,None,urls

    filename = soup.find('title').text[12:].replace('_孙允珠吧_百度贴吧','')
    filename = filename.replace('/','').replace('\\','').replace('|','').replace(':','').replace('"','').replace('*','').replace('?','').replace('>','').replace('<','').replace('.','' )

    print('# 还有',len(urls),'条记录. 新贴 url: ',urls[len(urls)-1],'-----------');
    for i in soup.find_all('img',attrs={'class':'BDE_Image'}) :
        pics.append(i['src'])
    return pics,filename,urls


# 是 JS 渲染加载的 , 用requests 获取不到, 用BeautifulSoup 也获取不到 . 所以视频的下载方法
# 应该还是要用 selenium .
def downloadVideo(a):
    pass

# 对抓取完毕的URL 写入Success.txt文件 .
def SuccessInFile(url):
    with open('D:/Success.txt','a') as f:
        f.write(url+'\n')

# 制作图片URL :
# http://imgsrc.baidu.com/forum/pic/item/ 
# pics 里面是抓取的单个帖子里的一期的非高清图片
# return的 picture 里面就全部都是高清图片的 URL 了 .
def MadeEveryPictureURL(pics):
    picture = []
    for pic in pics:
        for index,word in enumerate(pic[::-1]):
            if word == '/':
                picture.append("http://imgsrc.baidu.com/forum/pic/item/"+pic[len(pic)-index: ])
                break
    return picture

#        print(picture)
        # 创建文件夹之后 开始保存 :
def PathCreate(picture,filename):
    if len(picture) > 0:    
        isExists=os.path.exists('D:/SunYoonJoo/'+filename)
        if not isExists:
            os.makedirs('D:/SunYoonJoo/'+filename)

def SavePictureToDisk(picture,filename): # 保存图片到硬盘~~~
    for index,url in enumerate(picture):
        try: r = requests.get(url,headers=headers)
        except: continue
        if r.status_code == 200:
            print('# '+filename+ '  第 '+str(index+1)+' 张....')
            with open('D:/SunYoonJoo/'+filename+'/'+url[39::].replace('?','')+'.jpg','wb') as f:
                f.write(r.content)
        else:
            continue
def RewriteSingleForumToOriginal(urls): # 将还剩下的未爬取的 URL 重新写入覆盖文件 .
    with open('D:/SunYoonJoo.txt','w') as f:  # w: 覆盖,不会追加.
        for i in urls:
            f.write(i+'\n')

# 对Failfile 和 源文件进行去重...一般用不到. 有时候网络挂点
def TestDropCommon():
    with open('D:/SunYoonJoo.txt') as f: # open('D:/galgame/SunYoonJoo.txt')
        urls = f.readlines() ;
    for i in range(0,len(urls)):
        urls[i] = urls[i].strip('\n')   # print(urls)
    urls = list(set(urls))

    print('去重后 : 记录条数 :',len(urls))

    with open('D:/SunYoonJoo.txt','w') as f4:
        for i in urls:
            f4.write(i+'\n')


if __name__ == '__main__':
#    MainStation_EveryPage(SingleForumPage_Everyforum())
    Run()

