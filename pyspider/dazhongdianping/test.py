#!encoding:utf-8
'''
Created on 2015年9月14日

@author: zhangjin
'''
import requests
import hashlib
import json
import codecs

def getcities():
    apiUrl = "http://api.dianping.com/v1/metadata/get_cities_with_deals"
    appkey=4986383667
    secret = ""
    url_trail=getQueryString(appkey, secret, [])
    requestUrl = apiUrl + "?" + url_trail
    print requestUrl
    r = requests.get(requestUrl)
    print r.status_code
    print(r.text)

def getQueryString(appkey,secret,paramSet):
    paramMap = {}
    for pair in paramSet:
        paramMap[pair[0]] = pair[1]
    
    codec = appkey
    for key in sorted(paramMap.iterkeys()):
        codec += key + paramMap[key]
    
    codec += secret
    
    #签名计算
    sign = (hashlib.sha1(codec).hexdigest()).upper()

#拼接访问的URL
    url_trail = "appkey=" + appkey + "&sign=" + sign
    for pair in paramSet:
        url_trail += "&" + pair[0] + "=" + pair[1]

    print url_trail
    return url_trail
#     requestUrl = apiUrl + "?" + url_trail

#模拟请求
#     response = urllib.urlopen(requestUrl)

#     print response.read()
def filter(a,b):
        a[0] = 5
        a = list(set(a).difference(set(b)))
if __name__ == '__main__':
#     a = [1,2,4]
#     b = [1,2,3]
# #     filter(a,b)
#     a.extend(b)
#     print a
#     appkey = "4986383667"
#     secret = "636eb914dcb543d396b5cbf244bf1da3"
#     
#     paramSet = []
# #     getcitys()
#     paramSet.append(("format", "json"))
#     paramSet.append(("city", "上海"))
#     paramSet.append(("latitude", "31.21524"))
#     paramSet.append(("longitude", "121.420033"))
#     paramSet.append(("category", "美食"))
#     paramSet.append(("region", "长宁区"))
#     paramSet.append(("limit", "20"))
#     paramSet.append(("radius", "2000"))
#     paramSet.append(("offset_type", "0"))
#     paramSet.append(("has_coupon", "1"))
#     paramSet.append(("has_deal", "1"))
#     paramSet.append(("keyword", "泰国菜"))
#     paramSet.append(("sort", "7"))
#     getQueryString(appKey, secret, paramSet)
#     result = '{"status":"OK","cities":["全国","上海","北京","杭州","广州","南京","苏州","深圳"]}'
#     js = json.loads(result,"utf-8")
#     for city in js["cities"]:
#         print city
    with codecs.open('/home/zhangjin/data/dazhongdianping/data.json') as fr:
        for line in fr:
            s = json.loads(line,strict = False)
            for deal in s['deals']:
                print deal['deal_id']
