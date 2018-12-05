import pymysql
import xlrd
import decimal

# table_wait_fix = 'data_201803'
table_wait_fix = 'productmonitor'
store_base = 'store_baseinfo'
product_base = 'product_baseinfo'
three_class = 'threeclassificationtable'


# basic util
def mysql_connect(ip,username,password,database):
    # 打开数据库连接
    db = pymysql.connect(ip, username, password, database ,use_unicode=True, charset="utf8")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    return db,cursor

def excel_read(path):
    workbook = xlrd.open_workbook(path)
    return workbook

def sheet_read(workbook,sheet_name):
    sheet = workbook.sheet_by_name(sheet_name)
    return sheet
# basic util test

def sheet_read_test(path):
    # path = '/Users/lvyufeng/PycharmProjects/eb_crawler/utils/2018年04月度报表批注.xlsx'
    workbook = excel_read(path)
    print(workbook.sheet_names())
    sheet = sheet_read(workbook,'3.1')
    print(sheet)
    pass

# sheet_read_test()

# query_util
def query_store_id(cursor,store_name,website):
    sql = 'SELECT storeActualId FROM ' + store_base + ' WHERE storeName = %s AND platform = %s'
    try:
        # 执行SQL语句
        cursor.execute(sql,(store_name,website))
        # 获取所有记录列表
        results = cursor.fetchall()
        if len(results) == 1:
            return results[0][0]
        else:
            return [i[0] for i in results]
    except Exception as e:
        print("Error: unable to fetch data",e)
        return None
    pass

def count_city_ids(cursor,city):
    sql = "SELECT productActualID,std_stdPrice,monthSaleCount,isValid FROM " + table_wait_fix + " WHERE std_city = %s AND (website = 'TaoBao' OR website = 'Tmall')"
    try:
        # 执行SQL语句
        cursor.execute(sql,(city))
        # 获取所有记录列表
        results = cursor.fetchall()

        return [list(i) for i in results]
    except Exception as e:
        print("Error: unable to fetch data",e)
        return None
    pass
def get_city_count(path):
    # path = '2018年04月度报表批注.xlsx'
    workbook = excel_read(path)
    sheet = sheet_read(workbook, '附件4')
    result = {}
    for i in range(3, sheet.nrows):
        if '板块' in sheet.cell_value(i,0) or '版块' in sheet.cell_value(i,0) or '总计' in sheet.cell_value(i,0):
            pass
        else:
            result[str(sheet.cell_value(i,0)).strip('区').strip('县')] = sheet.cell_value(i,2)

    return result
    pass

# get_city_count()

def query_product_id(cursor,store_id,product_name):
    sql = 'SELECT productActualID FROM ' + product_base + ' WHERE storeActualID = %s AND productName = %s'
    try:
        # 执行SQL语句
        cursor.execute(sql,(store_id,product_name))
        # 获取所有记录列表
        results = cursor.fetchall()
        return results[0][0]
    except Exception as e:
        # print("Error: unable to fetch data", e)
        return None
    pass

def query_store_product_ids(cursor,store_id,year,month):
    # sql = 'SELECT  FROM ' + product_base + ' WHERE storeActualID = %s'

    sql = """SELECT productmonitor.productActualID,productmonitor.std_price,productmonitor.monthSaleCount,productmonitor.isValid_statistics FROM productmonitor,product_baseinfo 
            WHERE product_baseinfo.storeActualID = %s 
            and productmonitor.productActualID = product_baseinfo.productActualID
            and productmonitor.`year` = %s
            and productmonitor.monthOfYear = %s
    """
    try:
        # 执行SQL语句
        cursor.execute(sql,(store_id,year,month))
        # 获取所有记录列表
        results = cursor.fetchall()
        return [list(i) for i in results]
    except Exception as e:
        # print("Error: unable to fetch data", e)
        return None
    pass

