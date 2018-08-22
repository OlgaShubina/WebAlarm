import numpy as np
import math
import datetime

class SigmaMethodClass(object):
    def __init__(self, condition, name, active_interval, data):
        self.condition = condition
        self.name = name
        self.active_interval = active_interval
        self.data = data
        self.last_time = datetime.datetime.now()

    def calc_value(self, fact_cur, set_cur):
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

    def found_error(self):
        fact_cur = self.data[self.data.keys()[0]]
        set_cur = self.data[self.data.keys()[1]]
        #print(self.name)
        try:
            if set_cur.peekitem()[1] == 0:
                error = "error1"
                # print("error1")
            elif math.fabs(set_cur.peekitem()[1] - fact_cur.peekitem()[1]) >= self.condition[1]:
                error = "error2"
                # print("error2")
            else:
                value = self.calc_value(fact_cur, set_cur)
                #print(value, self.condition)
                if (value <= ((self.condition[0]))):
                    error = "correct"
                else:
                    error = "error3"
                    # print("error3")
            return error
        except(IndexError):
            print(self.name)
            pass


    def check_active(self):
        try:
            if self.data[self.data.keys()[0]].peekitem()[0] - self.last_time >= datetime.timedelta(seconds=self.active_interval):
                active = False
            else:
                active = True
            self.last_time=datetime.datetime.now()
        except(IndexError):
            active = False
        return active
