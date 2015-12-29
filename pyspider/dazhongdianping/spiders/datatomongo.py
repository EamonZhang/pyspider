#!/usr/bin/env python
#encoding=utf-8
'''
Created on 2015年9月24日

@author: zhangjin
'''
import codecs
import os
from os.path import join
import json

class DataMongoHandler(object):
    '''
    classdocs
    '''

    def __init__(self):
        # 建连接
        self.connection=pymongo.MongoClient('localhost',27017)
        # 切换数据库
        self.db = self.connection.test
        # 获取collection
        self.collection = self.db.testData
        self.datapath = r"/home/zhangjin/data/dazhongdianping/businessdata"

    def parseData(self):
        filenames = os.listdir(self.datapath)
        for filename in filenames:
            with codecs.open(join(self.datapath,filename), 'r', 'utf-8') as fr:
                for line in fr:
                    data = json.loads(line,encoding = 'utf8',strict = 'false')
                    if data['status'] == 'OK':
                        businesses = data['businesses']
                        print len(businesses)
                        yield businesses

    def insertData(self):
        datas = self.parseData()
        for data in datas:
            self.collection.insert(data)

    def distroy(self):
        self.connection.close()

    def excute(self):
        self.parseData()
        self.insertData()
        self.distroy()
    
import pymongo
import datetime
def test():
    # 建连接
    connection=pymongo.MongoClient('localhost',27017)
    # 切换数据库
    db = connection.test
    # 获取collection
    collection = db.testData
    # db和collection都是延时创建的，在添加Document时才真正创建
    # 文档添加，_id自动创建
    post = {"author": "Mike",
             "text": "My first blog post!",
             "tags": ["mongodb", "python", "pymongo"],
             "date": datetime.datetime.utcnow()}
    collection.insert(post)
    connection.close()
if __name__ == '__main__':
    handler = DataMongoHandler()
    handler.excute()
