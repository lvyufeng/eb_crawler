

def get_urls(file_path):
    urls = []
    with open(file_path,encoding='ISO-8859-1') as f:
        for line in f.readlines():
            split_line = line.split(',')
            urls.append(split_line[0].strip('\"'))
            # print(urls)
            # print(split_line)
    f.close()
    return urls

urls = get_urls('/Users/lvyufeng/PycharmProjects/eb_crawler/master/eb_crawler/utils/taskinfo.csv')

count = 0
for i in urls:
    if 'taobao' in i:
        count = count + 1

print(len(urls),count)
