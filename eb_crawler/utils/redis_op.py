import configparser
import redis

def insert_data(host,port,db,type,str):
    try:
        r = redis.Redis(host=host,port=port,db=db)
    except:
        print('redis connect error')
    else:
        r.lpush(type,str)
