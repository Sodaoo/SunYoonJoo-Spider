<h2>爬虫特点</h2>
1. Python3 爬虫 Requests + BeautifulSoup
2. 爬取的都是高清图片(原图). 
    网上的很多爬虫代码基本都是不清晰的压缩图片
3. 模特孙允珠非常漂亮...


<h2>爬取思路</h2>
Requests + BeautifulSoup
高清原图是不在贴吧帖子里的 . 你需要另外去发掘 
经测试 , 高清的原图的链接是这个 :http://imgsrc.baidu.com/forum/pic/item/+.............

<h2> 3文件说明</h2>
1. SunYoonJoo.py  这个是主文件 ,包括目录的生成 ,页面的抓取 ,图片的爆粗你都是在这个文件进行的.
2. TravelTheFile.py  这个主要是为了去掉抓取过程中误抓下来的广告页面 .
3. myproxy.py   设置代理 , 有时候抓取的过程中会遇到连续的抓取失败 , 这时候就是该设置代理的时候了...

# SunYoonJoo-Spider
a spider scraping the http://tieba.baidu.com/f?kw=%CB%EF%D4%CA%D6%E9&amp;fr=ala0&amp;loc=rec
待抓取网站的构造 :
![..](https://wx2.sinaimg.cn/mw690/006wh4bKly1fmwvimon1pj30je0gujtv.jpg) <br>

<br>




