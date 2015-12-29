# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from changditong.items import ItemLevel2
import psycopg2
import json
from requests.status_codes import codes

class JsonWriterPipeline(object):

    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_item(self, item, spider):
        if isinstance(item,ItemLevel2):
            """ 格式处理 """
            for k,values in item.iteritems():
                if isinstance(values, unicode):
                    item[k] =  values.replace(' ','').replace('\r','').replace("\t","").replace("\n","")
                if  isinstance(values, list):
                    item[k] = ""
                    #图片信息之后处理
                    if k == 'image_urls' :
                        item[k] = []
                        for value in values:
                            item[k].append("http://www.changditong.com"+value)
                    if k == 'itemsimilarplace':
                        rids = []
                        for value in values:
                            rid = filter(str.isdigit,value.encode('gbk'))
                            if rid not in rids:
                                rids.append(rid)
                        for rid in rids:
                            item[k] += rid+";"
                    else:
                        for value in values:
                            value = value.replace(' ','').replace('\r','').replace("\t","").replace("\n","")
                            item[k] += value
        return item

    def close_spider(self,spider):
        pass

"""
数据保存在数据库中
"""
class DBPipeline(object):

    def __init__(self):
        self.connection = psycopg2.connect(database="crawldata", user="postgres", password="123456", host="192.168.6.28", port="5432");
        self.number = 0

    def open_spider(self, spider):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_item(self, item, spider):
        data = dict(item)
#         line = json.dumps(data)
#         print line
        if isinstance(item,ItemLevel2):
            cur = self.connection.cursor()
            sql = """ INSERT INTO changditong(address, uid, name, cappersion, hot, category,area, 
            fitcategory, equipment, introduce, similarplace)
            VALUES ('%(itemaddress)s', '%(itemuid)s', '%(itemname)s', '%(itemcappersion)s', '%(itemhot)s', '%(itemcategory)s', 
            '%(itemarea)s', '%(itemfitcategory)s', '%(itemequipment)s', '%(itemintroduce)s', '%(itemsimilarplace)s');
            """ % data
#             print sql
            cur.execute(sql)
            cur.close()
            self.number += 1
            if self.number % 10 == 0:
                self.connection.commit()
        return item

    def close_spider(self,spider):
        self.connection.commit()
        self.connection.close()
