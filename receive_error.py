import pika
import time
import asyncio
import websockets
import asyncio
from websocket import create_connection

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

async def hello():
    async with websockets.connect('ws://localhost:8765') as websocket:
        await websocket.send("hello")
        greeting = await websocket.recv()
        print("< {}".format(greeting))



def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))
    ch.basic_ack(delivery_tag = method.delivery_tag)
    asyncio.get_event_loop().run_until_complete(hello())

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()