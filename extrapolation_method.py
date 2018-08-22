from scipy.interpolate import interp1d
import datetime


class ExtrapolationMethodClass(object):
    def __init__(self, condition, name, active_interval, data):
        self.condition = condition
        self.name = name
        self.active_interval = active_interval
        self.data = data
        self.last_time = datetime.datetime.now()

    def calc_value(self):
        x = []
        y = []
        new_y = 0
        buffer = self.data[self.data.keys()[0]]
        for k, i in buffer.items():
            x.append(k.timestamp())
            y.append((float(i)))

        #x_interp = np.linspace(x[0], x[len(x) - 1] + 18000, len(x) * 2.5)
        # y_interp = np.interp(x_interp, x, y)
        if len(x)!= 0:
            f = interp1d(x, y, fill_value='extrapolate')
            new_y = f(datetime.datetime.now().timestamp())
        return new_y

    def found_error(self):
        new_y = self.calc_value()
        if new_y < 20:
            error = "error4"
        else:
            error = "correct"
        return error

    def check_active(self):
        if len(self.data):
            active = False
        elif self.data[self.data.keys()[0]].peekitem()[0] - self.last_time >= datetime.timedelta(seconds=self.active_interval):
            active = False
        else:
            active = True
        self.last_time = datetime.datetime.now()
        return active