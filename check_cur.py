import numpy as np
import pika
import sys
import math
import statistics
from scipy.interpolate import interp1d
import datetime

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

class CheckData(object):
    def __init__(self, condition):
        self.condition = condition
        #self.value_arr = []

    def calc_value(self, fact_cur, set_cur):
        buff = []
        buff2 = []
        value_arr = []
        index_start = list(set_cur.keys())[0]
        for t,i in set_cur.items():
            if i != list(set_cur.values())[list(set_cur.values()).index(i)+1]:
                #rint(t)
                index_end = t
                if index_start != index_end:                          
                    for t1, i1 in fact_cur.items():
                        if t1> index_start and t1<index_end:
                            buff.append(i1) 

                value = np.std(buff) / np.average(buff)
                value_arr.append(value)
                index_start = list(set_cur.keys())[list(set_cur.keys()).index(t)+1]

                buff = []        
        
        return value_arr

    def calc_value2(self, fact_cur, set_cur):
        buff = []
        buff2 = []
        index_start = set_cur.iloc[-1]
        end_index = 0

        for t,i in set_cur.items():
            if math.fabs(i - set_cur[set_cur.iloc[set_cur.index(t)-1]]) > 10**(-3):
                index_end = t
                for t1, i1 in fact_cur.items():
                    if t1>= index_start and t1<index_end:
                        if set_cur[set_cur.iloc[set_cur.index(index_start)]]!=0:
                            buff2.append(i1 / set_cur[set_cur.iloc[set_cur.index(index_start)]])
                        else:
                            buff2.append(set_cur[set_cur.iloc[set_cur.index(index_start)]])
                        #print(i1, set_cur[set_cur.iloc[set_cur.index(index_start)]], t1, t)
                        end_index = fact_cur.index(t1)
                index_start = set_cur.iloc[set_cur.index(t)]
        for i in fact_cur.values()[end_index:]:
            #print(i)
            if(set_cur[set_cur.iloc[set_cur.index(index_start)]]==0):
                buff2.append(i)
            else:
                buff2.append(i/set_cur[set_cur.iloc[set_cur.index(index_start)]])
       # print(buff2)
        value = np.std(buff2)
       # print(statistics.stdev(buff2))

        return value


    def calc_value3(self, fact_cur, set_cur):
        buff = []
        buff2 = []
        value_arr = []
        index_start = 0
        for i in set_cur:
            if i != set_cur[set_cur.index(i) + 1]:
                index_end = set_cur.index(i)
                if index_start == index_end:
                    buff.append(fact_cur[int(index_start)])
                    buff2.append(set_cur[int(index_start)])
                else:
                    buff = fact_cur[int(index_start):int(index_end)]
                    buff2 = set_cur[int(index_start):int(index_end)]
                value = np.std(buff) / np.average(buff)
                value_arr.append(value)
                #print(np.std(buff),np.average(buff), buff, buff2, len(buff), len(buff2))
                index_start = set_cur.index(i) + 1
                buff = []
                buff2 = []
            # print(value_arr)
        return value_arr

    def found_error1(self, fact_cur, set_cur):
        if set_cur.peekitem()[1] == 0:
            error = "error1"
            #print("error1")
        elif math.fabs(set_cur.peekitem()[1] - fact_cur.peekitem()[1]) >= self.condition[1]:
            error = "error2"
            #print("error2")
        else:
            value = self.calc_value2(fact_cur, set_cur)
            #print(value)
            if (value<=self.condition[0]):
                error = "correct"
            else:
                error = "error3"
                #print("error3")
        return error
       # channel.basic_publish(exchange='', routing_key='task_queue', body="error-" + str(error), properties=pika.BasicProperties(delivery_mode=2,))
       # connection.close()
        #print(error)

    def found_error2(self, value):
        x = []
        y = []
        #print(value)
        for k,i in value.items():
            x.append(k.timestamp())
            y.append((float(i)))
        x_interp = np.linspace(x[0], x[len(x) - 1] + 18000, len(x) * 2.5)
        # y_interp = np.interp(x_interp, x, y)
        f = interp1d(x, y, fill_value='extrapolate')
        new_y = f(datetime.datetime.now().timestamp())
        #print(new_y)
        if new_y < 20:
            error = "error4"
        else:
            error = "correct"
        return error

    def process_found_error(self, buffer):
        array_error = []
        for t, ch in buffer.items():
            error = self.found_error(ch[ch.keys()[0]], ch[ch.keys()[1]])
            #if error == True:
            array_error.append(t)

        if len(array_error) != 0:
        #await asyncio.sleep(0)
            channel.basic_publish(exchange='', routing_key='task_queue', body=str(array_error),
                              properties=pika.BasicProperties(delivery_mode=2, ))
         # connection.close()
        print("done")

