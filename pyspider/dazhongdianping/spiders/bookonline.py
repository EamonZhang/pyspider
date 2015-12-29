#! /usr/bin/env python
#encoding=utf-8
'''
Created on 2015年9月23日

@author: zhangjin
'''
import requests
import codecs
import os
from dazhongdianping.spiders import crawlbycity
import json
from dazhongdianping.spiders.crawlbycity import SaveDataClass
import time
import random
from time import strftime, localtime
from gevent.pool import Pool
import gevent

appkey = "4986383667"
secret = "636eb914dcb543d396b5cbf244bf1da3"
#获取所有deal id
def request_deals_all():
#     with codecs.open(crawlbycity.baspath+"cities", 'r','utf-8') as fr:
#         for city in fr:
#             try:
#                 request_deals_city(city.strip())
#             except Exception as e:
#                 print e
#         合并online business id
    with codecs.open(crawlbycity.baspath+"onlinebusinessid", 'w+','utf-8') as fw:
        basepatch = crawlbycity.baspath+"onlinebusinessids"
        files = os.listdir(basepatch)
        files.sort()
        count = 0
        for datafile in files:
            with codecs.open(basepatch+"/"+datafile, 'r','utf-8') as fr:
                for line in fr:
                    jsondata = json.loads(line.strip(),encoding = "utf8",strict=False)
                    status = jsondata['status']
                    if status == 'OK':
                        data = jsondata['id_list']
#                         print data
                        for deal in data:
                            fw.write(str(deal)+"\n")
                            count += 1
                        fw.flush()
    print "business count :",count
    
    jobs = []
    spawn_pool = Pool(5)
    with codecs.open(crawlbycity.baspath+"onlinebusinessid",'r','utf-8') as fr:
        deals = []
        for deal in fr:
            deals.append(deal.strip())
            if len(deals) == 40:
                jobs.append(spawn_pool.spawn(request_business_data,deals))
                deals= [] 
    gevent.joinall(jobs)

def request_deals_city(city):
        print city
        apiUrl = "http://api.dianping.com/v1/reservation/get_all_id_list"
        paramSet = [("city", city)]
        url_trail=crawlbycity.getQueryString(appkey, secret, paramSet)
        requestUrl = apiUrl + "?" + url_trail
        r = requests.get(requestUrl)
        r.close()
        if r.status_code == 200:
            sdc = SaveDataClass('onlinebusinessids/'+city)
            sdc.outputdata(r.text)
            sdc.close()
        time.sleep(random.randint(2,8))

def request_business_data(batchIds):
        try:
            if len(batchIds) == 0:
                return
            sdc = SaveDataClass("businessdata/"+strftime("%Y%m%d%H%M%S",localtime())+"_"+batchIds[0])
            strbatchIds = ",".join(batchIds)
            apiUrl = "http://api.dianping.com/v1/reservation/get_batch_businesses_with_reservations_by_id";
            paramSet = [("business_ids", strbatchIds)]
            url_trail = crawlbycity.getQueryString(appkey, secret, paramSet)
            requestUrl = apiUrl + "?" + url_trail
            r = requests.get(requestUrl)
            if r.status_code == 200:
                sdc.outputdata(r.text)
                sdc.close()
        except Exception as e:
            print e

if __name__ == '__main__':
    request_deals_all()