#!/data/data/com.termux/files/usr/bin/python3

import socket
import sys
import os
from threading import Thread

# Part 9
# Developing a TCP Network Proxy - Pwn Adventure 3
# https://www.youtube.com/watch?v=iApNzWZG-10

class Proxy2Server(Thread):

    def __init__(self, host, port):
        super(Proxy2Server, self).__init__()
        self.game = None # game client socket not known yet
        self.port = port
        self.host = host
#        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        self.server.connect((host, port))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        # waiting for a connection
        self.server, addr = sock.accept()

    # run in thread
    def run(self):
        while True:
            data = self.server.recv(4096)
            if data:
                print("[{}] <- {}".format(self.port, data.__repr__()))
                try:
                    #reload(parser)                        
                    pass #parser.parse(data, self.port, 'server')
                except Exception as e:
                    print('client1[{}]'.format(self.port), e)
                # forward to client
                self.game.sendall(data)

class Proxy2Client(Thread):

    def __init__(self, host, port):
        super(Proxy2Client, self).__init__()
        self.server = None # real server socket not known yet
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        # waiting for a connection
        self.game, addr = sock.accept()

    def run(self):
        while True:
            data = self.game.recv(4096)
            if data:
                print("[{}] -> {}".format(self.port, data.__repr__()))
                try:
                    #reload(parser)        
                    #parser.parse(data, self.port, 'client')
                    pass
                except Exception as e:
                    print('client2[{}]'.format(self.port), e)
                # forward to server
                self.server.sendall(data)

class Proxy(Thread):

    def __init__(self, from_host, to_host, port, port2):
        super(Proxy, self).__init__()
        self.from_host = from_host
        self.to_host = to_host
        self.port = port
        self.port2 = port2

    def run(self):
        while True:
            print("[client1({})] setting up".format(self.port))
            self.g2p = Proxy2Client(self.from_host, self.port) # waiting for a client
            print("[client2({})] setting up".format(self.port2))
            self.p2s = Proxy2Server(self.to_host, self.port2)
            print("[client1({})] connection established".format(self.port))
            self.g2p.server = self.p2s.server
            self.p2s.game = self.g2p.game
            print("[client2({})] connection established".format(self.port2))
            self.g2p.start()
            self.p2s.start()


master_server = Proxy('0.0.0.0', "0.0.0.0", int(sys.argv[1]), int(sys.argv[2]))
master_server.start()

while True:
    try:
        cmd = input('$ ')
        if cmd[:4] == 'quit':
            os._exit(0)
    except Exception as e:
        print(e)


