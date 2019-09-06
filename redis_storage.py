import redis
import json


class RedisStorage(object):
    def __init__(self, host_, port_, db_):
        self.connect = redis.StrictRedis(host=host_, port=port_, db=db_)

    def save_name_channels(self, arr_ch):
        self.connect.set('name_channels', arr_ch)

    def get_name_channels(self):
        return self.connect.get('name_channels')

    def save_system_state(self, name, state):
        #self.connect.hmset(name, state)
        pass

    def get_system_state(self):
        arr_system_state = {}
        channels = self.get_name_channels()
        for ch in channels:
            arr_system_state[ch] = self.connect.hgetall(ch)
        return arr_system_state

    def set_group_for_clear(self, group_name):
        self.connect.lpush('group_for_clear', group_name)

    def get_group_for_clear(self):
        self.connect.lrange(0, -1)