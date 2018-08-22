import csv
from collections import defaultdict, OrderedDict
import datetime
from sortedcontainers import SortedDict
import time

files = ["VEPP_BeamShaker_U.1.csv","VEPP_BeamShaker_U.2.csv",
         "VEPP_CCD_1M1L_sigma_x.csv", "VEPP_CCD_1M1L_sigma_z.csv",
         "VEPP_CCD_4M1R_sigma_x.csv", "VEPP_CCD_4M1R_sigma_z.csv",
         "VEPP_Currents_e.csv", "VEPP_Currents_p.csv",
         "VEPP_Currents_e_tau.csv", "VEPP_Currents_p_tau.csv"]
dataset = SortedDict()
buff_dict = defaultdict(defaultdict)

with open("SND_L.csv", newline="") as file:
    reader = csv.reader(file)
    for row in reader:
        str = row[0]
        dataset[datetime.datetime.strptime(str[:str.rfind('.')], '%Y-%m-%d %H:%M:%S')] = [float(row[1])]


for f in files:
    with open(f, newline="") as file:
        buff = SortedDict()
        reader = csv.reader(file)
        for row in reader:
            str = row[0]
            str = str[:str.rfind('.')]
            buff[datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')] = float(row[1])
    buff_dict[f[:f.rfind('.')]] = buff
print(len(dataset), len(sorted(dataset.keys())))
count = 0

t1 = list(dataset.keys())[0] - datetime.timedelta(seconds=6)

for i in dataset.keys():
    arr = []
    for k,d in buff_dict.items():
        print(k, t1,i)
        key = []
        for t,v in d.items():
            if t==i:
                dataset[i].append(v)
                #print(dataset[i])
                key.append(t)
                break
            elif (t>t1) and (t<i):
                arr.append(t)
                key.append(t)
            else:
                #print(arr)
                if len(arr)!=0:
                    try:
                        dataset[i].append(d[arr[-1]])
                    except:
                        count+=1
                        print("except")
                        pass
                print("break")
                break
        for l in key:
            del buff_dict[k][l]
    t1 = i

keys = []
#print(dataset)
for i, k in dataset.items():
   # print(len(k))
    if len(k) < 11:
        keys.append(i)
    elif len(k)!=11:
        print(len(k))

for i in keys:
    del dataset[i]
print(len(dataset), count)