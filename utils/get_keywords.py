import pymongo

def get_keywords():
    keywords = []
    client = pymongo.MongoClient('localhost')
    db = client['test']
    collection = db['keywords']

    for i in collection.find():
        keywords.append(i['keyword'])


    return keywords

# print(get_keywords())

