import json
from pars_rule_config import RuleConfig
from sigma_method import SigmaMethodClass
from extrapolation_method import ExtrapolationMethodClass
from req import Req
from sortedcontainers import SortedDict
import datetime
from collections import defaultdict

class RuleFactory(object):
    def __init__(self):
        self.rule_config = RuleConfig("rule_config.yaml")
        json_data = open("group_config.json").read()
        self.group_config = json.loads(json_data)
        self.rule_buffer = []
        self.buffer = SortedDict()
        self.channel_condition = defaultdict(defaultdict)
        self.channel = []

    def create_buff(self):

        req = Req("172.16.1.117", 80, "/api/v1")

        array1 = []
        #print(self.group_config)
        for met in self.rule_config.list_method:
            channel = []
            for group in self.rule_config.__getattribute__(met)["group_list"]:
                #print(group)
                #for k, i in self.group_config[group[:group.find("/")]][group[:group.rfind("/")]].items():
                str = group[:group.rfind("/")]
                try:
                    channel += self.group_config[group[:group.find("/")]][str][group]
                    #print(self.group_config[group[:group.find("/")]][str][group])
                except(KeyError):
                    str = str[:str.rfind("/")]
                    channel += self.group_config[group[:group.find("/")]][str][group]
                   # print(self.group_config[group[:group.find("/")]][str][group])

            #print(self.channel)
            array = []
            buffer = SortedDict()
            #print(channel)
            print((datetime.datetime.now() - datetime.timedelta(hours=self.rule_config.__getattribute__(met)["insert_inteval"])),(datetime.datetime.now() + datetime.timedelta(hours=self.rule_config.__getattribute__(met)["insert_inteval"])), met)
            t1 = datetime.datetime.strftime((datetime.datetime.now() - datetime.timedelta(hours=self.rule_config.__getattribute__(met)["insert_inteval"])),'%Y-%m-%d %H:%M:%S.%f')
            t2 = datetime.datetime.strftime((datetime.datetime.now() + datetime.timedelta(hours=self.rule_config.__getattribute__(met)["insert_inteval"])),'%Y-%m-%d %H:%M:%S.%f')
            for i in req.CursorCompress(t1, t2, channel, "raw"):
                try:
                    array.append(i)
                except(KeyError):
                    pass
            for i in array:
                try:
                    del i["next"]
                except(KeyError):
                    pass
            #print(array)

            for group in self.rule_config.__getattribute__(met)["group_list"]:
                buff_data = SortedDict()
                #print(self.group_config[group[:group.find("/")]][group[:group.rfind("/")]])
                str = group[:group.rfind("/")]
                try:
                    arr = self.group_config[group[:group.find("/")]][str][group]
                except(KeyError):
                    str = str[:str.rfind("/")]
                    arr = self.group_config[group[:group.find("/")]][str][group]

                for ch in arr:
                    result = SortedDict()
                    #print(array[0][ch])
                    try:
                        for i in array[0][ch]:
                            result[datetime.datetime.strptime(i["time"],'%Y-%m-%d %H:%M:%S.%f')] = float(i["value"])
                    except(KeyError):
                        pass
                    buff_data[ch]=result
                #print(buff_data.keys())
                if len(buff_data)!=0:
                    self.buffer[group] = buff_data
                for k in buffer.keys():
                    self.channel_condition[k] = {"active": True}
                #channel.basic_publish(exchange='', routing_key='alarm_queue', body=str(json.dumps(self.channel_condition)),
                 #                        properties=pika.BasicProperties(delivery_mode=2, ))

            self.channel += channel
        #print(self.channel)
        return self.buffer

    def create_rule(self):
        for i in self.rule_config.list_method:
            for group in self.rule_config.__getattribute__(i)["group_list"]:
                self.rule_buffer.append(eval(self.rule_config.__getattribute__(i)["name_class"])(self.rule_config.__getattribute__(i)["error_value"],
                                                                                                 group, self.rule_config.__getattribute__(i)["active_interval"],
                                                                                                 self.buffer[group]))
        return self.rule_buffer


if __name__ =='__main__':
    factory = RuleFactory()
    factory.create_rule()
