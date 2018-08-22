import socket
import asyncio
import time
from req import Req
from sortedcontainers import SortedDict
import datetime
from check_cur import CheckData
import pika
from multiprocessing import Process, Manager, Pool, Array, Queue
from multiprocessing.managers import BaseManager, SyncManager
import json
import copy
from collections import defaultdict
from pars_rule_config import RuleConfig
from rule_factory import RuleFactory

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='alarm_queue', durable=True)

input_dict = {
    'met_1':{"VEPP/SOL/1S1": ['VEPP/SOL/1S1/MCur.1', 'VEPP/SOL/1S1/SCur'],
              "VEPP/SOL/1S2": ['VEPP/SOL/1S2/MCur.1', 'VEPP/SOL/1S2/SCur'],
              "VEPP/SOL/1S3": ['VEPP/SOL/1S3/MCur.1', 'VEPP/SOL/1S3/SCur'],
              "VEPP/SOL/2S1": ['VEPP/SOL/2S1/MCur.1', 'VEPP/SOL/2S1/SCur'],
              "VEPP/SOL/2S2": ['VEPP/SOL/2S2/MCur.1', 'VEPP/SOL/2S2/SCur'],
              "VEPP/SOL/2S3": ['VEPP/SOL/2S3/MCur.1', 'VEPP/SOL/2S3/SCur'],
              "VEPP/SOL/3S1": ['VEPP/SOL/3S1/MCur.1', 'VEPP/SOL/3S1/SCur'],
              "VEPP/SOL/3S2": ['VEPP/SOL/3S2/MCur.1', 'VEPP/SOL/3S2/SCur'],
              "VEPP/SOL/3S3": ['VEPP/SOL/3S3/MCur.1', 'VEPP/SOL/3S3/SCur'],
              "VEPP/SOL/4S1": ['VEPP/SOL/4S1/MCur.1', 'VEPP/SOL/4S1/SCur'],
              "VEPP/SOL/4S2": ['VEPP/SOL/4S2/MCur.1', 'VEPP/SOL/4S2/SCur'],
              "VEPP/SOL/4S3": ['VEPP/SOL/4S3/MCur.1', 'VEPP/SOL/4S3/SCur'],
              "VEPP/QUAD/1D1": ['VEPP/QUAD/1D1/MCur.1', 'VEPP/QUAD/1D1/SCur'],
              "VEPP/QUAD/1D2": ['VEPP/QUAD/1D2/MCur.1', 'VEPP/QUAD/1D2/SCur'],
              "VEPP/QUAD/1D3": ['VEPP/QUAD/1D3/MCur.1', 'VEPP/QUAD/1D3/SCur'],
              "VEPP/QUAD/1F2": ['VEPP/QUAD/1F2/MCur.1', 'VEPP/QUAD/1F2/SCur'],
              "VEPP/QUAD/1F3": ['VEPP/QUAD/1F3/MCur.1', 'VEPP/QUAD/1F3/SCur'],
              "VEPP/QUAD/2D1": ['VEPP/QUAD/2D1/MCur.1', 'VEPP/QUAD/2D1/SCur'],
              "VEPP/QUAD/2D2": ['VEPP/QUAD/2D2/MCur.1', 'VEPP/QUAD/2D2/SCur'],
              "VEPP/QUAD/2D3": ['VEPP/QUAD/2D3/MCur.1', 'VEPP/QUAD/2D3/SCur'],
              "VEPP/QUAD/2F2": ['VEPP/QUAD/2F2/MCur.1', 'VEPP/QUAD/2F2/SCur'],
              "VEPP/QUAD/2F3": ['VEPP/QUAD/2F3/MCur.1', 'VEPP/QUAD/2F3/SCur'],
              "VEPP/QUAD/3D1": ['VEPP/QUAD/3D1/MCur.1', 'VEPP/QUAD/3D1/SCur'],
              "VEPP/QUAD/3D2": ['VEPP/QUAD/3D2/MCur.1', 'VEPP/QUAD/3D2/SCur'],
              "VEPP/QUAD/3D3": ['VEPP/QUAD/3D3/MCur.1', 'VEPP/QUAD/3D3/SCur'],
              "VEPP/QUAD/3F2": ['VEPP/QUAD/3F2/MCur.1', 'VEPP/QUAD/3F2/SCur'],
              "VEPP/QUAD/3F3": ['VEPP/QUAD/3F3/MCur.1', 'VEPP/QUAD/3F3/SCur'],
              "VEPP/QUAD/4D1": ['VEPP/QUAD/4D1/MCur.1', 'VEPP/QUAD/4D1/SCur'],
              "VEPP/QUAD/4D2": ['VEPP/QUAD/4D2/MCur.1', 'VEPP/QUAD/4D2/SCur'],
              "VEPP/QUAD/4D3": ['VEPP/QUAD/4D3/MCur.1', 'VEPP/QUAD/4D3/SCur'],
              "VEPP/QUAD/4F2": ['VEPP/QUAD/4F2/MCur.1', 'VEPP/QUAD/4F2/SCur'],
              "VEPP/QUAD/4F3": ['VEPP/QUAD/4F3/MCur.1', 'VEPP/QUAD/4F3/SCur']
    },
    'met_2': {
              "Cryo/Level/Cr-1": ["Cryo/Level/Cr-1/LHe"],
              "Cryo/Level/Cr-2": ["Cryo/Level/Cr-2/LHe"],
              "Cryo/Level/Cr-3": ["Cryo/Level/Cr-3/LHe"],
              "Cryo/Level/Cr-4": ["Cryo/Level/Cr-4/LHe"]
    }
}
array1 = ['VEPP/SOL/1S1/MCur.1', 'VEPP/SOL/1S1/SCur',
          'VEPP/SOL/1S2/MCur.1', 'VEPP/SOL/1S2/SCur',
          'VEPP/SOL/1S3/MCur.1', 'VEPP/SOL/1S3/SCur',
          'VEPP/SOL/2S1/MCur.1', 'VEPP/SOL/2S1/SCur',
          'VEPP/SOL/2S2/MCur.1', 'VEPP/SOL/2S2/SCur',
          'VEPP/SOL/2S3/MCur.1', 'VEPP/SOL/2S3/SCur',
          'VEPP/SOL/3S1/MCur.1', 'VEPP/SOL/3S1/SCur',
          'VEPP/SOL/3S2/MCur.1', 'VEPP/SOL/3S2/SCur',
          'VEPP/SOL/3S3/MCur.1', 'VEPP/SOL/3S3/SCur',
          'VEPP/SOL/4S1/MCur.1', 'VEPP/SOL/4S1/SCur',
          'VEPP/SOL/4S2/MCur.1', 'VEPP/SOL/4S2/SCur',
          'VEPP/SOL/4S3/MCur.1', 'VEPP/SOL/4S3/SCur'#,
          #'VEPP/QUAD/1D1/MCur.1', 'VEPP/QUAD/1D1/SCur',
          #'VEPP/QUAD/1D2/MCur.1', 'VEPP/QUAD/1D2/SCur',
          #'VEPP/QUAD/1D3/MCur.1', 'VEPP/QUAD/1D3/SCur',
          #'VEPP/QUAD/1F2/MCur.1', 'VEPP/QUAD/1F2/SCur',
          #'VEPP/QUAD/1F3/MCur.1', 'VEPP/QUAD/1F3/SCur',
          #'VEPP/QUAD/2D1/MCur.1', 'VEPP/QUAD/2D1/SCur',
          #'VEPP/QUAD/2D2/MCur.1', 'VEPP/QUAD/2D2/SCur',
          #'VEPP/QUAD/2D3/MCur.1', 'VEPP/QUAD/2D3/SCur',
          #'VEPP/QUAD/2F2/MCur.1', 'VEPP/QUAD/2F2/SCur',
          #'VEPP/QUAD/2F3/MCur.1', 'VEPP/QUAD/2F3/SCur',
          #'VEPP/QUAD/3D1/MCur.1', 'VEPP/QUAD/3D1/SCur',
          #'VEPP/QUAD/3D2/MCur.1', 'VEPP/QUAD/3D2/SCur',
          #'VEPP/QUAD/3D3/MCur.1', 'VEPP/QUAD/3D3/SCur',
          #'VEPP/QUAD/3F2/MCur.1', 'VEPP/QUAD/3F2/SCur',
          #'VEPP/QUAD/3F3/MCur.1', 'VEPP/QUAD/3F3/SCur',
          #'VEPP/QUAD/4D1/MCur.1', 'VEPP/QUAD/4D1/SCur',
          #'VEPP/QUAD/4D2/MCur.1', 'VEPP/QUAD/4D2/SCur',
          #'VEPP/QUAD/4D3/MCur.1', 'VEPP/QUAD/4D3/SCur',
          #'VEPP/QUAD/4F2/MCur.1', 'VEPP/QUAD/4F2/SCur',
          #'VEPP/QUAD/4F3/MCur.1', 'VEPP/QUAD/4F3/SCur',
          ]
