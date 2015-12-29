#!/usr/bin/env python
from scrapy.item import Item, Field

class ItemLevel1(Item):

    area = Field()
    itemid = Field()
    person = Field()

class ItemLevel2(Item):

    itemaddress = Field()
    itemuid = Field()
    itemname = Field()
    itemcappersion = Field()
    itemhot = Field()
    image_urls = Field()
    images =Field()
    itemcategory = Field()
    itemarea = Field()
    itemfitcategory = Field()
    itemequipment = Field()
    itemintroduce = Field()
    itemsimilarplace = Field()
