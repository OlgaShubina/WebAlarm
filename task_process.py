from celery import Celery
from tcp_client import Process
from check_cur import CheckData
import asyncio

app = Celery('tasks', backend='amqp', broker='amqp://')

input_dict = {"VEPP/SOL/1S1": ['VEPP/SOL/1S1/MCur.1', 'VEPP/SOL/1S1/SCur'],
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
                                             'VEPP/SOL/4S3/MCur.1', 'VEPP/SOL/4S3/SCur']

@app.task
def main_process(self):
    proc = Process(input_dict)
    check = CheckData([10 ** (-3), 5])
    buffer = proc.create_buff()
    # print(len(buffer["VEPP/SOL/1S1"]['VEPP/SOL/1S1/MCur.1'].keys()))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(proc.process_receive(check))