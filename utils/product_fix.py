import pymysql
import xlrd
import decimal

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
def sheet_read_test():
    path = '/Users/lvyufeng/PycharmProjects/eb_crawler/utils/2018年04月度报表批注.xlsx'
    workbook = excel_read(path)
    print(workbook.sheet_names())
    sheet = sheet_read(workbook,'3.1')
    print(sheet)
    pass

# sheet_read_test()
def query_all_ids(platform,sheet_name):
    path = '2018年04月度报表批注.xlsx'
    db, cursor = mysql_connect('139.224.112.239', 'root', '1701sky', 'ebmis_db')
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
            'std_stdPrice':sheet.cell_value(i,4),
            'isValid':0,
        })
    db.close()

def top20_sku_fix():
    datas = []
    db,cursor = mysql_connect('localhost','root','19960704','ebmis_db')
    datas.extend(query_all_ids('Tmall', '3.1'))
    datas.extend(query_all_ids('TaoBao', '3.2'))

    # print(datas)
    for i in datas:
        update_single_product(db,cursor,i)