class ProcessData(object):
    def __init__(self):
        #manager = Manager()
        self.buffer = SortedDict()
        json_data = open("group_config.json").read()
        self.input = json.loads(json_data)
        self.channel = []
        self.check = CheckData([10 ** (-3), 5, 20])
        self.channel_condition = defaultdict(defaultdict)
        self.config = {'met_1': 1, 'met_2': 2}
        #self.queue = Queue()
        self.time_delta = {'met_1': 20, 'met_2':7200}
        self.rule_config = RuleConfig("rule_config.yaml")
        self.rule_buffer = []


    def create_buff(self):

        req = Req("172.16.1.117", 80, "/api/v1")

        array1 = []
        for met, data in self.input.items():
            array = []
            buffer = SortedDict()
            self.channel = []
            for k,i in data.items():
                self.channel+=i
            #print(self.channel)
            t1 = datetime.datetime.strftime((datetime.datetime.now() - datetime.timedelta(hours=self.config[met])),'%Y-%m-%d %H:%M:%S.%f')
            t2 = datetime.datetime.strftime((datetime.datetime.now() + datetime.timedelta(hours=self.config[met])),'%Y-%m-%d %H:%M:%S.%f')
            for i in req.CursorCompress(t1, t2, self.channel, "raw"):
                try:
                    array.append(i)
                except(KeyError):
                    pass
            for i in array:
                try:
                    del i["next"]
                except(KeyError):
                    pass
            #print(array, len(array1),len(array))

            for name,sec in data.items():
                buff_data = SortedDict()
               # print(name, sec)
                for ch in sec:
                    result = SortedDict()
                    #print(array[0][ch])
                    try:
                        for i in array[0][ch]:
                            result[datetime.datetime.strptime(i["time"],'%Y-%m-%d %H:%M:%S.%f')] = float(i["value"])
                    except(KeyError):
                        pass
                    buff_data[ch]=result
                print(buff_data.keys())
                if len(buff_data)!=0:
                    self.buffer[name] = {'data': buff_data, 'method': met}
                for k in buffer.keys():
                    self.channel_condition[k] = {"active": True}
            #channel.basic_publish(exchange='', routing_key='alarm_queue', body=str(json.dumps(self.channel_condition)),
             #                        properties=pika.BasicProperties(delivery_mode=2, ))
           # print(self.channel_condition)
        return self.buffer

    def create_subscribe(self, socket):
        for ch in self.channel:
            #print('n:%s|m:subscr|\n'%str(ch))
            socket.write(str('n:%s|m:subscr|\n'%str(ch)).encode())

    def pars_string(self, data, queue):
        try:
            name = data[data.find(":") + 1:data.find("|")]
            data = data[data.find("|") + 1:]
            time = data[data.find(":") + 1:data.find("|")]
            data = data[data.find("|") + 1:]
            value = data[data.find(":") + 1:data.find('\\')]

            queue.put((name, datetime.datetime.strptime(time, '%d.%m.%Y %H_%M_%S.%f'), float(value)))
        except ValueError:
            pass
        #queue.close()
       # print(queue.get())
        return str(data[data.find("\\")+3:])

    def await_func(self, data, queue):
        str = data
        #print(str)
        if str.find("descr") ==-1:
            while str != '':
                str = self.pars_string(str, queue)

    async def reconnect(self):
        reader, writer = await asyncio.open_connection('172.16.1.110', 20041)

    async def process_receive(self, queue):
        print("receive")
        reader, writer = await asyncio.open_connection('172.16.1.110', 20041)
        self.create_subscribe(writer)
        try:
            #x = 0
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
                #print(data)
                self.await_func(str(data), queue)
                #await asyncio.sleep(0)
                #print("data")
                #x+=1
        except ConnectionRefusedError:
            print("Refused connection")
            writer.close()
            time.sleep(10)
            reader, writer = await asyncio.open_connection('172.16.1.110', 20041)
            self.create_subscribe(writer)


    def process_found_error(self, queue):
        #x = 0
        cur_condition = dict(self.channel_condition)
        print("founed_error")
       # queue.close()
        t1 = datetime.datetime.now()
        while True:
            cur_condition = self.channel_condition
            t2=datetime.datetime.now()
            #print(queue)
            queue.put("done")
            while queue.get != "done":
                try:
                    cur = queue.get()
                    print(cur)
                    #arr = self.buffer
                    del self.buffer[str(cur[0][:cur[0].rfind("/")])]['data'][cur[0]][
                        self.buffer[str(cur[0][:cur[0].rfind("/")])]['data'][cur[0]].keys()[0]]
                    self.buffer[str(cur[0][:cur[0].rfind("/")])]['data'][cur[0]][cur[1]] = cur[2]
                    #self.buffer = arr
                except:
                    break
            #print((t2-t1).seconds)
            if (t2-t1).seconds>=20:
                print(self.buffer)
                t1 = datetime.datetime.now()
            array_error = []
            for t, ch in self.buffer.items():
                #print(ch)
                if ch['method'] == 'met_1':
                    error = self.check.found_error1(ch['data'][ch['data'].keys()[0]], ch['data'][ch['data'].keys()[1]])
                    self.channel_condition[t]["info"] = error
                elif ch['method'] == 'met_2':
                    error = self.check.found_error2(ch['data'][ch['data'].keys()[0]])
                    self.channel_condition[t]["info"] = error
                #print(ch['data'][ch['data'].keys()[0]].peekitem()[0])
                if datetime.datetime.now()-ch['data'][ch['data'].keys()[0]].peekitem()[0]>=datetime.timedelta(seconds=self.time_delta[ch['method']]):
                    print(self.time_delta[ch['method']], ch['data'][ch['data'].keys()[0]].peekitem()[0])
                    self.channel_condition[t]["active"] = False
                else:
                    self.channel_condition[t]["active"] = True
                #print(ch.keys()[0], ch.keys()[1])
                #if error == True:
                   # array_error.append(t)
            #print(self.channel_condition, cur_condition)
            #if cur_condition != self.channel_condition:
                # await asyncio.sleep(0)
                #print("condition")
            channel.basic_publish(exchange='', routing_key='alarm_queue', body=str(json.dumps(self.channel_condition)),
                                     properties=pika.BasicProperties(delivery_mode=2, ))
            time.sleep(3)
            #x += 1
        #print(buffer)

    def process_found_error2(self, queue):
        t1 = datetime.datetime.now()
        while True:
            t2=datetime.datetime.now()
            #print(queue)
            #queue.put("done")
           # print(queue.qsize())
            cur = ()
            while datetime.datetime.now()-t2<=datetime.timedelta(seconds=3):
                    cur = queue.get()
                    #print(cur)
                    del self.buffer[str(cur[0][:cur[0].rfind("/")])][cur[0]][
                        self.buffer[str(cur[0][:cur[0].rfind("/")])][cur[0]].keys()[0]]
                    self.buffer[str(cur[0][:cur[0].rfind("/")])][cur[0]][cur[1]] = cur[2]
            print("done")
            #print((t2-t1).seconds)
            if (t2-t1).seconds>=20:
                #print(self.buffer["VEPP/SOL/1S1"])
                t1 = datetime.datetime.now()
            for i in self.rule_buffer:
                error = i.found_error()
                active = i.check_active()
                self.channel_condition[i.name]["info"] = error
                self.channel_condition[i.name]["active"] = active
            channel.basic_publish(exchange='', routing_key='alarm_queue', body=str(json.dumps(self.channel_condition)),
                                     properties=pika.BasicProperties(delivery_mode=2, ))


            time.sleep(3)
            #x += 1
        #print(buffer)

    def async_func(self, queue):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.process_receive(queue))

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
    pool = Pool(processes=2)
    queue = Queue()
    rule_factory = RuleFactory()
    proc.buffer = rule_factory.create_buff()
    proc.rule_buffer = rule_factory.create_rule()
    proc.channel = rule_factory.channel
    #print(proc.buffer["VEPP/UM/F1/1F1"])
    p1 = Process(target=proc.async_func, args=(queue, ))
    p1.start()
    p2 = Process(target=proc.process_found_error2, args=(queue, ))
    p2.start()




