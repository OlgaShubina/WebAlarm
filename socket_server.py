import asyncio
import websockets
import pika
from threading import Thread
from multiprocessing import Process
import json
import time
from collections import defaultdict

input_dict = {"VEPP/SOL/1S1": ['VEPP/SOL/1S1/MCur.1', 'VEPP/SOL/1S1/SCur'],
              "VEPP/SOL/1S2": ['VEPP/SOL/1S2/MCur.1', 'VEPP/SOL/1S2/SCur'],
              "VEPP/SOL/1S3": ['VEPP/SOL/1S3/MCur.1', 'VEPP/SOL/1S3/SCur'],
              "VEPP/SOL/2S1": ['VEPP/SOL/2S1/MCur.1', 'VEPP/SOL/2S1/SCur'],
              "VEPP/SOL/2S2": ['VEPP/SOL/2S2/MCur.1', 'VEPP/SOL/2S2/SCur'],
              "VEPP/SOL/2S3": ['VEPP/SOL/2S3/MCur.1', 'VEPP/SOL/2S3/SCur'],
              "VEPP/SOL/3S1": ['VEPP/SOL/3S1/MCur.1', 'VEPP/SOL/3S1/SCur'],
              "VEPP/SOL/3S2": ['VEPP/SOL/3S2/MCur.1', 'VEPP/SOL/3S2/SCur'],
              "VEPP/SOL/3S3": ['VEPP/SOL/3S3/MCur.1', 'VEPP/SOL/3S3/SCur'],
              "VEPP/SOL/4S1": ['VEPP/SOL/4S1/MCur.1', 'VEPP/SOL/4S1/SCur'],
              "VEPP/SOL/4S2": ['VEPP/SOL/4S2/MCur.1', 'VEPP/SOL/4S2/SCur'],
              "VEPP/SOL/4S3": ['VEPP/SOL/4S3/MCur.1', 'VEPP/SOL/4S3/SCur'],
              "VEPP/QUAD/1D1": ['VEPP/QUAD/1D1/MCur.1', 'VEPP/QUAD/1D1/SCur'],
              "VEPP/QUAD/1D2": ['VEPP/QUAD/1D2/MCur.1', 'VEPP/QUAD/1D2/SCur'],
              "VEPP/QUAD/1D3": ['VEPP/QUAD/1D3/MCur.1', 'VEPP/QUAD/1D3/SCur'],
              "VEPP/QUAD/1F2": ['VEPP/QUAD/1F2/MCur.1', 'VEPP/QUAD/1F2/SCur'],
              "VEPP/QUAD/1F3": ['VEPP/QUAD/1F3/MCur.1', 'VEPP/QUAD/1F3/SCur'],
              "VEPP/QUAD/2D1": ['VEPP/QUAD/2D1/MCur.1', 'VEPP/QUAD/2D1/SCur'],
              "VEPP/QUAD/2D2": ['VEPP/QUAD/2D2/MCur.1', 'VEPP/QUAD/2D2/SCur'],
              "VEPP/QUAD/2D3": ['VEPP/QUAD/2D3/MCur.1', 'VEPP/QUAD/2D3/SCur'],
              "VEPP/QUAD/2F2": ['VEPP/QUAD/2F2/MCur.1', 'VEPP/QUAD/2F2/SCur'],
              "VEPP/QUAD/2F3": ['VEPP/QUAD/2F3/MCur.1', 'VEPP/QUAD/2F3/SCur'],
              "VEPP/QUAD/3D1": ['VEPP/QUAD/3D1/MCur.1', 'VEPP/QUAD/3D1/SCur'],
              "VEPP/QUAD/3D2": ['VEPP/QUAD/3D2/MCur.1', 'VEPP/QUAD/3D2/SCur'],
              "VEPP/QUAD/3D3": ['VEPP/QUAD/3D3/MCur.1', 'VEPP/QUAD/3D3/SCur'],
              "VEPP/QUAD/3F2": ['VEPP/QUAD/3F2/MCur.1', 'VEPP/QUAD/3F2/SCur'],
              "VEPP/QUAD/3F3": ['VEPP/QUAD/3F3/MCur.1', 'VEPP/QUAD/3F3/SCur'],
              "VEPP/QUAD/4D1": ['VEPP/QUAD/4D1/MCur.1', 'VEPP/QUAD/4D1/SCur'],
              "VEPP/QUAD/4D2": ['VEPP/QUAD/4D2/MCur.1', 'VEPP/QUAD/4D2/SCur'],
              "VEPP/QUAD/4D3": ['VEPP/QUAD/4D3/MCur.1', 'VEPP/QUAD/4D3/SCur'],
              "VEPP/QUAD/4F2": ['VEPP/QUAD/4F2/MCur.1', 'VEPP/QUAD/4F2/SCur'],
              "VEPP/QUAD/4F3": ['VEPP/QUAD/4F3/MCur.1', 'VEPP/QUAD/4F3/SCur'],
              "Cryo/Level/Cr-1": ["Cryo/Level/Cr-1/LHe"],
              "Cryo/Level/Cr-2": ["Cryo/Level/Cr-2/LHe"],
              "Cryo/Level/Cr-3": ["Cryo/Level/Cr-3/LHe"],
              "Cryo/Level/Cr-4": ["Cryo/Level/Cr-4/LHe"]
}

