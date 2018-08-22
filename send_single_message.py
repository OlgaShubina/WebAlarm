import asyncio
import websockets
import pika


connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.queue_declare(queue="alarm_queue", durable=True)

buff = {"VEPP/SOL/1S1": {"info": "error1", "active": True},
        "VEPP/SOL/1S2": {"info": "error2", "active": True},
        "VEPP/SOL/1S3": {"info": "error1", "active": True},
        "VEPP/SOL/2S1": {"info": "error3", "active": True},
        "VEPP/QUAD/2D3": {"info": "error1", "active": True},
        "VEPP/QUAD/2D1": {"info": "error2", "active": True},
        "VEPP/QUAD/4F3": {"info": "error1", "active": True},
        "VEPP/QUAD/2F2": {"info": "error3", "active": True}}
channel.basic_publish(exchange="", routing_key="alarm_queue", body=str(buff),
                              properties=pika.BasicProperties(delivery_mode=2, ))