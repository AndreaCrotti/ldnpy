__metaclass__ = type

BROADCAST_ADDR = "10.145.2.255:10001"

import multiprocessing


class Node:
    def __init__(self, port):
        self.port = port
        self.neighbours = []

    def route(self, msg):
        pass

    def check(self):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    pass
