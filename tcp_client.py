import asyncio
import time
import datetime
from req import Req
from pars_rule_config import RuleConfig
from bsddb3 import db
import json

DEFAULT_TIME_RESET = {'VEPP': 3600, 'Cryo': 4}
class ProcessDataBuffer(object):
    def __init__(self):
        self.channel = []
        self.rule_config = RuleConfig("rule_config.yaml")
        json_data = open("group_config.json").read()
        self.group_config = json.loads(json_data)

    def create_buff(self):

        req = Req("172.16.1.117", 80, "/api/v2")

        for met in self.rule_config.list_method:
            channel_array = []
            group = []

            t1 = datetime.datetime.strftime((datetime.datetime.now() - datetime.timedelta(
                hours=self.rule_config.__getattribute__(met)["insert_inteval"])), '%Y-%m-%d %H:%M:%S.%f')
            t2 = datetime.datetime.strftime((datetime.datetime.now() + datetime.timedelta(
                hours=self.rule_config.__getattribute__(met)["insert_inteval"])), '%Y-%m-%d %H:%M:%S.%f')

            group.append(self.rule_config.__getattribute__(met)["group_list"])

            for group in self.rule_config.__getattribute__(met)["group_list"]:
                str = group[:group.rfind("/")]
                try:
                    channel = self.group_config[group[:group.find("/")]][str][group]
                except(KeyError):
                    str = str[:str.rfind("/")]
                    channel = self.group_config[group[:group.find("/")]][str][group]
                channel_array += channel

            for i in req.CursorCompress(t1, t2, channel_array, "raw"):
                try:
                    if 'next' in i:
                        del i['next']
                    for ch in i:
                        cur_db = db.DB()
                        cur_db.open('./db/' + ch.replace('/', '_'), None, db.DB_BTREE, db.DB_CREATE)
                        #print('./db/' + ch.replace('/', '_'))
                        for data in i[ch]:
                            cur_db.put(bytes(list(data.keys())[0], 'utf-8'),
                                       bytes('{}'.format(list(data.values())[0]), 'utf-8'))
                        cur_db.close()
                except(KeyError) as err:
                    print(err)
                    pass

            self.channel += channel_array

    def create_subscribe(self, socket):
        for ch in self.channel:
            socket.write(str('n:%s|m:subscr|\n'%str(ch)).encode())

    def pars_string(self, data):
        try:
            name = data[data.find(":") + 1:data.find("|")]
            data = data[data.find("|") + 1:]
            time = data[data.find(":") + 1:data.find("|")]
            data = data[data.find("|") + 1:]
            value = data[data.find(":") + 1:data.find('\\')]
            cur_db = db.DB()
            cur_db.open('./db/' + name.replace('/', '_'), None, db.DB_BTREE, db.DB_DIRTY_READ | db.DB_CREATE)
            cursor = cur_db.cursor()
            if len(cur_db) >= DEFAULT_TIME_RESET[name[:name.find('/')]]:
                cur_db.delete(cursor.first()[0])
            cur_db.put(bytes(datetime.datetime.strptime(time, '%d.%m.%Y %H_%M_%S.%f').strftime('%Y-%m-%d %H:%M:%S.%f'),
                             'utf-8'), bytes(str(float(value)), 'utf-8'))
            cur_db.close()
        except ValueError:
            pass

        return str(data[data.find("\\")+3:])

    def await_func(self, data):
        str = data
        if str.find("descr") ==-1:
            while str != '':
                str = self.pars_string(str)

    async def reconnect(self):
        reader, writer = await asyncio.open_connection('172.16.1.110', 20041)

    async def process_receive(self):
        print("receive")
        reader, writer = await asyncio.open_connection('172.16.1.110', 20041)
        self.create_subscribe(writer)
        try:
            t1 = datetime.datetime.now()
            while True:
                t2 = datetime.datetime.now()
                if (t2 - t1).seconds >= 10:
                    writer.write(str('n:%s|m:get|\n' % str(self.channel[0])).encode())
                    if writer.can_write_eof():
                        reader, writer = await asyncio.open_connection('172.16.1.110', 20041)
                        self.create_subscribe(writer)
                t1 = datetime.datetime.now()
                data = (await reader.readline())
                self.await_func(str(data))
        except ConnectionRefusedError:
            print("Refused connection")
            writer.close()
            time.sleep(10)
            reader, writer = await asyncio.open_connection('172.16.1.110', 20041)
            self.create_subscribe(writer)

    def async_func(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.process_receive())


if __name__ =='__main__':
    process_data = ProcessDataBuffer()
    process_data.create_buff()
    print('Data buffer is crated!')
    process_data.async_func()


    # rule_factory = RuleFactory()
    # #proc.buffer = rule_factory.create_buff()
    # rule_factory.create_buff()
    # #print(proc.buffer)
    # proc.rule_buffer = rule_factory.create_rule()
    # proc.channel = rule_factory.channel
    # p1 = Process(target=proc.async_func, args=())
    # p1.start()
    # #proc.async_func(None)
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # channel = connection.channel()
    # channel.queue_declare(queue='alarm_queue', durable=True)
    # print('found_error')
    # #proc.process_found_error2(channel)
    # p2 = Process(target=proc.process_found_error2, args=(channel))
    # p2.start()





