import os

#os.walk()返回的是一个三元tupple(dirpath, dirnames, filenames),
# 第一个为起始路径，第二个为起始路径下的文件夹,第三个是起始路径下的文件.
# 故 SunYoonJoo 文件夹下的所有子文件夹的列表就是 : next(os.walk(path))[1]

#os.path.getsize(filename)


def removelist():
    path = 'D:/SunYoonJoo/'
    dir = []
    for d in next(os.walk(path))[1]:
        dir.append(path+d)



    # dir 里面是每个文件夹的路径 .
    # listdir 列出某目录下的所有文件 .
    # singleDirAllFile 储存单个子目录的所有图片 .
    picpath = []
    for dirpath in dir:
        singleDirAllFile = os.listdir(dirpath)
        for pic in singleDirAllFile:
            picpath.append(dirpath+'/'+pic)
    # D:/SunYoonJoo/160401图片_ins更新2P/e38f572eb9389b503b1568ed8235e5dde6116e02.jpg.jpg
    # 这个图片的大小是 20.8kb ,字节大小是 21371 是可以删除掉的 .
    # if os.path.getsize(xx) < 21371  , os.remove .

    waitingtoberemove = []
    i = 0
    while i < len(picpath):   # 不能用for循环 ,中途删除文件序号会混乱.
        if os.path.getsize(picpath[i]) < 21730:
            waitingtoberemove.append(picpath[i])
    #        os.remove(picpath[i])
        else: pass
        i+=1
    print(waitingtoberemove)

    n = len(waitingtoberemove)
    while n!= 0:
        os.remove(waitingtoberemove[n-1])
        n-=1
removelist()
