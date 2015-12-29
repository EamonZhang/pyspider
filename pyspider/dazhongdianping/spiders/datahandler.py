#encoding=utf-8
'''
Created on 2015年9月18日

@author: zhangjin
'''
import os
from os.path import join, getsize  
import codecs
import json
import psycopg2
from time import strftime, localtime
def getdirsize(dir):  
    size = 0L
    for root, dirs, files in os.walk(dir):  
        size += sum([getsize(join(root, name)) for name in files])  
    return size

def loadfiledata():
    bathpath = "/home/zhangjin/data/dazhongdianping/businessdata"
    files = os.listdir(bathpath)
    files.sort()
    for filename in files:
        filepath = join(bathpath,filename)
        parserjsondata(filepath)

def parserjsondata(filepath):
    if getsize(filepath) != 0:
        with codecs.open(filepath) as fr:
            for line in fr:
                try:
                    jsondata = json.loads(line.strip(),strict=False)
                    if jsondata['status'] == 'OK':
                        #解析团购
                        if jsondata.has_key('deals'):
                            for deal in jsondata['deals']:
                                businesses = deal['businesses']
                                save_poi_db(businesses)
                        #解析店铺
                        else:
                            businesses = jsondata['businesses']
                            save_poi_online_db(businesses)
                except Exception as e:
                    print line,e

def save_poi_db(pois):
        for poi in pois:
            global bussinessid
            if  poi['id'] in bussinessid:
                continue 
            bussinessid.add(poi['id'])
            #转义 escape sql 特殊字符
            for key,value in poi.items():
                poi[key] = str(value).replace("'", "''").replace('\\','\\\\')
            
            sql = """INSERT INTO dazhongdianping_20150924(id,city, name, longitude, latitude, address)
                VALUES ('%(id)s','%(city)s', '%(name)s', '%(longitude)s', '%(latitude)s', '%(address)s');""" % poi
            try:
                cur = connection.cursor()
                cur.execute(sql)
                cur.close()
                global number
                number += 1
                if number % 1000 == 0:
                    connection.commit()
                    print number,"        ",strftime("%Y%m%d%H%M%S",localtime())
            except Exception as e:
                connection.rollback()
                print e,sql

def save_poi_online_db(pois):
        for poi in pois:
            global bussinessid
            if  poi['business_id'] in bussinessid:
                continue 
            bussinessid.add(poi['business_id'])
            #转义 escape sql 特殊字符
            for key,value in poi.items():
                poi[key] = str(value).replace("'", "''").replace('\\','\\\\')
            
            sql = """INSERT INTO dazhongdianping_online_20150924(id,city, name, longitude, latitude, address,telephone)
                VALUES ('%(business_id)s','%(city)s', '%(name)s', '%(longitude)s', '%(latitude)s', '%(address)s','%(telephone)s');""" % poi
            try:
                cur = connection.cursor()
                cur.execute(sql)
                cur.close()
                global number
                number += 1
                if number % 1000 == 0:
                    connection.commit()
                    print number,"        ",strftime("%Y%m%d%H%M%S",localtime())
            except Exception as e:
                connection.rollback()
                print e,sql
bussinessid = set()
number = 0
connection = psycopg2.connect(database="crawldata", user="postgres", password="123456", host="192.168.6.28", port="5432");
if __name__ == '__main__':
    loadfiledata()
    connection.commit()
    connection.close()