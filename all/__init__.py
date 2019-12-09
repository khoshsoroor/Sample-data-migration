import yaml
import logging

logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('import_data.txt', 'wt', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(appname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        for k, v in self.__dict__.items():
            if type(v) == dict:
                setattr(self, k, Struct(**v))


f = open('setting.yml', 'rt')
setting = Struct(**yaml.load(f.read(), Loader=yaml.FullLoader))