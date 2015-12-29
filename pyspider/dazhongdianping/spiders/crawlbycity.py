#encoding:utf-8
'''
Created on 2015年9月17日

@author: zhangjin
'''
from gevent import monkey
from time import strftime, localtime
monkey.patch_all() 
import codecs
import hashlib
import requests
import json
from _dbus_bindings import String
import time
import random
import os
import gevent
from gevent.pool import Pool

baspath = r"/home/zhangjin/data/dazhongdianping/"
class CrawlClass(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.appkey = "4986383667"
        self.secret = "636eb914dcb543d396b5cbf244bf1da3"

    #获取城市列表
    def request_cities(self):
        apiUrl = "http://api.dianping.com/v1/metadata/get_cities_with_deals"
        url_trail=getQueryString(self.appkey, self.secret, [])
        requestUrl = apiUrl + "?" + url_trail
        r = requests.get(requestUrl)
        r.close()
        if r.status_code == 200:
            strdata = json.loads(r.text)["cities"]
            sdc = SaveDataClass('cities')
            sdc.outputdata(strdata)
            sdc.close()
#         time.sleep(random.randint(5,10))

    #获取所有deal id
    def request_deals_all(self):
        with codecs.open(baspath+"cities", 'r','utf-8') as fr:
            for city in fr:
                try:
                    self.request_deals_city(city.strip())
                except Exception as e:
                    print e
#         合并dealid
        with codecs.open(baspath+"deals", 'w+','utf-8') as fw:
            basepatch = baspath+"dealids"
            files = os.listdir(basepatch)
            files.sort()
            count = 0
            for datafile in files:
                with codecs.open(basepatch+"/"+datafile, 'r','utf-8') as fr:
                    for line in fr:
                        data = json.loads(line.strip(),encoding = "utf8",strict=False)['id_list']
                        for deal in data:
                            fw.write(deal+"\n")
                            count += 1
                        fw.flush()
        print "deal count :",count
         
        jobs = []
        spawn_pool = Pool(5) 
        with codecs.open(baspath+"deals",'r','utf-8') as fr:
            deals = []
            for deal in fr:
                deals.append(deal.strip())
                if len(deals) == 40:
                    jobs.append(spawn_pool.spawn(self.request_deals_data,deals))
                    deals= []
        gevent.joinall(jobs) 
    #获取城市内的所有团购列表
    def request_deals_city(self,city):
        print city
        apiUrl = "http://api.dianping.com/v1/deal/get_all_id_list"
        paramSet = [("city", city)]
        url_trail=getQueryString(self.appkey, self.secret, paramSet)
        requestUrl = apiUrl + "?" + url_trail
        r = requests.get(requestUrl)
        r.close()
        if r.status_code == 200:
            sdc = SaveDataClass('dealids/'+city)
            sdc.outputdata(r.text)
            sdc.close()
        time.sleep(random.randint(2,8))
#             print json.loads(r.text)["id_list"]
    #根据dealids列表获取数据
    def request_deals_data(self,batchIds):
        try:
            if len(batchIds) == 0:
                return
            sdc = SaveDataClass("data/"+strftime("%Y%m%d%H%M%S",localtime())+"_"+batchIds[0])
            strbatchIds = ",".join(batchIds)
            apiUrl = "http://api.dianping.com/v1/deal/get_batch_deals_by_id";
            paramSet= [("deal_ids", strbatchIds)]
            url_trail=getQueryString(self.appkey, self.secret, paramSet)
            requestUrl = apiUrl + "?" + url_trail
            r = requests.get(requestUrl)
            if r.status_code == 200:
                sdc.outputdata(r.text)
                sdc.close()
        except Exception as e:
            print e

def getQueryString(appkey,secret,paramSet):
    paramMap = {}
    for pair in paramSet:
        paramMap[pair[0]] = pair[1]

    codec = appkey
    for key in sorted(paramMap.iterkeys()):
        codec += key + paramMap[key]

    codec += secret
    #签名计算
    sign = (hashlib.sha1(codec).hexdigest()).upper()

    #拼接访问的URL
    url_trail = "appkey=" + appkey + "&sign=" + sign
    for pair in paramSet:
        url_trail += "&" + pair[0] + "=" + pair[1]
    return url_trail

from os.path import getsize
class SaveDataClass():
    
    #创建初始文件
    def __init__(self,filename):
        self.file = codecs.open(baspath+filename,'a+','utf-8')
    #写出数据
    def outputdata(self,data):
        if isinstance(data, String) or isinstance(data, unicode):
            self.file.write(data+"\n")
        if isinstance(data, list):
            for line in data:
                self.file.write(line+"\n")
        self.file.flush()
    def close(self):
        self.file.flush()
        self.file.close()
        filesize = getsize(self.file.name)
        print self.file.name,filesize
        if filesize == 0:
            time.sleep(50)

if __name__ == '__main__':
    crawl = CrawlClass()
    crawl.request_cities()
    crawl.request_deals_all()
