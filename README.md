# mongodb-stress-test
# requirments
please install packages and replace varibles with your mongodb environment
```
user, password = "***","***"
uri_1 = "s-***.mongodb.rds.aliyuncs.com:3717"
uri_2 = "s-***.mongodb.rds.aliyuncs.com:3717"
```
# running
`insertOne.py` use process + gevent to test insertOne operation
`insertMany.py` user multiProcess to test batch insert operation

# result
2 shard(each:4c8g)
mongodb: 
```
insert: 10k rps
batch inset: 20k rps
```
