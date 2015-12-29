#!/usr/bin/env python
from scrapy.item import Item, Field

class ItemLevel1(Item):

    itemname = Field()
    itemid = Field()
    itemtag = Field()
    itemaddress = Field()
    itemlon = Field()
    itemlat = Field()
    itemurl = Field()

class ItemLevel2(Item):

    itemintruduction = Field()
    itemuid = Field()
    itemfacilities = Field()
    itemtraffic = Field()
    itemimages = Field()
    itembusinesshour = Field()
    itemcanbook = Field()
