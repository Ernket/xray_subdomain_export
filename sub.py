import sys
import re
import os
import time
import requests
#import traceback

def findurl(re_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    response = requests.get(re_url, headers=headers)
    a=response.url
    try:
        ul=re.findall('//(.*)\.baidu.com',a)
        return ul[0]+".baidu.com"
    except:
        print("跳转到了非baidu.com站点...")

#判断是否存在文件名
try:
    filename = sys.argv[1]
    #w_filename=sys.argv[2]
except:
    print("Usage: python Elapse.py <subdomain file> #d<saved file name>")
    time.sleep(3)
    sys.exit(0)

#检测文件是否存在，并自动往后查询
def check_file(filename):
    filelist=[]
    #判断是否存在类似500-sub.html的格式
    file_num=re.findall('(\d*)-.*\.html',filename)
    if file_num:
        num=int(file_num[0])
        initfile=filename.replace(str(num)+"-",'')
    else:
        #如果没有，那就初始化为0
        num=0
    while True:
        a=os.path.isfile(filename)
        if a:
            filelist.append(filename)
            num+=500
            filename=str(num)+"-"+initfile
        else:
            
            print("文件: "+filename+" 不存在，正在导出列表...")
            return filelist 

checkexist=check_file(filename)
num=1
for forname in checkexist:
    w_filename="result-"+str(num)+".txt"
    sub_file = open(forname,"r",encoding="utf-8")
    write_file=open(w_filename,"a",encoding='UTF-8')

    #sub用于判断是否重复
    sub=[]

    for i in sub_file:
        # 无脑匹配url和状态码和title
        result=re.findall(r'{"link":"(.*?)","status":(.*?),"title":"(.*?)","server',i)
        try:
            url=result[0][0]
            http_code=result[0][1]
            title=result[0][2]
            if http_code != "200":
                print("状态码非200，正在跳过处理...")
                continue
            repeat=findurl(url)
            if repeat in sub:
                print("检测到302跳转后类似泛解析，正在跳过处理...")
            else:
                sub.append(repeat)
                write_file.write(url+"\n")
                print("成功写入一条数据...")
                print("url: "+url+" code: "+http_code+" title: "+title)
        except:
            print("这行未检测到内容...")
            #traceback.print_exc()
            pass

    sub_file.close()
    write_file.close()
    num+=1