def query_sanpinyibiao_product_ids(cursor,keyword,year,month):
    # sql = 'SELECT productActualID,std_price,monthSaleCount,isValid_statistics FROM ' + table_wait_fix + ' WHERE keyword = %s'

    sql = """SELECT productmonitor.productActualID,productmonitor.std_price,productmonitor.monthSaleCount,productmonitor.isValid_statistics FROM productmonitor,product_baseinfo 
                WHERE product_baseinfo.singleKeyword = %s 
                and productmonitor.productActualID = product_baseinfo.productActualID
                and productmonitor.`year` = %s
                and productmonitor.monthOfYear = %s
        """

    try:
        # 执行SQL语句
        cursor.execute(sql,(keyword,year,month))
        # 获取所有记录列表
        results = cursor.fetchall()
        return [list(i) for i in results]
    except Exception as e:
        # print("Error: unable to fetch data", e)
        return None
    pass

def query_category_product_ids(cursor,keyword,year,month):
    sql = """SELECT productmonitor.productActualID,productmonitor.std_price,productmonitor.monthSaleCount,productmonitor.isValid_statistics FROM productmonitor,product_baseinfo 
                    WHERE product_baseinfo.singleKeyword = %s 
                    and productmonitor.productActualID = product_baseinfo.productActualID
                    and productmonitor.`year` = %s
                    and productmonitor.monthOfYear = %s
            """
    try:
        # 执行SQL语句
        cursor.execute(sql,(keyword,year,month))
        # 获取所有记录列表
        results = cursor.fetchall()
        return [list(i) for i in results]
    except Exception as e:
        print("Error: unable to fetch data", e)
        return []
    pass

def query_all_ids(db, cursor,platform,sheet_name,path):
    # path = '2018年04月度报表批注.xlsx'
    # db, cursor = mysql_connect('139.224.112.239', 'root', '1701sky', 'ebmis_db')
    workbook = excel_read(path)
    sheet = sheet_read(workbook, sheet_name)
    product_id = None
    datas = []
    for i in range(3,sheet.nrows):
        # print(sheet.cell_value(i,6))
        store_id = query_store_id(cursor, sheet.cell_value(i,6),platform)
        if type(store_id) == list:
            for id in store_id:
                product_id = query_product_id(cursor, id, sheet.cell_value(i, 1))
                if product_id:
                    break
            print(sheet.cell_value(i, 0), store_id, product_id)
        else:
            product_id = query_product_id(cursor, store_id, sheet.cell_value(i,1))
            print(sheet.cell_value(i,0),store_id,product_id)
        datas.append({
            'productActualID':product_id,
            'monthSaleCount':int(sheet.cell_value(i,3)),
            'productPromPrice':sheet.cell_value(i,4),
            'std_price':sheet.cell_value(i,4),
            'isValid_statistics':0,
        })
    # db.close()

    return datas
    pass

def get_all_products(db, cursor,platform,sheet_name,path,year,month):
    update_list,remove_list = [],[]
    update,remove = compute_top20_store(db, cursor,platform,sheet_name,path,year,month)
    for i in update:
        if i[3] == 1:
            update_list.append({
                'productActualID':i[0],
                'monthSaleCount':i[2],
                'productPromPrice':i[1],
                'std_price':i[1],
                'isValid_statistics':0,
            })
    for i in remove:
        if i[3] == 1:
            remove_list.append({
                'productActualID':i[0],
            })

    return update_list,remove_list

def get_all_spyb_products(db,cursor,path,year,month):
    update_list,remove_list = [],[]
    update,remove = compute_sanpinyibiao(db,cursor,path,year,month)
    for i in update:
        if i[3] == 1:
            update_list.append({
                'productActualID':i[0],
                'monthSaleCount':i[2],
                'productPromPrice':i[1],
                'std_price':i[1],
                'isValid_statistics':0,
            })
    for i in remove:
        if i[3] == 1:
            remove_list.append({
                'productActualID':i[0],
            })

    return update_list,remove_list

