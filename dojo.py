__metaclass__ = type

BROADCAST_ADDR = "10.145.2.255:10001"

import multiprocessing
import socket

DEL = "::"


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
    def __init__(self, port):
        self.port = port
        self.neighbours = []

    def route(self, msg):
        msg_obj = Msg.from_string(msg)
        if msg_obj.dest == self.port:
            print("Received message %s" % str(msg_obj))
        elif msg_obj.dest in self.neighbours:
            msg_obj.passed_from.append(self.port)
            self.send(msg_obj)
        else:
            not_seen = [x for x in self.neighbours if not x in msg_obj.passed_from]

    def send(self, msg_obj):
        pass

    def check(self):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    m = Msg('19999', '23232', 'content')
    st = m.to_string()
    assert m == Msg.from_string(st)

    # for n in range(10):
    #     Node("1200%d" % n).run()
