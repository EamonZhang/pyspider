# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

 
import json
import codecs
from quyundong.items import ItemLevel2
import psycopg2
from scrapy.mail import MailSender
from scrapy import settings

class JsonWriterPipeline(object):

    def __init__(self):
#         self.fileLevel2 = codecs.open('data_lev2', 'w', encoding='utf-8')
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
#             line = json.dumps(dict(item))
#             self.fileLevel2.write(line.decode('unicode_escape')+"\n")
#             self.fileLevel2.flush()
        return item

    def close_spider(self,spider):
#         self.fileLevel2.flush()
#         self.fileLevel2.close()
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
        if isinstance(item,ItemLevel2):
            cur = self.connection.cursor();
            sql = """ 
            INSERT INTO quyundong(
            qyd_id, name,tel, address,city, price, otherserver, sale, invoice, park, 
            bus, subway, images,storey,floor,light,type,brief,item)
            VALUES ('%(itemuid)s', '%(itemname)s', '%(itemtel)s', '%(itemaddress)s', '%(itemcity)s',
            '%(itempriceinfo)s', '%(itemotherserver)s', '%(itemsaleinfo)s', '%(iteminvoice)s', '%(itempark)s', 
            '%(itembus)s', '%(itemsubway)s', '%(itemimages)s','%(itemstorey)s','%(itemfloor)s','%(itemlight)s','%(itemtype)s','%(itembrief)s','%(itemsportsitems)s');
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

if __name__ == '__main__':
        """ 爬取数据数据完成 - 邮件通知"""
        mailer = MailSender()
        mailer.send(to=["zhangjin@zhumengyuan.com"], subject="Some subject", body="Some body", cc=["zhangjin@zhumengyuan.com"])
