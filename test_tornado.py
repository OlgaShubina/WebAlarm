import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import pika
from threading import Thread


clients = []

def threaded_rmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    print ('Connected:localhost')
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    print ('Consumer ready, on my_queue')
    channel.basic_consume(consumer_callback, queue="task_queue", no_ack=True)
    channel.start_consuming()


def consumer_callback(ch, method, properties, body):
        print (" [x] Received %r" % (body,))
        for itm in clients:
            itm.write_message(body)

class SocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    def open(self):
        print ("WebSocket opened")
        clients.append(self)
    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print ("WebSocket closed")
        clients.remove(self)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print ("get page")
        self.render("websocket.html")


application = tornado.web.Application([
    (r'/ws', SocketHandler),
    (r"/", MainHandler),
])

if __name__ == "__main__":
    thread = Thread(target = threaded_rmq)
    thread.start()

    application.listen(8765)
    tornado.ioloop.IOLoop.instance().start()