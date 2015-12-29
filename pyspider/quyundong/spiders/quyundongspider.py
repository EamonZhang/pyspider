#!/usr/bin/env python
#__*__encoding:utf-8__*__

from scrapy.selector import Selector
from quyundong.items import ItemLevel2
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import logging
import traceback
import scrapy

""" 城市编码 页数 城市名 """
citys = {"52":u"北京","76":u"广州","77":u"深圳","321":u"上海","343":u"天津"}
sportsitems = {"1":u"羽毛球","6":u"乒乓球","8":u"游泳馆","11":u"足球场","12":u"网球场","13":u"篮球场","25":u"壁球"}

def initStartUrls():
    urls = []
    for cityCode in citys.iterkeys():
        for sportItemCode in sportsitems.iterkeys():
            url = "http://www.quyundong.com/index.html?city_id=%s&cat_id=%s&page=1" % (cityCode,sportItemCode)
            urls.append(url)
    return urls

class QuyundongSpider(CrawlSpider):
    name = "quyundong"
    download_delay = 1
    allowed_domains = ["www.quyundong.com"]
    start_urls = initStartUrls()
#     rules = [Rule(LinkExtractor(allow=['detail'],tags=('a'),restrict_xpaths=('//div[@class="info l"]')), 'parse_torrent')]

    def __init__(self, *a, **kw):
        CrawlSpider.__init__(self, *a, **kw)
        self.crawledurl = set()
        self.itemIds = set()

    """
    翻页，下一级页面
    """
    def parse_start_url(self, response):
        if response.url in self.crawledurl:
            print response.url ,"repead"
            return
        self.crawledurl.add(response.url)
#         print response.url
        sel = Selector(response)
#         print response.body
        nextPage = sel.xpath('//div[@class="page"]/li[@class="next"]/a/@href').extract()
        """ 翻页 """
        if len(nextPage) == 1:
            nextPage = "http://www.quyundong.com" + nextPage[0].strip()
            request = scrapy.Request(nextPage,callback=self.parse_start_url)
            yield request
#         """ 下一级页面 """
        detailUrls = sel.xpath('//div[@class="info l"]/h3/a/@href').extract()
        url = response.url
        city_id = url[url.find("city_id"):url.find("&",url.find("city_id"))].replace("city_id=","")
        cat_id = url[url.find("cat_id"):url.find("&",url.find("cat_id"))].replace("cat_id=","")
        for detailUrl in detailUrls:
            detailUrl ="http://www.quyundong.com"+detailUrl.strip()
            request = scrapy.Request(detailUrl,callback=self.parse_torrent,meta={'cityname': citys[city_id],"sportsitem":sportsitems[cat_id]})
            yield request
    def parse_torrent(self, response):
        self.log("start parse url %s " % (response.url), logging.INFO)
        #过滤重复抓取
        if response.url in self.crawledurl:
            print response.url ,"repead"
            return
        self.crawledurl.add(response.url)
#         print response.url
        try:
            sel = Selector(response)
            site = sel.xpath('//div[@class="pic-biref"]')
            if len(site) == 0:
                site = sel.xpath('//div[@class="court_info"]')
            item = ItemLevel2()
            item.setdefaultvalues()
            item['itemuid'] = response.url[response.url.rfind('/')+1:].replace('.html','')
            item['itemname'] = site.xpath('h2/text()').extract()[0]
            item['itemimages'] = site.xpath('//div[@class="smallImg"]/ul/li/a/img/@src').extract()
            item['itembrief'] = sel.xpath('//dl[@class="order-dl"]/dd/p/text()').extract()
            item['itemsportsitems'] = response.meta["sportsitem"]
            item['itemcity'] = response.meta["cityname"]
            siteinfo = site.xpath('dl[@class="service_dl"]')
            tagetitles = siteinfo.xpath('dt').extract()
            tagetexts = siteinfo.xpath('dd')
    #         print item['itemuid'] , len(tagetitles),len(tagetexts)
            for title,text in zip(tagetitles,tagetexts):
                text = text.xpath('text()').extract()
    #             print title,text
                if '地址' in title:
                    item['itemaddress'] = text
                elif '电话' in title:
                    item['itemtel'] = text
                elif '场馆价格' in title:
                    item['itempriceinfo'] = text
                elif '其它服务' in title:
                    item['itemotherserver'] = text
                elif '卖品' in title:
                    item['itemsaleinfo'] = text
                elif '发票' in title:
                    item['iteminvoice'] = text
                elif '停车' in title:
                    item['itempark'] = text
                elif '公交' in title:
                    item['itembus'] = text
                elif '地铁' in title:
                    item['itemsubway'] = text
                elif '层高' in title:
                    item['itemstorey'] = text
                elif '地板' in title:
                    item['itemfloor'] = text
                elif '灯光' in title:
                    item['itemlight'] = text
                elif '类型' in title:
                    item['itemtype'] = text
                else:
                    print title,text
            yield item
        except Exception,e:
            print 'url ',response.url
            traceback.print_exc()
            print Exception,e
if __name__ == '__main__':
    urls = initStartUrls()
    for url in urls:
        print url