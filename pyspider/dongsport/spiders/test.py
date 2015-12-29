#!/usr/bin/env python
#!__*__encoding:utf-8__*__
'''
Created on 2015年8月31日

@author: zhangjin
'''
import requests
import os

def fileRead():
    with open("data") as f:
        for line in f:
            line = line.strip()
            print line.split("\t")[0]
            print line.split("\t")[1]

def crawlImage(url,path):
    if not os.path.exists(path) or not os.path.isdir(path):
        os.mkdir(path)
    name = url[url.rfind("/"):]
    path += name
    r = requests.get(url)
    with open(path, 'wb') as fd:
        for chunk in r.iter_content():
            fd.write(chunk)

if __name__ == '__main__':
    fileRead()
