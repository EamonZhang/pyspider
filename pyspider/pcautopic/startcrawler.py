#!/usr/bin/evn python
#__*__encoding:utf-8__*__
'''
Created on 2015年8月7日

@author: zhangjin
'''
import requests
import codecs
import HTMLParser
import time
import random

import logging
from os.path import dirname, abspath 

#主页
mainurl = "http://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=2%20&brandId=0%20&fctId=0%20&seriesId=0"
#细览页
detailurl = "http://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=2%%20&brandId=%s%%20&fctId=0%%20&seriesId=0"

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename="log/"+time.strftime("%Y-%m-%d", time.localtime())+'mylog.log',
                filemode='w')

class MyPaserMainPage(HTMLParser.HTMLParser):
    r""" 解析主页信息 """
    
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.data = []
        self.cid = None
        self.flag = False
    def handle_starttag(self, tag, attrs):
        HTMLParser.HTMLParser.handle_starttag(self, tag, attrs)
        if tag == "a":
            self.flag = True
            for name,value in attrs:
                if name == "href":
                    self.cid = value

    def handle_data(self, data):
        if self.flag :
            self.data.append((self.cid,data))
        self.flag = False

class MyPaserDetailPage(HTMLParser.HTMLParser):
    r""" 解析内部页信息 """
    
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.data = []
        self.cid = None
        self.flag = False
    def handle_starttag(self, tag, attrs):
        HTMLParser.HTMLParser.handle_starttag(self, tag, attrs)
        if tag == "li":
            self.flag = False
            for name,value in attrs:
                if name == "class" and value == 'current':
                    self.flag = True
                    break
        if self.flag and tag == "a":
            for name,value in attrs:
                if name == 'id':
                    self.cid = value

    def handle_data(self, data):
        if self.cid is not None :
            self.data.append((self.cid,data))
        self.cid = None

class MyOutPut(object):
    '''
    输出结果
    '''

    def __init__(self):
        ISOTIMEFORMAT='%Y-%m-%d'
        PREFIX = dirname(abspath(__file__)) 
        ss = time.strftime(ISOTIMEFORMAT, time.localtime() )
        path = '%s/data/car_%s' % (PREFIX,ss,)
        self.fw = codecs.open(path, 'w', 'utf-8',)

    def out(self,data):
        if isinstance(data,tuple):
            self.fw.write("%s\t%s\n" % data)
    def close(self):
        self.fw.close()

def start():
    #抓取概览页
    out = MyOutPut()

    seed = crawlerMainPage()
    process = 0
    for cid ,name in seed:
        process = process+1
        print time.strftime("%Y-%m-%d %X"),process,"-",len(seed),cid,name
        logging.info("%s\t%s" % (cid,name))
        out.out((cid ,name))
        #每页之间抓取时间间隔 10 ～ 20 s
        time.sleep(random.randint(10, 30))
        data = crawlerDetailPage(cid)
        for a ,b in data:
            logging.info("%s\t%s" % (a,b))
            out.out((a ,b))
    out.close()

def crawlerDetailPage(cid):
    r""" 抓取内部页信息 """
    cid = cid.replace('/pic/brand-','').replace('.html','')
    url= detailurl % (cid,)
    r = requests.get(url)
    if r.status_code == 200:
        data = r.content.decode('gbk')
        parser = MyPaserDetailPage()
        parser.feed(data)
        return parser.data
    else:
        print cid," detail page error status code : ",r.status_code

def crawlerMainPage():
    r""" 抓取主页信息 """

    r = requests.get(mainurl)
    if r.status_code == 200:
        data = r.content.decode('gbk')
        parser = MyPaserMainPage()
        parser.feed(data)
        return parser.data
    else:
        print "main page error status code : ",r.status_code
if __name__ == '__main__':
    start()
