#!/usr/bin/env python
#__*__encoding:utf-8__*__

from scrapy.selector import Selector
from dongsport.items import ItemLevel1, ItemLevel2
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import logging

""" 城市编码 页数 城市名 """
seed = [
            (10011,673,'beijing'),
            (10031,604,'shanghai'),
            (1002102,89,'dalian'),
            (1003301,214,'hangzhou'),
            (1003201,145,'nanjing'),
            (1003202,105,'qingdao'),
            (1005101,115,'chengdu'),
            (1004401,302,'guangzhou'),
            (1004403,294,'shenzhen'),
            (1002101,111,'shenyang'),
            (1006101,14,'xian'),
            (1004201,19,'wuhan'),
            (10012,55,'tianjin'),
            (1005101,115,'chengdu'),
            (1004301,10,'changsha'),
            (1003701,12,'jinan'),
            (1004101,13,'zhengzhou'),
            (10066,6,'chongqing'),
            ]

def initStartUrls():
        urls = []
        for citycode,totalpage,cityname in seed:
            for page in range(1,totalpage+1):
                urls.append("http://www.dongsport.com/venue/list-%d-0-0-0-0-0-0-0-%d.html" % (citycode,page))
        return urls

class DongSportSpider(CrawlSpider):
    name = "dongsport"
    download_delay = 2
    allowed_domains = ["dongsport.com"]
    start_urls = initStartUrls()
    rules = [Rule(LinkExtractor(allow=['detail_'],tags=('a'),restrict_xpaths=('//div[@id="detail"]')), 'parse_torrent')]

    def __init__(self, *a, **kw):
        CrawlSpider.__init__(self, *a, **kw)
        self.crawledurl = set()
        self.itemIds = set()

    def parse_torrent(self, response):
        self.log("start parse url %s " % (response.url), logging.INFO)
        #过滤重复抓取
        if response.url in self.crawledurl:
            print response.url ,"repead"
            return
        self.crawledurl.add(response.url)

        sel = Selector(response)
        sites = sel.xpath('//div[@class="ven-text"]')
        item = ItemLevel2()
        item['itemuid'] = filter(str.isdigit,response.url)
        item['itemintruduction'] = sites[0].xpath('p/text()').extract()
        item['itemfacilities'] = sites[1].xpath('span/text()').extract()
        item['itemtraffic'] = sites[2].xpath('text()').extract()
        item['itemimages'] = sel.xpath('//a[@class="fancybox"]/@href').extract()
        item['itemcanbook'] = sel.xpath('//div[@id="details_link"]/ul/li/@viewid').extract()
        yield item
    def parse_start_url(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html
        @url http://www.dongsport.com/venue/
        @scrapes name
        """

        self.log("start parse url %s " % (response.url), logging.INFO)
        if response.url in self.crawledurl:
            print response.url ,"repead"
            return
        self.crawledurl.add(response.url)
        """ 
            截取经纬度信息,摘自javascript
        """
        try:
            dicItem = {}
            contextlines = response.body.split('\r\n')
            for contextline in contextlines:
                if "custId:" in contextline: 
                    contextline = contextline.strip()
                    itemid = contextline[contextline.find('custId:')+len('custId:'):contextline.find(',' ,contextline.find('custId: '))].replace("'",'').replace("}",'').strip()
                    itemlon = contextline[contextline.find('longitude:')+len('longitude:'):contextline.find(',' ,contextline.find('longitude'))].replace("'",'').replace("}",'').strip()
                    itemlat = contextline[contextline.find('latitude:')+len('latitude:'):contextline.find(',' ,contextline.find('latitude'))].replace("'",'').replace("}",'').strip()
                    dicItem[itemid] = [itemlon,itemlat]
    
            """ 
                解析Item信息
            """
            sel = Selector(response)
            sites = sel.xpath('//div[@class="t_listbox"]')
            for site in sites:
                item = ItemLevel1()
                item['itemname'] = site.xpath('div[@class="t_lb"]/div[@class="left v_l_text"]/h3/a/text()').extract()[0]
                item['itemid'] = site.xpath('@custid').extract()[0]
                item['itemtag'] = site.xpath('div[@class="t_lb"]/div[@class="left v_l_text"]/ul/li[3]/text()').extract()[0]
                item['itemaddress'] = site.xpath('div[@class="t_lb"]/div[@class="left v_l_text"]/ul/li[1]/text()').extract()[0]
                item['itemurl'] = site.xpath('div[@class="t_lb"]/div[@class="left v_l_text"]/h3/a/@href').extract()
                """网页中经纬度定义反"""
                item['itemlat'] = dicItem[item['itemid']][0]
                item['itemlon'] = dicItem[item['itemid']][1]
                if item['itemid'] not in self.itemIds:
                    self.itemIds.add(item['itemid'])
                    yield item
        except Exception as e:
            self.log(e, logging.ERROR)
"""
抓取图片
"""
import os
import requests
from scrapy.conf import settings
def crawlImage(url,path):
    path = settings.get("IMAGE_BASE_PASH")+path
    if not os.path.exists(path) or not os.path.isdir(path):
        os.mkdir(path)
    name = url[url.rfind("/"):]
    path += name
    r = requests.get(url)
    with open(path, 'wb') as fd:
        for chunk in r.iter_content():
            fd.write(chunk)
    r.close()

if __name__ == '__main__':
    pass