def get_all_cat_products(db,cursor,path,year,month):
    update_list, remove_list = [], []
    update, remove = compute_category(db,cursor,path,year,month)
    for i in update:
        if i[3] == 1:
            update_list.append({
                'productActualID': i[0],
                'monthSaleCount': i[2],
                'productPromPrice': i[1],
                'std_price': i[1],
                'isValid_statistics': 0,
            })
    for i in remove:
        if i[3] == 1:
            remove_list.append({
                'productActualID': i[0],
            })

    return update_list, remove_list

    pass
def get_city_info(cursor):
    sql = "SELECT productActualID,loc_city,singleKeyword FROM " + product_base + " WHERE loc_province = '%s'" %('重庆')
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        return [list(i) for i in results]
    except Exception as e:
        # print("Error: unable to fetch data", e)
        return None
    pass

def get_sanpinyibiao(cursor):
    sql = "SELECT 三级 FROM " + three_class + " WHERE loc_famous = 1"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        return [list(i) for i in results]
    except Exception as e:
        # print("Error: unable to fetch data", e)
        return None
    pass

def get_cat_3(cursor,cat_1):
    sql = "SELECT 三级 FROM " + three_class + " WHERE 一级 = '%s'" %(cat_1)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        return [i[0] for i in results]
    except Exception as e:
        # print("Error: unable to fetch data", e)
        return None
    pass
# query_util test
def query_util_test(db,cursor):
    # db,cursor = mysql_connect('139.224.112.239','root','1701sky','ebmis_db')
    store_id = query_store_id(cursor,'天猫超市')
    print(store_id)
    # product_id = query_product_id(cursor,store_id,'陈吉旺福 重庆小麻花512g 袋装独立小包装糕点心零食特产手工制作')
    # print(product_id)
    # db.close()
    pass
# query_util_test()

# update_utils
def update_single_product(db,cursor,data,year,month):
    # SQL 更新语句
    update_sql = "UPDATE " + table_wait_fix + " SET "
    where_condition = " WHERE productActualID = '%s' and year = '%s' and monthOfYear = '%s'" % (data['productActualID'],year,month)
    data.pop('productActualID')
    mid = ','.join([key + "=" + "'%s'" % (str(data[key])) for key in data.keys()])
    try:
        # 执行SQL语句
        cursor.execute(update_sql + mid + where_condition)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # 发生错误时回滚
        print(e)
        db.rollback()
    pass

# delete util
def remove_single_product(db,cursor,data,year,month):
    db.ping(reconnect=True)
    # SQL 删除语句
    sql = "DELETE FROM " + table_wait_fix + " WHERE productActualID = '%s' and year = '%s' and monthOfYear = '%s'" % (data['productActualID'],year,month)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
    except Exception as e:
        # 发生错误时回滚
        print(e)
        db.rollback()

    # 关闭连接
    # db.close()
    pass
# compute util
def compute_store_price(db, cursor,store_id,actual_total,year,month):
    # db, cursor = mysql_connect('localhost', 'root', '19960704', 'ebmis_db')
    product_ids = list(query_store_product_ids(cursor,store_id,year,month))
    result = []
    remove = []
    product_valid_totals = [i[1]*decimal.Decimal(i[2]) if i[3]==1 else 0 for i in product_ids]
    product_invalid_totals = [i[1]*decimal.Decimal(i[2]) if i[3]==0 else 0 for i in product_ids]
    product_prices = [i[1] for i in product_ids]
    # print(product_ids)
    valid_total = sum(product_valid_totals)
    invalid_total = sum(product_invalid_totals)

    sub = actual_total - invalid_total
    nums = [int(i/valid_total*sub/product_prices[product_valid_totals.index(i)]) if product_ids[product_valid_totals.index(i)][3]==1 else 0 for i in product_valid_totals]

    for index,item in enumerate(product_ids):
        if item[3] == 0:
            result.append(item)
        elif nums[index] != 0:
            item[2] = nums[index]
            result.append(item)
        else:
            remove.append(item)
    # print(result)
    # return product_ids
    total = sum([i[1]*decimal.Decimal(i[2]) for i in result])
    if product_ids[product_prices.index(min(product_prices))] in result:
        product_ids[product_prices.index(min(product_prices))][2] += int((actual_total - total) / min(product_prices))
    else:
        item = product_ids[product_prices.index(min(product_prices))]
        remove.remove(item)
        item[2] = int((actual_total - total) / min(product_prices))
        result.append(item)

    # print(min(product_prices))
    total = sum([i[1] * decimal.Decimal(i[2]) for i in result])


    # return actual_total,total
    print(actual_total,total)
    # db.close()
    return result,remove
    pass
