import socket

class TCPServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.sock.bind(self.host, self.port)

    def read(self):
        self.sock.listen(1)
        conn, addr = self.sock.accept()
        data = conn.recv(1024)

    def process(self):
        while True:
            conn, addr = self.sock.accept()
            data = conn.recv(1024)
            print(data)
            if not data:
                break
            conn.send(data.upper())

            conn.close()