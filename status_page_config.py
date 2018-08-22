import yaml

class StatusConfig(object):
    """docstring for Congig"""

    def __init__(self, file_name):
        self.config = yaml.load(open(file_name))
        self.head = self.config["head"]
        self.celery = self.config["celery"]
        self.graphics = self.config["graphics"]
        self.graphic_list = self.graphics["graphic_list"]