def compute_top20_store(db, cursor,platform,sheet_name,path,year,month):
    # path = '2018年04月度报表批注.xlsx'
    # db, cursor = mysql_connect('139.224.112.239', 'root', '1701sky', 'ebmis_db')
    workbook = excel_read(path)
    sheet = sheet_read(workbook, sheet_name)
    update_datas = []
    remove_datas = []
    for i in range(2,sheet.nrows):
        # print(sheet.cell_value(i,6))
        store_id = query_store_id(cursor, sheet.cell_value(i,1),platform)
        result,remove = compute_store_price(db, cursor,store_id,decimal.Decimal(sheet.cell_value(i,3) * 10000),year,month)
        update_datas.extend(result)
        remove_datas.extend(remove)
        # datas.append(store_id)
    # db.close()
    # print(datas)
    return update_datas,remove_datas

def compute_sanpinyibiao_price(db, cursor,keyword,actual_total,year,month):
    # db, cursor = mysql_connect('localhost', 'root', '19960704', 'ebmis_db')
    product_ids = list(query_sanpinyibiao_product_ids(cursor,keyword,year,month))
    if product_ids == []:
        return [],[]
    result = []
    remove = []
    product_valid_totals = [i[1]*decimal.Decimal(i[2]) if i[3]==1 else 0 for i in product_ids]
    product_invalid_totals = [i[1]*decimal.Decimal(i[2]) if i[3]==0 else 0 for i in product_ids]
    product_prices = [i[1] for i in product_ids]
    # print(product_ids)
    valid_total = sum(product_valid_totals)
    invalid_total = sum(product_invalid_totals)
    total_price = sum(product_prices)

    sub = actual_total - invalid_total
    nums = [int(i/valid_total*sub/product_prices[product_valid_totals.index(i)]) if product_ids[product_valid_totals.index(i)][3]==1 else 0 for i in product_valid_totals] if valid_total != decimal.Decimal(0) else [int(sub/total_price) for i in product_prices]

    for index,item in enumerate(product_ids):
        if item[3] == 0:
            result.append(item)
        elif nums[index] != 0:
            item[2] = nums[index]
            result.append(item)
        else:
            remove.append(item)
    # print(result)
    # return product_ids
    total = sum([i[1]*decimal.Decimal(i[2]) for i in result])
    if product_ids[product_prices.index(min(product_prices))] in result:
        product_ids[product_prices.index(min(product_prices))][2] += int((actual_total - total) / min(product_prices))
    else:
        item = product_ids[product_prices.index(min(product_prices))]
        remove.remove(item)
        item[2] = int((actual_total - total) / min(product_prices))
        result.append(item)

    # print(min(product_prices))
    total = sum([i[1] * decimal.Decimal(i[2]) for i in result])


    # return actual_total,total
    print(actual_total,total)
    # db.close()
    return result,remove
    pass

def compute_sanpinyibiao(db,cursor,path,year,month):
    # path = '2018年04月度报表批注.xlsx'
    # db, cursor = mysql_connect('139.224.112.239', 'root', '1701sky', 'ebmis_db')
    workbook = excel_read(path)
    sheet = sheet_read(workbook, '附件5')
    update_datas = []
    remove_datas = []
    for i in range(2,22):
        # print(sheet.cell_value(i,6))
        result,remove = compute_sanpinyibiao_price(db,cursor,sheet.cell_value(i,1),decimal.Decimal(sheet.cell_value(i,2) * 10000),year,month)
        update_datas.extend(result)
        remove_datas.extend(remove)
    return update_datas,remove_datas

