import pymongo
import pymysql
import datetime
from decimal import Decimal
from etl_tools.cut_keyword import compare_name_keyword

category = ['124374002', '50020306', '50004711', '125226012', '50020299', '125060020', '50258012', '50016817', '123920001', '50025676', '50016806', '125256004', '125220009', '125076018', '125244008', '50013095', '126000001', '123188007',  '50015135', '125020022', '50004721', '50008047', '50009879', '50020319', '50050732', '123330001', '125204013', '124488006', '50025690', '50005948', '50009836', '50012190', '123258002', '121382038', '50018598', '50010535', '124466012', '123222004', '124174011', '50050694', '124848002', '125208008', '50012191', '50604012', '50009821', '124230011', '123634001', '50050395', '125226013', '50009858', '50015262', '50018801', '50010420', '125224009', '50013098', '50012991', '122666001', '50166001', '50015700', '124506003', '50138004', '50009557', '50013076', '124250006', '125048026', '125194002', '50013062', '50326001', '50009919', '50280002', '50020316', '50050725', '50023332', '50050687', '125088024', '50013057', '50008910', '50016796', '125060021', '50003923', '50009849', '50016850', '50025674', '125112030', '50050695', '50150002', '50013074', '50026317', '50050643', '50050728', '50004785', '50015198', '125284013', '50166002', '123190007', '50050393', '50009854', '50013000', '50016429', '50012195', '50009984', '125098026', '50009830',  '50015761', '50012990', '50008063', '125088017', '50050579', '50598001', '50013096', '50013092', '50050423', '50776032', '50050416', '50050147', '50016807', '125110023', '50015227', '50009856', '125260008', '50050428', '50008435', '50050372', '50002256', '123224005', '50020318', '124464007', '50020303', '50025683', '50026800', '124332006', '50528001', '50013082', '125216013', '50016091', '50015272', '50020310', '50012590', '50015218', '124484016', '50016818', '121484023', '50008628', '50023364', '124334003', '125226015', '50012988', '50050427', '50009839', '125286002', '50050698', '50025692', '50015214', '50015228', '125076017', '50394001', '125224006', '50015134', '50009843', '50050431', '124390001', '50013089', '50009983', '50018804', '50015211', '50026558', '50020304', '50009828', '50013185',  '50009560', '50012995', '50050382', '50008604', '50016848', '123190006', '50008617', '50018802', '121420038', '126472004', '123918001', '50050151', '50050396', '50009837', '50009857', '121422026', '50144001', '50025700', '124226017', '125268013', '50015704', '50050359', '50013100', '125210011', '50020300', '50013072', '50005945', '50013083', '50008908', '50007215', '124462015', '50016771', '50008432', '50050580', '50008630', '50015221', '50015207', '50016772', '50015197', '50050419', '50013067', '50050702', '50008624', '125200009', '125218010', '125228003', '50013061', '50015380', '50013087', '123922001', '50013085', '50020309', '50012186', '121408030', '50003251', '124500003', '50050425', '50050397', '50004709', '125020020', '50020312', '125044020', '50012989', '50013091', '50025699', '123236003', '50050150', '126412022', '121366039', '50015222', '124246009', '125084029', '50008612', '123218003', '50050420', '50018808', '123252002', '50050727', '50013088', '125098029', '50016422', '50050429', '121418019', '125040033', '125224010', '123248003', '50020311', '125092021', '50013075', '124458005', '50278005', '50050432', '125280010', '50050149', '50004783', '50008467', '121484022', '124174012', '125054019', '123222007', '125202009', '124228006', '50016443', '50026460', '50023334', '125236009', '50008430', '124498005', '50012992', '50026803', '125104027', '50050391', '50010891', '125260002', '50012196', '50008328',  '121448014', '125248005', '50008046',  '217305', '50166003', '124470001', '50013066', '50146001', '50008665', '125076013', '50015292', '50005773', '125242010', '50023066', '50015137', '125284014', '50050143', '125222011', '50552001', '124294001', '50013079', '50148001', '50025222', '50050669', '50050699', '50013103', '50015136', '121456017', '125114020', '121448015', '50026804', '50020320', '50025682', '50016852', '50050390', '125078026', '125042037', '50012998', '125224011', '121454038', '125218009', '50008649', '50026003', '124486012', '50012987', '50050724', '50020307', '50020323', '50009986', '50012999', '121404016', '125228012', '125268012', '50013084', '50015710', '50015715', '123190004', '50009861', '50003253', '124636001', '50015223', '50050731', '50013086', '50009562', '50146002', '50018812', '121470011', '50013090', '123256002', '126104013', '124466007', '125036027', '123238003', '121484024', '50150001', '50016845', '50005949', '50016847', '50020314', '50017138', '124476007', '50008674', '125230009', '50016853', '125060019', '50050415', '50020317', '50003860', '50025684', '50016801', '50023263',  '125258012', '50023331', '50023333', '50050693', '123210006', '125226016', '50018597', '124392005',  '50015717', '217308', '50008616', '50023044', '125284009', '50050672', '50011946', '124494004', '125216006', '50050667', '50008650', '50013064', '50012985', '50154001', '50020275', '50005776', '50015294', '125080007', '50013054', '217313', '210605', '50010550', '50050145', '123190005', '125236010', '50018837', '124488014', '50003404', '50026085', '50015209', '125200008', '125074026', '50009556', '125244010', '123220003', '124508011', '50016851', '50013065', '50152001', '125286001', '50008618', '124392004', '50018803', '126492001', '50008044', '50011943', '50020305', '50016854', '50009866', '50002766', '50012392', '50138003', '125112017', '50050421', '50015703', '124350003', '50050426', '50009860', '50015716', '125052025', '50019055', '124358002', '50023067', '50008613', '50012994', '50011942', '125036029', '50050413', '50050719', '50050394', '50017141', '50013093', '50009824', '123196007', '124456024', '121366028', '124348004', '50016236', '50015194', '50009898', '50005777', '50005946', '50050380', '125098025', '50016428', '125040021', '50020313', '50006762', '124372005', '50050383', '124478008', '50050578', '124240006', '50012993', '50013073', '50009846', '50010421', '124128007', '50020302', '50013078', '50050417', '124204011', '125672021', '50012943', '121416017', '50013101', '50050371', '50011947', '50012982', '50015962', '50013193', '50013152', '50050729', '124494008', '50016819', '50016235', '124388001', '124558013', '123210007', '123378001', '50015956', '124230012', '50002614', '50020298', '50003702', '50050701', '125020021', '50009859', '50023264', '123246002', '50009980', '50025680', '50013097', '125252002', '124216008', '50004784', '50005778', '50009981', '50050422', '123224003', '50013080', '124534019', '125092022', '123206005', '50013069', '50013094', '50050688', '50015711', '50023040', '123250002', '50008919', '125282004', '121408043', '125110019', '50020321', '50025687', '50025689', '50013081', '50013071', '50015196', '125268011', '123202003', '123244002', '124326002', '124432001', '124392002', '123194007', '50050730', '50009558', '124360005', '50016849', '123256001', '121454027', '123232002', '50013099', '50020296', '50050573', '125284012', '124146003', '50009979', '124204010', '50009841', '125226003', '50016427', '50013063', '50004710', '50020322', '50010566', '50012981', '50015219', '50012997', '50026316', '50015725', '50015213', '125084043', '50015755', '50009985', '50008431', '50050733',  '50050379', '50008625', '123196006', '120856009', '50012986', '50008651', '50008045', '50013068', '50012382', '124386002',  '50016846', '50328001', '125046003', '50018809', '123200008', '50050668', '50050434', '125208007', '50020315', '50006825', '125040022', '50016048', '125232009', '50015713', '125216012', '50013070', '50050385', '50050388', '50013102', '50008048', '50017231', '124464006', '50136009', '50015195', '124252006', '125032026', '126334003', '50556001', '50008623', '50020280', '50050424', '124092006', '50008433', '50012983', '50005774', '50050381', '50005947', '50050418', '123240003', '121364031', '50025691', '50009878', '123188001', '50008434', '50050146', '124356006', '125230008', '50015699', '50050414', '125094020', '50009835', '50016820', '124142014', '125022037', '50012996', '124484015', '50016855', '50009559', '50050734', '50013077', '50050430', '125098028', '50004720', '50020308', '50050433']


