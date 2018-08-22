import csv
import matplotlib.pyplot as plt
#import numpy as np
from check_cur import CheckData
import traces
from sortedcontainers import SortedDict
#from pandas import date_range,Series,DataFrame,read_csv, qcut
from collections import defaultdict, OrderedDict
import datetime
import sys


if __name__ =='__main__':
    fact_cur1 = SortedDict()
    set_cur1 = SortedDict()
    fact_cur2 = SortedDict()
    set_cur2 = SortedDict()
    fact_cur3 = SortedDict()
    set_cur3 = SortedDict()
    fact_cur = SortedDict()
    set_cur = SortedDict()

    obj = CheckData([10 ** (-3)])
    t1 = datetime.datetime.now()
    with open("VEPP_SOL_4S1_MCur.1.1.csv", "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            fact_cur1[datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S.%f')] = (float(row[1]))

    with open("VEPP_SOL_4S1_SCur.1.csv", "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            set_cur1[datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S.%f')]=(float(row[1]))
    obj.found_error(fact_cur1, set_cur1)

    t2 = datetime.datetime.now()
    obj = CheckData([10 ** (-3)])
    with open("VEPP_SOL_4S1_MCur.1.2.csv", "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            fact_cur2[datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S.%f')] = (float(row[1]))

    with open("VEPP_SOL_4S1_SCur.2.csv", "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            set_cur2[datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S.%f')]=(float(row[1]))
    obj.found_error(fact_cur2, set_cur2)

    t3 = datetime.datetime.now()
    with open("VEPP_SOL_4S1_MCur.1.3.csv", "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            fact_cur3[datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S.%f')] = (float(row[1]))

    with open("VEPP_SOL_4S1_SCur.3.csv", "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            set_cur3[datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S.%f')]=(float(row[1]))
    obj.found_error(fact_cur3, set_cur3)

    t4 = datetime.datetime.now()
    with open("VEPP_SOL_4S1_MCur.1.csv", "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            fact_cur[datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')] = (float(row[1]))

    with open("VEPP_SOL_4S1_SCur.csv", "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            set_cur[datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')] = (float(row[1]))


    obj.found_error(fact_cur, set_cur)
    t5 = datetime.datetime.now()

    f = open('result.txt', 'w')
    f.write("24 hours" + " " + str(t2-t1) + " " + str(sys.getsizeof(fact_cur1)+sys.getsizeof(set_cur1)) + "\n")
    f.write("12 hours" + " " + str(t3 - t2) + " " + str(sys.getsizeof(fact_cur2) + sys.getsizeof(set_cur2)) + "\n")
    f.write("6 hours" + " " + str(t4 - t3) + " " + str(sys.getsizeof(fact_cur3) + sys.getsizeof(set_cur3)) + "\n")
    f.write("3 hours" + " " + str(t5 - t4) + " " + str(sys.getsizeof(fact_cur) + sys.getsizeof(set_cur)) + "\n")