connected = set()


def thread_rmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            #host='172.16.1.117'))
            host='0.0.0.0'))
            #host = 'localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='alarm_queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,
                          queue='alarm_queue')

    channel.start_consuming()

def callback(ch, method, properties, body):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if connected.__len__()!=0:
        loop.run_until_complete(send_message(body))
    print(" [x] Received %r" % (body,))
    ch.basic_ack(delivery_tag = method.delivery_tag)


async def handler(websocket, path):
    while True:
        global connected
        # Register.
        connected.add(websocket)
        print(connected, path)
        try:
            # Implement logic here.

            result_arr = defaultdict(defaultdict)
            json_data = open("group_config.json").read()
            group_config = json.loads(json_data)
            for i,k in group_config.items():
                arr = defaultdict(list)
                result_dict = {}
                for i1, k1 in k.items():
                    for ch in k1.keys():
                        str1 = ch[ch.find('/') + 1:]
                        # print(str1[str1.find('/')+1:])
                        arr[i1].append(str1[str1.find('/') + 1:])
                    result_arr[i] = arr

                print(str(result_dict))
                #result_arr[i] = arr

            #for i in input_dict.keys():
            #    arr[str(i[:i.rfind('/')])].append(str(i[i.rfind('/')+1:]))
            #print(arr)
            #for k, i  in arr.items():
             #   result_arr[str(k[:k.find('/')])].update({str(k[k.find('/')+1:]): i})
            #print(result_arr)
            await asyncio.wait([ws.send(str(json.dumps({"channels": result_arr}))) for ws in connected])
            await asyncio.sleep(120)
        finally:
            # Unregister.
            connected.remove(websocket)
            #pass

async def send_message(body):
    global connected
    print(str(body), connected)
    for ws in connected:
        print(ws)
    try:
        await asyncio.wait([ws.send(body.decode("utf-8")) for ws in connected])
        #await asyncio.sleep(10)
    finally:
        # Unregister.
        pass

thread = Thread(target = thread_rmq)
thread.start()
print("dfs")
#start_server = websockets.serve(handler, '172.16.1.117', 8080)
start_server = websockets.serve(handler, '0.0.0.0', 8080)
#start_server = websockets.serve(handler, 'localhost', 8080)

loop = asyncio.get_event_loop()
#asyncio.set_event_loop(loop)
#p = Process(target=loop.run_until_complete(start_server), args=())
#p.start()
#p.join()

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()