import pymongo
import pymysql

def db_connect(config):



    db = pymysql.connect("localhost", "root", "19960704", "ebmis_db",use_unicode=True, charset="utf8")