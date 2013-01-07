__metaclass__ = type

BROADCAST_ADDR = "10.145.2.255:10001"

import multiprocessing
DEL = "::"


class Msg:
    def __init__(self, src, dest, content):
        self.src = src
        self.dest = dest
        self.content = content
        self.passed_from = []

    @classmethod
    def from_string(cls, st_repr):
        src, dest, content, passed_from = st_repr.split('::')
        return cls(Msg(src, dest, content, passed_from.split(',')))

    def to_string(self):
        return str(self)

    def __str__(self):
        return "%s::%s::%s::%s" % (self.src, self.dest, self.content, ','.join(self.passed_from))


class Node:
    def __init__(self, port):
        self.port = port
        self.neighbours = []

    def route(self, msg):
        if msg.dest == self.port:
            print("Received message %s" % str(msg))
        elif msg.dest in self.neighbours:
            msg.passed_from.append(self.port)
            self.send(msg, msg.dest)
        else:
            not_seen = [x for x in self.neighbours if not x in msg.passed_from]

    def check(self):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    for n in range(10):
        Node("1200%d" % n).run()
