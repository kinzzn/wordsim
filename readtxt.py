# -*- coding:utf-8 -*-

import re
from pymongo import MongoClient

def readtxt2db():
    client = MongoClient('localhost',27017)
    db = client['NLP']
    collection = db['Cilin']

    # # 读取文件写入数据库
    # txtpath = 'E:/20180129-词语相似度/词林扩展版.txt'
    # txt = open(txtpath, 'r')
    # lines = txt.readlines()
    # for line in lines:
    #     line.replace('\n','')   # 当前数据库中发现有空格
    #     line.replace('\r','')
    #     items = line.split(' ')
    #     index = items[0]
    #     for i in range(1,len(items)):
    #         collection.insert({'index':index,'word':items[i]})
    #         # print(index+' '+items[i])

    # 测试查询
    for item in collection.find({'index':{'$regex':'^Aa02A.*'}}):
        print(item['index'])
    print(collection.find({'index':{'$regex':'^Aa02A.*'}}).count())

readtxt2db()











