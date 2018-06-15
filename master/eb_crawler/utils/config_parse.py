import configparser

def config_parse(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config

