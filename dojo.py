__metaclass__ = type

BROADCAST_ADDR = "10.145.2.255:10001"

import multiprocessing
import socket

DEL = "::"

LISTEN_ADDRESS = ('127.0.0.1', 19999)


class Msg:
    def __init__(self, src, dest, content, passed_from=None):
        self.src = src
        self.dest = dest
        self.content = content
        self.passed_from = passed_from or []

    def __eq__(self, other):
        return self.src == other.src and self.dest == other.dest

    @classmethod
    def from_string(cls, st_repr):
        src, dest, content, passed_from = st_repr.split('::')
        return cls(src, dest, content, passed_from.split(','))

    def to_string(self):
        return str(self)

    def __str__(self):
        return "%s::%s::%s::%s" % (self.src, self.dest, self.content, ','.join(self.passed_from))


class Node:
    def __init__(self, address):
        self.address = address
        self.neighbours = []
        self.sockets = {}

    def get_socket(self, address):
        if address in self.sockets:
            return self.sockets[address]
        else:
            # 127.0.0.1:10002
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(address)
            self.sockets[address] = sock

    def route(self, msg):
        msg_obj = Msg.from_string(msg)
        if msg_obj.dest == self.address:
            print("Received message %s" % str(msg_obj))
        elif msg_obj.dest in self.neighbours:
            msg_obj.passed_from.append(self.address)
            self.send(msg_obj)
        else:
            not_seen = [x for x in self.neighbours if not x in msg_obj.passed_from]

    def send(self, msg_obj):
        sock = self.get_socket(msg_obj.dest)
        sock.sendall(msg_obj.to_string())

    def check(self):
        pass

    def run(self):
        listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen.bind(self.address)
        listen.listen(5)
        while True:
            rd, wr, ex = socket.select([listen] + self.sockets.values(), [], [], 1000)
            if listen in rd:
                newsock = listen.accept()
                self.sockets[newsock.getpeeraddr()] = newsock
            for sock in rd:
                for neighb, neighbsock in self.sockets.items():
                    if sock == neighbsock:
                        data = sock.read(1024)
                        if data:
                            self.receive(neighb, sock.read(1024))
                        else:
                            del self.sockets[neighb]

if __name__ == '__main__':
    m = Msg('19999', '23232', 'content')
    st = m.to_string()
    assert m == Msg.from_string(st)

    # multiprocessing.Process(target=bind_udp).run()
    # multiprocessing.Process(target=bind_udp).run()
    # for n in range(10):
    #     Node("1200%d" % n).run()