def compute_category_price(db, cursor,keywords,actual_total,year,month):
    # db, cursor = mysql_connect('localhost', 'root', '19960704', 'ebmis_db')
    product_ids = []
    for i in keywords:
        product_ids.extend(query_category_product_ids(cursor,i,year,month))
    if product_ids == []:
        return [],[]
    result = []
    remove = []
    product_valid_totals = [i[1]*decimal.Decimal(i[2]) if i[3]==1 else 0 for i in product_ids]
    product_invalid_totals = [i[1]*decimal.Decimal(i[2]) if i[3]==0 else 0 for i in product_ids]
    product_prices = [i[1] for i in product_ids]
    # print(product_ids)
    valid_total = sum(product_valid_totals)
    invalid_total = sum(product_invalid_totals)
    total_price = sum(product_prices)

    sub = actual_total - invalid_total
    nums = [int(i/valid_total*sub/product_prices[product_valid_totals.index(i)]) if product_ids[product_valid_totals.index(i)][3]==1 else 0 for i in product_valid_totals] if valid_total != decimal.Decimal(0) else [int(sub/total_price) for i in product_prices]

    for index,item in enumerate(product_ids):
        if item[3] == 0:
            result.append(item)
        elif nums[index] != 0:
            item[2] = nums[index]
            result.append(item)
        else:
            remove.append(item)
    # print(result)
    # return product_ids
    total = sum([i[1]*decimal.Decimal(i[2]) for i in result])
    if product_ids[product_prices.index(min(product_prices))] in result:
        product_ids[product_prices.index(min(product_prices))][2] += int((actual_total - total) / min(product_prices))
    else:
        item = product_ids[product_prices.index(min(product_prices))]
        remove.remove(item)
        item[2] = int((actual_total - total) / min(product_prices))
        result.append(item)

    # print(min(product_prices))
    total = sum([i[1] * decimal.Decimal(i[2]) for i in result])


    # return actual_total,total
    print(actual_total,total)
    # db.close()
    return result,remove
    pass

def compute_category(db,cursor,path,year,month):
    # path = '2018年04月度报表批注.xlsx'
    # db, cursor = mysql_connect('139.224.112.239', 'root', '1701sky', 'ebmis_db')
    workbook = excel_read(path)
    sheet = sheet_read(workbook, '附件3')
    update_datas = []
    remove_datas = []
    for i in range(2,35):
        # print(sheet.cell_value(i,3),decimal.Decimal(sheet.cell_value(i,4) * 10000))
        keys = get_cat_3(cursor,sheet.cell_value(i,3))
        # print(keys)
        result,remove = compute_category_price(db,cursor,keys,decimal.Decimal(sheet.cell_value(i,4) * 10000),year,month)
        update_datas.extend(result)
        remove_datas.extend(remove)
    return update_datas,remove_datas
# compute_sanpinyibiao()
# for different sheet fix
def prepare(db, cursor,month):

    sql = """
    INSERT into productmonitor(productmonitor.productInnerId,
 productmonitor.productActualID,
  productmonitor.weight,
  productmonitor.std_weight,
  productmonitor.std_weight_unit,
  productmonitor.productPrice,
  productmonitor.productPromPrice,
  productmonitor.std_price,
  productmonitor.unit_price,
  productmonitor.monthSaleCount,
  productmonitor.commentCount,
  productmonitor.platform,
  productmonitor.extractTime,
  productmonitor.analyzeTime,
  productmonitor.year,
  productmonitor.monthOfYear,
  productmonitor.dayOfMonth) SELECT productmonitor.productInnerId,
 productmonitor.productActualID,
  productmonitor.weight,
  productmonitor.std_weight,
  productmonitor.std_weight_unit,
  productmonitor.productPrice,
  productmonitor.productPromPrice,
  productmonitor.std_price,
  productmonitor.unit_price,
  productmonitor.monthSaleCount,
  productmonitor.commentCount,
  productmonitor.platform,
  productmonitor.extractTime,
  productmonitor.analyzeTime,
  productmonitor.year,
  %s,
  productmonitor.dayOfMonth FROM productmonitor WHERE `year` = 2018 and monthOfYear = 4"""


    try:
        # 执行SQL语句
        cursor.execute(sql,month)
        # 获取所有记录列表
        db.commit()

    except Exception as e:
        print("Error: unable to fetch data", e)


