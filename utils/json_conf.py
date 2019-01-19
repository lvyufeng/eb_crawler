import json
import os


class JsonConf:
    '''json配置文件类'''

    @staticmethod
    def store(data):
        with open("config.json", 'w') as json_file:
            json_file.write(json.dumps(data, indent=4))

    @staticmethod
    def load(path):
        if not os.path.exists(path):
            return None
        with open(path) as json_file:
            try:
                data = json.load(json_file)
            except:
                data = {}
            json_file.close()
            return data

    @staticmethod
    def set(data_dict,path):
        json_obj = JsonConf.load(path)
        for key in data_dict:
            json_obj[key] = data_dict[key]
        JsonConf.store(json_obj)
        print(json.dumps(json_obj, indent=4))


if __name__ == "__main__":
    data = {"a": " 1", "f": "100", "b": "3000"}
    JsonConf.set(data,'')