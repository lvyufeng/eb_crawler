# import pymongo
#
# client = pymongo.MongoClient('localhost',27017)
# # client = pymongo.MongoClient('localhost',27017)
# test = client['test']
# pd = test['test_tb']
# print(pd.find().count())
# #
# test = [1,2,3]
# t = (v for v in test)
# print(t,(1,2,3))
import re
save = open('jd_cat.csv','w+',encoding='gbk')

with open('test.html','r') as f:
    text = f.read()
    # print(text)
    list = re.compile(r"(?<=\"n\":\").+?(?=\")").findall(text)
    # print(list)
    for i in list:
        cat = re.compile(r"(?<=cat=).+?(?=&)").findall(i)
        name = re.compile(r"(?<=\|).+?(?=\|\|0)").findall(i)
        if cat:
            save.write('\"%s\",\"%s\"\n' %(cat[0],name[0]))
        else:
            cat = re.compile(r"^[0-9].+?(?=\|\|0)").findall(i)
            if cat:
                save.write('\"%s\",\"%s\"\n' %(cat[0].split('|')[0],cat[0].split('|')[1]))
            pass
f.close()
save.close()