sku_keys = ['itemid','storeid','platform','name','salecount','commentcount','platform_categoryid','origin','province','city','factoryAddress','keyword','price','createtime','status','one']
# mongodb
#
# client = pymongo.MongoClient('202.202.5.140')
# database = client['test']
# collection = database['data_201811']

client = pymongo.MongoClient('localhost')
database = client['test']
collection = database['data_201812']
# mysql
db = pymysql.connect("202.202.5.140", "root", "cqu1701", "eb",charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


def suning_category(category):
    cats = ['喂养用品', '奶粉', '营养辅食', '食品保健/酒水饮料', '进口食品', '生鲜']
    if category in cats:
        return True
    else:
        return False

def pre_prosessing_price(price,promprice):
    if price is None or price == '' or '?' in price:
        price = '0'
    if promprice is None or promprice == '' or '?' in promprice:
        promprice = '0'

    if '-' in price and price.find('-') != 0:
        low = Decimal(price.split('-')[0])
        high = Decimal(price.split('-')[-1])

        price = ((high + low) / 2).quantize(Decimal('0.00'))
    else:
        try:
            price = Decimal(price).quantize(Decimal('0.00'))
        except:
            pass
    if '-' in promprice and promprice.find('-') != 0:
        low = Decimal(promprice.split('-')[0])
        high = Decimal(promprice.split('-')[-1])

        promprice = ((high + low) / 2).quantize(Decimal('0.00'))
    else:
        promprice = Decimal(promprice).quantize(Decimal('0.00'))

    if promprice > Decimal('0'):
        return promprice
    else:
        return price

    # pass

def find_area(city,data):
    data.pop('_id')
    try:
        data.pop('deliveryStartArea')
    except:
        pass
    keyword = data['keyword']
    data.pop('keyword')
    for i in data.values():
        try:
            if city in i:
                data['keyword'] = keyword
                return True
        except:
            continue

    return False

def find_store_location(city,data):
    try:
        if city in data['storeLocation']:
            # if 'storeLocation' in data else False
            return True
        else:
            return False
    except:
        return False
def get_store(data):
    store = {}

    store_kv = {'storeid':'storeActualID',
                'storename':'storeName',
                'company':'companyName',
                'province':'province',
                'city':'city',
                'platform' : 'website',
                'status': 1
                }

    if (data['website'] == 'Tmall' or data['website'] == 'TaoBao'):
        store_kv['company'] = 'factoryName'

    if data['website'] == 'JingDong':
        store_kv['province'] = 'storeLocation'

    for k,v in store_kv.items():
        try:
            store[k] = data[v]
        except:
            continue


    if data['website'] == 'TaoBao' and data['storeName'] == data['shopkeeper'] and ('店' in data['storeName'] or '天猫' in data['storeName']):
        store['platform'] = 'Tmall'

    if data['website'] == 'SuNing':
        store['province'] = '重庆'
    if (data['website'] == 'Tmall' or data['website'] == 'TaoBao') and 'factoryAddress' in data:
        area = ['万州','涪陵','渝中','大渡口','江北','沙坪坝','九龙坡','南岸','北碚','綦江','大足','渝北','巴南','黔江','长寿','江津','合川','永川','南川','璧山','铜梁','潼南','荣昌','梁平','城口','丰都','垫江','武隆','忠县','开县','忠州','开州','云阳','奉节','巫山','巫溪','石柱','秀山','酉阳','彭水',]

        for i in area:
            if i in data['factoryAddress']:
                store['city'] = i
                break
        if (data['website'] == 'YouLeGou') and 'companyName' in data:
            area = ['万州', '涪陵', '渝中', '大渡口', '江北', '沙坪坝', '九龙坡', '南岸', '北碚', '綦江', '大足', '渝北', '巴南', '黔江', '长寿', '江津',
                    '合川', '永川', '南川', '璧山', '铜梁', '潼南', '荣昌', '梁平', '城口', '丰都', '垫江', '武隆', '忠县', '开县', '忠州', '开州',
                    '云阳', '奉节', '巫山', '巫溪', '石柱', '秀山', '酉阳', '彭水', ]

            for i in area:
                if i in data['companyName']:
                    store['city'] = i
                    break
        # pass
        # if '区' in data['factoryAddress']:
        #     store['city'] = data['factoryAddress'][data['factoryAddress'].find('市')+1:data['factoryAddress'].find('区')+1]
        # elif '县' in data['factoryAddress']:
        #     store['city'] = data['factoryAddress'][data['factoryAddress'].find('市')+1:data['factoryAddress'].find('县')+1]



    store['status'] = 1
    return store


    pass

def get_sku(data):
    sku = {}


    sku_kv = {
                'itemid':'productActualID',
                'storeid':'storeActualID',
                'platform':'website',
                'name':'productName',
                'salecount':'monthSaleCount',
                'commentcount':'commentCount',
                'platform_categoryid':'categoryId',
                'origin':'origin',
                'province':'province',
                'city':'city',
                'factoryAddress':'factoryAddress',

                'keyword':'keyword',
    }

    if (data['website'] == 'Tmall' or data['website'] == 'TaoBao'):
        sku_kv['company'] = 'factoryName'

    if data['website'] == 'JingDong':
        sku_kv['province'] = 'storeLocation'


    for k,v in sku_kv.items():
        try:
            sku[k] = data[v]
        except:
            sku[k] = None
    if data['website'] == 'TaoBao' and data['storeName'] == data['shopkeeper'] and ('店' in data['storeName'] or '天猫' in data['storeName']):
        sku['platform'] = 'Tmall'
    if sku['storeid'] == None:
        sku['storeid'] = '00000000'
    sku['price'] = pre_prosessing_price(data['productPrice'], data['productPromPrice'])
    sku['createtime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sku['status'] = 0




    if data['website'] == 'SuNing':
        sku['province'] = '重庆'
    if (data['website'] == 'Tmall' or data['website'] == 'TaoBao') and 'factoryAddress' in data:
        area = ['万州','涪陵','渝中','大渡口','江北','沙坪坝','九龙坡','南岸','北碚','綦江','大足','渝北','巴南','黔江','长寿','江津','合川','永川','南川','璧山','铜梁','潼南','荣昌','梁平','城口','丰都','垫江','武隆','忠县','开县','云阳','奉节','巫山','巫溪','石柱','秀山','酉阳','彭水',]

        for i in area:
            if i in data['factoryAddress']:
                sku['city'] = i
                break


    return sku

def trans_store():
    count = 0
    total = 0
    for i in collection.find():
        total = total + 1
        valid = find_area('重庆',i)
        if valid:
            if i['website'] == 'SuNing' and not suning_category(i['category1']):
                continue
            if i['website'] == 'Tmall' and i['categoryId'] not in category:

                continue
            if '蛋糕' in i['productName'] or '鲜花' in i['productName']:
                continue
            count = count + 1
            store = get_store(i)


            sql = 'insert into ' + 'store' + '(' + ','.join(store.keys()) + ') ' + 'values(' + ','.join(['%s' for i in store.keys()]) + ')'
            # print(store)
            # data = eval(i['website'])(i)
            # # + datetime.datetime.now().strftime('%Y%m')
            # sql = 'INSERT INTO ' + 'sku_201810' + '(' + ','.join(data.keys()) + ') ' + 'values(' + ','.join(['%s' for i in data.keys()]) + ')'
            try:
                # 执行sql语句
                cursor.execute(sql,tuple(store.values()))
                # 执行sql语句
                db.commit()
            except Exception as e:
                # 发生错误时回滚
                db.rollback()

        # count = count + 1
            print('total: %s, count: %s' %(total,count))
def trans_sku(table):
    sql = 'INSERT INTO ' + table + '(' + ','.join(sku_keys) + ') ' + 'values(' + ','.join(['%s' for i in sku_keys]) + ')'

    total = 0
    # sku_list = []
    for i in collection.find():
        total = total + 1
        valid = find_area('重庆',i)
        if valid:
            print(total)
            if i['website'] == 'SuNing' and not suning_category(i['category1']):
                continue
            if (i['website'] == 'Tmall' or i['website'] == 'TaoBao') and i['categoryId'] not in category:
                continue
            if '蛋糕' in i['productName'] or '鲜花' in i['productName']:
                continue

            sku = get_sku(i)

            #sku['commentcount'] = sku['commentcount'] /2 + 10
            matched_keywords, level1 = compare_name_keyword(sku['name'],sku['keyword'])
            sku['keyword'] = matched_keywords
            sku['one'] = level1
            # sku_list.append(tuple([sku[key] for key in sku_keys]))
            # pass
            # # + datetime.datetime.now().strftime('%Y%m')
            try:
            # 执行sql语句
                cursor.execute(sql, tuple([sku[key] for key in sku_keys]))
                # 执行sql语句
                db.commit()
            except Exception as e:
                # 发生错误时回滚
                db.rollback()
    # for i in sku_list:
    #     try:
    #         comment = int(i['commentcount'])
    #     except Exception as e:
    #         print(e)
    #         pass
    # try:
    #     # 执行sql语句
    #     cursor.executemany(sql, sku_list)
    #     # 执行sql语句
    #     db.commit()
    # except Exception as e:
    #     # 发生错误时回滚
    #     db.rollback()


# 关闭数据库连接
def find_city():
    # sql = 'INSERT INTO ' + 'sku_201810' + '(' + ','.join(sku_keys) + ') ' + 'values(' + ','.join(['%s' for i in sku_keys]) + ')'
    total = 0
    count = 0
    # sku_list = []
    for i in collection.find():
        total = total + 1
        valid = find_store_location('重庆',i)
        if valid:
            # sku = get_sku(i)
            count = count + 1
            print(total,count)

def find_category():
    # sql = 'INSERT INTO ' + 'sku_201810' + '(' + ','.join(sku_keys) + ') ' + 'values(' + ','.join(['%s' for i in sku_keys]) + ')'
    total = 0
    count = 0
    cat_list = []
    for i in collection.find():
        cat_list.append(i['category1'])

    print(set(cat_list))

trans_sku('sku_201812')
# find_category()
# find_city()
trans_store()

db.close()
