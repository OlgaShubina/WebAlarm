from scipy.interpolate import interp1d
import datetime
from bsddb3 import db
from sortedcontainers import SortedDict

class ExtrapolationMethodClass(object):
    def __init__(self, condition, name, active_interval, data):
        self.condition = condition
        self.name = name
        self.active_interval = active_interval
        self.data = data
        self.last_time = datetime.datetime.now()
        self.cur_time = None

    def calc_value(self):
        x = []
        y = []
        new_y = 0
        cur_db = db.DB()
        cur_db.open(self.data[0], None, db.DB_BTREE, db.DB_DIRTY_READ)

        buffer = SortedDict({datetime.datetime.strptime(time.decode('utf-8'), '%Y-%m-%d %H:%M:%S.%f'):
                                   float(value.decode('utf-8')) for time, value in dict(cur_db).items()})
        if buffer:
            self.cur_time = buffer.peekitem()[0]

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
        if not self.cur_time:
             active = False
        elif self.cur_time - self.last_time >= datetime.timedelta(seconds=self.active_interval):
            active = False
        else:
            active = True
        self.last_time = datetime.datetime.now()
        return active