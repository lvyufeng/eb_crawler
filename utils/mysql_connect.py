import pymysql

def mysql_connect(ip,username,password,database):
    # 打开数据库连接
    db = pymysql.connect(ip, username, password, database ,use_unicode=True, charset="utf8")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    return db,cursor

def select_all(cursor,table,condition = None):
    if condition:
        sql = 'select * from ' + table + ' where ' + ' and '.join([key + '=' + condition[key] for key in condition.keys()])
    else:
        sql = 'select * from ' + table
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results
    except:
        print("Error: unable to fetch data")
        return None