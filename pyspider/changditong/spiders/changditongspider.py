#!/usr/bin/env python
#__*__encoding:utf-8__*__

from scrapy.selector import Selector
from changditong.items import ItemLevel1, ItemLevel2
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request, selector
import logging
import scrapy


class ChangditongSpider(CrawlSpider):
    name = "changditong"
    download_delay = 2
    allowed_domains = ["changditong.com"]
    start_urls = ["http://www.changditong.com/product/list?page=1"]
#     rules = [Rule(LinkExtractor(allow=['detail_'],tags=('a'),restrict_xpaths=('//ul[@class="linkedlist"]/div[@class="img"]')), 'parse_torrent')]

    def __init__(self, *a, **kw):
        CrawlSpider.__init__(self, *a, **kw)
        self.crawledurl = set()
        self.itemIds = set()
        self.seeds = set()

    def parse_start_url(self, response):
        if response.url in self.crawledurl:
            print response.url ,"repead"
            return
        self.crawledurl.add(response.url)
        print response.url
        sel = Selector(response)
        """ 
                解析Item信息
        """
        sites = sel.xpath('//ul[@class="linkedlist"]/li/div[@class="img"]')
        for site in sites:
            item = ItemLevel1()
            item['area'] = site.xpath('div[@class="caption"]/span[@area]/text()').extract() 
            item['person'] = site.xpath('div[@class="caption"]/span[@person]/text()').extract()
            url = "http://www.changditong.com"+str(site.xpath('a/@href').extract()[0])
            request = Request(url,
                         callback=self.parse_torrent,meta={'item':item})
            yield request
        """ 
                下一页
        """
        nexturls = sel.xpath('//div[@class="pagerbox"]/form/table/tbody/tr/td/a/@href').extract()
        for nexturl in nexturls:
            nexturl = "http://www.changditong.com/product/"+nexturl
            if nexturl not in self.seeds and nexturl != response.url:
                self.seeds.add(nexturl)
                request = scrapy.Request(nexturl,self.parse_start_url)
                yield request

    def parse_torrent(self, response):
        self.log("start parse url %s " % (response.url), logging.INFO)
        #过滤重复抓取
        if response.url in self.crawledurl:
            print response.url ,"repead"
            return
        self.crawledurl.add(response.url)
        item1 = response.meta['item']
        item = ItemLevel2()
        item["itemuid"] = filter(str.isdigit,response.url)
        sel = Selector(response)
        item["itemcappersion"] = item1["person"]
        #名称
        item["itemname"] = sel.xpath('//div[@class="pl30"]/h1/text()').extract()
        #热度
        item["itemhot"] = sel.xpath('//div[@class="pl30"]/div[@id="tit2"]/span/text()').extract()
        #地址
        item["itemaddress"] = sel.xpath('//div[@class="pl30"]/div[@id="tit2"]/text()').extract()
        #图片
        item["image_urls"] = sel.xpath('//div[@id="pcimgBox"]/a/@href').extract()
        #介绍
        item["itemintroduce"] = sel.xpath('//div[@class="ctxt"]/p/text()').extract()
        #场地类型 适合活动类型
        item["itemcategory"] = sel.xpath('//div[@class="cright crbgfff"]/text()').extract()[0]
        item["itemfitcategory"] = sel.xpath('//div[@class="cright crbgfff"]/text()').extract()[1]
        #场地大小  场地配备
        item["itemarea"] = sel.xpath('//div[@class="cright bgefefef"]/text()').extract()[0]
        item["itemequipment"] = sel.xpath('//div[@class="cright bgefefef"]/text()').extract()[1]
        # 相似场地
        item["itemsimilarplace"] = sel.xpath('//ul[@class="linkedlist"]/li/div/a/@href').extract()
        yield item
