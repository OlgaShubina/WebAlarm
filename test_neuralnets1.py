import csv
from collections import defaultdict, OrderedDict
import datetime
from sortedcontainers import SortedDict

files = ["VEPP_BeamShaker_U.1.csv", "VEPP_BeamShaker_U.2.csv",
         "VEPP_CCD_1M1L_sigma_x.csv", "VEPP_CCD_1M1L_sigma_z.csv",
         "VEPP_CCD_4M1R_sigma_x.csv", "VEPP_CCD_4M1R_sigma_z.csv",
         "VEPP_Currents_e.csv", "VEPP_Currents_p.csv",
         "VEPP_Currents_e_tau.csv", "VEPP_Currents_p_tau.csv"]
dataset = {}


with open("SND_L.csv", newline="") as file:
    reader = csv.reader(file)
    for row in reader:
        str = row[0]
        dataset[str[:str.rfind('.')]] = [float(row[1])]


for f in files:
    with open(f, newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            str = row[0]
            str = str[:str.rfind('.')]
            if(str in dataset):
                dataset[str].append(float(row[1]))
            else:
                #step=0
                #while(not(str in dataset)):
                    #if(step<=3):
                str = datetime.datetime.strftime(
                            datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(seconds=1),
                            '%Y-%m-%d %H:%M:%S')
                    #else:
                        #break
                    #step += 1
                    #print(str)
                if (str in dataset):
                    dataset[str].append(float(row[1]))




keys = []
buff_dict = defaultdict(list)
for i, k in dataset.items():
    #buff = OrderedDict(int)
    #if len(k) >= 11:
        #for n in k:
            #buff[n]+=1
        #buff_dict[i] = buff.keys()

    if len(k) != 11:
        keys.append(i)

for i in keys:
    del dataset[i]
with open('dataset.csv', 'w', newline='') as csvfile:
    spamwriter = csv.DictWriter(csvfile, fieldnames=['1', '2', '3', '4', '5','6','7','8','9','10','11'])
    for i,k in dataset.items():
        spamwriter.writerow({'1':float(k[0]), '2':float(k[1]), '3':float(k[2]), '4':float(k[3]), '5':float(k[4]),
                             '6':float(k[5]),'7':float(k[6]),'8':float(k[7]),'9':float(k[8]),'10':float(k[9]),'11':float(k[10])})

print(len(dataset))