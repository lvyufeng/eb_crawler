from urllib import parse

def get_urls(file_path,platform):
    """
    :param file_path: 文件路径
    :param platform: 电商平台
    :return: url list
    """

    urls = []
    with open(file_path,encoding='ISO-8859-1') as f:
        for line in f.readlines():
            split_line = line.split(',')
            # 'taobao' in split_line[0] or 'tmall'
            if platform in split_line[0]:
                id = split_line[0].strip('\"').split('=')[-1]
                data = parse.quote('{"exParams":"{\"id\":\"'+id+'\"}","itemNumId":"'+id+'"}')
                urls.append('http://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=' + data)
            # print(urls)
            # print(split_line)
    f.close()
    return urls