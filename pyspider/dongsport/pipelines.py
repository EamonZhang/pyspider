# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from dongsport.items import ItemLevel1, ItemLevel2
import psycopg2
from datetime import date
import logging

class JsonWriterPipeline(object):

    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_item(self, item, spider):
        if isinstance(item,ItemLevel1):
            for k,value in item.iteritems():
                """ 格式处理 """
                if k == 'itemname' or k == 'itemaddress' or k == 'itemtag':
                    value = value.replace(' ','').replace('\r','').replace("\t","").replace("\n","")
                    value = value.replace('场馆标签：','')
                    value = value.replace('详细地址：','')
                    item[k] = value
        if isinstance(item,ItemLevel2):
            """ 格式处理 """
            for k,values in item.iteritems():
                if  isinstance(values, list):
                    item[k] = ""
                    #图片信息之后处理
                    if k == 'itemimages' :
                        for value in values:
                            value = value.replace(' ','').replace('\r','').replace("\t","").replace("\n","")
                            item[k] += value+";"
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
from time import localtime,strftime
class DBPipeline(object):

    def __init__(self):
        self.number = 0
        self.create_talbe_data = strftime("%Y%m%d",localtime())

    def open_spider(self, spider):
        self.connection = psycopg2.connect(database=spider.settings.get("DB_DATA"), 
                                           user=spider.settings.get("DB_USER_NAME"), password=spider.settings.get("DB_PWD"), 
                                           host=spider.settings.get("DB_HOST"), port=spider.settings.get("DB_PORT"));
        sql = spider.settings.get("CREATE_TABLE_SQL")
        sql = sql.replace("create_talbe_data",self.create_talbe_data)
        cur = self.connection.cursor();
        cur.execute(sql)
        cur.close()
        self.connection.commit()
        spider.log("CREATE DB Ok!", logging.INFO)

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def create_table(self):
        pass

    def process_item(self, item, spider):
        data = dict(item)
        if isinstance(item,ItemLevel1):
            itemId = data.get("itemid")
            item_name = data.get("itemname")
            item_address = data.get("itemaddress")
            item_tag = data.get("itemtag")
            item_lon = data.get("itemlon")
            item_lat = data.get("itemlat")
            cur = self.connection.cursor();
            cur.execute("INSERT INTO dongsport_base_"+self.create_talbe_data+" (sport_id, name, tag, address, lon, lat) VALUES (%s, %s, %s, %s, %s, %s);",
                        (itemId,item_name,item_tag,item_address,item_lon,item_lat))
            cur.close()
            self.number += 1
            if self.number % 1000 == 0:
                self.connection.commit()
        if isinstance(item,ItemLevel2):
            itemId = data.get("itemuid")
            item_facilities = data.get("itemfacilities")
            item_traffic = data.get("itemtraffic")
            item_canbook = data.get("itemcanbook")
            item_intruduction = data.get("itemintruduction")
            item_images = data.get("itemimages")
            cur = self.connection.cursor();
            cur.execute(" INSERT INTO dongsport_deepinfo_"+self.create_talbe_data+" (sport_id, facilities, traffic, book, intruduction,images) VALUES (%s, %s, %s, %s, %s,%s);",
                        (itemId,item_facilities,item_traffic,item_canbook,item_intruduction,item_images))
            cur.close()
            self.number += 1
            if self.number % 100 == 0:
                self.connection.commit()
        return item

    def close_spider(self,spider):
        self.connection.commit()
        self.connection.close()
    
if __name__ == '__main__':
    print date
