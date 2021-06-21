# -*- coding: utf-8 -*-
from pymongo import MongoClient
from urllib import quote_plus
import uuid
import time
from gevent import monkey;monkey.patch_all()
import gevent
import random
import string
import os
import multiprocessing


user, password = "***","***"
uri_1 = "s-***.mongodb.rds.aliyuncs.com:3717"
uri_2 = "s-***.mongodb.rds.aliyuncs.com:3717"
client = MongoClient([uri_1,uri_2])
client.admin.authenticate(user, password)
db=client.test

def create_data():
    data = {}
    message = "Rancher is open source software that combines everything an organization"
    for i in xrange(100):
        #精确到微妙
        millis = int(round(time.time() * 1000000))
        k = "user" + str(i)
        v = str(millis) + message +str(i)
        data[k] = v
    return data

def ret_doc():
    for i in range(1000000):
        doc_list = [create_data() for i in range(500)]
        yield doc_list
        doc_list = []

def insertMany(name=None):
    for docs in ret_doc():
       ret = db.test.insert_many(docs,ordered=False)
       print ret

def geventProcess(process_num):
    def insertOne(record_num):
        for i in xrange(record_num):
            doc = create_data()
            ret= db.test.insert_one(doc)
            print ret

    jobs = []
    client = MongoClient([uri_1,uri_2])
    client.admin.authenticate(user, password)
    db=client.test
    for n in range(process_num):
         jobs.append(gevent.spawn(insertOne,10000))
    gevent.joinall(jobs)

def multiProcess(process_num,func):
    jobs = []
    for i in xrange(process_num):
        p = multiprocessing.Process(target=func, args=(500,))
        jobs.append(p)
        p.start()
    for proc in jobs:
        proc.join()
    print 'All subprocesses done.'

def Search(k=None,limit=None):
    cur = None
    if limit:
        if k:
            cur =db.test.find({"key":str(k)}).limit(limit)
        else:
            print "query limit: %d" % limit
            cur =db.test.find().limit(limit)
    else:
        if k:
            cur =db.test.find({"key":str(k)})
        else:
            cur =db.test.find({"a":1})
    return cur

def testSearch(max):
    client = MongoClient([uri_1,uri_2])
    client.admin.authenticate(user, password)
    db=client.test
    for i in range(max):
        Search()

if __name__ == "__main__":
    start = time.time()
    multiProcess(4,geventProcess)
    end = time.time()
    print end-start
