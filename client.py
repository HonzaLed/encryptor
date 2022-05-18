#!/data/data/com.termux/files/usr/bin/python3

import socket
import sys
import os
from threading import Thread
import encryptor as enc
import codecs
# Part 9
# Developing a TCP Network Proxy - Pwn Adventure 3
# https://www.youtube.com/watch?v=iApNzWZG-10

class Server(Thread):

    def __init__(self, host, port, seed, mod):
        super(Server, self).__init__()
        self.seed = seed
        self.mod = mod
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    def run(self):
        while True:
            data = self.server.recv(4096)
            if data:
                #print("[{}] -> {}".format(self.port, data.__repr__()))
                try:
                    print("<- server["+self.host+"]:", enc.decrypt(data.decode(), self.seed, self.mod))
                except Exception as e:
                    print('server[{}]'.format(self.host), e)
"""
class Proxy(Thread):

    def __init__(self, from_host, to_host, port):
        super(Proxy, self).__init__()
        self.from_host = from_host
        self.to_host = to_host
        self.port = port

    def run(self):
        while True:
            print("[proxy({})] setting up".format(self.port))
            self.g2p = Game2Proxy(self.from_host, self.port) # waiting for a client
            self.p2s = Proxy2Server(self.to_host, self.port)
            print("[proxy({})] connection established".format(self.port))
            self.g2p.server = self.p2s.server
            self.p2s.game = self.g2p.game

            self.g2p.start()
            self.p2s.start()


master_server = Proxy('0.0.0.0', sys.argv[1], int(sys.argv[2]))
master_server.start()
"""
secret=input("Please input encryption secret: ")
seed, mod = secret.split("$")
server = Server(sys.argv[1], int(sys.argv[2]), int(seed), int(mod))
server.start()
while True:
    try:
        cmd = input(': ')
        if cmd == 'quitquit':
            os._exit(0)
        server.server.sendall(enc.complex_encrypt(cmd, server.seed, server.mod).encode())
        print("-> server["+server.host+"]:", cmd)
    except Exception as e:
        print(e)


