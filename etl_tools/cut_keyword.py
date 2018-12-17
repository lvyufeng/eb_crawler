import jieba

def cut_keyword(keyword):
    t = jieba.cut(keyword,cut_all=False)
    return [i for i in t]  # 全模式

def compare_name_keyword(name,keyword):
    words = cut_keyword(keyword)
    count = 0
    for i in words:
        if i in name:
            count = count + 1
    if count > 1:
        return True
    else:
        return False

# print(cut_keyword('合川凤山米'))