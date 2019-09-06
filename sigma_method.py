import numpy as np
import math
import datetime
from bsddb3 import db
from sortedcontainers import SortedDict

class SigmaMethodClass(object):
    def __init__(self, condition, name, active_interval, data):
        self.condition = condition
        self.name = name
        self.active_interval = active_interval
        self.data = data
        self.last_time = datetime.datetime.now()
        self.cur_time = None

    def calc_value(self, fact_cur, set_cur):
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
        fact_db = db.DB()
        set_db = db.DB()
        fact_cur = None
        set_cur = None
        try:
            fact_db.open(self.data[0], None, db.DB_BTREE, db.DB_DIRTY_READ)
            set_db.open(self.data[1], None, db.DB_BTREE, db.DB_DIRTY_READ)
        except(db.DBNoSuchFileError):
            pass
        try:
            fact_cur = SortedDict({datetime.datetime.strptime(time.decode('utf-8'), '%Y-%m-%d %H:%M:%S.%f'):
                                       float(value.decode('utf-8')) for time, value in dict(fact_db).items()})
            set_cur = SortedDict({datetime.datetime.strptime(time.decode('utf-8'), '%Y-%m-%d %H:%M:%S.%f'):
                                       float(value.decode('utf-8')) for time, value in dict(set_db).items()})
        except(db.DBError):
            pass

        if fact_cur:
            self.cur_time = fact_cur.peekitem()[0]
            try:
                if set_cur.peekitem()[1] == 0:
                    error = "error1"
                    # print("error1")
                elif math.fabs(set_cur.peekitem()[1] - fact_cur.peekitem()[1]) >= self.condition[1]:
                    error = "error2"
                    # print("error2")
                else:
                    value = self.calc_value(fact_cur, set_cur)

                    if (value >= ((self.condition[0]))):
                        error = "error3"
                    else:
                        error = "correct"
                        # print("error3")
                return error
            except(IndexError) as error:
                pass

    def check_active(self):
        if not self.cur_time:
            active = False
        elif self.cur_time - self.last_time >= datetime.timedelta(seconds=self.active_interval):
            active = False
        else:
            active = True
        self.last_time=datetime.datetime.now()
        return active
