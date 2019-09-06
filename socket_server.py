import asyncio
import websockets
import pika
from threading import Thread
import json
from redis_storage import RedisStorage
import subprocess


redis_storage = RedisStorage("localhost", 6379, 1)

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
    subprocess.call("rule_factory.py 1", shell=True)

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
        connected.add(websocket)
        print(connected, path)
        try:
            json_data = open("group_config.json").read()
            group_config = json.loads(json_data)
            dict_result = {}
            d = {}

            for i, k in group_config.items():
                for i1, k1 in k.items():
                    for ch in k1.keys():
                        arr = ch.split('/')
                        # last = arr[0]
                        d = dict_result
                        for s in arr:
                            d.setdefault(s, {})
                            d = d[s]
            #print(dict_result)

            await asyncio.wait([ws.send(str(json.dumps({"channels": dict_result}))) for ws in connected])
            #await asyncio.wait([ws.send(str(json.dumps({"channels":redis_storage.get_system_state()}))) for ws in connected])
            await asyncio.sleep(120)
        finally:
            connected.remove(websocket)

async def send_message(body):
    global connected
    #print(str(body), connected)
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