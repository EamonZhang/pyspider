#!/usr/bin/env python
from scrapy.item import Item, Field

class ItemLevel1(Item):

    itemid = Field()
    itemurl = Field()

class ItemLevel2(Item):

    itemtel = Field()
    itemaddress = Field()
    itemcity = Field()
    itemname = Field()
    itemuid = Field()
    itempriceinfo = Field()
    itemotherserver = Field()
    itemimages = Field()
    itemsaleinfo = Field()
    iteminvoice = Field()
    itempark = Field()
    itembus = Field()
    itemsubway = Field()
    itemstorey = Field()
    itemfloor = Field()
    itemlight = Field()
    itemtype = Field()
    itembrief = Field()
    itemsportsitems = Field()

    def setdefaultvalues(self):
        self.setdefault('itemtel', "")
        self.setdefault('itemaddress', "")
        self.setdefault('itemname', "")
        self.setdefault('itemuid', "")
        self.setdefault('itempriceinfo', "")
        self.setdefault('itemotherserver', "")
        self.setdefault('itemimages', "")
        self.setdefault('itemsaleinfo', "")
        self.setdefault('iteminvoice', "")
        self.setdefault('itempark', "")
        self.setdefault('itembus', "")
        self.setdefault('itemsubway', "")
        self.setdefault('itemstorey', "")
        self.setdefault('itemfloor', "")
        self.setdefault('itemlight', "")
        self.setdefault('itemtype', "")
        self.setdefault("itembrief", "")
        self.setdefault("itemsportsitems", "")
