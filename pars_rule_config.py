import yaml

class RuleConfig(object):
    """docstring for Congig"""

    def __init__(self, file_name):
        self.config = yaml.load(open(file_name))
        self.list_method = self.config["list_method"]
        for i in self.list_method:
            self.__setattr__(i, self.config[i])




