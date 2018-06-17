import configparser
import redis

def redis_connect(host,port,db):
    try:
        r = redis.Redis(host=host,port=port,db=db)
        return r
    except:
        print('redis connect error')
        return None
def insert_data(r,type,index,str):
    try:
        r.zadd(type, str,index)
    except:
        print('redis insert error')


