#encoding:utf-8
'''
Created on 2015年9月14日

@author: zhangjin
'''
import hashlib
import requests
import json
import codecs
import psycopg2
import time
import random
import os
from time import localtime,strftime

class ResumeBrokenDownloads(object):
    """"
    断点续传
    """
    def __init__(self):
        self.current_path = os.path.abspath('.')+"/resume_broken"
    #读取上次结束断点信息
    def read_resume_broken(self):
        broken_point = []
        with codecs.open(self.current_path, 'a+', 'utf-8') as fr:
            for line in fr:
                broken_point.append(line.strip().replace("/n",''))
        return broken_point
    #保存完成记录信息
    def save_resume_broken(self,items):
        with codecs.open(self.current_path, 'a+', 'utf-8') as fw:
            for item in items:
                fw.write(item+"\n")

class CrawlDaZhongDianPing(object):
    def __init__(self):
        self.appkey = "4986383667"
        self.secret = "636eb914dcb543d396b5cbf244bf1da3"
        self.file = codecs.open(r"/home/zhangjin/data/dazhongdianping/data.json",'a+')
        self.connection = psycopg2.connect(database="crawldata", user="postgres", password="123456", host="192.168.6.28", port="5432");
        self.number = 0
        self.bussinessids = set()
        self.dealids = []
        self.rbd = ResumeBrokenDownloads()
    def close(self):
        self.file.close()
        self.connection.commit()
        self.connection.close()
    #获取城市列表
    def start_crawl_cities(self):
        apiUrl = "http://api.dianping.com/v1/metadata/get_cities_with_deals"
        url_trail=getQueryString(self.appkey, self.secret, [])
        requestUrl = apiUrl + "?" + url_trail
        r = requests.get(requestUrl)
        r.close()
        if r.status_code == 200:
            return json.loads(r.text)["cities"]

    #获取城市中店铺ID集合
    def start_crawl_dealids(self,city):
        apiUrl = "http://api.dianping.com/v1/deal/get_all_id_list"
        paramSet = [("city", city)]
        url_trail=getQueryString(self.appkey, self.secret, paramSet)
        requestUrl = apiUrl + "?" + url_trail
        r = requests.get(requestUrl)
        r.close()
        if r.status_code == 200:
            return json.loads(r.text)["id_list"]
        
    def start_crawl_deals(self,batchIds):
        strbatchIds = ",".join(batchIds)
        apiUrl = "http://api.dianping.com/v1/deal/get_batch_deals_by_id";
        paramSet= [("deal_ids", strbatchIds)]
        url_trail=getQueryString(self.appkey, self.secret, paramSet)
        requestUrl = apiUrl + "?" + url_trail
        r = requests.get(requestUrl)
        if r.status_code == 200:
#                 print r.text
            self.file.write(r.text+"\n")
            self.rbd.save_resume_broken(batchIds)
            return self.parse_businesses_from_deal(r.text)

    def save_poi_db(self,pois):
        for poi in pois:
            #转义 escape sql 特殊字符
            for key,value in poi.items():
                poi[key] = str(value).replace("'", "''")

            sql = """INSERT INTO dazhongdianping(id,city, name, longitude, latitude, address)
                VALUES ('%(id)s','%(city)s', '%(name)s', '%(longitude)s', '%(latitude)s', '%(address)s');""" % poi
            try:
                cur = self.connection.cursor()
                cur.execute(sql)
                cur.close()
                self.number += 1
                if self.number % 40 == 0:
                        self.connection.commit()
                if self.number % 1000 == 0:
                        print self.number,"        ",strftime("%Y%m%d%H%M%S",localtime())
            except:
                print sql

    def parse_businesses_from_deal(self,text):
        pois = []
        jsdata = json.loads(text,strict=False)
        if not jsdata.has_key("deals"):
            return pois
        deals = jsdata["deals"]
        for deal in deals:
            businesses = deal['businesses']
            for business in businesses:
                if business['id'] not in self.bussinessids:
                    pois.append(business)
                    self.bussinessids.add(business['id'])
        return pois

    def filterdup(self,rids):
        for rid in self.dealids:
            if id in rids:
                rids.remove(rid)
    #         return list(set(rids).difference(set(self.ids)))
        self.dealids.extend(rids)

""" 基础工具类 """
def split_ids(ids,pageSize):
    result = []
    listLen = len(ids)
    index = 0
    while(index < listLen):
        result.append(ids[index:index + pageSize])
        index = index + pageSize
    return result

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
    
def start_crawl_execute():
    crawl = CrawlDaZhongDianPing()
    cities = crawl.start_crawl_cities()
    for city in cities:
        if city == "全国" or city == "上海" or city == "北京" or city == "杭州":
            continue
        dealids = crawl.start_crawl_dealids(city)
        #读取已完成数据
        items = crawl.rbd.read_resume_broken()
        dealids = list(set(dealids).difference(set(items)))

        crawl.filterdup(dealids)
        print city,len(dealids)
        batchdealIds = split_ids(dealids,40)
        for batchIds in batchdealIds:
            try:
                pois = crawl.start_crawl_deals(batchIds)
                crawl.save_poi_db(pois)
                time.sleep(random.randint(1,3))
            except Exception as e:
                print e
    crawl.close()
if __name__ == '__main__':
    start_crawl_execute()