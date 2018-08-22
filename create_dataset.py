import socket
import asyncio
import time
import datetime
import csv
import time
from sortedcontainers import SortedDict
from check_cur import CheckData
import pika
from multiprocessing import Process, Manager, Pool, Array, Queue
from multiprocessing.managers import BaseManager, SyncManager
import json
import copy
from collections import defaultdict
from pars_rule_config import RuleConfig

channel = ["VEPP/SOL/1S1/MCur.1"]


def close_files(csv_writers):
    while csv_writers:
        name, (csvfile, writer) = csv_writers.popitem()
        csvfile.close()

def create_subscribe(socket):
    for ch in channel:
        # print('n:%s|m:subscr|\n'%str(ch))
        socket.write(str('n:%s|m:subscr|\n' % str(ch)).encode())


def pars_string(data, queue):
    try:
        name = data[data.find(":") + 1:data.find("|")]
        data = data[data.find("|") + 1:]
        time = data[data.find(":") + 1:data.find("|")]
        data = data[data.find("|") + 1:]
        value = data[data.find(":") + 1:data.find('\\')]
        #print(time, value, name)
        queue.put((name, datetime.datetime.strptime(time, '%d.%m.%Y %H_%M_%S.%f'), float(value)))
    except ValueError:
        pass
    return str(data[data.find("\\")+3:])

def await_func(data, queue):
    str = data
    print(str)
    if str.find("descr") ==-1:
        while str != '':
            str = pars_string(str, queue)

async def process_receive(queue):
    reader, writer = await asyncio.open_connection('172.16.1.110', 20041)
    create_subscribe(writer)
    try:
        t1 = datetime.datetime.now()
        t = datetime.datetime.now()
        while datetime.datetime.now() - t <= datetime.timedelta(hours=7):
            t2 = datetime.datetime.now()
            if (t2 - t1).seconds >= 10:
                writer.write(str('n:%s|m:get|\n' % str(channel[0])).encode())
                if writer.can_write_eof():
                    reader, writer = await asyncio.open_connection('172.16.1.110', 20041)
                    create_subscribe(writer)
            t1 = datetime.datetime.now()
            data = (await reader.readline())

            await_func(str(data), queue)

    except ConnectionRefusedError:
        print("Refused connection")
        writer.close()
        time.sleep(10)
        reader, writer = await asyncio.open_connection('172.16.1.110', 20041)
        create_subscribe(writer)

def async_func(queue):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_receive(queue))

def write_csw(queue):
    print("write")
    csv_writers = defaultdict(tuple)
    for ch in channel:
        name = str(ch).replace('/', '_') + '.csv'
        csvfile = open(name, 'w')
        writer = csv.DictWriter(csvfile, fieldnames=['time', 'value'])
        csv_writers[ch] = (csvfile, writer)
    #print(csv_writers)
    t = datetime.datetime.now()
    while datetime.datetime.now() - t <= datetime.timedelta(hours=7, seconds=10):
            time.sleep(20)
            buffer = defaultdict(defaultdict)
            #print(queue.qsize())
            queue.put("done")
            cur = ()
            while cur!="done":
                try:
                    cur = queue.get()
                    #print(cur)
                    buffer[str(cur[0])][cur[1]] = cur[2]
                except:
                    break
            #print(buffer)
            del buffer["d"]

            for ch in channel:
               # print(ch)
                csvfile, writer = csv_writers[ch]
                for t,v in buffer[ch].items():
                    print(t, v)
                    writer.writerow({"time": str(t), "value": str(v)})

    close_files(csv_writers)


if __name__ =='__main__':
    queue = Queue()


    p1 = Process(target=async_func, args=(queue,))
    p1.start()
    p1 = Process(target=write_csw, args=(queue,))
    p1.start()

