#!usr/bin/env python
#__*__encoding:utf-8__*__
'''
Created on 2015年8月7日

@author: zhangjin
'''
import codecs
import sys

def start_differ(f1,f2):
    r""" 收集信息 ,进行比较"""
    a=[]
    with codecs.open(f1,'r', 'utf-8') as fr:
        for line in fr:
            a.append(line.strip())
    b=[]
    with codecs.open(f2,'r', 'utf-8') as fr:
        for line in fr:
            b.append(line.strip())

    dif = list(set(a).difference(set(b)))
    print "_"*15,f1," - " ,f2,len(dif),"_"*15
    for l in dif:
        print l
    dif = list(set(b).difference(set(a)))
    print "_"*15,f2," - " ,f1,len(dif),"_"*15
    for l in dif:
        print l

if __name__ == '__main__':
    print "*"*16,"详情","*"*16
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    start_differ(f1,f2)