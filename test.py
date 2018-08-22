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

    with open("VEPP_SOL_4S1_MCur.1.1.csv", "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            fact_cur1[datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S.%f')] = (float(row[1]))

    with open("VEPP_SOL_4S1_SCur.1.csv", "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            set_cur1[datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S.%f')]=(float(row[1]))
    obj.found_error(fact_cur1, set_cur1)
