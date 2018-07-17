import configparser

class config_parser():
    def __init__(self,path = ''):
        if not path.strip():
            self.__path = 'conf.ini'
        else:
            self.__path = path

    # 获取配置数据
    def getStr(self,section,option):
        cf = configparser.ConfigParser()
        try:
            cf.read(self.__path)
            ret = cf.get(section,option)
            return ret
        except Exception as e:
            print(e)
            return ''

    def getInt(self,section,option):
        cf = configparser.ConfigParser()
        try:
            cf.read(self.__path)
            ret = cf.get(section,option)
            return int(ret)
        except Exception as e:
            print(e)
            return 0