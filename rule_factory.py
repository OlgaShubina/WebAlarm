import json
from pars_rule_config import RuleConfig
import datetime
from collections import defaultdict
from sigma_method import SigmaMethodClass
from extrapolation_method import ExtrapolationMethodClass
import pika
import time
from redis_storage import RedisStorage

redis_storage = RedisStorage("localhost", 6379, 1)

class RuleFactory(object):
    def __init__(self):
        self.rule_config = RuleConfig("rule_config.yaml")
        json_data = open("group_config.json").read()
        self.group_config = json.loads(json_data)
        self.rule_buffer = []
        self.channel_condition = defaultdict(defaultdict)

    def create_rule(self):
        for i in self.rule_config.list_method:
            for group in self.rule_config.__getattribute__(i)["group_list"]:
                str = group[:group.rfind("/")]
                try:
                    channel = ['./db/'+ ch.replace('/','_') for ch in self.group_config[group[:group.find("/")]][str][group]]
                except(KeyError):
                    str = str[:str.rfind("/")]
                    channel = ['./db/'+ ch.replace('/','_') for ch in self.group_config[group[:group.find("/")]][str][group]]
                self.rule_buffer.append(eval(self.rule_config.__getattribute__(i)["name_class"])(self.rule_config.__getattribute__(i)["error_value"],
                                                                                                 group, self.rule_config.__getattribute__(i)["active_interval"],
                                                                                                 channel))
        return self.rule_buffer

    def process_found_error(self, channel):
        print('found error')
        t1 = datetime.datetime.now() - datetime.timedelta(minutes=1)
        while True:
            t2=datetime.datetime.now()
            if (t2-t1).seconds >= 20:
                t1 = datetime.datetime.now()
            for i in self.rule_buffer:
                error = i.found_error()
                active = i.check_active()
                self.channel_condition[i.name]["info"] = error
                self.channel_condition[i.name]["active"] = active
                redis_storage.save_system_state(i.name, self.channel_condition[i.name])
            channel.basic_publish(exchange='', routing_key='alarm_queue', body=str(json.dumps(self.channel_condition)),
                                     properties=pika.BasicProperties(delivery_mode=2, ))
            time.sleep(3)



if __name__ =='__main__':
    factory = RuleFactory()
    factory.create_rule()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='alarm_queue', durable=True)
    factory.process_found_error(channel)
