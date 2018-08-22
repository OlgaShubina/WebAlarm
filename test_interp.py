import numpy as np
import csv
import matplotlib.pyplot as plt
import datetime
from scipy.interpolate import interp1d
import scipy


def lagranz(x, y, t):
    z = 0
    for j in range(len(y)):
        p = 1
        for i in range(len(x)):
            if i != j:
                p *= (t - x[i])/(x[j] - x[i])
                #print(p)
        z += y[j]*p
    return z

with open("Cryo_Level_Cr-1_LHe.csv", "r", newline="") as file:
    reader = csv.reader(file)
    x = []
    y = []
    for row in reader:
        x.append((datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f').timestamp()))
        y.append((float(row[1])))
    x_interp = np.linspace(x[0], x[len(x)-1]+18000, len(x)*2.5)
    #y_interp = np.interp(x_interp, x, y)
    f = interp1d(x, y, fill_value='extrapolate')
    f2 = interp1d(x, y, kind='cubic')
    z = np.polyfit(x, y, 4)
    p = np.poly1d(z)
   # print(f(x[len(x)-1]+1800))
    #pylab.plot(x, p(x), "r--")
    #f3 = [lagranz(x,y,i) for i in x_interp]
    #f3 = scipy.interpolate.lagrange(x, y)
   # print(f3)
    #plt.plot(x, y, 'o')
    #plt.plot(x_interp, y_interp, 'yellow')
    #plt.plot(x_interp, f3, '--')
    #print(f3(x_interp))
    plt.plot(x, y, 'o', x_interp, f(x_interp), '-', x, p(x), '--')
    plt.legend(['data', 'linear', 'cubic'], loc='best')
    plt.show()
