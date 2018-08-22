import http.client
import time
import datetime
import csv
import json


class Req(object):
    """docstring for """

    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        self.path = path

    def get_freq(self, response):

        js = json.loads(response)
        return js

    def get_chunk_compress(self, uuid, fields, level):
        headers = {'Content-type': 'application/json'}
        data = {"fields": fields, "level": level}
        data_js = json.dumps(data)
        conn = http.client.HTTPConnection(self.host, self.port)
        conn.request("POST", self.path + "/chunk_compress/" + str(uuid), data_js, headers)
        response = conn.getresponse().read().decode('utf-8')
        return response

    def CursorCompress(self, t1, t2, channels, level, fields=None):
        try:
            data = {"t1": t1, "t2": t2, "channels": channels, "fields": fields, "level": level}

            data_js = json.dumps(data)
            headers = {'Content-type': 'application/json'}
            conn = http.client.HTTPConnection(self.host, self.port)
            conn.request("POST", self.path + "/cursor_compress", data_js, headers)
            response = conn.getresponse()
            js = json.loads(response.read().decode('utf-8'))
            data = response.read()
            count = 0
            current_uuid = js["first"]["uuid"]
            length = js["len_dict"]
            while (count < length):
                r = self.get_chunk_compress(current_uuid, fields, level)
                current_chunk = self.get_freq(r)
                yield current_chunk
                current_uuid = current_chunk.get("next", None)
                if current_uuid is None:
                    break

                count += 1
            return js
        except KeyError:
            logging.error("1")