def fill_city(db, cursor):
    # db, cursor = mysql_connect('139.224.112.239', 'root', '1701sky', 'ebmis_db')
    result = get_city_info(cursor)
    # db.close()

    local,cursor = mysql_connect('localhost','root','19960704','ebmis_db')
    for i in result:
        update_single_product(local,cursor, {
            'productActualID': i[0],
            'std_city': i[1],
            'keyword':i[2]
        })
    pass

# fill_city()

def top20_sku_fix(db,cursor,path,year,month):
    datas = []
    # db,cursor = mysql_connect('localhost','root','19960704','ebmis_db')
    # db, cursor = mysql_connect('139.224.112.239', 'root', '1701sky', 'ebmis_db')
    datas.extend(query_all_ids(db,cursor,'Tmall', '3.1',path))
    datas.extend(query_all_ids(db,cursor,'TaoBao', '3.2',path))

    # print(datas)
    for i in datas:
        update_single_product(db,cursor,i,year,month)
    # datas = query_all_ids('TaoBao', '3.2')
    # print(datas)
    pass

def top20_store_fix(db, cursor,path,year,month):
    # db, cursor = mysql_connect('139.224.112.239', 'root', '1701sky', 'ebmis_db')
    platform = {
        'Tmall':'2.1',
        'TaoBao':'2.2'
    }
    remove_list,update_list = [],[]
    for k,v in platform.items():
        # print(k,v)
        update_list,remove_list = get_all_products(db, cursor,k,v,path,year,month)

        for i in update_list:
            update_single_product(db, cursor, i,year,month)
        for j in remove_list:
            remove_single_product(db, cursor, j,year,month)

    pass

def city_fix(db, cursor):
    citys = get_city_count()
    # db, cursor = mysql_connect('localhost', 'root', '19960704', 'ebmis_db')
    for k,v in citys.items():
        result = count_city_ids(cursor,k)
        print(k,v,len(result))
    pass

def sanPinYiBiao_fix(db,cursor,path,year,month):
    update_list, remove_list = get_all_spyb_products(db,cursor,path,year,month)
    # db, cursor = mysql_connect('localhost', 'root', '19960704', 'ebmis_db')
    for i in update_list:
        update_single_product(db, cursor, i,year,month)
    for j in remove_list:
        remove_single_product(db, cursor, j,year,month)
    pass

def category_fix(db,cursor,path,year,month):
    compute_category(db,cursor,path,year,month)
    update_list, remove_list = get_all_cat_products(db,cursor,path,year,month)
    # db, cursor = mysql_connect('localhost', 'root', '19960704', 'ebmis_db')
    for i in update_list:
        update_single_product(db, cursor, i,year,month)
    for j in remove_list:
        remove_single_product(db, cursor, j,year,month)
    pass


db, cursor = mysql_connect('localhost', 'root', '19960704', 'ebmis_db_new')
year = 2018
excel_list = {
    1:'2018年1月报表v1.xlsx',
    2:'2018年2月报表(改）.xlsx',
    3:'2018年03月度报表.xlsx',
}

for k,v in excel_list.items():
    print(k,v)
    month = k
    path = v
    prepare(db, cursor,month)
    top20_sku_fix(db, cursor,path,year,month)
    top20_store_fix(db, cursor,path,year,month)
    sanPinYiBiao_fix(db,cursor,path,year,month)
    category_fix(db,cursor,path,year,month)

db.close()