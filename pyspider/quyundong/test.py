# encoding:utf8
'''
Created on 2015年9月8日

@author: zhangjin
'''

if __name__ == '__main__':
    data = {'itempriceinfo': '',
            'itemotherserver': '', 
            'itemtype': '',
            'itemuid': '17002-12', 
            'itemtel': u'', 
            'itembrief': u'\u5468\u4e00\u81f3\u65e5\uff1a7--18\u70b980\u5143/\u5c0f\u65f6\uff0c18--22\u70b9100\u5143/\u5c0f\u65f6', 
            'itemstorey': '', 
            'itempark': '',
            'itemfloor': '',
            'itembus': '',
            'itemaddress': u'\u9ec4\u9601\u9547\u5927\u4e95\u6751\u9ec4\u6885\u8def73\u53f7',
             'itemsportsitems': u'\u7f51\u7403\u573a',
             'itemcity': u'\u6df1\u5733',
             'itemsaleinfo': '',
             'itemlight': '',
             'itemname': u'\u91d1\u6e90\u7f51\u7403\u573a', 'itemimages': u'http://gsadmin.7yundong.cn/uploads/images/2015-02-06/333538ef4d7ce632d4220f72a4e1c19e.jpg;', 'itemsubway': '', 'iteminvoice': ''}
    sql = """ 
             INSERT INTO quyundong(
             qyd_id, name,tel, address,city, price, otherserver, sale, invoice, park, 
             bus, subway, images,storey,floor,light,type,brief,item)
             VALUES ('%(itemuid)s', '%(itemname)s', '%(itemtel)s', '%(itemaddress)s','%(itemcity)s'
             '%(itempriceinfo)s', '%(itemotherserver)s', '%(itemsaleinfo)s', '%(iteminvoice)s', '%(itempark)s', 
             '%(itembus)s', '%(itemsubway)s', '%(itemimages)s','%(itemstorey)s','%(itemfloor)s','%(itemlight)s','%(itemtype)s','%(itembrief)s','%(itemsportsitems)s');
             """ % data
    print sql
