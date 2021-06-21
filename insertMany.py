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
    message = "Rancher is open source software that combines everything an organizationneeds toadopand"
    for i in xrange(100):
        millis = int(round(time.time() * 1000))
        k = "user" + str(i)
        v = str(millis) + message + str(i)
        data[k] = v
    return data

def ret_doc():
    for i in xrange(10000):
        doc_list = [create_data() for i in range(1)]
        yield doc_list

def insertMany(name=None):
    print 'Run task %s (%s)...' % (name, os.getpid())
    for docs in ret_doc():
       ret = db.test.insert_many(docs)
       print ret

def multiProcess(process_num,func):
    jobs = []
    for i in xrange(process_num):
        p = multiprocessing.Process(target=func)
        jobs.append(p)
        p.start()
    for proc in jobs:
        proc.join()
    print 'All subprocesses done.'



if __name__ == "__main__":

    start = time.time()
    multiProcess(100,insertMany)
    end = time.time()
    print end-start
