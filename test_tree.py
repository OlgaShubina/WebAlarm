import json
import time
from collections import defaultdict

if __name__ =='__main__':
    json_data = open("group_config.json").read()
    group_config = json.loads(json_data)

    dict_result = {}
    d = {}

    for i, k in group_config.items():
        for i1, k1 in k.items():
            for ch in k1.keys():
                arr = ch.split('/')
                #last = arr[0]
                d = dict_result
                for s in arr:
                    d.setdefault(s, {})
                    d = d[s]
    print(dict_result)