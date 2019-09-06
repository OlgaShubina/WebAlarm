import asyncio
import time
import datetime
from check_cur import CheckData
import pika
from multiprocessing import Process
from multiprocessing.managers import BaseManager, SyncManager
import json
from collections import defaultdict
from pars_rule_config import RuleConfig
from rule_factory import RuleFactory
from bsddb3 import db


class ProcessData(object):
    def __init__(self):
        self.channel = []
        self.check = CheckData([10 ** (-3), 5, 20])
        self.channel_condition = defaultdict(defaultdict)
        self.config = {'met_1': 1, 'met_2': 2}
        #self.queue = Queue()
        self.time_delta = {'met_1': 20, 'met_2':7200}
        self.rule_config = RuleConfig("rule_config.yaml")
        self.rule_buffer = []





    def main_func(self, buffer, queue, loop):
        loop.run_until_complete(asyncio.gather(proc.process_receive(queue), proc.process_found_error(buffer, queue)))


class MyListManager(BaseManager):
    pass


syncarr = []
def get_arr():
    return syncarr

class MyManager(SyncManager):
    pass

syncdict = {}
def get_dict():
    return syncdict

if __name__ =='__main__':
    proc = ProcessData()
    #pool = Pool(processes=2)
    #queue = Queue()
    rule_factory = RuleFactory()
    #proc.buffer = rule_factory.create_buff()
    rule_factory.create_buff()
    #print(proc.buffer)
    proc.rule_buffer = rule_factory.create_rule()
    proc.channel = rule_factory.channel
    p1 = Process(target=proc.async_func, args=())
    p1.start()
    #proc.async_func(None)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='alarm_queue', durable=True)
    print('found_error')
    #proc.process_found_error2(channel)
    p2 = Process(target=proc.process_found_error2, args=(channel))
    p2.start()





